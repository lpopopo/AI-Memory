#!/usr/bin/env python3
"""Best-effort point-in-time validation of the V5 momentum model."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR, run_buy_hold
from optimize_v8_robust import CONFIG, metrics, v5_target_function
from robust_portfolio_engine import run_engine
from test_v3_refined import combine_weights, is_bear, is_bull, month_end_dates, value_weights
from test_v4_stock_alpha import prepare_indicators
from test_v4_universe_alpha import load_universe_data


START = "2007-01-01"  # 2006 provides indicator warm-up for newly fetched names.
END = "2025-12-30"
REPORT_START = "2019-01-01"
POINT_DIR = ROOT / "datasets" / "data_point_in_time"
BENCHMARKS = {"SPY", "QQQ", "VTV", "IWD", "SCHD", "VIX", "^VIX"}


def rebase(curve: pd.Series, start: str, end: str = END) -> pd.Series:
    sliced = curve.loc[start:end].dropna()
    return sliced / sliced.iloc[0]


def load_data():
    close = pd.read_csv(POINT_DIR / "adjusted_close.csv", index_col=0, parse_dates=True).sort_index()
    long = pd.read_csv(
        ROOT / "datasets" / "data_long" / "yfinance_adjusted_close_2000_2025.csv",
        index_col=0, parse_dates=True,
    ).sort_index()
    etfs = ["SPY", "QQQ", "VTV", "IWD", "SCHD"]
    close = close.drop(columns=etfs, errors="ignore").join(long[etfs].reindex(close.index))
    history = pd.read_csv(POINT_DIR / "membership_history.csv", parse_dates=["opt-in", "opt-out"])
    return close.loc[:END], history


class Membership:
    def __init__(self, history: pd.DataFrame):
        self.history = history

    def at(self, date: pd.Timestamp) -> set[str]:
        h = self.history
        mask = (h["opt-in"] <= date) & (h["opt-out"].isna() | (h["opt-out"] > date))
        return set(h.loc[mask, "symbol"])

    def event_dates(self, calendar: pd.DatetimeIndex) -> set[pd.Timestamp]:
        events = pd.concat([self.history["opt-in"], self.history["opt-out"]]).dropna().unique()
        result = set()
        for event in pd.to_datetime(events):
            pos = calendar.searchsorted(event)
            if pos < len(calendar):
                result.add(calendar[pos])
        return result


def growth_weights_pit(
    config, close, indicators, membership: Membership, dt, target_total,
    coverage_adjust=False,
):
    members = membership.at(dt)
    eligible = []
    ready = 0
    for stock in members:
        if stock not in close or pd.isna(close.at[dt, stock]):
            continue
        values = [
            indicators["ma50"].at[dt, stock], indicators["ma200"].at[dt, stock],
            indicators["mom63"].at[dt, stock], indicators["mom126"].at[dt, stock],
            indicators["mom252"].at[dt, stock],
        ]
        if any(pd.isna(v) for v in values):
            continue
        ready += 1
        price = close.at[dt, stock]
        ma50, ma200, m63, m126, _m252 = values
        if price >= 5 and price > ma50 and price > ma200 and m63 > 0:
            eligible.append((m63 + m126, stock))
    eligible.sort(reverse=True)
    selected = [stock for _, stock in eligible[:config.stock_top_n]]
    if not selected:
        return {}, {"members": len(members), "ready": ready, "selected": []}
    coverage = ready / len(members) if members else 0.0
    effective_target = target_total * coverage if coverage_adjust else target_total
    each = effective_target / config.stock_top_n
    return ({stock: each for stock in selected},
            {"members": len(members), "ready": ready, "coverage": coverage, "selected": selected})


def pit_target_function(close, indicators, membership, coverage_adjust, selection_log):
    def target(dt):
        bull = is_bull(CONFIG, close, indicators, dt)
        bear = is_bear(CONFIG, close, indicators, dt)
        if bear:
            value_target, growth_target = 0.70, 0.30
        elif bull:
            value_target, growth_target = 0.30, 0.70
        else:
            value_target, growth_target = 0.40, 0.60
        value = value_weights(CONFIG, close, indicators, dt, value_target)
        if bear:
            value = {s: w for s, w in value.items()
                     if pd.notna(indicators["ma200"].at[dt, s])
                     and close.at[dt, s] > indicators["ma200"].at[dt, s]}
        growth, audit = growth_weights_pit(
            CONFIG, close, indicators, membership, dt, growth_target, coverage_adjust
        )
        audit.update({"date": str(dt.date()), "bull": bool(bull), "bear": bool(bear)})
        selection_log.append(audit)
        return combine_weights(value, growth)
    return target


def summarize_curve(curve):
    periods = {
        "full_2007_2025": (START, END),
        "development_2007_2018": (START, "2018-12-31"),
        "report_2019_2025": (REPORT_START, END),
        "high_coverage_2015_2025": ("2015-01-01", END),
    }
    return {name: metrics(rebase(curve, start, end)) for name, (start, end) in periods.items()}


def main():
    close, history = load_data()
    indicators = prepare_indicators(close)
    membership = Membership(history)
    calendar = close.loc[START:END].index
    rebalance_dates = set(month_end_dates(calendar)) | membership.event_dates(calendar)

    results = {}
    curves = {}
    logs = {}
    for name, adjust in [("V5_PIT_available", False), ("V5_PIT_coverage_adjusted", True)]:
        print("Running", name, flush=True)
        selection_log = []
        result = run_engine(
            close.loc[START:END], rebalance_dates,
            pit_target_function(close, indicators, membership, adjust, selection_log),
            transaction_cost=0.001, stop_loss_pct=0.30, stop_exempt=BENCHMARKS,
        )
        curves[name] = result.equity
        results[name] = summarize_curve(result.equity)
        logs[name] = selection_log

    # Re-run the current-constituent version over the identical 2007-2025 dates
    # with the same causal drifting-weight engine.
    current_close = load_universe_data().loc[START:END]
    current_indicators = prepare_indicators(load_universe_data())
    current_indicators = {k: v.loc[START:END] if isinstance(v, pd.DataFrame) else v
                          for k, v in current_indicators.items()}
    current_result = run_engine(
        current_close, set(month_end_dates(current_close.index)),
        v5_target_function(current_close, current_indicators), transaction_cost=0.001,
        stop_loss_pct=0.30, stop_exempt=BENCHMARKS,
    )
    curves["V5_current_constituents"] = current_result.equity
    results["V5_current_constituents"] = summarize_curve(current_result.equity)

    for name, weights in {
        "SPY": {"SPY": 1.0}, "QQQ": {"QQQ": 1.0},
        "SPY_QQQ_50_50": {"SPY": 0.5, "QQQ": 0.5},
    }.items():
        curve = run_buy_hold(close.loc[START:END], weights, name)
        curves[name] = curve
        results[name] = summarize_curve(curve)

    metadata = json.load(open(POINT_DIR / "metadata.json"))
    output = {
        "method": {
            "membership": metadata["membership_source"],
            "prices": metadata["price_source"], "period": [START, END],
            "membership_events_trigger_rebalance": True,
            "current_member_lookahead": False,
            "execution": "close signal -> next session close",
            "transaction_cost": 0.001, "individual_stop": 0.30,
        },
        "coverage": {
            k: metadata[k] for k in [
                "membership_symbols", "existing_symbols", "requested_missing_symbols",
                "fetched_missing_with_any_data", "price_symbols_with_any_data", "limitations",
            ]
        },
        "metrics": results,
        "selection_frequency": {
            name: Counter(s for row in log for s in row.get("selected", [])).most_common(30)
            for name, log in logs.items()
        },
    }
    path = RESULTS_DIR / "v5_point_in_time_metrics.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame(curves).to_csv(RESULTS_DIR / "v5_point_in_time_curves.csv", index_label="date")
    for name, m in results.items():
        r = m["report_2019_2025"]
        print(f"{name}: CAGR={r['cagr']:.2%} DD={r['max_drawdown']:.2%} Sharpe={r['sharpe']:.2f}")
    print(path)


if __name__ == "__main__":
    main()
