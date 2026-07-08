#!/usr/bin/env python3
"""Frozen V9 ablation for common-factor theme aggregation.

This comparison changes only the aggregation switch. It does not optimize the
70-point score threshold or alter event availability timestamps.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from validate_v9_april_retrospective import END, FROZEN, START
from validate_v9_information_strategy import failure_date, load_data, stats
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store


def run(aggregate_common_factors: bool):
    panels, vix, _ = load_data()
    events, raw = load_event_store(ROOT / "datasets/v9_information_events.json")
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    cfg = V9Config(
        transaction_cost=.001,
        source_healthy=raw["source_health"] == "healthy",
        source_failure_date=failure_date(raw),
        aggregate_common_factors=aggregate_common_factors,
        **FROZEN,
    )
    result = V9Backtester(panels, vix, events, cfg, updates).run()
    info_columns = [c for c in result.weights.columns if c not in {"SPY", "QQQ", "cash"}]
    invested = result.weights[info_columns].abs().sum(axis=1) > 1e-12 if info_columns else []
    entries = [x for x in result.ledger if x.get("reason") == "buy" and x.get("is_info")]
    diag = {
        "stock_invested_days": int(sum(invested)),
        "symbols_held": sorted({x["symbol"] for x in entries}),
        "entry_count": len(entries),
    }
    return result, stats(result.equity, START, END), diag


def main():
    legacy, legacy_stats, legacy_diag = run(False)
    optimized, optimized_stats, optimized_diag = run(True)
    output = {
        "status": "frozen_parameter_ablation_not_promotion_evidence",
        "period": [START, END],
        "unchanged_parameters": FROZEN,
        "single_change": "aggregate AI-capex subthemes and sum all positions in each common-factor bucket",
        "legacy": {"metrics": legacy_stats, "diagnostics": legacy_diag},
        "optimized": {"metrics": optimized_stats, "diagnostics": optimized_diag},
        "delta": {
            "total_return": optimized_stats["total_return"] - legacy_stats["total_return"],
            "max_drawdown": optimized_stats["max_drawdown"] - legacy_stats["max_drawdown"],
            "entry_count": optimized_diag["entry_count"] - legacy_diag["entry_count"],
        },
        "interpretation": (
            "No historical performance delta is expected when both frozen runs have zero information-stock entries. "
            "The change repairs future capacity accounting and is validated by unit tests, not by claiming historical alpha."
        ),
    }
    results = ROOT / "results"
    metrics_path = results / "v9_common_factor_ablation_metrics.json"
    report_path = results / "v9_common_factor_ablation_report.md"
    metrics_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(
        f"""# V9 共同因子主题聚合消融回测

## 口径

- 区间：{START} 至 {END}。
- 唯一变化：旧版按事件细分主题分别计数；优化版将 AI 互连、存储、HBM 上游、云工厂、定制芯片等聚合为 `ai_capex`，并对同一风险桶内全部持仓求和。
- 固定 70 分门槛、点时事件、两日确认、交易成本和其余冻结参数；未调参、未回填事件。

## 结果

| 版本 | 累计收益 | 最大回撤 | 信息股入场 |
| --- | ---: | ---: | ---: |
| 旧主题计数 | {legacy_stats['total_return']:.2%} | {legacy_stats['max_drawdown']:.2%} | {legacy_diag['entry_count']} |
| 共同因子聚合 | {optimized_stats['total_return']:.2%} | {optimized_stats['max_drawdown']:.2%} | {optimized_diag['entry_count']} |

## 判定

两组冻结回测均无信息股入场，因此收益和回撤没有变化。这不能证明聚合规则提升收益，也不能成为 V9 晋级依据。优化的有效证据是：旧实现会覆盖而非累加同主题多持仓，且不同 AI-capex 标签可绕开共同主题上限；新实现修复了这两个容量计算缺陷，并由单元测试验证。
""",
        encoding="utf-8",
    )
    print(json.dumps({"metrics": str(metrics_path), "report": str(report_path), **output["delta"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
