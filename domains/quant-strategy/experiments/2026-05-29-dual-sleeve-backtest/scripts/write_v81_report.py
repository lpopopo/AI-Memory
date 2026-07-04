#!/usr/bin/env python3
"""Render the V8.1 dynamic enhancement validation report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def pct(value):
    return f"{value * 100:.2f}%"


def rolling_comparison(data, left="V8.1", right="V8"):
    lrows = {r["window"]: r for r in data["comparison_evidence"][left]["rolling_3y"]}
    rrows = {r["window"]: r for r in data["comparison_evidence"][right]["rolling_3y"]}
    windows = sorted(set(lrows) & set(rrows))
    return {
        "windows": len(windows),
        "cagr_wins": sum(lrows[w]["cagr"] > rrows[w]["cagr"] for w in windows),
        "drawdown_wins": sum(lrows[w]["max_drawdown"] > rrows[w]["max_drawdown"] for w in windows),
        "sharpe_wins": sum(lrows[w]["sharpe"] > rrows[w]["sharpe"] for w in windows),
    }


def main():
    data = json.load(open(RESULTS / "v81_dynamic_optimization_metrics.json"))
    selected = data["selected"]
    compare = data["benchmarks_and_attribution"]
    period = "secondary_2019_2025"
    roll_v8 = rolling_comparison(data, "V8.1", "V8")
    roll_static = rolling_comparison(data, "V8.1", "SPY_QQQ_50_50")
    cfg = selected["config"]

    labels = ["V8", "V8.1_core_only_same_config", "V8.1_full", "SPY", "QQQ", "SPY_QQQ_50_50"]
    names = {
        "V8": "正式V8",
        "V8.1_core_only_same_config": "V8.1同配置核心（无增强）",
        "V8.1_full": "V8.1动态QQQ/VT增强",
        "SPY": "SPY", "QQQ": "QQQ", "SPY_QQQ_50_50": "SPY/QQQ 50/50",
    }
    rows = []
    for key in labels:
        m = compare[key][period]
        rows.append(
            f"| {names[key]} | {pct(m['cagr'])} | {pct(m['max_drawdown'])} | "
            f"{pct(m['volatility'])} | {m['sharpe']:.2f} | {m['sortino']:.2f} |"
        )

    lines = [
        "# V8.1 动态指数增强验证报告", "",
        "**开发期：** 2006-01-01 至 2018-12-31  ",
        "**二次历史确认：** 2019-01-01 至 2025-12-30（不是全新样本外）  ",
        "**资产：** 独立指数资金池，仅 SPY、QQQ、VT、现金；无杠杆  ",
        "**结论：** **不晋级，正式策略继续使用V8。**", "",
        "## 选中配置", "",
        f"- 检查频率：{cfg['frequency']}。",
        f"- 迟滞带：{cfg['hysteresis']:.0%}。",
        f"- 连续确认：{cfg['confirmation']}次。",
        f"- 趋势关闭后最低核心比例：{cfg['floor_fraction']:.0%}。",
        "- 增强预算：未使用核心仓位与50%两者的较小值。",
        "- 增强候选：QQQ/VT需站上MA200且126日动量为正，再按63日+126日动量择强。",
        "", "## 2019–2025统一对比", "",
        "| 策略 | CAGR | 最大回撤 | 波动率 | Sharpe | Sortino |",
        "|---|---:|---:|---:|---:|---:|",
        *rows,
        "", "## 晋级门槛", "",
        "| 检查 | 结果 |", "|---|---|",
    ]
    check_labels = {
        "development_hard_gate": "开发期满足回撤≤30%、Sharpe≥0.90，再按CAGR择优",
        "secondary_cagr": "2019–2025 CAGR≥17%",
        "secondary_drawdown": "2019–2025最大回撤≤30%",
        "secondary_sharpe": "2019–2025 Sharpe≥0.90",
        "cost_0_5pct_improves_on_v8_cagr_by_1pp": "0.5%成本下CAGR至少比V8高1个百分点",
        "parameter_plateau_at_least_3": "至少3组邻近参数表现接近",
    }
    for key, passed in data["promotion_checks"].items():
        lines.append(f"| {check_labels[key]} | {'通过' if passed else '未通过'} |")

    full = compare["V8.1_full"][period]
    core = compare["V8.1_core_only_same_config"][period]
    v8 = compare["V8"][period]
    selection = selected["enhancer_selection_frequency"]
    lines += [
        "", "## 收益归因", "",
        f"- 正式V8：CAGR {pct(v8['cagr'])}、回撤 {pct(v8['max_drawdown'])}、Sharpe {v8['sharpe']:.2f}。",
        f"- 仅加入1%迟滞与25%最低核心仓位：CAGR {pct(core['cagr'])}、回撤 {pct(core['max_drawdown'])}、Sharpe {core['sharpe']:.2f}。",
        f"- 再加入动态增强：CAGR降至 {pct(full['cagr'])}，回撤扩大至 {pct(full['max_drawdown'])}，Sharpe降至 {full['sharpe']:.2f}。",
        f"- 增强选择次数：QQQ {selection.get('QQQ', 0)} 次，VT {selection.get('VT', 0)} 次。VT没有贡献实际持仓。",
        f"- 历史最高QQQ权重：{pct(selected['max_observed_weights']['QQQ'])}；历史最高VT权重：{pct(selected['max_observed_weights']['VT'])}。",
        "", "## 滚动三年", "",
        f"- 对比正式V8：{roll_v8['windows']}个窗口中，V8.1有{roll_v8['cagr_wins']}个CAGR更高、{roll_v8['drawdown_wins']}个回撤更小、{roll_v8['sharpe_wins']}个Sharpe更高。",
        f"- 对比静态50/50：{roll_static['windows']}个窗口中，V8.1有{roll_static['cagr_wins']}个CAGR更高、{roll_static['drawdown_wins']}个回撤更小、{roll_static['sharpe_wins']}个Sharpe更高。",
        "", "## 压力期", "",
        "| 时段 | V8.1收益 | V8.1回撤 | V8收益 | V8回撤 | 静态50/50收益 | 静态回撤 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    periods = [
        ("financial_crisis_2008", "2008金融危机"),
        ("covid_2020", "2020疫情"),
        ("inflation_2022", "2022通胀熊市"),
    ]
    for key, label in periods:
        a = data["comparison_evidence"]["V8.1"]["stress"][key]
        b = data["comparison_evidence"]["V8"]["stress"][key]
        c = data["comparison_evidence"]["SPY_QQQ_50_50"]["stress"][key]
        lines.append(
            f"| {label} | {pct(a['cagr'])} | {pct(a['max_drawdown'])} | "
            f"{pct(b['cagr'])} | {pct(b['max_drawdown'])} | "
            f"{pct(c['cagr'])} | {pct(c['max_drawdown'])} |"
        )
    lines += [
        "", "## 成本敏感性", "",
        "| 单边成本 | CAGR | 最大回撤 | Sharpe |", "|---:|---:|---:|---:|",
    ]
    for cost, periods_data in data["cost_sensitivity"].items():
        m = periods_data[period]
        lines.append(f"| {float(cost):.2%} | {pct(m['cagr'])} | {pct(m['max_drawdown'])} | {m['sharpe']:.2f} |")
    lines += [
        "", "## 决策", "",
        "- 动态QQQ/VT增强没有提供增量价值，且明显扩大回撤；不写入正式策略。",
        "- 1%迟滞与25%最低核心仓位值得保留为后续独立研究候选，但本轮开发期硬门槛未通过，不能借用2019–2025表现直接晋级。",
        "- 实时信号器支持`--version v8.1`，但输出明确标记`research_only_not_promoted`。",
        "", "## 复现", "",
        "```bash",
        "python -m unittest -v scripts/test_v81_dynamic_enhancer.py",
        "python scripts/optimize_v81_dynamic.py",
        "python scripts/write_v81_report.py",
        "python scripts/v8_signal.py --version v8.1 --json",
        "```", "",
        "*不构成投资建议。*",
    ]
    path = RESULTS / "v81_dynamic_optimization_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
