#!/usr/bin/env python3
"""Ablate the legacy Fear Score against one sentiment-only exposure signal."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_market_sentiment_overlay import DEV_END, FORWARD_START, START, TEST_END, TEST_START, load_data
from market_sentiment import compute_sentiment, confirmed_contrarian_state
from optimize_v8_core import ensemble_target_function
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from test_v3_refined import month_end_dates


def fear_score_series(close: pd.DataFrame) -> pd.DataFrame:
    """Vectorized equivalent of market_fear.py's completed-close score."""
    out = pd.DataFrame(index=close.index)
    vix = close["^VIX"]
    out["vix_level"] = np.select([vix >= 35, vix >= 30, vix >= 22, vix >= 16], [4, 3, 2, 1], default=0)
    v5 = vix.pct_change(5, fill_method=None)
    out["vix_5d"] = np.select([v5 >= .50, v5 >= .30, v5 >= .15], [3, 2, 1], default=0)
    term = vix / close["^VIX3M"]
    out["term"] = np.select([term >= 1.05, term >= 1.00], [3, 2], default=0)
    for symbol in ("SPY", "QQQ"):
        c = close[symbol]
        dd = c / c.rolling(63).max() - 1
        out[f"{symbol}_dd"] = np.select([dd <= -.12, dd <= -.08, dd <= -.04], [3, 2, 1], default=0)
        ma50, ma200 = c.rolling(50).mean(), c.rolling(200).mean()
        out[f"{symbol}_trend"] = np.select([c < ma200, c < ma50], [3, 1], default=0)
    # SMH is absent from the long sentiment cache. QQQ is used only for this
    # ablation and the limitation is reported; no zero-point SMH assumption.
    for num, den, name in (("IWM", "SPY", "smallcap"), ("RSP", "SPY", "equal_weight"), ("HYG", "LQD", "credit")):
        change = (close[num] / close[den]).pct_change(21, fill_method=None)
        out[name] = np.select([change <= -.05, change <= -.025], [2, 1], default=0)
    valid = close[["SPY", "QQQ", "^VIX", "^VIX3M"]].notna().all(axis=1)
    score = out.sum(axis=1).where(valid)
    regime = pd.cut(score, [-np.inf, 4, 8, 13, np.inf], labels=["normal", "elevated", "stress", "panic"])
    return pd.DataFrame({"fear_score": score, "fear_regime": regime.astype("string")}, index=close.index)


def base_targets(close: pd.DataFrame) -> pd.DataFrame:
    fn = ensemble_target_function(close[["SPY", "QQQ"]])
    monthly = set(month_end_dates(close.index))
    current = {"SPY": 0.0, "QQQ": 0.0}
    rows = []
    for dt in close.index:
        if dt in monthly:
            current = fn(dt)
        rows.append({"date": dt, **current})
    return pd.DataFrame(rows).set_index("date")


def scale_to_gross(target: dict[str, float], gross: float) -> dict[str, float]:
    current = sum(target.values())
    if current <= gross or current <= 0:
        return dict(target)
    scale = gross / current
    return {s: w * scale for s, w in target.items()}


def targets_for(close: pd.DataFrame, sentiment: pd.DataFrame, fear: pd.DataFrame, mode: str) -> pd.DataFrame:
    base = base_targets(close)
    confirmed = confirmed_contrarian_state(close, sentiment)
    rows = []
    fear_mult = {"normal": 1.0, "elevated": .70, "stress": .40, "panic": .20}
    for dt in close.index:
        raw = base.loc[dt].to_dict()
        if mode == "v8":
            target = raw
        elif mode == "fear_gate":
            mult = fear_mult.get(str(fear.at[dt, "fear_regime"]), .40)
            target = {s: w * mult for s, w in raw.items()}
        elif mode == "sentiment_auxiliary":
            target = dict(raw)
            if bool(confirmed.at[dt, "active"]):
                room = max(0.0, 1.0 - sum(target.values()))
                add = min(.10, room)
                target["SPY"] += add / 2
                target["QQQ"] += add / 2
        else:
            score = sentiment.at[dt, "sentiment_score"]
            if pd.isna(score):
                target = {"SPY": 0.0, "QQQ": 0.0}
            else:
                active = bool(confirmed.at[dt, "active"])
                if score <= 20:
                    cap = .55 if active else .35
                elif score <= 40:
                    cap = .55
                elif score <= 60:
                    cap = .75
                elif score <= 80:
                    cap = .95
                else:
                    cap = .75
                target = scale_to_gross(raw, cap)
                if active:
                    room = max(0.0, cap - sum(target.values()))
                    add = min(.10, room)
                    target["SPY"] += add / 2
                    target["QQQ"] += add / 2
            if mode == "dual_gate":
                mult = fear_mult.get(str(fear.at[dt, "fear_regime"]), .40)
                fear_target = {s: w * mult for s, w in raw.items()}
                target = scale_to_gross(target, sum(fear_target.values()))
        rows.append({"date": dt, **target})
    return pd.DataFrame(rows).set_index("date")


