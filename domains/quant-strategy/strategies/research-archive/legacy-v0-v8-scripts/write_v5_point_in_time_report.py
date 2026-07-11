#!/usr/bin/env python3
"""Render the V5 point-in-time constituent validation report."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
POINT = ROOT / "datasets" / "data_point_in_time"


def pct(value):
    return f"{value * 100:.2f}%"


def main():
    data = json.load(open(RESULTS / "v5_point_in_time_metrics.json"))
    metadata = json.load(open(POINT / "metadata.json"))
    metrics = data["metrics"]
    coverage = pd.DataFrame(metadata["coverage_by_month"])
    coverage["date"] = pd.to_datetime(coverage["date"])
    coverage["year"] = coverage["date"].dt.year
    yearly = coverage.groupby("year").agg(
        price_coverage=("price_coverage", "mean"),
        indicator_coverage=("indicator_coverage", "mean"),
    )

    rows = []
    order = [
        "V5_current_constituents", "V5_PIT_available", "V5_PIT_coverage_adjusted",
        "SPY", "QQQ", "SPY_QQQ_50_50",
    ]
    labels = {
        "V5_current_constituents": "V5 当前成分偏差版",
        "V5_PIT_available": "V5 时间点成员（可用价格）",
        "V5_PIT_coverage_adjusted": "V5 时间点成员（覆盖率缩仓）",
        "SPY": "SPY", "QQQ": "QQQ", "SPY_QQQ_50_50": "SPY/QQQ 50/50",
    }
    for key in order:
        m = metrics[key]["report_2019_2025"]
        rows.append(
            f"| {labels[key]} | {pct(m['cagr'])} | {pct(m['max_drawdown'])} | "
            f"{m['sharpe']:.2f} | {m['sortino']:.2f} | {m['final_value']:.2f}× |"
        )

    current = metrics["V5_current_constituents"]["report_2019_2025"]
    pit = metrics["V5_PIT_available"]["report_2019_2025"]
    adjusted = metrics["V5_PIT_coverage_adjusted"]["report_2019_2025"]
    full_current = metrics["V5_current_constituents"]["full_2007_2025"]
    full_pit = metrics["V5_PIT_available"]["full_2007_2025"]

    lines = [
        "# V5 时间点成分股重新回测", "",
        "**状态：** best-effort survivorship-bias-aware validation  ",
        "**回测：** 2007-01-01 至 2025-12-30（2006 用作新增历史价格的指标预热）  ",
        "**报告期：** 2019-01-01 至 2025-12-30  ",
        "**执行：** 收盘信号，下一交易日收盘执行；权重自然漂移；单边成本 0.1%  ",
        "", "## 结论", "",
        f"移除未来成分股前视后，V5 报告期 CAGR 从 {pct(current['cagr'])} 降至 {pct(pit['cagr'])}，下降 {pct(current['cagr']-pit['cagr'])}；Sharpe 从 {current['sharpe']:.2f} 降至 {pit['sharpe']:.2f}。",
        f"按当月可计算指标的成员覆盖率进一步缩减动量仓位后，CAGR 为 {pct(adjusted['cagr'])}、最大回撤 {pct(adjusted['max_drawdown'])}、Sharpe {adjusted['sharpe']:.2f}。",
        "V5 不再显示可验证的基准超额收益，应继续作为候选扫描器，而不是组合收益引擎。",
        "", "## 2019–2025 对比", "",
        "| 策略 | CAGR | 最大回撤 | Sharpe | Sortino | 期末净值 |",
        "|---|---:|---:|---:|---:|---:|",
        *rows,
        "", "## 全期偏差幅度", "",
        f"- 2007–2025 当前成分版：CAGR {pct(full_current['cagr'])}，Sharpe {full_current['sharpe']:.2f}。",
        f"- 2007–2025 时间点成员版：CAGR {pct(full_pit['cagr'])}，Sharpe {full_pit['sharpe']:.2f}。",
        f"- 当前成分回看使全期 CAGR 高估约 {pct(full_current['cagr']-full_pit['cagr'])}。",
        "", "## 数据覆盖审计", "",
        "- 成分历史来源：[index-constitution 0.6.1](https://pypi.org/project/index-constitution/)（公开资料规范化，MIT）。",
        "- 价格来源：仓库 Yahoo 调整收盘缓存，并使用 yfinance 补取缺失历史代码。",
        f"- 历史成员并集：{metadata['membership_symbols']} 个。",
        f"- 原当前成分价格库覆盖：{metadata['existing_symbols']} 个。",
        f"- Yahoo 补取成功：{metadata['fetched_missing_with_any_data']} 个。",
        f"- 最终至少有一段价格的成员：{metadata['price_symbols_with_any_data']} 个；仍缺 {metadata['membership_symbols']-metadata['price_symbols_with_any_data']} 个。",
        "", "| 年份 | 平均价格覆盖 | 平均指标就绪覆盖 |", "|---:|---:|---:|",
    ]
    for year in [2007, 2010, 2015, 2018, 2019, 2022, 2025]:
        row = yearly.loc[year]
        lines.append(f"| {year} | {pct(row['price_coverage'])} | {pct(row['indicator_coverage'])} |")
    lines += [
        "", "## 已消除与仍残留的偏差", "",
        "已消除：",
        "",
        "- 股票只有在当日属于 S&P 500 或 Nasdaq-100 时才能参与排名。",
        "- opt-in 之前不得入池，opt-out 当日退出成员集合；成分变更会触发重新配置。",
        "- 组合使用因果 T+1 收盘执行、自然权重漂移和真实换手成本。",
        "", "仍残留：", "",
        "- 免费 Yahoo 数据缺少大量破产、收购和改名证券；缺价成员无法参与排名。",
        "- S&P 历史名单在早期并不完整，2006 年只有约 457 个 S&P 成员记录。",
        "- 历史名单来自公开资料规范化，并非 CRSP/Norgate 等商业参考级数据库。",
        "- 因此这版是显著减少幸存者偏差，不是宣称完全消除。完全验证仍需含退市收益和永久证券标识的商业数据。",
        "", "## 可复现", "",
        "```bash",
        "pip install index-constitution==0.6.1",
        "python scripts/build_point_in_time_data.py",
        "python -m unittest -v scripts/test_v5_point_in_time.py",
        "python scripts/backtest_v5_point_in_time.py",
        "python scripts/write_v5_point_in_time_report.py",
        "```", "",
        "机器结果：`results/v5_point_in_time_metrics.json`（默认被仓库 `.gitignore` 忽略）。",
        "", "*不构成投资建议。*",
    ]
    path = RESULTS / "v5_point_in_time_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
