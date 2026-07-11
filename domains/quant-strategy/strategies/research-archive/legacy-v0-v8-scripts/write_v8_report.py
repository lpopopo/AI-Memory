#!/usr/bin/env python3
"""Build the evidence-backed V8 model optimization report."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR, run_buy_hold
from optimize_v8_etf import load_etfs, rebase
from optimize_v8_robust import metrics


def pct(value):
    return f"{value * 100:.2f}%"


def rolling_audit(strategy: pd.Series, benchmark: pd.Series):
    rows = []
    for start_year in range(2006, 2024):
        start = f"{start_year}-01-01"
        end = f"{start_year + 2}-12-31"
        s = strategy.loc[start:end].dropna()
        b = benchmark.loc[start:end].dropna()
        if len(s) < 600 or len(b) < 600:
            continue
        sm = metrics(s / s.iloc[0]); bm = metrics(b / b.iloc[0])
        rows.append({
            "window": f"{start_year}-{start_year+2}",
            "strategy_cagr": sm["cagr"], "benchmark_cagr": bm["cagr"],
            "strategy_dd": sm["max_drawdown"], "benchmark_dd": bm["max_drawdown"],
            "strategy_sharpe": sm["sharpe"], "benchmark_sharpe": bm["sharpe"],
        })
    return rows


def main():
    core = json.load(open(RESULTS_DIR / "v8_core_optimization_metrics.json"))
    etf = json.load(open(RESULTS_DIR / "v8_etf_optimization_metrics.json"))
    stock = json.load(open(RESULTS_DIR / "v8_robust_optimization_metrics.json"))
    breakout_path = ROOT.parent / "2026-07-03-breakout-pattern-backtest" / "results" / "robustness_metrics.json"
    breakout = json.load(open(breakout_path))
    pit_path = RESULTS_DIR / "v5_point_in_time_metrics.json"
    pit = json.load(open(pit_path)) if pit_path.exists() else None

    ensemble = pd.read_csv(
        RESULTS_DIR / "v8_core_ensemble_equity_curve.csv", index_col=0, parse_dates=True
    ).iloc[:, 0]
    close = load_etfs()
    benchmark = run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "benchmark")
    rolling = rolling_audit(ensemble, benchmark)
    roll_summary = {
        "windows": len(rolling),
        "cagr_wins": sum(r["strategy_cagr"] > r["benchmark_cagr"] for r in rolling),
        "drawdown_wins": sum(r["strategy_dd"] > r["benchmark_dd"] for r in rolling),
        "sharpe_wins": sum(r["strategy_sharpe"] > r["benchmark_sharpe"] for r in rolling),
    }

    c = core["ensemble"]
    b = core["benchmarks"]["SPY_QQQ_50_50"]
    v5 = stock["metrics"]["V5_robust"]
    c_proxy = stock["metrics"]["V5_C20_monthly"]
    pattern_c = breakout["patterns"]["C"]["stop_and_20d"]["spy_above_ma200"]["out_of_sample_2019_2025"]
    etf_best = etf["best"]
    pit_v5 = pit["metrics"]["V5_PIT_available"]["report_2019_2025"] if pit else None
    pit_adjusted = pit["metrics"]["V5_PIT_coverage_adjusted"]["report_2019_2025"] if pit else None

    lines = [
        "# V8 模型策略完整优化报告", "",
        "**研究冻结日期：** 2026-07-03  ",
        "**开发期：** 2006-01-01 至 2018-12-31  ",
        "**报告期：** 2019-01-01 至 2025-12-30（本轮查看后不得再作为全新样本外调参）  ",
        "**成交：** 收盘信号，下一交易日收盘执行；权重自然漂移；每次真实换手计成本  ",
        "", "## 最终结论", "",
        "复杂个股模型当前不能证明可交易 alpha：V5/V7 存在当前成分股回看历史的幸存者偏差；Pattern C 单独有效，但接入完整动量袖套后降低组合表现；ETF 轮动也未击败简单基准。",
        "",
        "当前唯一可晋级为 **V8 防守核心** 的规则是：",
        "",
        "- 基础权重：SPY 50% / QQQ 50%。",
        "- 每月末分别检查 SPY、QQQ 的 MA150 与 MA200。每站上一条均线，启用该 ETF 基础权重的一半；两条均线上方为满额，两条下方为空仓。",
        "- 信号在下一交易日收盘执行；未配置仓位保留现金；不使用杠杆。",
        "- 个股选股、Pattern C、Double Radar 和新闻/机构覆盖层继续作为研究/扫描器，不得凭自身信号直接下单。",
        "", "## 核心证据", "",
        "| 模型 | 时段 | CAGR | 最大回撤 | Sharpe |", "|---|---|---:|---:|---:|",
        f"| V8 防守核心 | 开发期 | {pct(c['development']['cagr'])} | {pct(c['development']['max_drawdown'])} | {c['development']['sharpe']:.2f} |",
        f"| 静态 50/50 | 开发期 | {pct(b['development']['cagr'])} | {pct(b['development']['max_drawdown'])} | {b['development']['sharpe']:.2f} |",
        f"| V8 防守核心 | 报告期 | {pct(c['oos_2019_2025']['cagr'])} | {pct(c['oos_2019_2025']['max_drawdown'])} | {c['oos_2019_2025']['sharpe']:.2f} |",
        f"| 静态 50/50 | 报告期 | {pct(b['oos_2019_2025']['cagr'])} | {pct(b['oos_2019_2025']['max_drawdown'])} | {b['oos_2019_2025']['sharpe']:.2f} |",
        "", f"滚动 3 年共 {roll_summary['windows']} 个窗口：V8 在 {roll_summary['drawdown_wins']} 个窗口回撤更小、{roll_summary['sharpe_wins']} 个窗口 Sharpe 更高，但仅在 {roll_summary['cagr_wins']} 个窗口 CAGR 更高。它是风险挡位，不是超额收益引擎。",
        "", "## 被拒绝或降级的模块", "",
        "| 模块 | 证据 | 决定 |", "|---|---|---|",
        (f"| V5 时间点成分重测 | 报告期 CAGR {pct(pit_v5['cagr'])}、最大回撤 {pct(pit_v5['max_drawdown'])}、Sharpe {pit_v5['sharpe']:.2f}；覆盖率缩仓版 CAGR {pct(pit_adjusted['cagr'])} | 未击败基准，维持扫描器身份 |"
         if pit_v5 else
         f"| V5 正确记账 | 报告期 CAGR {pct(v5['report_2019_2025']['cagr'])}、Sharpe {v5['report_2019_2025']['sharpe']:.2f}，但使用今天的成分股回看历史 | 降级为扫描器，禁止引用收益率作实盘依据 |"),
        f"| C 代理接入 V5 | C20 报告期 CAGR {pct(c_proxy['report_2019_2025']['cagr'])}、Sharpe {c_proxy['report_2019_2025']['sharpe']:.2f}，显著弱于未过滤 V5 | 拒绝作为主模型硬门槛 |",
        f"| 独立 Pattern C | 样本外均收益 {pattern_c['mean_pct']:.2f}%，95% CI [{pattern_c['mean_ci95_pct'][0]:.2f}%, {pattern_c['mean_ci95_pct'][1]:.2f}%] | 保留研究候选，不直接下单 |",
        f"| ETF 双袖套 | 报告期 CAGR {pct(etf_best['oos_2019_2025']['cagr'])}、Sharpe {etf_best['oos_2019_2025']['sharpe']:.2f} | 未击败 SPY/QQQ 基准，拒绝晋级 |",
        "| 5 日时间止损/射击之星/3 日假突破退出 | 修正成交后的消融均显示删掉规则更好 | 从形态模块删除；不能再称已验证 |",
        "", "## 成本敏感性", "",
        "| 单边比例成本 | 报告期 CAGR | 最大回撤 | Sharpe |", "|---:|---:|---:|---:|",
    ]
    for cost, values in core["cost_sensitivity"]["results"].items():
        m = values["oos_2019_2025"]
        lines.append(f"| {float(cost):.2%} | {pct(m['cagr'])} | {pct(m['max_drawdown'])} | {m['sharpe']:.2f} |")
    lines += [
        "", "## 使用边界", "",
        "- V8 防守核心适合降低组合波动和回撤，不适合用来承诺高收益或追赶 +55% 年度目标。",
        "- 对小账户，固定每单约 USD 1 的费用仍须在下单层单独计算；本回测只做比例成本敏感性。",
        "- 现有真实持仓不应因研究模型切换而自动买卖；仍以用户/券商确认、个股止损和账户集中度规则为最高执行约束。",
        "- 若未来获得 point-in-time 成分股、退市股和历史行业映射，才可重新评估个股 alpha 袖套。",
        "- 下一批新增行情数据是前瞻验证集；不得继续使用 2019–2025 选择参数。",
        "", "## 可复现证据", "",
        "- `scripts/robust_portfolio_engine.py`：因果组合内核。",
        "- `scripts/test_robust_portfolio_engine.py`：权重漂移、T+1、止损、成本及分段归一化测试。",
        "- `results/v8_core_optimization_metrics.json`：V8 核心网格与成本敏感性。",
        "- `results/v8_etf_optimization_metrics.json`：ETF 双袖套拒绝证据。",
        "- `results/v8_robust_optimization_metrics.json`：V5/V7 正确记账及 C 接入证据。",
        "", "*不构成投资建议。*",
    ]
    report = RESULTS_DIR / "v8_model_optimization_report.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    audit = {
        "rolling_3y": rolling, "rolling_summary": roll_summary,
        "promoted": "V8 defensive core",
        "rejected": ["V5/V7 performance claims", "C as hard gate", "ETF dual-sleeve alpha"],
    }
    (RESULTS_DIR / "v8_model_optimization_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(roll_summary)
    print(report)


if __name__ == "__main__":
    main()
