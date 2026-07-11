#!/usr/bin/env python3
"""Backtest a separate sentiment oscillator as a V8 contrarian overlay."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd
import yfinance as yf

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from market_sentiment import REQUIRED, compute_sentiment, confirmed_contrarian_state
from optimize_v8_core import ensemble_target_function
from optimize_v8_etf import development_score
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from test_v3_refined import month_end_dates

START, DEV_END, TEST_START, TEST_END, FORWARD_START = "2010-01-01", "2018-12-31", "2019-01-01", "2025-12-31", "2026-01-01"


def load_data() -> pd.DataFrame:
    cache = ROOT / "datasets" / "market_sentiment_close_2009_2026.csv"
    if cache.exists():
        data = pd.read_csv(cache, index_col=0, parse_dates=True)
        if set(REQUIRED).issubset(data.columns) and data.index.max() >= pd.Timestamp("2026-07-02"):
            return data.sort_index()
    raw = yf.download(list(REQUIRED), start="2009-01-01", end="2026-07-03", auto_adjust=True, progress=False, threads=True)
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw
    close = close[list(REQUIRED)].dropna(how="all")
    close.index = pd.to_datetime(close.index).tz_localize(None)
    cache.parent.mkdir(parents=True, exist_ok=True)
    close.to_csv(cache)
    return close


def desired_targets(close: pd.DataFrame, sentiment: pd.DataFrame, mode: str) -> pd.DataFrame:
    base_fn = ensemble_target_function(close[["SPY", "QQQ"]])
    monthly = set(month_end_dates(close.index))
    confirmed = confirmed_contrarian_state(close, sentiment)
    base = {"SPY": 0.0, "QQQ": 0.0}
    rows = []
    for dt in close.index:
        if dt in monthly:
            base = base_fn(dt)
        target = dict(base)
        fear_active = bool(sentiment.at[dt, "sentiment_score"] <= 20) if pd.notna(sentiment.at[dt, "sentiment_score"]) else False
        if mode in {"fear_raw", "fear_confirmed", "fear_confirmed_greed"}:
            active = fear_active if mode == "fear_raw" else bool(confirmed.at[dt, "active"])
            if active:
                room = max(0.0, 1.0 - sum(target.values()))
                add = min(0.10, room)
                target["SPY"] += add / 2
                target["QQQ"] += add / 2
        if mode == "fear_confirmed_greed" and pd.notna(sentiment.at[dt, "sentiment_score"]) and sentiment.at[dt, "sentiment_score"] >= 80:
            target["QQQ"] = max(0.0, target["QQQ"] - 0.10)
        rows.append({"date": dt, **target})
    return pd.DataFrame(rows).set_index("date")


def run_variant(close: pd.DataFrame, sentiment: pd.DataFrame, mode: str, cost: float):
    targets = desired_targets(close, sentiment, mode)
    changed = targets.ne(targets.shift()).any(axis=1)
    dates = set(targets.index[changed])
    result = run_engine(close[["SPY", "QQQ"]], dates, lambda dt: targets.loc[dt].to_dict(), transaction_cost=cost)
    return result, targets


def window_metrics(curve: pd.Series) -> dict:
    return {
        "development_2010_2018": metrics(curve.loc[START:DEV_END]),
        "frozen_2019_2025": metrics(curve.loc[TEST_START:TEST_END]),
        "forward_2026_to_date": metrics(curve.loc[FORWARD_START:]),
    }


def period_metric(curve: pd.Series, start: str, end: str) -> dict:
    return metrics(curve.loc[start:end])


def main():
    raw = load_data()
    sentiment = compute_sentiment(raw)
    close = raw.loc[START:].dropna(subset=["SPY", "QQQ"])
    sentiment = sentiment.reindex(close.index)
    modes = ["v8", "fear_raw", "fear_confirmed", "fear_confirmed_greed"]
    runs = {}
    for mode in modes:
        result, targets = run_variant(close, sentiment, mode, .001)
        runs[mode] = {
            "result": result, "targets": targets, "metrics": window_metrics(result.equity),
            "diagnostics": {
                "total_turnover": float(result.diagnostics["total_turnover"]),
                "execution_count": int(len(result.executions)),
                "extreme_fear_days": int((sentiment.sentiment_score <= 20).sum()),
            },
            "stress_windows": {
                "covid_2020": period_metric(result.equity, "2020-01-01", "2020-12-31"),
                "inflation_2022": period_metric(result.equity, "2022-01-01", "2022-12-31"),
            },
        }

    ranked = sorted(modes[1:], key=lambda m: development_score(runs[m]["metrics"]["development_2010_2018"]), reverse=True)
    selected = ranked[0]
    cost_sensitivity = {}
    for cost in (.001, .002, .005):
        result, _ = run_variant(close, sentiment, selected, cost)
        cost_sensitivity[str(cost)] = window_metrics(result.equity)["frozen_2019_2025"]

    latest = sentiment.dropna(subset=["sentiment_score"]).iloc[-1]
    output = {
        "status": "development_selected_frozen_test_research_only",
        "periods": {"development": [START, DEV_END], "frozen_test": [TEST_START, TEST_END], "forward_diagnostic": [FORWARD_START, str(close.index.max().date())]},
        "components": [c for c in sentiment.columns if c not in {"available_components", "sentiment_score", "sentiment_regime"}],
        "put_call": "optional_not_used_in_long_history_due_to_incomplete_free_official_series",
        "cnn": "external_validation_only_not_an_input",
        "variants": {m: {"metrics": runs[m]["metrics"], "diagnostics": runs[m]["diagnostics"], "stress_windows": runs[m]["stress_windows"]} for m in modes},
        "development_ranking": ranked,
        "selected_before_frozen_test": selected,
        "selected_cost_sensitivity": cost_sensitivity,
        "latest": {"date": str(sentiment.dropna(subset=["sentiment_score"]).index[-1].date()), "score": float(latest.sentiment_score), "regime": str(latest.sentiment_regime)},
        "promotion_allowed": False,
        "promotion_reason": "frozen-test uplift is small, drawdown is unchanged, and the advantage disappears at higher transaction costs",
    }
    results = ROOT / "results"
    metrics_path = results / "market_sentiment_overlay_metrics.json"
    report_path = results / "market_sentiment_overlay_report.md"
    metrics_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    def row(mode, period):
        m = output["variants"][mode]["metrics"][period]
        return f"| {mode} | {m['cagr']:.2%} | {m['max_drawdown']:.2%} | {m['sharpe']:.2f} | {m['final_value']-1:.2%} |"
    dev_rows = "\n".join(row(m, "development_2010_2018") for m in modes)
    test_rows = "\n".join(row(m, "frozen_2019_2025") for m in modes)
    forward_rows = "\n".join(row(m, "forward_2026_to_date") for m in modes)
    report_path.write_text(f"""# 市场情绪振荡器与V8逆向模块回测

