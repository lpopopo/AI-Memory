#!/usr/bin/env python3
"""Constrained V9.1 entry/exit study. Results are diagnostic, never promotion evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from validate_v9_information_strategy import load_data, stats
from validate_v91_technical_confirmation import V91, diagnostics
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store

START, END = "2026-05-01", "2026-07-10"
ENTRY_PATHS = ("any", "breakout", "pullback", "trend")
EXIT_POLICIES = {
    "current": {"hard_stop": .08, "trailing_stop_mode": "ma20", "time_stop_days": 3},
    "tight": {"hard_stop": .06, "trailing_stop_mode": "ma20", "time_stop_days": 3},
    "patient": {"hard_stop": .10, "trailing_stop_mode": "ma50", "time_stop_days": 5},
    "technical_staged": {"hard_stop": .06, "trailing_stop_mode": "ma20", "time_stop_days": 3, "dynamic_stop_mode": "technical_staged"},
}


def completed_trade_pnl(ledger):
    open_lots, rows = {}, []
    for item in ledger:
        if not item.get("is_info"):
            continue
        symbol = item["symbol"]
        if item["action"] == "BUY":
            open_lots[symbol] = item
        elif symbol in open_lots:
            buy = open_lots.pop(symbol)
            pnl = (item["price"] - buy["price"]) * buy["shares"] - buy["cost"] - item["cost"]
            rows.append({"symbol": symbol, "entry": buy["date"], "exit": item["date"], "exit_reason": item["reason"], "pnl": pnl})
    return rows


def run(path, policy, panels, vix, events, updates):
    cfg = V9Config(
        source_healthy=True,
        transaction_cost=.001,
        tech_path_mode=path,
        **V91,
        **policy,
    )
    result = V9Backtester(panels, vix, events, cfg, updates).run()
    diag = diagnostics(result)
    closed = completed_trade_pnl(result.ledger)
    return {
        "metrics": stats(result.equity, START, END),
        "entries": diag["entries"],
        "stock_invested_days": diag["stock_invested_days"],
        "information_net_contribution": diag["information_net_contribution"],
        "closed_trades": closed,
        "stop_loss_count": sum(x["exit_reason"] == "stop_loss" for x in closed),
    }


def main():
    panels, vix, _ = load_data()
    events, _ = load_event_store(ROOT / "datasets/v9_information_events.json")
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    results = {}
    for path in ENTRY_PATHS:
        for policy_name, policy in EXIT_POLICIES.items():
            results[f"{path}__{policy_name}"] = run(path, policy, panels, vix, events, updates)
    output = {
        "status": "diagnostic_grid_no_parameter_promotion",
        "period": [START, END],
        "fixed_v91_parameters": V91,
        "entry_paths": list(ENTRY_PATHS),
        "exit_policies": EXIT_POLICIES,
        "results": results,
        "interpretation_rule": "Do not select a live rule from this grid. Prefer only variants that preserve or improve return and drawdown with multiple independent trades, then forward-test them.",
    }
    (RESULTS_DIR / "v91_entry_exit_study_metrics.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# V9.1 入场与止损受限消融", "", "区间：2026-05-01 至 2026-07-10。固定可信事件门槛、技术权重 1.6、75 分门槛与成本；仅比较预先限定的技术路径和退出政策。", "", "| 入场路径 / 退出政策 | 收益 | 最大回撤 | 买入 | 止损卖出 | 资讯净贡献 |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for name, row in results.items():
        m = row["metrics"]
        lines.append(f"| {name} | {m['total_return']:.2%} | {m['max_drawdown']:.2%} | {row['entries']} | {row['stop_loss_count']} | {row['information_net_contribution']:.2%} |")
    lines += ["", "结论：这是小样本机制研究，不是参数优化或策略晋升依据。"]
    (RESULTS_DIR / "v91_entry_exit_study_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
