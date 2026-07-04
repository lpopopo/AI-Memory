#!/usr/bin/env python3
"""Optimize and validate the V8.1 dynamic QQQ/VT enhancement sleeve."""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

import pandas as pd
import yfinance as yf

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR, run_buy_hold
from optimize_v8_core import ensemble_target_function
from optimize_v8_etf import DEV_END, DEV_START, END, OOS_START, load_etfs, rebase
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import V81Allocator, V81Config, rebalance_dates


DATA_DIR = ROOT / "datasets" / "data_v81"
VT_CACHE = DATA_DIR / "VT_adjusted_close.csv"
PROMOTION = {"cagr": 0.17, "max_drawdown": -0.30, "sharpe": 0.90}


def load_v81_data() -> pd.DataFrame:
    base = load_etfs()[["SPY", "QQQ"]].loc[DEV_START:END]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if VT_CACHE.exists():
        vt = pd.read_csv(VT_CACHE, index_col=0, parse_dates=True).iloc[:, 0]
    else:
        raw = yf.download(
            "VT", start=DEV_START, end="2026-01-01", auto_adjust=True, progress=False
        )
        if raw.empty:
            raise RuntimeError("failed to download VT history")
        if isinstance(raw.columns, pd.MultiIndex):
            vt = raw["Close"].iloc[:, 0]
        else:
            vt = raw["Close"]
        vt.name = "VT"
        vt.to_csv(VT_CACHE, index_label="Date")
    base["VT"] = vt.reindex(base.index)
    return base


def run_variant(close, config: V81Config, cost=0.001, enhancer=True):
    allocator = V81Allocator(close, config, enhancer=enhancer)
    result = run_engine(
        close, rebalance_dates(close.index, config.frequency), allocator.target,
        transaction_cost=cost,
    )
    return result, allocator


def config_grid():
    for frequency, band, confirmation, floor in itertools.product(
        ["monthly", "weekly"], [0.0, 0.01, 0.02], [1, 2], [0.0, 0.25]
    ):
        yield V81Config(frequency, band, confirmation, floor)


def split_metrics(curve):
    return {
        "development_2006_2018": metrics(rebase(curve, DEV_START, DEV_END)),
        "secondary_2019_2025": metrics(rebase(curve, OOS_START, END)),
        "full_2006_2025": metrics(rebase(curve, DEV_START, END)),
    }


def stress_metrics(curve):
    periods = {
        "financial_crisis_2008": ("2008-01-01", "2008-12-31"),
        "covid_2020": ("2020-01-01", "2020-12-31"),
        "inflation_2022": ("2022-01-01", "2022-12-31"),
    }
    return {name: metrics(rebase(curve, start, end)) for name, (start, end) in periods.items()}


def rolling_three_year(curve):
    rows = []
    for year in range(2006, 2024):
        segment = curve.loc[f"{year}-01-01":f"{year+2}-12-31"].dropna()
        if len(segment) >= 600:
            rows.append({"window": f"{year}-{year+2}", **metrics(segment / segment.iloc[0])})
    return rows


def passes_development(metrics_row, thresholds=PROMOTION):
    return (
        metrics_row["max_drawdown"] >= thresholds["max_drawdown"]
        and metrics_row["sharpe"] >= thresholds["sharpe"]
    )