def run(close, sentiment, fear, mode, cost=.001):
    target = targets_for(close, sentiment, fear, mode)
    changed = target.ne(target.shift()).any(axis=1)
    result = run_engine(close[["SPY", "QQQ"]], set(target.index[changed]), lambda dt: target.loc[dt].to_dict(), transaction_cost=cost)
    return result


def windows(curve):
    return {
        "development_2010_2018": metrics(curve.loc[START:DEV_END]),
        "frozen_2019_2025": metrics(curve.loc[TEST_START:TEST_END]),
        "covid_2020": metrics(curve.loc["2020-01-01":"2020-12-31"]),
        "inflation_2022": metrics(curve.loc["2022-01-01":"2022-12-31"]),
        "forward_2026": metrics(curve.loc[FORWARD_START:]),
    }


def main():
    raw = load_data().dropna(subset=["SPY", "QQQ"])
    close = raw.loc[START:]
    sentiment = compute_sentiment(raw).reindex(close.index)
    fear = fear_score_series(close)
    modes = ["v8", "fear_gate", "sentiment_auxiliary", "sentiment_only", "dual_gate"]
    runs = {m: run(close, sentiment, fear, m) for m in modes}
    output = {
        "status": "fear_score_replacement_ablation_research_only",
        "periods": {"development": [START, DEV_END], "frozen": [TEST_START, TEST_END]},
        "variants": {m: {"metrics": windows(r.equity), "turnover": float(r.diagnostics["total_turnover"]), "executions": int(len(r.executions))} for m, r in runs.items()},
        "cost_sensitivity_sentiment_only": {str(c): windows(run(close, sentiment, fear, "sentiment_only", c).equity)["frozen_2019_2025"] for c in (.001, .002, .005)},
        "cost_sensitivity_sentiment_auxiliary": {str(c): windows(run(close, sentiment, fear, "sentiment_auxiliary", c).equity)["frozen_2019_2025"] for c in (.001, .002, .005)},
        "latest": {"sentiment": float(sentiment.sentiment_score.dropna().iloc[-1]), "fear_score_without_smh": float(fear.fear_score.dropna().iloc[-1])},
        "limitations": ["SMH history is absent from the sentiment cache, so the Fear Score comparator excludes SMH rather than assigning it zero points.", "Put/Call is not included in the long-history sentiment baseline."],
    }
    test = {m: output["variants"][m]["metrics"]["frozen_2019_2025"] for m in modes}
    full_replacement_wins = test["sentiment_only"]["sharpe"] > test["fear_gate"]["sharpe"] and test["sentiment_only"]["max_drawdown"] >= test["fear_gate"]["max_drawdown"]
    auxiliary_wins = test["sentiment_auxiliary"]["sharpe"] > test["v8"]["sharpe"] and test["sentiment_auxiliary"]["cagr"] > test["v8"]["cagr"]
    output["decision"] = {
        "sentiment_as_only_exposure_gate": "reject" if not full_replacement_wins else "candidate",
        "remove_fear_score_keep_v8_plus_sentiment_auxiliary": "shadow_candidate" if auxiliary_wins else "reject",
    }
    output["formal_change_allowed"] = False

    results = ROOT / "results"
    metrics_path = results / "sentiment_vs_fear_gate_metrics.json"
    report_path = results / "sentiment_vs_fear_gate_report.md"
    metrics_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    def row(mode, period):
        m = output["variants"][mode]["metrics"][period]
        return f"| {mode} | {m['cagr']:.2%} | {m['max_drawdown']:.2%} | {m['sharpe']:.2f} | {m['final_value']-1:.2%} | {output['variants'][mode]['turnover']:.1f} |"
    dev = "\n".join(row(m, "development_2010_2018") for m in modes)
    frozen = "\n".join(row(m, "frozen_2019_2025") for m in modes)
    report_path.write_text(f"""# 单一市场情绪指标替代Fear Score消融回测

## 口径

比较V8、Fear Score缩放、单一情绪指标和双门控。单一情绪指标同时承担风险温度与逆向确认：极恐未确认时总仓上限35%，确认后55%；fear/fair/greed/extreme-greed依次使用55%/75%/95%/75%上限。逆向确认仍只使用未分配现金、最多10%。信号完成收盘形成，下一收盘执行。

## 开发期2010–2018

| 版本 | CAGR | 最大回撤 | Sharpe | 累计收益 | 全期换手 |
| --- | ---: | ---: | ---: | ---: | ---: |
{dev}

## 冻结期2019–2025

| 版本 | CAGR | 最大回撤 | Sharpe | 累计收益 | 全期换手 |
| --- | ---: | ---: | ---: | ---: | ---: |
{frozen}

## 自动判定

单一情绪指标直接承担总仓位门控：`{output['decision']['sentiment_as_only_exposure_gate']}`。

移除Fear Score、保留V8趋势核心并只使用情绪确认辅助：`{output['decision']['remove_fear_score_keep_v8_plus_sentiment_auxiliary']}`。

正式规则暂不自动改变：Fear比较器缺少SMH历史，且候选替代仍需成本与新数据验证。
""", encoding="utf-8")
    print(json.dumps({"metrics": str(metrics_path), "report": str(report_path), "decision": output["decision"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
