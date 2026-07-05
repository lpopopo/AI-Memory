#!/usr/bin/env python3
"""Frozen-parameter April-to-date V9 retrospective and point-in-time comparison."""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_core import ensemble_target_function
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import rebalance_dates
from v87_dynamic_regime import V87Allocator, V87Config
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store
from validate_v9_information_strategy import benchmark, failure_date, load_data, stats

START = "2026-04-27"
END = "2026-07-02"
FROZEN = {"score_threshold": 70.0, "tech_weight": 1.0, "score_cap_scale": 1.0}


def publication_time_events(events, raw):
    """Build a clearly hypothetical publication-time event set.

    Date-only timestamps remain approximate. Events without publication timestamps
    retain their actual local availability time and are not backdated.
    """
    rows = {x["event_id"]: x for x in raw["events"]}
    out = []
    approximate = 0
    missing = 0
    for event in events:
        published = rows[event.event_id].get("published_at")
        if not published:
            missing += 1
            out.append(event)
            continue
        ts = pd.Timestamp(published)
        if ts.tzinfo is not None:
            ts = ts.tz_convert("UTC").tz_localize(None)
        if ts.hour == 12 and ts.minute == 0 and ts.second == 0:
            approximate += 1
        out.append(replace(event, effective_at=ts, point_in_time_eligible=False))
    return sorted(out, key=lambda e: e.effective_at), {"approximate_publication_times": approximate, "missing_publication_times": missing}


def run_v9(panels, vix, events, updates, cost, source_healthy=True, source_failure_date=None):
    cfg = V9Config(transaction_cost=cost, source_healthy=source_healthy, source_failure_date=source_failure_date, **FROZEN)
    return V9Backtester(panels, vix, events, cfg, updates).run()


def diagnostics(result):
    audit = [x for x in result.audit if START <= x["date"] <= END]
    invested = [x for x in audit if x["stock_targets"]]
    symbols = sorted({s for x in invested for s in x["stock_targets"]})
    entries = []
    max_scores = {}
    confirmed_symbol_days = 0
    threshold_symbol_days = 0
    qualified_symbol_days = 0
    previous = set()
    for row in audit:
        for item in row.get("watchlist", []):
            max_scores[item["symbol"]] = max(max_scores.get(item["symbol"], float("-inf")), float(item["score"]))
            confirmed_symbol_days += int(item["confirmed"])
            threshold_symbol_days += int(item["score"] >= FROZEN["score_threshold"])
            qualified_symbol_days += int(item["confirmed"] and item["score"] >= FROZEN["score_threshold"])
        current = set(row["stock_targets"])
        for symbol in sorted(current - previous):
            entries.append({"date": row["date"], "symbol": symbol, "target_weight": row["stock_targets"][symbol]})
        previous = current
    top_scores = [{"symbol": s, "max_score": score} for s, score in sorted(max_scores.items(), key=lambda x: x[1], reverse=True)[:10]]
    return {"stock_invested_days": len(invested), "symbols_held": symbols, "entry_count": len(entries), "entries": entries, "confirmed_symbol_days": confirmed_symbol_days, "threshold_symbol_days": threshold_symbol_days, "qualified_symbol_days": qualified_symbol_days, "top_max_scores": top_scores}


