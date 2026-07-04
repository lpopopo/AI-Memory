#!/usr/bin/env python3
"""Re-evaluate V5/V7 on the causal drifting-weight engine and test C integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR, run_buy_hold, summarize
from robust_portfolio_engine import run_engine
from test_v4_stock_alpha import V4Config, combine_weights, is_bear, is_bull, month_end_dates, prepare_indicators, value_weights
from test_v4_universe_alpha import growth_weights_universe, load_universe_data, run_v4_universe
from test_v7_full_hybrid import compute_fear_backtest, double_radar_weights, growth_weights_v6_multifactor


START = "2006-01-01"
END = "2025-12-30"
DEV_END = pd.Timestamp("2018-12-31")
STOP_EXEMPT = {"SPY", "QQQ", "VTV", "IWD", "SCHD", "VIX", "^VIX"}


CONFIG = V4Config(
    name="v8_robust",
    bull_value_weight=0.30, bull_growth_weight=0.70,
    normal_value_weight=0.40, normal_growth_weight=0.60,
    bear_value_weight=0.70, bear_growth_weight=0.30,
    bull_rule="qqq200_m126", bear_rule="both_below_200_negative_m63",
    stock_top_n=10, value_mode="top2", score_mode="m63_m126", fallback="cash",
)


def c_recovery_signals(close: pd.DataFrame, indicators: dict) -> pd.DataFrame:
    """Close-only causal proxy for Pattern C, used only for integration testing."""
    ma20 = close.rolling(20).mean()
    ma50 = indicators["ma50"]
    below = close < ma20
    two_or_three_below = below.shift(1) & below.shift(2)
    reclaimed = (close > ma20) & two_or_three_below
    trend = (close > ma50) & (ma20 > ma50)
    return (reclaimed & trend).fillna(False)


def regime_targets(dt, close, indicators):
    bull = is_bull(CONFIG, close, indicators, dt)
    bear = is_bear(CONFIG, close, indicators, dt)
    if bear:
        return bear, 0.70, 0.30
    if bull:
        return bear, 0.30, 0.70
    return bear, 0.40, 0.60


def v5_target_function(close, indicators, c_signals=None, c_lookback=0):
    def target(dt):
        bear, value_target, growth_target = regime_targets(dt, close, indicators)
        v = value_weights(CONFIG, close, indicators, dt, value_target)
        if bear:
            v = {s: w for s, w in v.items()
                 if pd.notna(indicators["ma200"].at[dt, s])
                 and close.at[dt, s] > indicators["ma200"].at[dt, s]}
        g = growth_weights_universe(CONFIG, close, indicators, dt, growth_target, not bear)
        if c_signals is not None:
            loc = c_signals.index.get_loc(dt)
            start = max(0, loc - c_lookback + 1)
            recent = c_signals.iloc[start:loc + 1].any(axis=0)
            g = {s: w for s, w in g.items() if bool(recent.get(s, False))}
            if g:
                each = growth_target / len(g)
                g = {s: each for s in g}
        return combine_weights(v, g)
    return target


def v7_target_function(close, indicators):
    def target(dt):
        fear = compute_fear_backtest(dt, close, indicators)
        bull = is_bull(CONFIG, close, indicators, dt)
        bear = is_bear(CONFIG, close, indicators, dt)
        if bear:
            value_target, growth_target, radar_target = 0.70, 0.30, 0.0
        elif bull:
            value_target, growth_target, radar_target = 0.20, 0.55, 0.25
        else:
            value_target, growth_target, radar_target = 0.35, 0.50, 0.15
        v = value_weights(CONFIG, close, indicators, dt, value_target)
        if bear:
            v = {s: w for s, w in v.items()
                 if pd.notna(indicators["ma200"].at[dt, s])
                 and close.at[dt, s] > indicators["ma200"].at[dt, s]}
        g = growth_weights_v6_multifactor(CONFIG, close, indicators, dt, growth_target)
        r = double_radar_weights(close, indicators, dt, radar_target)
        raw = combine_weights(v, g, r)
        return {s: w * fear.risk_multiplier for s, w in raw.items()}
    return target


def weekly_dates(index: pd.DatetimeIndex) -> set[pd.Timestamp]:
    series = pd.Series(index=index, data=index)
    return set(series.groupby(index.to_period("W-FRI")).last().tolist())


def metrics(curve: pd.Series) -> dict:
    curve = curve.dropna()
    if curve.empty:
        raise ValueError("cannot summarize an empty curve")
    rebased = curve / float(curve.iloc[0])
    row = summarize("x", rebased)
    return {k: float(row[k]) for k in ["final_value", "cagr", "max_drawdown", "volatility", "sharpe", "sortino"]}


def split_metrics(curve: pd.Series) -> dict:
    return {
        "full_2006_2025": metrics(curve),
        "development_2006_2018": metrics(curve.loc[:DEV_END]),
        "report_2019_2025": metrics(curve.loc["2019-01-01":]),
    }


def main():
    full_close = load_universe_data()
    if "^VIX" in full_close and "VIX" not in full_close:
        full_close["VIX"] = full_close["^VIX"]
    full_indicators = prepare_indicators(full_close)
    if "mom252" not in full_indicators:
        full_indicators["mom252"] = full_close / full_close.shift(252) - 1
    close = full_close.loc[START:END]
    indicators = {k: v.loc[START:END] if isinstance(v, pd.DataFrame) else v
                  for k, v in full_indicators.items()}
    monthly = set(month_end_dates(close.index))
    c_signals = c_recovery_signals(close, indicators)

    curves = {}
    legacy, _ = run_v4_universe(close, indicators, CONFIG, transaction_cost=0.001, stop_loss_pct=0.30)
    curves["V5_legacy_accounting"] = legacy

    variants = {
        "V5_robust": (monthly, v5_target_function(close, indicators)),
        "V7_robust": (monthly, v7_target_function(close, indicators)),
        "V5_C5_monthly": (monthly, v5_target_function(close, indicators, c_signals, 5)),
        "V5_C10_monthly": (monthly, v5_target_function(close, indicators, c_signals, 10)),
        "V5_C20_monthly": (monthly, v5_target_function(close, indicators, c_signals, 20)),
        "V5_C10_weekly": (weekly_dates(close.index), v5_target_function(close, indicators, c_signals, 10)),
    }
    engine_meta = {}
    for name, (dates, fn) in variants.items():
        print(f"Running {name}...", flush=True)
        result = run_engine(
            close, dates, fn, transaction_cost=0.001, stop_loss_pct=0.30,
            stop_exempt=STOP_EXEMPT,
        )
        curves[name] = result.equity
        engine_meta[name] = result.diagnostics

    curves["SPY"] = run_buy_hold(close, {"SPY": 1.0}, "SPY")
    curves["QQQ"] = run_buy_hold(close, {"QQQ": 1.0}, "QQQ")
    curves["SPY_QQQ_50_50"] = run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "mix")
    output = {
        "method": {
            "window": [START, END], "development_end": str(DEV_END.date()),
            "execution": "close signal -> next session close",
            "weight_accounting": "drifting holdings; turnover charged on every target execution",
            "universe_warning": "current cached constituents; survivorship bias remains",
            "c_filter_warning": "close-only Pattern C proxy, not the OHLC setup-low implementation",
        },
        "metrics": {name: split_metrics(curve) for name, curve in curves.items()},
        "engine": engine_meta,
    }
    path = RESULTS_DIR / "v8_robust_optimization_metrics.json"
    path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame(curves).to_csv(RESULTS_DIR / "v8_robust_equity_curves.csv", index_label="date")
    for name in curves:
        m = output["metrics"][name]["report_2019_2025"]
        print(f"{name}: CAGR={m['cagr']:.2%} DD={m['max_drawdown']:.2%} Sharpe={m['sharpe']:.2f}")
    print(path)


if __name__ == "__main__":
    main()
