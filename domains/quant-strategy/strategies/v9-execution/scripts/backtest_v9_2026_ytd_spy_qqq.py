#!/usr/bin/env python3
"""2026 YTD backtest of current V9 engine vs SPY/QQQ benchmarks.

Uses local data_v9 + frozen V9Config defaults. Research output only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from v9_data import load_data
from v9_evaluation import calculate_stats
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store

WARMUP = "2024-01-02"
START = "2026-01-02"
END = None  # last available close
OUT_JSON = ROOT / "results" / "v9_2026_ytd_spy_qqq_backtest.json"
OUT_MD = ROOT / "results" / "v9_2026_ytd_spy_qqq_backtest.md"
MEM = (
    Path(r"D:\code\AI-Memory\domains\quant-strategy\memory\daily")
    / "2026-07-11-v9-2026ytd-spy-qqq-backtest.md"
)


def metrics(curve: pd.Series) -> dict:
    out = calculate_stats(curve)
    n = max(len(curve) - 1, 1)
    years = n / 252
    out["cagr"] = (1 + out["total_return"]) ** (1 / years) - 1 if years > 0 else 0.0
    out["n_days"] = int(len(curve))
    return out


def bh_curve(close: pd.Series, start: str, end: str) -> pd.Series:
    s = close.loc[start:end].dropna()
    return (1 + s.pct_change().fillna(0)).cumprod()


def main() -> None:
    panels, vix, meta = load_data()
    end = END or str(pd.Timestamp(meta["last_date"]).date())
    events_pit, raw = load_event_store(ROOT / "datasets/v9_information_events.json", use_retrospective=False)
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")

    runs: dict = {}

    # Current V9 unified defaults
    cfg_v9 = V9Config()
    res_v9 = V9Backtester(panels, vix, events_pit, cfg_v9, updates).run(
        warmup_start=WARMUP, trading_start=START, trading_end=end
    )
    runs["V9_current_70_30_point_in_time"] = {
        "metrics": metrics(res_v9.equity),
        "info_entries": int(sum(1 for x in res_v9.ledger if x.get("action") == "BUY" and x.get("is_info"))),
        "diagnostics": {
            k: res_v9.diagnostics.get(k)
            for k in ("execution", "turnover", "information_contribution")
            if k in res_v9.diagnostics
        },
    }

    # Embedded core-only (info sleeve disabled) — isolates SPY/QQQ MA rule at 70% cash rest
    cfg_core70 = V9Config(v8_core_weight=0.70, info_sleeve_weight=0.0)
    res_core70 = V9Backtester(panels, vix, [], cfg_core70, []).run(
        warmup_start=WARMUP, trading_start=START, trading_end=end
    )
    runs["V9_index_core_70pct_cash_30pct"] = {
        "metrics": metrics(res_core70.equity),
        "info_entries": 0,
        "diagnostics": {"execution": "core-only; unused 30% cash"},
    }

    # V8-equivalent full index core
    cfg_v8 = V9Config(v8_core_weight=1.0, info_sleeve_weight=0.0)
    res_v8 = V9Backtester(panels, vix, [], cfg_v8, []).run(
        warmup_start=WARMUP, trading_start=START, trading_end=end
    )
    runs["V8_equivalent_full_core"] = {
        "metrics": metrics(res_v8.equity),
        "info_entries": 0,
        "diagnostics": {"execution": "100% SPY/QQQ MA150/MA200 core"},
    }

    close = panels["close"]
    spy = bh_curve(close["SPY"], START, end)
    qqq = bh_curve(close["QQQ"], START, end)
    static = bh_curve(0.5 * close["SPY"] + 0.5 * close["QQQ"], START, end)
    # proper 50/50 daily rebalanced:
    rets = close[["SPY", "QQQ"]].loc[START:end].pct_change().fillna(0)
    static50 = (1 + 0.5 * rets["SPY"] + 0.5 * rets["QQQ"]).cumprod()

    runs["buy_hold_SPY"] = {"metrics": metrics(spy), "info_entries": 0, "diagnostics": {"execution": "buy-and-hold"}}
    runs["buy_hold_QQQ"] = {"metrics": metrics(qqq), "info_entries": 0, "diagnostics": {"execution": "buy-and-hold"}}
    runs["static_SPY_QQQ_50_50_daily"] = {
        "metrics": metrics(static50),
        "info_entries": 0,
        "diagnostics": {"execution": "daily 50/50 rebalance, no cost"},
    }

    out = {
        "status": "v9_2026_ytd_backtest",
        "period": [START, end],
        "warmup_start": WARMUP,
        "data_source": "datasets/data_v9",
        "market_data_last_date": meta.get("last_date"),
        "config": {
            "v8_core_weight": cfg_v9.v8_core_weight,
            "info_sleeve_weight": cfg_v9.info_sleeve_weight,
            "transaction_cost": cfg_v9.transaction_cost,
            "event_mode": "point_in_time",
            "event_count": len(events_pit),
            "source_health": raw.get("source_health"),
        },
        "runs": runs,
        "limitation": (
            "YTD sample is short; annualized Sharpe is unstable. "
            "Point-in-time V9 information alpha may still be near zero if no Rule E entries fired."
        ),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    def pct(x: float) -> str:
        return f"{x * 100:.2f}%"

    lines = [
        "# V9 2026YTD 回测：组合 vs SPY / QQQ",
        "",
        f"区间：`{START}` 至 `{end}`。引擎：当前 `v9-execution` + `V9Config` 默认（70% 指数核心 / 30% 个股）。",
        "数据：`datasets/data_v9`。资讯：point-in-time 事件档案（不使用 retrospective backfill）。",
        "",
        "| 模型 | 累计收益 | 最大回撤 | 年化Sharpe* | 资讯买入次数 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    order = [
        "buy_hold_SPY",
        "buy_hold_QQQ",
        "static_SPY_QQQ_50_50_daily",
        "V8_equivalent_full_core",
        "V9_index_core_70pct_cash_30pct",
        "V9_current_70_30_point_in_time",
    ]
    for name in order:
        m = runs[name]["metrics"]
        lines.append(
            f"| {name} | {pct(m['total_return'])} | {pct(m['max_drawdown'])} | {m['annualized_sharpe']:.2f} | {runs[name]['info_entries']} |"
        )
    lines += [
        "",
        "*样本不足一年，年化 Sharpe 不稳定。",
        "",
        "## 读法",
        "",
        "- `buy_hold_SPY` / `buy_hold_QQQ`：纯买入持有基准。",
        "- `V8_equivalent_full_core`：100% 仓位跑 SPY/QQQ MA150/MA200（无个股）。",
        "- `V9_index_core_70pct_cash_30pct`：现行天花板下仅指数核心、个股袖套空置为现金。",
        "- `V9_current_70_30_point_in_time`：最新 V9 全规则；若资讯买入为 0，则收益应接近 core-70% 路径。",
        "",
        f"产物：`{OUT_JSON.as_posix()}`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Memory note
    mem_lines = [
        "# 2026-07-11 V9 回测 2026YTD：SPY / QQQ 收益",
        "",
        f"用最新 `v9-execution` 引擎回测 `{START}` → `{end}`。",
        f"报告：`strategies/v9-execution/results/v9_2026_ytd_spy_qqq_backtest.md`。",
        "",
        "## 结果",
        "",
        "| 模型 | 累计收益 | 最大回撤 | 资讯买入 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name in order:
        m = runs[name]["metrics"]
        mem_lines.append(
            f"| {name} | {pct(m['total_return'])} | {pct(m['max_drawdown'])} | {runs[name]['info_entries']} |"
        )
    mem_lines += [
        "",
        "## 结论",
        "",
        f"- 同期买入持有：SPY **{pct(runs['buy_hold_SPY']['metrics']['total_return'])}**，QQQ **{pct(runs['buy_hold_QQQ']['metrics']['total_return'])}**。",
        f"- 最新 V9（point-in-time）：**{pct(runs['V9_current_70_30_point_in_time']['metrics']['total_return'])}**，资讯买入 {runs['V9_current_70_30_point_in_time']['info_entries']} 次。",
        f"- V8 等价全核心：**{pct(runs['V8_equivalent_full_core']['metrics']['total_return'])}**。",
        "- 若 V9 资讯交易为 0，YTD 收益主要由嵌入式 SPY/QQQ 核心 + 现金缓冲决定，通常低于满仓 QQQ。",
        "",
        "不改正式规则；短样本年化指标仅供参考。",
    ]
    MEM.write_text("\n".join(mem_lines) + "\n", encoding="utf-8")

    print(json.dumps({k: {"ret": runs[k]["metrics"]["total_return"], "dd": runs[k]["metrics"]["max_drawdown"], "info": runs[k]["info_entries"]} for k in order}, indent=2))
    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", MEM)


if __name__ == "__main__":
    main()