def main():
    panels, vix, meta = load_data()
    events, raw = load_event_store(ROOT / "datasets/v9_information_events.json")
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    retrospective, timestamp_notes = publication_time_events(events, raw)
    failed_on = failure_date(raw)

    point = run_v9(panels, vix, events, updates, .001, raw["source_health"] == "healthy", failed_on)
    retrospective_runs = {str(c): run_v9(panels, vix, retrospective, updates, c) for c in (.001, .002, .005)}
    close = panels["close"]
    v8 = benchmark(close, ensemble_target_function(close))
    allocator = V87Allocator(close[["SPY", "QQQ"]], vix, V87Config(.7, 70, 75, .5, 1))
    v87 = run_engine(close, rebalance_dates(close.index, "monthly"), allocator.target, transaction_cost=.001).equity
    mix = (close.SPY.pct_change(fill_method=None).fillna(0) * .5 + close.QQQ.pct_change(fill_method=None).fillna(0) * .5 + 1).cumprod()

    comparisons = {
        "V9_point_in_time": stats(point.equity, START, END),
        "V9_publication_time_hypothetical": stats(retrospective_runs["0.001"].equity, START, END),
        "V8": stats(v8, START, END),
        "V8.7": stats(v87, START, END),
        "QQQ": stats(close.QQQ, START, END),
        "SPY_QQQ_50_50": stats(mix, START, END),
    }
    output = {
        "status": "retrospective_hypothesis_test_not_promotion_evidence",
        "period": [START, END],
        "data": meta,
        "parameters": {"selection": "frozen_before_this_run", **FROZEN},
        "execution": "signal at completed close; rebalance at next completed close",
        "event_counts": {
            "archive": len(events),
            "point_in_time_reliable": sum(e.source_completeness >= 15 and e.point_in_time_eligible for e in events),
            "retrospective_backfill": sum(not e.point_in_time_eligible for e in events),
        },
        "timestamp_notes": timestamp_notes,
        "comparisons": comparisons,
        "retrospective_cost_sensitivity": {cost: stats(run.equity, START, END) for cost, run in retrospective_runs.items()},
        "point_in_time_diagnostics": diagnostics(point),
        "retrospective_diagnostics": diagnostics(retrospective_runs["0.001"]),
        "validity": {
            "parameters_optimized_on_test_period": False,
            "retrospective_result_is_live_reproducible": False,
            "promotion_allowed": False,
            "reasons": [
                "31 historical posts were acquired after publication and therefore cannot prove live availability.",
                "31 publication timestamps are date-only approximations, so intraday availability is unknown.",
                "The evaluation window is only about two months and contains one dominant AI-infrastructure theme.",
            ],
        },
    }
    metrics_path = RESULTS_DIR / "v9_april_retrospective_metrics.json"
    metrics_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = "\n".join(
        f"| {name} | {m['total_return']:.2%} | {m['max_drawdown']:.2%} | {m['annualized_sharpe']:.2f} |"
        for name, m in comparisons.items()
    )
    cost_rows = "\n".join(
        f"| {float(cost):.1%} | {m['total_return']:.2%} | {m['max_drawdown']:.2%} | {m['annualized_sharpe']:.2f} |"
        for cost, m in output["retrospective_cost_sensitivity"].items()
    )
    rd = output["retrospective_diagnostics"]
    report = f"""# V9 2026年4月至今回顾性严谨回测

## 口径

- 参数在本轮前冻结：评分线70、技术权重1、仓位倍率1；没有在本区间选择最优参数。
- 信号只使用完成收盘数据，并在下一完成收盘执行；包含0.1%基础交易成本。
- `point-in-time`按本地首次获得资讯时间；`publication-time hypothetical`假设历史帖子发布时即可完整获得，只用于检验选题和规则，不代表可实盘复现。
- 数据区间为{START}至{END}，最新完整交易日来自行情缓存 `{meta['last_date']}`。

## 结果

| 模型 | 累计收益 | 最大回撤 | 年化Sharpe* |
|---|---:|---:|---:|
{rows}

*样本仅约两个月，年化Sharpe高度不稳定。*

## 回顾性V9成本敏感度

| 单位换手成本 | 累计收益 | 最大回撤 | 年化Sharpe |
|---:|---:|---:|---:|
{cost_rows}

## 选股行为

- 回顾性资讯个股持仓日：{rd['stock_invested_days']}。
- 入场次数：{rd['entry_count']}。
- 曾持有股票：{', '.join(rd['symbols_held']) if rd['symbols_held'] else '无'}。
- 完成技术确认的股票-交易日：{rd['confirmed_symbol_days']}；达到70分的股票-交易日：{rd['threshold_symbol_days']}；两者同时满足：{rd['qualified_symbol_days']}。
- 最高观察分数：{', '.join(f"{x['symbol']} {x['max_score']:.1f}" for x in rd['top_max_scores'][:5]) if rd['top_max_scores'] else '无'}。
- 真实点时回放的资讯个股持仓日：{output['point_in_time_diagnostics']['stock_invested_days']}。

## 判定

回顾性结果可以回答“若在发布日期已完整获得帖子，冻结规则表现如何”，但不能证明当时真实可交易。31条历史补录帖中有31条只有日期级近似发布时间，盘中先后顺序不可验证；样本期短且主题集中。因此该结果只能作为假设检验，不能用于V9晋级或再次调参。正式策略仍为V8。
"""
    report_path = RESULTS_DIR / "v9_april_retrospective_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(json.dumps({"metrics": str(metrics_path), "report": str(report_path), "comparisons": comparisons}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
