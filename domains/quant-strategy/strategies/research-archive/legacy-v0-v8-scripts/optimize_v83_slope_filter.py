#!/usr/bin/env python3
"""Evaluate slope confirmation without looking at the secondary period during selection."""

from __future__ import annotations

import itertools
import json
import sys
from dataclasses import asdict
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_etf import DEV_END, DEV_START, END, OOS_START, load_etfs, rebase
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import rebalance_dates
from v83_slope_filter import V83Allocator, V83Config

PROMOTION = {"cagr": .17, "max_drawdown": -.30, "sharpe": .90}


def configs():
    yield V83Config()
    for lookback, threshold, apply_to in itertools.product(
        [21, 63, 126], [0.0, .005, .01], ["ma200", "both"]
    ):
        yield V83Config(lookback, threshold, apply_to)


def run(close, config, cost=.001):
    allocator = V83Allocator(close, config)
    result = run_engine(close, rebalance_dates(close.index, "monthly"), allocator.target,
                        transaction_cost=cost)
    return result, allocator


def periods(curve):
    return {
        "development_2006_2018": metrics(rebase(curve, DEV_START, DEV_END)),
        "secondary_2019_2025": metrics(rebase(curve, OOS_START, END)),
        "full_2006_2025": metrics(rebase(curve, DEV_START, END)),
    }


def rolling(curve):
    rows=[]
    for year in range(2006, 2024):
        x=curve.loc[f"{year}-01-01":f"{year+2}-12-31"].dropna()
        if len(x)>=600:
            rows.append({"window":f"{year}-{year+2}", **metrics(x/x.iloc[0])})
    return rows


def stress(curve):
    return {name: metrics(rebase(curve, start, end)) for name,start,end in [
        ("2008","2008-01-01","2008-12-31"),
        ("2020","2020-01-01","2020-12-31"),
        ("2022","2022-01-01","2022-12-31"),
    ]}


def main():
    close=load_etfs()[["SPY","QQQ"]].loc[DEV_START:END]
    candidates=[]; results={}; allocators={}
    for i,cfg in enumerate(configs()):
        result,allocator=run(close,cfg)
        dev=periods(result.equity)["development_2006_2018"]
        eligible=dev["max_drawdown"]>=-.30 and dev["sharpe"]>=.90
        key=f"candidate_{i:02d}"
        candidates.append({"key":key,"config":asdict(cfg),"development":dev,
                           "development_eligible":eligible,
                           "turnover":result.diagnostics["total_turnover"]})
        results[key]=result; allocators[key]=allocator
    pool=[x for x in candidates if x["development_eligible"]]
    if not pool: pool=[x for x in candidates if x["development"]["max_drawdown"]>=-.30]
    selected=max(pool or candidates,key=lambda x:x["development"]["cagr"])
    result=results[selected["key"]]
    selected["metrics"]=periods(result.equity)
    selected["rolling_3y"]=rolling(result.equity)
    selected["stress"]=stress(result.equity)
    selected["latest_audit"]=allocators[selected["key"]].audit[-1]
    costs={}
    cfg=V83Config(**selected["config"])
    for cost in [.001,.002,.005]: costs[str(cost)]=periods(run(close,cfg,cost)[0].equity)
    secondary=selected["metrics"]["secondary_2019_2025"]
    checks={"development_gate":selected["development_eligible"],
            "secondary_cagr":secondary["cagr"]>=.17,
            "secondary_drawdown":secondary["max_drawdown"]>=-.30,
            "secondary_sharpe":secondary["sharpe"]>=.90}
    output={"method":{"development":[DEV_START,DEV_END],"secondary":[OOS_START,END],
                     "secondary_is_not_fresh_oos":True,"candidate_count":len(candidates),
                     "selection":"maximize development CAGR after hard gates",
                     "transaction_cost":.001,"no_leverage":True},
            "selected":selected,"development_eligible_count":sum(x["development_eligible"] for x in candidates),
            "all_candidates":candidates,"baseline_v8":periods(results["candidate_00"].equity),
            "cost_sensitivity":costs,"promotion_checks":checks,"promoted":all(checks.values())}
    path=RESULTS_DIR/"v83_slope_filter_metrics.json"
    path.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"selected":selected,"eligible_count":output["development_eligible_count"],
                      "checks":checks},ensure_ascii=False,indent=2)); print(path)


if __name__=="__main__": main()
