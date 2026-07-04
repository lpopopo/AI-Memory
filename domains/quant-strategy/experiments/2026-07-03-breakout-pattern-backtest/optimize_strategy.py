"""Robust evaluation layer for the corrected breakout backtest.

This deliberately separates evidence generation from strategy promotion. It
adds causal fills, exit-rule ablations, a fixed out-of-sample split, clustered
bootstrap intervals, and a capacity-constrained marked-to-market portfolio.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import run_backtest as bt


HERE = Path(__file__).resolve().parent
OOS_START = pd.Timestamp("2019-01-01")
MAX_POSITIONS = 10
BOOTSTRAP_SAMPLES = 2000
SEED = 20260703


def load_cached_data() -> dict[str, pd.DataFrame]:
    data = {}
    for path in sorted((HERE / "data_cache").glob("*.csv")):
        df = pd.read_csv(path, parse_dates=["Date"], index_col="Date").sort_index()
        if len(df) > 100:
            data[path.stem] = df
    if "SPY" not in data:
        raise RuntimeError("SPY cache is required")
    return data


def trade_stats(trades: list[bt.Trade]) -> dict:
    if not trades:
        return {"trades": 0, "win_rate_pct": 0.0, "mean_pct": 0.0,
                "median_pct": 0.0, "profit_factor": 0.0}
    values = np.asarray([t.net_return for t in trades], dtype=float)
    gains = values[values > 0].sum()
    losses = -values[values < 0].sum()
    return {
        "trades": len(trades),
        "win_rate_pct": float((values > 0).mean() * 100),
        "mean_pct": float(values.mean() * 100),
        "median_pct": float(np.median(values) * 100),
        "profit_factor": float(gains / losses) if losses else float("inf"),
    }


def clustered_bootstrap(trades: list[bt.Trade]) -> dict:
    """Resample whole tickers so correlated trades are not treated as IID."""
    grouped = defaultdict(list)
    for trade in trades:
        grouped[trade.ticker].append(trade.net_return)
    tickers = sorted(grouped)
    if len(tickers) < 2:
        return {"mean_ci95_pct": [None, None], "prob_mean_positive": None}
    rng = np.random.default_rng(SEED)
    means = np.empty(BOOTSTRAP_SAMPLES)
    for i in range(BOOTSTRAP_SAMPLES):
        sampled = rng.choice(tickers, size=len(tickers), replace=True)
        returns = [r for ticker in sampled for r in grouped[ticker]]
        means[i] = np.mean(returns) * 100
    lo, hi = np.quantile(means, [0.025, 0.975])
    return {
        "mean_ci95_pct": [float(lo), float(hi)],
        "prob_mean_positive": float((means > 0).mean()),
    }


def portfolio_metrics(
    trades: list[bt.Trade], data: dict[str, pd.DataFrame], max_positions: int = MAX_POSITIONS
) -> dict:
    """Simulate capped concurrent positions and mark them to market daily."""
    if not trades:
        return {"accepted_trades": 0}
    entries = defaultdict(list)
    for t in sorted(trades, key=lambda x: (x.entry_date, x.ticker)):
        entries[pd.Timestamp(t.entry_date)].append(t)
    calendar = data["SPY"].index
    start = max(min(entries), calendar.min())
    end = min(max(t.exit_date for t in trades), calendar.max())
    calendar = calendar[(calendar >= start) & (calendar <= end)]
    cash = 1.0
    positions: dict[str, dict] = {}
    values = []
    accepted = skipped = 0
    exposure_sum = 0.0

    def price(ticker: str, date: pd.Timestamp, field: str = "Close") -> float:
        df = data[ticker]
        if date in df.index:
            return float(df.at[date, field])
        prior = df.index[df.index <= date]
        return float(df.at[prior[-1], field])

    for date in calendar:
        # Entries occur at the open, before close-based exits free capacity.
        equity_open = cash + sum(
            p["shares"] * price(ticker, date, "Open") for ticker, p in positions.items()
        )
        for trade in entries.get(date, []):
            if len(positions) >= max_positions or trade.ticker in positions:
                skipped += 1
                continue
            allocation = min(cash, equity_open / max_positions)
            if allocation <= 0:
                skipped += 1
                continue
            cash -= allocation
            positions[trade.ticker] = {
                "shares": allocation * (1 - bt.TX_COST) / trade.entry_price,
                "trade": trade,
            }
            accepted += 1

        for ticker, pos in list(positions.items()):
            trade = pos["trade"]
            if pd.Timestamp(trade.exit_date) == date:
                cash += pos["shares"] * trade.exit_price * (1 - bt.TX_COST)
                del positions[ticker]

        equity = cash + sum(
            p["shares"] * price(ticker, date, "Close") for ticker, p in positions.items()
        )
        values.append(equity)
        exposure_sum += len(positions) / max_positions

    curve = pd.Series(values, index=calendar, dtype=float)
    daily = curve.pct_change().dropna()
    years = max((calendar[-1] - calendar[0]).days / 365.25, 1 / 365.25)
    cagr = curve.iloc[-1] ** (1 / years) - 1
    drawdown = curve / curve.cummax() - 1
    sharpe = ((daily.mean() * 252 - bt.RISK_FREE) /
              (daily.std() * math.sqrt(252))) if daily.std() > 0 else 0.0
    return {
        "accepted_trades": accepted,
        "skipped_capacity_or_duplicate": skipped,
        "max_positions": max_positions,
        "cagr_pct": float(cagr * 100),
        "max_drawdown_pct": float(-drawdown.min() * 100),
        "sharpe": float(sharpe),
        "final_equity": float(curve.iloc[-1]),
        "average_exposure_pct": float(exposure_sum / len(curve) * 100),
    }


def evaluate(trades: list[bt.Trade], data: dict[str, pd.DataFrame]) -> dict:
    insample = [t for t in trades if t.entry_date < OOS_START]
    oos = [t for t in trades if t.entry_date >= OOS_START]
    yearly = {}
    for year in sorted({t.entry_date.year for t in oos}):
        yearly[str(year)] = trade_stats([t for t in oos if t.entry_date.year == year])
    return {
        "all": trade_stats(trades),
        "in_sample_2006_2018": trade_stats(insample),
        "out_of_sample_2019_2025": {
            **trade_stats(oos), **clustered_bootstrap(oos),
            "portfolio": portfolio_metrics(oos, data),
            "by_year": yearly,
        },
    }


def apply_market_regime(trades: list[bt.Trade], data: dict[str, pd.DataFrame]) -> list[bt.Trade]:
    """Causal gate: SPY close above its 200-day average on signal day."""
    spy = data["SPY"]["Close"]
    ma200 = spy.rolling(200).mean()
    kept = []
    for trade in trades:
        date = pd.Timestamp(trade.signal_date)
        if date in spy.index and pd.notna(ma200.loc[date]) and spy.loc[date] > ma200.loc[date]:
            kept.append(trade)
    return kept


def benchmark_metrics(data: dict[str, pd.DataFrame], start: pd.Timestamp) -> dict:
    close = data["SPY"].loc[data["SPY"].index >= start, "Close"]
    daily = close.pct_change().dropna()
    years = (close.index[-1] - close.index[0]).days / 365.25
    cagr = (close.iloc[-1] / close.iloc[0]) ** (1 / years) - 1
    dd = close / close.cummax() - 1
    sharpe = (daily.mean() * 252 - bt.RISK_FREE) / (daily.std() * math.sqrt(252))
    return {
        "start": str(close.index[0].date()), "end": str(close.index[-1].date()),
        "cagr_pct": float(cagr * 100), "max_drawdown_pct": float(-dd.min() * 100),
        "sharpe": float(sharpe), "final_equity": float(close.iloc[-1] / close.iloc[0]),
    }


def write_report(output: dict) -> None:
    def row(pattern, config, gate="unfiltered"):
        return output["patterns"][pattern][config][gate]["out_of_sample_2019_2025"]

    lines = [
        "# 突破形态策略稳健性优化报告", "",
        "**固定样本外：** 2019-01-01 至 2025-12-31  ",
        "**成交语义：** 收盘确认，下一交易日开盘成交；止损按止损价或不利跳空开盘价成交  ",
        "**统计方法：** 按股票聚类 bootstrap 95% CI；10 个并发仓位逐日盯市  ",
        "", "## 结论", "",
        "- 原版 A 的样本外均收益置信区间跨越 0，暂不能证明独立 edge。",
        "- C 是当前唯一在原规则下仍保持样本外正期望的形态。",
        "- 5 日时间止损、射击之星收紧止损、3 日假突破退出均未被消融实验支持。",
        "- 当前候选规则是 **C + 初始止损 + 最长持有 20 日 + SPY>MA200**；仍受幸存者偏差约束。",
        "", "## 样本外核心结果", "",
        "| 形态/规则 | 交易数 | 均收益 | 95% CI | 组合 CAGR | 最大回撤 | Sharpe |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    specs = [
        ("A 原规则", "A", "full", "unfiltered"),
        ("A 止损+20日", "A", "stop_and_20d", "unfiltered"),
        ("B 止损+20日", "B", "stop_and_20d", "unfiltered"),
        ("C 原规则", "C", "full", "unfiltered"),
        ("C 止损+20日", "C", "stop_and_20d", "unfiltered"),
        ("C 止损+20日+MA200", "C", "stop_and_20d", "spy_above_ma200"),
        ("直接突破 止损+20日", "breakout_no_retest", "stop_and_20d", "unfiltered"),
    ]
    for label, pattern, config, gate in specs:
        x = row(pattern, config, gate); p = x["portfolio"]; ci = x["mean_ci95_pct"]
        lines.append(
            f"| {label} | {x['trades']} | {x['mean_pct']:.2f}% | "
            f"[{ci[0]:.2f}%, {ci[1]:.2f}%] | {p['cagr_pct']:.2f}% | "
            f"{p['max_drawdown_pct']:.2f}% | {p['sharpe']:.2f} |"
        )
    spy = output["benchmark"]["SPY_2019_2025"]
    lines += [
        f"| SPY 买入持有 | — | — | — | {spy['cagr_pct']:.2f}% | "
        f"{spy['max_drawdown_pct']:.2f}% | {spy['sharpe']:.2f} |", "",
        "## 候选执行规则", "",
        "1. 仅启用 Pattern C：收盘位于 MA50 上方且 MA20>MA50，连续 2–3 日收于 MA20 下方，随后收复 MA20。",
        "2. 信号日收盘后确认；仅当 SPY 同日收盘高于 MA200 时允许入场；下一交易日开盘成交。",
        "3. 初始止损设于假摔阶段最低点；跳空跌破时按开盘价承担真实缺口。",
        "4. 不使用 5 日时间止损、射击之星收紧、3 日假突破退出或 +15%/+25% 追踪止损。",
        "5. 最长持有 20 个交易日，最多同时持有 10 个仓位；同一股票不重叠持仓。",
        "", "## 尚未解决", "",
        "- 股票池是当前存活且人工挑选的 53 只证券，仍存在幸存者与选择偏差。",
        "- 本轮比较了多个退出组合，存在多重检验；后续新增数据必须作为真正前瞻样本。",
        "- 当前候选组合的目标是改善风险调整收益，并未跑赢同期 SPY 的绝对 CAGR。",
        "- 尚未并入仓库的双袖套/恐慌门控总策略，暂不应直接 promote 到实盘决策。",
        "", "完整机器可读结果见 `results/robustness_metrics.json`。", "",
        "*不构成投资建议。*",
    ]
    (HERE / "results" / "robustness_report.md").write_text("\n".join(lines), encoding="utf-8")


def collect_signals(data: dict[str, pd.DataFrame], pattern: str):
    detector = {
        "A": bt.detect_pattern_a,
        "B": bt.detect_pattern_b,
        "C": bt.detect_pattern_c,
        "breakout_no_retest": bt.detect_breakout_no_retest,
    }[pattern]
    prepared = {}
    signals = {}
    for ticker, raw in data.items():
        if ticker == "SPY":
            continue
        prepared[ticker] = bt.add_indicators(raw)
        signals[ticker] = detector(prepared[ticker], ticker)
    return prepared, signals


def main() -> None:
    data = load_cached_data()
    configs = {
        "full": {},
        "no_false_breakout_exit": {"use_false_breakout_exit": False},
        "no_trailing_stop": {"use_trailing_stop": False},
        "no_shooting_star": {"use_shooting_star": False},
        "no_time_stop": {"use_time_stop": False},
        "stop_and_20d": {
            "use_false_breakout_exit": False, "use_trailing_stop": False,
            "use_shooting_star": False, "use_time_stop": False,
        },
        "trailing_stop_and_20d": {
            "use_false_breakout_exit": False, "use_trailing_stop": True,
            "use_shooting_star": False, "use_time_stop": False,
        },
    }
    output = {
        "method": {
            "generated_at": pd.Timestamp.now(tz="Asia/Shanghai").isoformat(),
            "oos_start": str(OOS_START.date()),
            "bootstrap": f"ticker-clustered, n={BOOTSTRAP_SAMPLES}, seed={SEED}",
            "portfolio_max_positions": MAX_POSITIONS,
            "entry": "signal close, next-session open",
            "stop_fill": "stop price, or adverse gap open",
        },
        "patterns": {},
        "benchmark": {"SPY_2019_2025": benchmark_metrics(data, OOS_START)},
    }
    for pattern in ("A", "B", "C", "breakout_no_retest"):
        print(f"Detecting and evaluating {pattern}...", flush=True)
        output["patterns"][pattern] = {}
        prepared, signals = collect_signals(data, pattern)
        for name, options in configs.items():
            trades = []
            for ticker, ticker_signals in signals.items():
                for signal in ticker_signals:
                    trade = bt.simulate_trade(
                        prepared[ticker], signal,
                        pattern=signal.get("pattern", pattern), **options
                    )
                    if trade:
                        trades.append(trade)
            output["patterns"][pattern][name] = {
                "unfiltered": evaluate(trades, data),
                "spy_above_ma200": evaluate(apply_market_regime(trades, data), data),
            }
            oos = output["patterns"][pattern][name]["unfiltered"]["out_of_sample_2019_2025"]
            print(f"  {name}: n={oos['trades']} mean={oos['mean_pct']:.3f}% "
                  f"CI={oos['mean_ci95_pct']}", flush=True)

    out = HERE / "results" / "robustness_metrics.json"
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(output)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
