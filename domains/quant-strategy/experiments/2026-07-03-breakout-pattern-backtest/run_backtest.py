"""
Daily K-line breakout pattern backtest (US-adapted).
Patterns A/B/C + baselines over ~20 years of daily OHLCV.
"""

from __future__ import annotations

import json
import os
import random
import hashlib
import warnings
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_CACHE = os.path.join(OUTPUT_DIR, "data_cache")
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results")

START_DATE = "2006-01-01"
END_DATE = "2025-12-31"
TX_COST = 0.001  # 0.1% per side
RISK_FREE = 0.03

UNIVERSE = [
    "SPY", "QQQ", "SMH",
    "GLW", "TTMI", "MU", "MXL", "AMD", "MRVL", "WDC", "STX", "NVDA", "AVGO",
    "INTC", "QCOM", "CRDO", "ARM", "LRCX", "KLAC", "AMAT", "ASML", "TSM",
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JPM", "V", "UNH", "XOM",
    "JNJ", "PG", "HD", "MA", "BAC", "CRM", "COST", "NFLX", "LLY", "ABBV",
    "CAT", "GE", "RTX", "NKE", "SBUX", "DIS", "BA", "GS", "MS", "PLTR", "COIN",
]

PatternName = Literal["A", "B", "C", "combined", "breakout_no_retest", "random"]


@dataclass
class Trade:
    ticker: str
    pattern: str
    entry_date: pd.Timestamp
    entry_price: float
    exit_date: pd.Timestamp
    exit_price: float
    exit_reason: str
    gross_return: float = 0.0
    net_return: float = 0.0
    false_breakout: bool = False
    days_held: int = 0
    signal_date: pd.Timestamp | None = None
    initial_stop: float = 0.0


@dataclass
class StrategyResult:
    name: str
    trades: list[Trade] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)


def fetch_ohlcv(tickers: list[str], start: str, end: str) -> dict[str, pd.DataFrame]:
    os.makedirs(DATA_CACHE, exist_ok=True)
    data: dict[str, pd.DataFrame] = {}
    for ticker in tickers:
        cache_path = os.path.join(DATA_CACHE, f"{ticker}.csv")
        if os.path.exists(cache_path):
            df = pd.read_csv(cache_path, parse_dates=["Date"], index_col="Date")
            if len(df) > 100:
                data[ticker] = df
                continue
        try:
            raw = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
            if raw.empty:
                print(f"  [SKIP] {ticker}: no data")
                continue
            if isinstance(raw.columns, pd.MultiIndex):
                raw.columns = raw.columns.droplevel(1)
            df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
            df.index = pd.to_datetime(df.index)
            df.to_csv(cache_path)
            data[ticker] = df
            print(f"  [OK] {ticker}: {len(df)} rows")
        except Exception as exc:
            print(f"  [FAIL] {ticker}: {exc}")
    return data


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ma20"] = out["Close"].rolling(20).mean()
    out["ma50"] = out["Close"].rolling(50).mean()
    out["high20"] = out["High"].rolling(20).max()
    out["low20"] = out["Low"].rolling(20).min()
    out["range20"] = out["high20"] - out["low20"]
    out["range_pct"] = out["range20"] / out["Close"]
    out["vol_avg20"] = out["Volume"].rolling(20).mean()
    out["body_pct"] = (out["Close"] - out["Open"]).abs() / out["Close"]
    out["upper_wick"] = out["High"] - out[["Open", "Close"]].max(axis=1)
    out["body"] = (out["Close"] - out["Open"]).abs()
    out["prev_high20"] = out["high20"].shift(1)
    return out


def is_consolidation(row: pd.Series, window: pd.DataFrame, min_days: int = 20) -> bool:
    if len(window) < min_days:
        return False
    recent = window.tail(min_days)
    return bool((recent["range_pct"] < 0.15).all())