def main():
    close = load_v81_data()
    candidates = []
    curves = {}
    allocators = {}
    for config in config_grid():
        key = f"{config.frequency}_b{int(config.hysteresis*100)}_c{config.confirmation}_f{int(config.floor_fraction*100)}"
        result, allocator = run_variant(close, config)
        dev = split_metrics(result.equity)["development_2006_2018"]
        candidates.append({
            "key": key, "config": asdict(config), "development": dev,
            "development_eligible": passes_development(dev),
            "turnover": result.diagnostics["total_turnover"],
        })
        curves[key] = result
        allocators[key] = allocator

    eligible = [x for x in candidates if x["development_eligible"]]
    selection_pool = eligible or [
        x for x in candidates if x["development"]["max_drawdown"] >= -0.30
    ]
    if not selection_pool:
        selection_pool = candidates
    selection_pool.sort(key=lambda x: x["development"]["cagr"], reverse=True)
    selected = selection_pool[0]
    selected_key = selected["key"]
    selected_config = V81Config(**selected["config"])
    selected_result = curves[selected_key]
    selected_allocator = allocators[selected_key]

    # Only after development-only selection is frozen do we inspect 2019-2025.
    selected["metrics"] = split_metrics(selected_result.equity)
    selected["stress"] = stress_metrics(selected_result.equity)
    selected["rolling_3y"] = rolling_three_year(selected_result.equity)
    selected["max_observed_weights"] = {
        symbol: float(selected_result.weights[symbol].max()) if symbol in selected_result.weights else 0.0
        for symbol in ["SPY", "QQQ", "VT", "cash"]
    }
    selected["enhancer_selection_frequency"] = dict(Counter(
        row["enhancer_selected"] for row in selected_allocator.audit
        if row["enhancer_selected"] is not None
    ))

    core_only_result, _ = run_variant(close, selected_config, enhancer=False)
    v8_result = run_engine(
        close, rebalance_dates(close.index, "monthly"), ensemble_target_function(close),
        transaction_cost=0.001,
    )
    benchmarks = {
        "V8": split_metrics(v8_result.equity),
        "V8.1_core_only_same_config": split_metrics(core_only_result.equity),
        "V8.1_full": selected["metrics"],
    }
    for name, weights in {
        "SPY": {"SPY": 1.0}, "QQQ": {"QQQ": 1.0},
        "SPY_QQQ_50_50": {"SPY": 0.5, "QQQ": 0.5},
    }.items():
        benchmarks[name] = split_metrics(run_buy_hold(close, weights, name))

    comparison_curves = {
        "V8.1": selected_result.equity,
        "V8": v8_result.equity,
        "SPY_QQQ_50_50": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "mix"),
    }
    comparison_evidence = {
        name: {"stress": stress_metrics(curve), "rolling_3y": rolling_three_year(curve)}
        for name, curve in comparison_curves.items()
    }

    cost_sensitivity = {}
    for cost in [0.001, 0.002, 0.005]:
        result, _ = run_variant(close, selected_config, cost=cost)
        cost_sensitivity[str(cost)] = split_metrics(result.equity)

    near_optimal = [
        x for x in candidates
        if x["development"]["max_drawdown"] >= -0.30
        and x["development"]["cagr"] >= selected["development"]["cagr"] - 0.01
    ]
    secondary = selected["metrics"]["secondary_2019_2025"]
    cost_50 = cost_sensitivity["0.005"]["secondary_2019_2025"]
    promotion_checks = {
        "development_hard_gate": selected["development_eligible"],
        "secondary_cagr": secondary["cagr"] >= PROMOTION["cagr"],
        "secondary_drawdown": secondary["max_drawdown"] >= PROMOTION["max_drawdown"],
        "secondary_sharpe": secondary["sharpe"] >= PROMOTION["sharpe"],
        "cost_0_5pct_improves_on_v8_cagr_by_1pp": (
            cost_50["cagr"] >= benchmarks["V8"]["secondary_2019_2025"]["cagr"] + 0.01
        ),
        "parameter_plateau_at_least_3": len(near_optimal) >= 3,
    }
    promoted = all(promotion_checks.values())

    output = {
        "method": {
            "development": [DEV_START, DEV_END],
            "secondary_historical_confirmation": [OOS_START, END],
            "secondary_is_not_fresh_oos": True,
            "asset_scope": ["SPY", "QQQ", "VT", "cash"],
            "no_leverage": True, "enhancer_max": 0.50,
            "selection": "maximize development CAGR after hard gates",
            "promotion_thresholds": PROMOTION,
            "vt_first_valid_date": str(close["VT"].first_valid_index().date()),
        },
        "selected": selected,
        "development_eligible_count": len(eligible),
        "near_optimal_count": len(near_optimal),
        "near_optimal": near_optimal,
        "all_candidates": candidates,
        "benchmarks_and_attribution": benchmarks,
        "comparison_evidence": comparison_evidence,
        "cost_sensitivity": cost_sensitivity,
        "promotion_checks": promotion_checks,
        "promoted": promoted,
        "latest_audit": selected_allocator.audit[-1],
    }
    path = RESULTS_DIR / "v81_dynamic_optimization_metrics.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame({
        "V8.1": selected_result.equity, "V8": v8_result.equity,
        "V8.1_core_only": core_only_result.equity,
    }).to_csv(RESULTS_DIR / "v81_dynamic_equity_curves.csv", index_label="date")
    print("selected", selected_key, selected["development"])
    print("secondary", secondary)
    print("eligible", len(eligible), "near_optimal", len(near_optimal))
    print("promotion", promoted, promotion_checks)
    print(path)


if __name__ == "__main__":
    main()
