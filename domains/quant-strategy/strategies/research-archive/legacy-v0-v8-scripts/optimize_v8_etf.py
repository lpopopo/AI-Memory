#!/usr/bin/env python3
"""Survivorship-resistant ETF dual-sleeve optimization on the robust engine."""

from __future__ import annotations

import itertools
import json
import sys
from dataclasses import asdict
from pathlib import Path

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR, run_buy_hold
from robust_portfolio_engine import run_engine
from test_v3_refined import V3Config, combine_weights, growth_weights, is_bear, is_bull, month_end_dates, value_weights
from test_v4_stock_alpha import prepare_indicators
from optimize_v8_robust import metrics


ETF_COLUMNS = [
    "SPY", "QQQ", "VTV", "IWD", "SCHD", "SMH", "XLK", "XLC", "XLY",
    "XLI", "XLF", "XLV", "XLE", "XLB", "XLU", "XLRE", "XLP", "IBB", "ITA",
]
DEV_START = "2006-01-01"
DEV_END = "2018-12-31"
OOS_START = "2019-01-01"
END = "2025-12-30"


def load_etfs() -> pd.DataFrame:
    path = ROOT / "datasets" / "data_long" / "yfinance_adjusted_close_2000_2025.csv"
    frame = pd.read_csv(path, index_col=0, parse_dates=True).sort_index()
    columns = [s for s in ETF_COLUMNS if s in frame]
    return frame.loc[DEV_START:END, columns].dropna(subset=["SPY", "QQQ"])


def configs():
    idx = 0
    for bull_value, normal_value, bear_growth, top_n, bull_rule, bear_rule, fallback in itertools.product(
        [0.20, 0.30], [0.40, 0.50], [0.0, 0.15], [2, 3],
        ["qqq100_m63", "qqq200_m126"],
        ["both_below_200", "both_below_200_negative_m63"],
        ["cash", "spy"],
    ):
        idx += 1
        yield V3Config(
            name=f"v8_etf_{idx:03d}",
            bull_value_weight=bull_value, bull_growth_weight=1 - bull_value,
            normal_value_weight=normal_value, normal_growth_weight=1 - normal_value,
            bear_value_weight=1 - bear_growth, bear_growth_weight=bear_growth,
            bull_rule=bull_rule, bear_rule=bear_rule, growth_top_n=top_n,
            value_mode="top2", score_mode="m63_m126", fallback=fallback,
        )


def target_function(config, close, indicators, overlay="none"):
    def target(dt):
        bull = is_bull(config, close, indicators, dt)
        bear = is_bear(config, close, indicators, dt)
        if bear:
            value_target, growth_target = config.bear_value_weight, config.bear_growth_weight
        elif bull:
            value_target, growth_target = config.bull_value_weight, config.bull_growth_weight
        else:
            value_target, growth_target = config.normal_value_weight, config.normal_growth_weight
        value = value_weights(config, close, indicators, dt, value_target)
        growth = growth_weights(config, close, indicators, dt, growth_target, bull)
        raw = combine_weights(value, growth)
        if overlay == "bear_filter" and bear:
            raw = {s: w for s, w in raw.items()
                   if pd.notna(indicators["ma200"].at[dt, s])
                   and close.at[dt, s] > indicators["ma200"].at[dt, s]}
        elif overlay == "all_trend_filter":
            raw = {s: w for s, w in raw.items()
                   if pd.notna(indicators["ma200"].at[dt, s])
                   and close.at[dt, s] > indicators["ma200"].at[dt, s]}
        elif overlay == "market_scale":
            spy_ok = close.at[dt, "SPY"] > indicators["ma200"].at[dt, "SPY"]
            qqq_ok = close.at[dt, "QQQ"] > indicators["ma200"].at[dt, "QQQ"]
            multiplier = 1.0 if spy_ok and qqq_ok else (0.65 if spy_ok or qqq_ok else 0.30)
            raw = {s: w * multiplier for s, w in raw.items()}
        return raw
    return target