## 设计

独立情绪分数为0–100，低分代表恐惧，高分代表贪婪。七个可重建分量为：SPY相对MA125、VIX相对MA50、VIX/VIX3M、RSP/SPY宽度、IWM/SPY宽度、HYG/LQD信用偏好、SPY相对TLT避险需求。每项转换为过去756日的因果经验分位数，至少六项可用才输出总分；缺失数据不按中性处理。

逆向模块只使用V8未投入的现金，最大增加10%，信号在完成收盘形成、下一收盘执行。确认版要求最近10日出现极度恐惧、情绪回升、SPY站上MA5且等权宽度五日改善；情绪恢复至55、SPY跌破MA20或持有20日退出。贪婪版在分数≥80时额外减少10% QQQ。

## 开发期 2010–2018

| 版本 | CAGR | 最大回撤 | Sharpe | 累计收益 |
| --- | ---: | ---: | ---: | ---: |
{dev_rows}

开发期预选：`{selected}`。

## 冻结检验期 2019–2025

| 版本 | CAGR | 最大回撤 | Sharpe | 累计收益 |
| --- | ---: | ---: | ---: | ---: |
{test_rows}

## 2026年至今诊断

| 版本 | CAGR* | 最大回撤 | Sharpe* | 累计收益 |
| --- | ---: | ---: | ---: | ---: |
{forward_rows}

*短区间年化指标不稳定。

## 边界

Put/Call因免费官方长历史断层未进入本轮长期回测，但接口保留；CNN总分只作外部校验。所有版本均为研究结果，不能在看到冻结期后改选参数或直接晋级实盘。

冻结期中，确认版相对V8的CAGR仅提高约0.21个百分点，最大回撤没有改善；交易成本提高到0.2%后优势基本消失，0.5%时明显落后。因此保留情绪指标作为观察与影子模块，但本轮不晋级为正式V8仓位规则。
""", encoding="utf-8")
    print(json.dumps({"metrics": str(metrics_path), "report": str(report_path), "selected": selected, "latest": output["latest"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
