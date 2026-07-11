#!/usr/bin/env python3
"""Pre-registered V9.1 shadow comparison; never alters the frozen V9 chain."""
from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_core import ensemble_target_function
from validate_v9_information_strategy import benchmark, failure_date, load_data, stats
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store

START = "2026-04-27"
END = "2026-07-10"
V91 = {
    "entry_rule_version": "E",
    "score_threshold": 75.0,
    "tech_weight": 1.6,
    "trusted_event_only": True,
    "min_source_completeness": 15,
    "min_fundamental": 10,
}


def diagnostics(result):
    info_trades = [x for x in result.ledger if x.get("is_info")]
    entries = [x for x in info_trades if x.get("action") == "BUY"]
    info_columns = [c for c in result.weights.columns if c not in {"SPY", "QQQ", "cash"}]
    invested_days = int((result.weights[info_columns].abs().sum(axis=1) > 1e-12).sum()) if info_columns else 0
    funnel = {}
    for item in result.funnel:
        funnel[item["reason"]] = funnel.get(item["reason"], 0) + 1
    return {
        "entries": len(entries),
        "symbols": sorted({x["symbol"] for x in entries}),
        "stock_invested_days": invested_days,
        "information_net_contribution": sum(x.get("info_official_pnl", 0.0) + x.get("info_obs_pnl", 0.0) for x in result.audit),
        "information_trades": info_trades,
        "pending_orders_latest": result.audit[-1].get("pending_orders", []) if result.audit else [],
        "funnel_rejections": dict(sorted(funnel.items())),
    }


def run(name, config, start, end):
    panels, vix, _ = load_data()
    events, raw = load_event_store(ROOT / "datasets/v9_information_events.json")
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    result = V9Backtester(panels, vix, events, config, updates).run()
    return name, {"metrics": stats(result.equity, start, end), "diagnostics": diagnostics(result)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default=START)
    parser.add_argument("--end", default=END)
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    start, end = args.start, args.end
    label = f"_{args.label}" if args.label else ""
    _, raw = load_event_store(ROOT / "datasets/v9_information_events.json")
    failed_on = failure_date(raw)
    shared = {"transaction_cost": .001, "source_failure_date": failed_on}
    runs = dict([
        run("V9_actual_source", V9Config(source_healthy=raw["source_health"] == "healthy", entry_rule_version="E", **shared), start, end),
        run("V9_healthy_source_counterfactual", V9Config(source_healthy=True, entry_rule_version="E", **shared), start, end),
        run("V9_1_actual_source", V9Config(source_healthy=raw["source_health"] == "healthy", **V91, **shared), start, end),
        run("V9_1_healthy_source_counterfactual", V9Config(source_healthy=True, **V91, **shared), start, end),
    ])
    panels, _, _ = load_data()
    runs["V8_defensive_core"] = {
        "metrics": stats(benchmark(panels["close"], ensemble_target_function(panels["close"])), start, end),
        "diagnostics": {"entries": None, "stock_invested_days": None, "information_net_contribution": None},
    }
    v9 = runs["V9_healthy_source_counterfactual"]
    v91 = runs["V9_1_healthy_source_counterfactual"]
    output = {
        "status": "shadow_hypothesis_not_promoted",
        "period": [start, end],
        "v91_pre_registered_parameters": V91,
        "data_source_health": raw["source_health"],
        "runs": runs,
        "healthy_source_delta_vs_v9": {
            "total_return": v91["metrics"]["total_return"] - v9["metrics"]["total_return"],
            "max_drawdown": v91["metrics"]["max_drawdown"] - v9["metrics"]["max_drawdown"],
            "entry_count": v91["diagnostics"]["entries"] - v9["diagnostics"]["entries"],
        },
        "limitations": [
            "This is a single pre-registered shadow variant, not an optimization sweep.",
            "Actual source health is partial, so no new information entry can be treated as live-authorized.",
            "The reliable point-in-time event sample remains below 50 and cannot support promotion.",
        ],
    }
    path = RESULTS_DIR / f"v91_technical_confirmation_metrics{label}.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = ["# V9.1 技术确认强化影子验证", "", "## 预注册假设", "", "可信点时事件（来源完整度≥15、基本面≥10）先进入候选池；技术确认权重由 1.0 提高到 1.6，总分门槛从 70 调整到 75，Rule E 等待区间随门槛变为 70–75。原 V9 冻结链和默认参数未修改。", "", "## 结果", "", "| 版本 | 收益 | 最大回撤 | 资讯买入 | 资讯持仓日 |", "| --- | ---: | ---: | ---: | ---: |"]
    for name in ("V8_defensive_core", "V9_actual_source", "V9_healthy_source_counterfactual", "V9_1_actual_source", "V9_1_healthy_source_counterfactual"):
        row = runs[name]
        rows.append(f"| {name} | {row['metrics']['total_return']:.2%} | {row['metrics']['max_drawdown']:.2%} | {row['diagnostics']['entries']} | {row['diagnostics']['stock_invested_days']} |")
    rows += ["", "## 判定", "", "该输出仅用于验证技术权重强化是否改变信号通过率、回撤与交易质量。没有达到足够可靠事件、独立交易数和前向观察期前，不得晋升或替代 V8/V9。"]
    (RESULTS_DIR / f"v91_technical_confirmation_report{label}.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