def rebase(curve: pd.Series, start: str, end: str = END) -> pd.Series:
    sliced = curve.loc[start:end].dropna()
    return sliced / sliced.iloc[0]


def development_score(m: dict) -> float:
    # Chosen before reading the 2019-2025 result: favor risk-adjusted return and
    # penalize drawdown. All inputs are development-period only.
    return m["sharpe"] + 0.75 * m["cagr"] + 0.75 * m["max_drawdown"]


def main():
    close = load_etfs()
    indicators = prepare_indicators(close)
    monthly = set(month_end_dates(close.index))
    rows = []
    curves = {}
    for i, config in enumerate(configs(), 1):
        if i % 25 == 0:
            print(f"evaluated {i} configurations", flush=True)
        result = run_engine(close, monthly, target_function(config, close, indicators), transaction_cost=0.001)
        dev = metrics(rebase(result.equity, DEV_START, DEV_END))
        rows.append({
            "config": asdict(config), "overlay": "none", "development": dev,
            "development_score": development_score(dev),
            "turnover": result.diagnostics["total_turnover"],
        })
        curves[(config.name, "none")] = result.equity
    rows.sort(key=lambda x: x["development_score"], reverse=True)

    # Stage 2 uses only the top 20 development configurations. Risk overlays
    # are also selected strictly on development data.
    by_name = {cfg.name: cfg for cfg in configs()}
    stage2 = []
    for base in rows[:20]:
        config = by_name[base["config"]["name"]]
        for overlay in ("none", "bear_filter", "all_trend_filter", "market_scale"):
            key = (config.name, overlay)
            if key in curves:
                curve = curves[key]
                dev = base["development"]
                total_turnover = base["turnover"]
            else:
                result = run_engine(
                    close, monthly, target_function(config, close, indicators, overlay),
                    transaction_cost=0.001,
                )
                curve = result.equity
                curves[key] = curve
                dev = metrics(rebase(curve, DEV_START, DEV_END))
                total_turnover = result.diagnostics["total_turnover"]
            stage2.append({
                "config": asdict(config), "overlay": overlay, "development": dev,
                "development_score": development_score(dev), "turnover": total_turnover,
            })
    stage2.sort(key=lambda x: x["development_score"], reverse=True)

    # OOS is evaluated only after both configuration and overlay ranking freeze.
    finalists = stage2[:10]
    for item in finalists:
        curve = curves[(item["config"]["name"], item["overlay"])]
        item["oos_2019_2025"] = metrics(rebase(curve, OOS_START))
        item["full_2006_2025"] = metrics(rebase(curve, DEV_START))

    benchmarks = {}
    for name, weights in {
        "SPY": {"SPY": 1.0}, "QQQ": {"QQQ": 1.0},
        "SPY_QQQ_50_50": {"SPY": 0.5, "QQQ": 0.5},
    }.items():
        curve = run_buy_hold(close, weights, name)
        benchmarks[name] = {
            "development": metrics(rebase(curve, DEV_START, DEV_END)),
            "oos_2019_2025": metrics(rebase(curve, OOS_START)),
        }

    output = {
        "method": {
            "universe": ETF_COLUMNS, "development": [DEV_START, DEV_END],
            "oos": [OOS_START, END], "selection": "ranked only on development_score",
            "execution": "close signal -> next session close", "transaction_cost": 0.001,
            "base_grid_size": len(rows), "overlay_grid_size": len(stage2),
        },
        "best": finalists[0], "finalists": finalists, "benchmarks": benchmarks,
    }
    path = RESULTS_DIR / "v8_etf_optimization_metrics.json"
    path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    best_curve = curves[(finalists[0]["config"]["name"], finalists[0]["overlay"])]
    best_curve.to_csv(RESULTS_DIR / "v8_etf_best_equity_curve.csv", index_label="date")
    print("best", finalists[0]["config"], "overlay", finalists[0]["overlay"])
    print("development", finalists[0]["development"])
    print("oos", finalists[0]["oos_2019_2025"])
    print("benchmarks", {k: v["oos_2019_2025"] for k, v in benchmarks.items()})
    print(path)


if __name__ == "__main__":
    main()
