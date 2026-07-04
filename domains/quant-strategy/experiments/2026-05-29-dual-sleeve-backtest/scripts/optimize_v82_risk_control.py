#!/usr/bin/env python3
"""Development-only selection of V8 risk weighting / volatility control."""

from __future__ import annotations

import itertools
import json
import sys
from dataclasses import asdict
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_core import ensemble_target_function
from optimize_v8_etf import DEV_END, DEV_START, END, OOS_START, load_etfs, rebase
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import rebalance_dates
from v82_risk_control import V82Allocator, V82Config

PROMOTION = {"cagr": 0.17, "max_drawdown": -0.30, "sharpe": 0.90}


def configurations():
    # Baseline plus bounded hypotheses; duplicates are deliberately excluded.
    yield V82Config()
    for risk_lookback, qqq_cap in itertools.product([60, 126], [0.50, 0.60, 1.0]):
        yield V82Config("inverse_vol", risk_lookback, None, 60, qqq_cap)
    for target, vol_lookback in itertools.product([0.10, 0.12, 0.15], [20, 60]):
        yield V82Config("fixed", 60, target, vol_lookback, 1.0)
    for risk_lookback, target, vol_lookback, qqq_cap in itertools.product(
        [60, 126], [0.10, 0.12, 0.15], [20, 60], [0.50, 0.60, 1.0]
    ):
        yield V82Config("inverse_vol", risk_lookback, target, vol_lookback, qqq_cap)


def run(close, config, cost=0.001):
    allocator = V82Allocator(close, config)
    result = run_engine(close, rebalance_dates(close.index, "monthly"), allocator.target,
                        transaction_cost=cost)
    return result, allocator


def period_metrics(curve):
    return {
        "development_2006_2018": metrics(rebase(curve, DEV_START, DEV_END)),
        "secondary_2019_2025": metrics(rebase(curve, OOS_START, END)),
        "full_2006_2025": metrics(rebase(curve, DEV_START, END)),
    }


def rolling_three_year(curve):
    rows = []
    for year in range(2006, 2024):
        segment = curve.loc[f"{year}-01-01":f"{year+2}-12-31"].dropna()
        if len(segment) >= 600:
            rows.append({"window": f"{year}-{year+2}", **metrics(segment / segment.iloc[0])})
    return rows


def main():
    close = load_etfs()[["SPY", "QQQ"]].loc[DEV_START:END]
    candidates = []
    results = {}
    allocators = {}
    for i, config in enumerate(configurations()):
        result, allocator = run(close, config)
        dev = period_metrics(result.equity)["development_2006_2018"]
        key = f"candidate_{i:02d}"
        eligible = dev["max_drawdown"] >= -0.30 and dev["sharpe"] >= 0.90
        candidates.append({"key": key, "config": asdict(config), "development": dev,
                           "development_eligible": eligible,
                           "turnover": result.diagnostics["total_turnover"]})
        results[key] = result
        allocators[key] = allocator

    pool = [x for x in candidates if x["development_eligible"]]
    if not pool:
        pool = [x for x in candidates if x["development"]["max_drawdown"] >= -0.30]
    selected = max(pool or candidates, key=lambda x: x["development"]["cagr"])
    selected_result = results[selected["key"]]
    selected["metrics"] = period_metrics(selected_result.equity)
    selected["rolling_3y"] = rolling_three_year(selected_result.equity)
    selected["latest_audit"] = allocators[selected["key"]].audit[-1]

    v8 = run_engine(close, rebalance_dates(close.index, "monthly"),
                    ensemble_target_function(close), transaction_cost=0.001)
    costs = {}
    config = V82Config(**selected["config"])
    for cost in [0.001, 0.002, 0.005]:
        result, _ = run(close, config, cost)
        costs[str(cost)] = period_metrics(result.equity)

    secondary = selected["metrics"]["secondary_2019_2025"]
    checks = {
        "development_gate": selected["development_eligible"],
        "secondary_cagr": secondary["cagr"] >= PROMOTION["cagr"],
        "secondary_drawdown": secondary["max_drawdown"] >= PROMOTION["max_drawdown"],
        "secondary_sharpe": secondary["sharpe"] >= PROMOTION["sharpe"],
    }
    output = {
        "method": {"development": [DEV_START, DEV_END], "secondary": [OOS_START, END],
                   "secondary_is_not_fresh_oos": True, "candidate_count": len(candidates),
                   "selection": "maximize development CAGR after DD/Sharpe hard gates",
                   "no_leverage": True, "transaction_cost": 0.001},
        "selected": selected,
        "development_eligible_count": sum(x["development_eligible"] for x in candidates),
        "all_candidates": candidates,
        "formal_v8": period_metrics(v8.equity),
        "cost_sensitivity": costs,
        "promotion_checks": checks,
        "promoted": all(checks.values()),
    }
    path = RESULTS_DIR / "v82_risk_control_metrics.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"selected": selected, "eligible_count": output["development_eligible_count"],
                      "formal_v8": output["formal_v8"], "checks": checks},
                     ensure_ascii=False, indent=2))
    print(path)


if __name__ == "__main__":
    main()