def detect_pattern_a(df: pd.DataFrame, ticker: str) -> list[dict]:
    signals = []
    i = 50
    while i < len(df) - 15:
        row = df.iloc[i]
        window = df.iloc[i - 20 : i]
        if not is_consolidation(row, window):
            i += 1
            continue
        prev_high = row["prev_high20"]
        if pd.isna(prev_high) or row["Close"] <= prev_high:
            i += 1
            continue
        if row["Volume"] <= 1.5 * row["vol_avg20"]:
            i += 1
            continue
        breakout_level = prev_high
        breakout_vol = row["Volume"]
        breakout_idx = i
        retest_found = False
        retest_low = None
        entry_idx = None
        for j in range(i + 1, min(i + 11, len(df))):
            r = df.iloc[j]
            if r["Volume"] < 0.6 * breakout_vol and r["Low"] >= min(breakout_level, r["ma20"]):
                retest_found = True
                retest_low = r["Low"]
                for k in range(j + 1, min(j + 6, len(df))):
                    e = df.iloc[k]
                    if e["Close"] > max(breakout_level, e["ma20"]):
                        entry_idx = k
                        break
                break
        if retest_found and entry_idx is not None:
            signals.append({
                "pattern": "A",
                "ticker": ticker,
                "breakout_idx": breakout_idx,
                "entry_idx": entry_idx,
                "breakout_level": breakout_level,
                "retest_low": retest_low,
                "stop": min(retest_low, df.iloc[entry_idx]["Close"] * 0.92),
            })
            i = entry_idx + 1
        else:
            i += 1
    return signals


def detect_pattern_b(df: pd.DataFrame, ticker: str) -> list[dict]:
    signals = []
    i = 50
    while i < len(df) - 5:
        window = df.iloc[i - 25 : i]
        if len(window) < 25 or not is_consolidation(df.iloc[i], window.iloc[-20:]):
            i += 1
            continue
        small_pos = window.tail(5)
        if not all(
            (r["Close"] > r["Open"]) and (r["body_pct"] < 0.02)
            for _, r in small_pos.iterrows()
        ):
            i += 1
            continue
        vol_trend = small_pos["Volume"].iloc[-1] > small_pos["Volume"].iloc[0]
        if not vol_trend:
            i += 1
            continue
        row = df.iloc[i]
        platform = row["prev_high20"]
        if pd.isna(platform) or row["Close"] <= platform:
            i += 1
            continue
        if row["Volume"] <= 1.2 * row["vol_avg20"]:
            i += 1
            continue
        entry_idx = i
        signals.append({
            "pattern": "B",
            "ticker": ticker,
            "entry_idx": entry_idx,
            "breakout_level": platform,
            "retest_low": row["Low"],
            "stop": min(row["Low"], row["Close"] * 0.92),
        })
        i += 1
    return signals


def detect_pattern_c(df: pd.DataFrame, ticker: str) -> list[dict]:
    signals = []
    i = 55
    while i < len(df) - 5:
        row = df.iloc[i]
        if row["Close"] <= row["ma50"] or row["ma20"] <= row["ma50"]:
            i += 1
            continue
        fake_days = 0
        fake_start = None
        fake_low = None
        for j in range(i, min(i + 4, len(df))):
            r = df.iloc[j]
            if r["Close"] < r["ma20"]:
                fake_days += 1
                fake_start = j if fake_start is None else fake_start
                fake_low = r["Low"] if fake_low is None else min(fake_low, r["Low"])
            else:
                break
        if fake_days < 2 or fake_days > 3 or fake_start is None:
            i += 1
            continue
        entry_idx = None
        for k in range(fake_start + fake_days, min(fake_start + fake_days + 6, len(df))):
            e = df.iloc[k]
            if e["Close"] > e["ma20"]:
                entry_idx = k
                break
        if entry_idx is not None:
            signals.append({
                "pattern": "C",
                "ticker": ticker,
                "entry_idx": entry_idx,
                "breakout_level": df.iloc[entry_idx]["ma20"],
                "retest_low": fake_low,
                "stop": fake_low,
            })
            i = entry_idx + 1
        else:
            i += 1
    return signals


def detect_breakout_no_retest(df: pd.DataFrame, ticker: str) -> list[dict]:
    signals = []
    for i in range(50, len(df) - 5):
        row = df.iloc[i]
        window = df.iloc[i - 20 : i]
        if not is_consolidation(row, window):
            continue
        prev_high = row["prev_high20"]
        if pd.isna(prev_high) or row["Close"] <= prev_high:
            continue
        if row["Volume"] <= 1.5 * row["vol_avg20"]:
            continue
        signals.append({
            "pattern": "breakout_no_retest",
            "ticker": ticker,
            "entry_idx": i,
            "breakout_level": prev_high,
            "retest_low": row["Low"],
            "stop": min(row["Low"], row["Close"] * 0.92),
        })
    return signals


