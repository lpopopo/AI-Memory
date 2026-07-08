#!/usr/bin/env python3
"""Ablate AQR/Citadel/GMO/Man-inspired V9 overlays without tuning them."""
from __future__ import annotations

import json
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from validate_v9_april_retrospective import END, START, publication_time_events
from validate_v9_information_strategy import load_data, stats
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store

VARIANTS = {
    "baseline": {},
    "aqr_triple_confirmation": {"institutional_triple_confirmation": True},
    "citadel_flow_fragility": {"institutional_flow_overlay": True},
    "gmo_man_evidence_quality_sizing": {"institutional_quality_sizing": True},
    "all_institutional_overlays": {
        "institutional_triple_confirmation": True,
        "institutional_flow_overlay": True,
        "institutional_quality_sizing": True,
    },
}


def diagnostics(result):
    buys = [x for x in result.ledger if x["is_info"] and x["action"] == "BUY"]
    sells = [x for x in result.ledger if x["is_info"] and x["action"] == "SELL"]
    reasons = {}
    for row in result.funnel:
        reasons[row.get("reason", "unknown")] = reasons.get(row.get("reason", "unknown"), 0) + 1
    return {
        "information_buys": len(buys),
        "information_sells": len(sells),
        "symbols_bought": sorted({x["symbol"] for x in buys}),
        "information_turnover": float(sum(abs(x["shares"] * x["price"]) for x in result.ledger if x["is_info"])),
        "funnel_reasons": dict(sorted(reasons.items())),
    }


def run(events, updates, source_healthy, threshold, entry_rule, transaction_cost, options):
    panels, vix, _ = load_data()
    cfg = V9Config(
        score_threshold=threshold,
        entry_rule_version=entry_rule,
        source_healthy=source_healthy,
        transaction_cost=transaction_cost,
        **options,
    )
    result = V9Backtester(panels, vix, events, cfg, updates).run()
    return {"metrics": stats(result.equity, START, END), "diagnostics": diagnostics(result)}


def main():
    events, raw = load_event_store(ROOT / "datasets/v9_information_events.json")
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    publication, timestamp_notes = publication_time_events(events, raw)

    official = {name: run(events, updates, raw["source_health"] == "healthy", 70.0, "E", .001, opts) for name, opts in VARIANTS.items()}
    # A deliberately separate execution diagnostic. Threshold 55 and publication-time
    # events are not promotion evidence; they only exercise sizing/filter behavior in
    # a sample where the frozen 70-point strategy has no information trades.
    diagnostic = {name: run(publication, updates, True, 55.0, "A", .001, opts) for name, opts in VARIANTS.items()}
    all_costs = {str(cost): run(publication, updates, True, 55.0, "A", cost, VARIANTS["all_institutional_overlays"]) for cost in (.001, .002, .005)}

    output = {
        "status": "institutional_overlay_ablation_research_only",
        "period": [START, END],
        "official_frozen_70_point_in_time": official,
        "execution_diagnostic_55_publication_time": diagnostic,
        "all_overlay_cost_sensitivity_diagnostic": all_costs,
        "timestamp_notes": timestamp_notes,
        "quality_data_boundary": "No point-in-time financial statement panel exists. The GMO/Man module sizes only by point-in-time primary-evidence validation; FCF, debt, margin and customer concentration are specification-only until data is acquired.",
        "promotion_allowed": False,
    }
    results = ROOT / "results"
    metrics_path = results / "v9_institutional_overlay_ablation_metrics.json"
    report_path = results / "v9_institutional_overlay_ablation_report.md"
    metrics_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    def rows(section):
        return "\n".join(
            f"| {name} | {row['metrics']['total_return']:.2%} | {row['metrics']['max_drawdown']:.2%} | {row['metrics']['annualized_sharpe']:.2f} | {row['diagnostics']['information_buys']} | {row['diagnostics']['information_turnover']:.3f} |"
            for name, row in section.items()
        )
    report_path.write_text(f"""# 四大机构思想驱动的V9优化消融回测

## 优化模块

- AQR：价格位于MA20之上且MA20高于MA50、相对QQQ为正、成交量不低于20日均量80%。
- Citadel：用候选参与度、AI相对QQQ、MA20延伸、VIX和spot-up/vol-up构造0–10流量脆弱度；4–6分新仓缩小25%，7分以上缩小50%并阻止追高。
- GMO/Man：没有点时财务面板，因此只按当时已知的一手证据验证强度把新仓乘以100%/75%/60%；没有用今天的FCF或债务数据回填历史。

## 正式冻结口径：70分、真实首次发现时间

| 版本 | 收益 | 最大回撤 | Sharpe | 信息买入 | 信息换手 |
| --- | ---: | ---: | ---: | ---: | ---: |
{rows(official)}

## 执行压力诊断：55分、发布时点假设

此部分只用于让模块产生足够订单以检查行为，不是可复现实盘历史，也不能用于晋级。

| 版本 | 收益 | 最大回撤 | Sharpe | 信息买入 | 信息换手 |
| --- | ---: | ---: | ---: | ---: | ---: |
{rows(diagnostic)}

## 证据边界

正式70分样本若继续零交易，只能说明新模块没有改变冻结结论，不能证明其有效。真正的GMO/Man质量评分仍需点时季度财务、债务、客户集中度和分部AI收入数据。
""", encoding="utf-8")
    print(json.dumps({"metrics": str(metrics_path), "report": str(report_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
