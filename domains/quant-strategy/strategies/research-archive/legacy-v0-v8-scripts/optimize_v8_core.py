#!/usr/bin/env python3
"""Optimize a transparent SPY/QQQ trend-managed core using development data only."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR, run_buy_hold
from optimize_v8_etf import DEV_END, DEV_START, END, OOS_START, development_score, load_etfs, rebase
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from test_v3_refined import month_end_dates


def target_function(close, spy_weight, ma_days, below_multiplier):
    ma = close[["SPY", "QQQ"]].rolling(ma_days).mean()
    base = {"SPY": spy_weight, "QQQ": 1 - spy_weight}

    def target(dt):
        weights = {}
        for symbol, weight in base.items():
            healthy = pd.notna(ma.at[dt, symbol]) and close.at[dt, symbol] > ma.at[dt, symbol]
            weights[symbol] = weight * (1.0 if healthy else below_multiplier)
        return weights
    return target


def ensemble_target_function(close, spy_weight=0.5):
    """Average 150/200-day trend votes to reduce single-parameter dependence."""
    ma150 = close[["SPY", "QQQ"]].rolling(150).mean()
    ma200 = close[["SPY", "QQQ"]].rolling(200).mean()
    base = {"SPY": spy_weight, "QQQ": 1 - spy_weight}

    def target(dt):
        result = {}
        for symbol, weight in base.items():
            votes = int(close.at[dt, symbol] > ma150.at[dt, symbol]) + int(
                close.at[dt, symbol] > ma200.at[dt, symbol]
            )
            result[symbol] = weight * votes / 2
        return result
    return target


def main():
    close = load_etfs()[["SPY", "QQQ"]]
    monthly = set(month_end_dates(close.index))
    candidates = []
    curves = {}
    for spy_weight, ma_days, below_multiplier in itertools.product(
        [0.4, 0.5, 0.6], [100, 150, 200], [0.0, 0.25, 0.5]
    ):
        name = f"spy{int(spy_weight*100)}_ma{ma_days}_risk{int(below_multiplier*100)}"
        result = run_engine(
            close, monthly, target_function(close, spy_weight, ma_days, below_multiplier),
            transaction_cost=0.001,
        )
        dev = metrics(rebase(result.equity, DEV_START, DEV_END))
        candidates.append({
            "name": name, "spy_weight": spy_weight, "qqq_weight": 1-spy_weight,
            "ma_days": ma_days, "below_multiplier": below_multiplier,
            "development": dev, "development_score": development_score(dev),
            "turnover": result.diagnostics["total_turnover"],
        })
        curves[name] = result.equity
    candidates.sort(key=lambda x: x["development_score"], reverse=True)
    finalists = candidates[:10]
    for item in finalists:
        item["oos_2019_2025"] = metrics(rebase(curves[item["name"]], OOS_START))

    best = finalists[0]
    cost_sensitivity = {}
    for cost in (0.001, 0.002, 0.005):
        result = run_engine(
            close, monthly, ensemble_target_function(close), transaction_cost=cost,
        )
        cost_sensitivity[str(cost)] = {
            "development": metrics(rebase(result.equity, DEV_START, DEV_END)),
            "oos_2019_2025": metrics(rebase(result.equity, OOS_START)),
        }

    ensemble_result = run_engine(
        close, monthly, ensemble_target_function(close), transaction_cost=0.001
    )
    ensemble = {
        "description": "50/50 SPY/QQQ; average of MA150 and MA200 binary trend votes",
        "development": metrics(rebase(ensemble_result.equity, DEV_START, DEV_END)),
        "oos_2019_2025": metrics(rebase(ensemble_result.equity, OOS_START)),
    }

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
            "development": [DEV_START, DEV_END], "oos": [OOS_START, END],
            "selection": "development only", "execution": "signal close -> next close",
            "transaction_cost": 0.001, "grid_size": len(candidates),
        },
        "best": finalists[0], "finalists": finalists, "ensemble": ensemble,
        "cost_sensitivity": {
            "applies_to": "V8 core ensemble",
            "results": cost_sensitivity,
        }, "benchmarks": benchmarks,
    }
    path = RESULTS_DIR / "v8_core_optimization_metrics.json"
    path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    curves[finalists[0]["name"]].to_csv(RESULTS_DIR / "v8_core_best_equity_curve.csv", index_label="date")
    ensemble_result.equity.to_csv(RESULTS_DIR / "v8_core_ensemble_equity_curve.csv", index_label="date")
    print("best", finalists[0])
    print("benchmarks", benchmarks)
    print(path)


if __name__ == "__main__":
    main()