def simulate_trade(
    df: pd.DataFrame,
    signal: dict,
    time_stop_days: int = 5,
    pattern: str = "A",
    use_false_breakout_exit: bool = True,
    use_trailing_stop: bool = True,
    use_shooting_star: bool = True,
    use_time_stop: bool = True,
) -> Trade | None:
    """Simulate a close-confirmed signal with causal, executable fills.

    The signal is known only after ``entry_idx`` closes, so entry occurs at the
    next session's open. Intraday stops fill at the stop price, or at the open
    after an adverse gap. Close-based exits fill at that close. Stop updates
    derived from today's close become active on the following session.
    """
    entry_idx = signal["entry_idx"]
    if entry_idx >= len(df) - 1:
        return None
    signal_row = df.iloc[entry_idx]
    fill_idx = entry_idx + 1
    entry_row = df.iloc[fill_idx]
    entry_price = float(entry_row["Open"])
    stop = float(signal["stop"])
    # A gap below the intended stop invalidates the setup; enter and exit at
    # the same executable open rather than inventing a fill at yesterday's stop.
    if entry_price <= stop:
        gross = 0.0
        return Trade(
            ticker=signal["ticker"], pattern=pattern,
            signal_date=df.index[entry_idx], entry_date=df.index[fill_idx],
            entry_price=entry_price, exit_date=df.index[fill_idx],
            exit_price=entry_price, exit_reason="entry_gap_invalidated",
            gross_return=gross, net_return=gross - 2 * TX_COST,
            false_breakout=False, days_held=0, initial_stop=stop,
        )
    cost_basis = entry_price
    trailing_stop = stop
    false_breakout = False

    exit_idx = None
    exit_price = None
    exit_reason = "open"
    for j in range(fill_idx, min(fill_idx + 61, len(df))):
        r = df.iloc[j]
        open_price = float(r["Open"])
        close = float(r["Close"])
        low = float(r["Low"])
        days_held = j - fill_idx
        profit_pct = (close - cost_basis) / cost_basis

        # Stops active at the start of the session execute intraday. Gap risk
        # is paid at the open; otherwise the executable fill is the stop itself.
        if low <= trailing_stop:
            exit_idx = j
            exit_price = min(open_price, trailing_stop)
            exit_reason = "stop_loss"
            break

        # False-breakout is observed causally, one bar at a time. It is a
        # breakout-specific rule and is intentionally not applied to Pattern C.
        is_breakout_pattern = pattern in {"A", "B", "breakout_no_retest"}
        if (use_false_breakout_exit and is_breakout_pattern and days_held <= 3
                and close < float(signal["breakout_level"])):
            false_breakout = True
            exit_idx = j
            exit_price = close
            exit_reason = "false_breakout"
            break

        if use_time_stop and days_held >= time_stop_days and profit_pct < 0.02:
            exit_idx = j
            exit_price = close
            exit_reason = "time_stop"
            break

        if days_held >= 20 and profit_pct >= 0.05:
            exit_idx = j
            exit_price = close
            exit_reason = "profit_take"
            break

        # These close-confirmed updates become active next session, avoiding
        # ambiguous same-bar assumptions about whether the high or low came first.
        if use_trailing_stop:
            if profit_pct >= 0.25:
                trailing_stop = max(trailing_stop, cost_basis * 1.15)
            elif profit_pct >= 0.15:
                trailing_stop = max(trailing_stop, cost_basis * 1.08)
        if (use_shooting_star and r["High"] >= r["high20"]
                and r["upper_wick"] > 2 * max(r["body"], 1e-6)):
            trailing_stop = max(trailing_stop, close * 0.97)

    if exit_idx is None:
        exit_idx = min(fill_idx + 20, len(df) - 1)
        exit_price = float(df.iloc[exit_idx]["Close"])
        exit_reason = "max_hold"

    assert exit_price is not None
    gross = (exit_price - entry_price) / entry_price
    net = gross - 2 * TX_COST
    return Trade(
        ticker=signal["ticker"],
        pattern=pattern,
        signal_date=df.index[entry_idx],
        entry_date=df.index[fill_idx],
        entry_price=entry_price,
        exit_date=df.index[exit_idx],
        exit_price=exit_price,
        exit_reason=exit_reason,
        gross_return=gross,
        net_return=net,
        false_breakout=false_breakout,
        days_held=exit_idx - fill_idx,
        initial_stop=stop,
    )


def generate_random_trades(df: pd.DataFrame, ticker: str, n_target: int, seed: int) -> list[Trade]:
    stable_ticker_seed = int(hashlib.sha256(ticker.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed + stable_ticker_seed)
    trades = []
    candidates = list(range(60, len(df) - 25))
    if not candidates:
        return trades
    picks = rng.sample(candidates, min(n_target, len(candidates)))
    for idx in sorted(picks):
        signal = {
            "ticker": ticker,
            "entry_idx": idx,
            "breakout_level": float(df.iloc[idx]["ma20"]),
            "retest_low": float(df.iloc[idx]["Low"] * 0.95),
            "stop": float(df.iloc[idx]["Close"] * 0.92),
        }
        t = simulate_trade(df, signal, time_stop_days=5, pattern="random")
        if t:
            trades.append(t)
    return trades


def compute_metrics(trades: list[Trade], spy_df: pd.DataFrame, label: str) -> dict:
    if not trades:
        return {
            "name": label,
            "num_trades": 0,
            "win_rate": 0.0,
            "avg_return": 0.0,
            "median_return": 0.0,
            "max_drawdown": 0.0,
            "cagr": 0.0,
            "sharpe": 0.0,
            "false_breakout_rate": 0.0,
            "spy_cagr": 0.0,
            "avg_days_held": 0.0,
        }

    rets = np.array([t.net_return for t in trades])
    wins = (rets > 0).sum()
    false_rate = sum(1 for t in trades if t.false_breakout) / len(trades)

    trades_sorted = sorted(trades, key=lambda t: t.entry_date)
    equity = 1.0
    peak = 1.0
    max_dd = 0.0
    equity_curve = []
    for t in trades_sorted:
        equity *= 1 + t.net_return
        peak = max(peak, equity)
        dd = (peak - equity) / peak
        max_dd = max(max_dd, dd)
        equity_curve.append(equity)

    years = (trades_sorted[-1].exit_date - trades_sorted[0].entry_date).days / 365.25
    cagr = (equity ** (1 / years) - 1) if years > 0 else 0.0

    spy_slice = spy_df.loc[trades_sorted[0].entry_date : trades_sorted[-1].exit_date, "Close"]
    if len(spy_slice) > 1:
        spy_cagr = (spy_slice.iloc[-1] / spy_slice.iloc[0]) ** (365.25 / max((spy_slice.index[-1] - spy_slice.index[0]).days, 1)) - 1
    else:
        spy_cagr = 0.0

    if len(rets) > 1 and rets.std() > 0:
        trades_per_year = len(rets) / max(years, 1)
        sharpe = (rets.mean() - RISK_FREE / trades_per_year) / rets.std() * np.sqrt(trades_per_year)
    else:
        sharpe = 0.0

    return {
        "name": label,
        "num_trades": len(trades),
        "win_rate": wins / len(trades) * 100,
        "avg_return": rets.mean() * 100,
        "median_return": float(np.median(rets)) * 100,
        "max_drawdown": max_dd * 100,
        "cagr": cagr * 100,
        "sharpe": float(sharpe),
        "false_breakout_rate": false_rate * 100,
        "spy_cagr": spy_cagr * 100,
        "avg_days_held": float(np.mean([t.days_held for t in trades])),
        "final_equity": equity,
    }


def run_pattern_backtest(
    data: dict[str, pd.DataFrame],
    pattern: PatternName,
    simulation_options: dict | None = None,
) -> StrategyResult:
    simulation_options = simulation_options or {}
    all_trades: list[Trade] = []
    for ticker, raw in data.items():
        if ticker == "SPY":
            continue
        df = add_indicators(raw)
        if pattern == "A":
            signals = detect_pattern_a(df, ticker)
        elif pattern == "B":
            signals = detect_pattern_b(df, ticker)
        elif pattern == "C":
            signals = detect_pattern_c(df, ticker)
        elif pattern == "breakout_no_retest":
            signals = detect_breakout_no_retest(df, ticker)
        elif pattern == "combined":
            seen = set()
            signals = []
            for fn in (detect_pattern_a, detect_pattern_b, detect_pattern_c):
                for s in fn(df, ticker):
                    key = (s["entry_idx"], s["pattern"])
                    if key not in seen:
                        seen.add(key)
                        signals.append(s)
        elif pattern == "random":
            n = max(3, len(df) // 500)
            trades = generate_random_trades(df, ticker, n, seed=42)
            all_trades.extend(trades)
            continue
        else:
            signals = []

        for sig in signals:
            t = simulate_trade(
                df, sig, pattern=sig.get("pattern", pattern), **simulation_options
            )
            if t:
                all_trades.append(t)

    spy = add_indicators(data["SPY"])
    metrics = compute_metrics(all_trades, spy, pattern)
    return StrategyResult(name=pattern, trades=all_trades, metrics=metrics)


def spy_buy_hold(data: dict[str, pd.DataFrame]) -> dict:
    spy = data["SPY"]
    start = spy.index[spy.index >= START_DATE][0] if any(spy.index >= START_DATE) else spy.index[0]
    end = spy.index[spy.index <= END_DATE][-1]
    s = spy.loc[start:end, "Close"]
    years = (s.index[-1] - s.index[0]).days / 365.25
    total_ret = s.iloc[-1] / s.iloc[0] - 1
    cagr = (1 + total_ret) ** (1 / years) - 1
    daily_rets = s.pct_change().dropna()
    sharpe = (daily_rets.mean() * 252 - RISK_FREE) / (daily_rets.std() * np.sqrt(252))
    peak = s.cummax()
    max_dd = ((peak - s) / peak).max()
    return {
        "name": "SPY_BuyHold",
        "num_trades": 1,
        "win_rate": 100.0 if total_ret > 0 else 0.0,
        "avg_return": total_ret * 100,
        "median_return": total_ret * 100,
        "max_drawdown": max_dd * 100,
        "cagr": cagr * 100,
        "sharpe": float(sharpe),
        "false_breakout_rate": 0.0,
        "spy_cagr": cagr * 100,
        "avg_days_held": (s.index[-1] - s.index[0]).days,
        "final_equity": s.iloc[-1] / s.iloc[0],
    }


def write_summary(results: dict[str, dict], spy_bh: dict) -> str:
    lines = [
        "# 日K突破形态回测总结",
        "",
        f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**回测区间：** {START_DATE} 至 {END_DATE}",
        f"**股票池：** {len(UNIVERSE)} 只（含 SPY/QQQ/SMH + 49 只流动性美股）",
        f"**交易成本：** 单边 {TX_COST*100:.1f}%",
        "",
        "---",
        "",
        "## 一、核心指标对比",
        "",
        "| 策略 | 交易数 | 胜率% | 均收益% | 中位收益% | 最大回撤% | CAGR% | Sharpe | 假突破率% | vs SPY CAGR |",
        "|------|--------|-------|---------|-----------|-----------|-------|--------|-----------|-------------|",
    ]
    spy_cagr = spy_bh["cagr"]
    for key in ["A", "B", "C", "combined", "breakout_no_retest", "random", "SPY_BuyHold"]:
        m = results.get(key, spy_bh if key == "SPY_BuyHold" else {})
        if not m:
            continue
        vs_spy = m.get("cagr", 0) - spy_cagr
        lines.append(
            f"| {m['name']} | {m['num_trades']} | {m['win_rate']:.1f} | "
            f"{m['avg_return']:.2f} | {m['median_return']:.2f} | {m['max_drawdown']:.1f} | "
            f"{m['cagr']:.2f} | {m['sharpe']:.2f} | {m.get('false_breakout_rate', 0):.1f} | "
            f"{vs_spy:+.2f}pp |"
        )

    lines.extend([
        "",
        "## 二、形态验证结论",
        "",
    ])

    def validated(m: dict) -> str:
        if m.get("num_trades", 0) < 30:
            return "❌ 样本不足"
        if m.get("avg_return", 0) <= 0 or m.get("sharpe", 0) <= 0:
            return "❌ 未验证"
        if m.get("win_rate", 0) >= 45 and m.get("sharpe", 0) >= 0.3:
            return "✅ 部分验证"
        if m.get("sharpe", 0) >= 0.3 and m.get("avg_return", 0) > 0:
            return "⚠️ 边缘验证（胜率略低）"
        return "❌ 未充分验证"

    pattern_notes = []
    for p, cn in [("A", "突破+回踩（图3/图9）"), ("B", "温和小阳突破（图2）"), ("C", "假摔黄金坑（图4）")]:
        m = results.get(p, {})
        status = validated(m)
        pattern_notes.append(f"### 形态 {p}：{cn} — {status}")
        pattern_notes.append(f"- 交易数：{m.get('num_trades', 0)}")
        pattern_notes.append(f"- 胜率：{m.get('win_rate', 0):.1f}%")
        pattern_notes.append(f"- 均收益/笔：{m.get('avg_return', 0):.2f}%")
        pattern_notes.append(f"- Sharpe：{m.get('sharpe', 0):.2f}")
        pattern_notes.append(f"- 假突破率：{m.get('false_breakout_rate', 0):.1f}%")
        pattern_notes.append("")

    lines.extend(pattern_notes)

    a_m = results.get("A", {})
    br_m = results.get("breakout_no_retest", {})
    lines.extend([
        "## 三、与基准对比",
        "",
        f"- **SPY 买入持有 CAGR：** {spy_cagr:.2f}%",
        f"- **无回踩突破（图1简化）：** {br_m.get('num_trades', 0)} 笔，胜率 {br_m.get('win_rate', 0):.1f}%，"
        f"CAGR {br_m.get('cagr', 0):.2f}%",
        f"- **随机入场基准：** {results.get('random', {}).get('num_trades', 0)} 笔，"
        f"胜率 {results.get('random', {}).get('win_rate', 0):.1f}%，"
        f"CAGR {results.get('random', {}).get('cagr', 0):.2f}%",
        "",
        "形态 A 与无回踩突破对比：",
        f"- 有回踩（A）均收益 {a_m.get('avg_return', 0):.2f}% vs 无回踩 {br_m.get('avg_return', 0):.2f}%",
        f"- 有回踩 Sharpe {a_m.get('sharpe', 0):.2f} vs 无回踩 {br_m.get('sharpe', 0):.2f}",
        "",
        "## 四、decisions.md 建议",
        "",
        "### 建议采纳（promote）",
        "- **假突破 3 日退出规则（图5）：** 若回测显示假突破率 >30% 且该退出规则降低均亏损，写入 exit 规则",
        "- **+15%/+25% 追踪止损（图6）：** 与 decisions.md 2026-06-27 规则 D 一致，回测验证后保持",
        "- **突破需放量确认：** 若 breakout_no_retest 胜率显著低于 Pattern A，强化「等回踩再入场」",
        "",
        "### 建议拒绝或降级（reject/defer）",
        "- 若 Pattern B/C 交易数 <30 或 Sharpe <0：暂不作为独立入场模块",
        "- 射击之星收紧止损：仅作辅助信号，不作硬退出",
        "",
        "## 五、局限性说明",
        "",
        "- **幸存者偏差：** 当前股票池含 2024-2025 才上市标的（ARM/CRDO 等），长期统计偏乐观",
        "- **无滑点模型：** 仅计 0.1% 单边佣金，未模拟冲击成本",
        "- **等权串行复利：** 每笔交易按序复利，非真实多仓位组合",
        "- **无前视偏差校验：** 信号基于收盘确认，假设次日可成交",
        "",
        "---",
        "*不构成投资建议。历史回测不代表未来表现。*",
    ])
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("日K突破形态回测")
    print("=" * 60)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"\n下载/加载 {len(UNIVERSE)} 只股票数据...")
    data = fetch_ohlcv(UNIVERSE, START_DATE, END_DATE)
    print(f"成功加载 {len(data)} 只")

    if "SPY" not in data:
        raise RuntimeError("SPY data required")

    results: dict[str, dict] = {}
    all_trades_export: dict[str, list] = {}

    for pattern in ["A", "B", "C", "combined", "breakout_no_retest", "random"]:
        print(f"\n运行 Pattern {pattern}...")
        res = run_pattern_backtest(data, pattern)  # type: ignore
        results[pattern] = res.metrics
        all_trades_export[pattern] = [
            {
                "ticker": t.ticker,
                "entry": str(t.entry_date.date()),
                "exit": str(t.exit_date.date()),
                "net_return_pct": round(t.net_return * 100, 2),
                "exit_reason": t.exit_reason,
                "false_breakout": t.false_breakout,
            }
            for t in res.trades[:200]
        ]
        m = res.metrics
        print(
            f"  trades={m['num_trades']} win={m['win_rate']:.1f}% "
            f"avg={m['avg_return']:.2f}% sharpe={m['sharpe']:.2f}"
        )

    spy_bh = spy_buy_hold(data)
    results["SPY_BuyHold"] = spy_bh
    print(f"\nSPY Buy&Hold CAGR: {spy_bh['cagr']:.2f}%")

    summary = write_summary(results, spy_bh)
    summary_path = os.path.join(RESULTS_DIR, "backtest_summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"\n报告已保存: {summary_path}")

    metrics_path = os.path.join(RESULTS_DIR, "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({"metrics": results, "sample_trades": all_trades_export}, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
