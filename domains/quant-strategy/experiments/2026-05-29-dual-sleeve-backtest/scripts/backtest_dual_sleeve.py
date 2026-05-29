#!/usr/bin/env python3
import json
import time
from pathlib import Path

import pandas as pd
import yfinance as yf


START = "2016-05-29"
END = "2026-05-29"
INITIAL_CAPITAL = 1.0
TRADING_DAYS = 252

BENCHMARKS = ["SPY", "QQQ"]
VALUE_ETFS = ["VTV", "IWD", "SCHD"]
TACTICAL_ETFS = [
    "XLK",
    "XLC",
    "XLY",
    "XLI",
    "XLF",
    "XLV",
    "XLE",
    "XLB",
    "XLU",
    "XLRE",
    "XLP",
    "SMH",
    "IBB",
    "ITA",
]
ALL_SYMBOLS = sorted(set(BENCHMARKS + VALUE_ETFS + TACTICAL_ETFS))

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"


def fetch_close_prices():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = DATA_DIR / "yfinance_adjusted_close.csv"
    if cache_path.exists():
        close = pd.read_csv(cache_path, index_col=0, parse_dates=True)
        missing_required = [s for s in BENCHMARKS if s not in close.columns or close[s].dropna().empty]
        if not missing_required:
            return close
        cache_path.unlink()

    series = {}
    failures = {}
    for symbol in ALL_SYMBOLS:
        try:
            series[symbol] = fetch_symbol_close(symbol)
        except Exception as err:
            failures[symbol] = str(err)

    missing_required = [s for s in BENCHMARKS if s not in series]
    if missing_required:
        raise RuntimeError(f"missing required benchmark data: {missing_required}; failures={failures}")

    close = pd.concat(series, axis=1)
    close.columns = list(series.keys())

    close = close.sort_index()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    close = close.dropna(how="all")
    close.to_csv(cache_path)
    if failures:
        (DATA_DIR / "download_failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
    return close


def fetch_symbol_close(symbol):
    path = DATA_DIR / f"{symbol}_adjusted_close.csv"
    if path.exists():
        cached = pd.read_csv(path, index_col=0, parse_dates=True)
        if symbol in cached.columns and not cached[symbol].dropna().empty:
            return cached[symbol]

    last_error = None
    for attempt in range(3):
        try:
            data = yf.download(
                tickers=symbol,
                start=START,
                end=END,
                auto_adjust=True,
                progress=False,
                threads=False,
            )
            if data.empty:
                raise RuntimeError("empty data")
            if isinstance(data.columns, pd.MultiIndex):
                close = data["Close"][symbol] if ("Close", symbol) in data.columns else data["Close"].iloc[:, 0]
            else:
                close = data["Close"]
            close = close.rename(symbol).dropna()
            if len(close) < 200:
                raise RuntimeError(f"insufficient rows: {len(close)}")
            close.to_frame().to_csv(path)
            return close
        except Exception as err:
            last_error = err
            time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(str(last_error))


def month_end_dates(index):
    markers = []
    periods = index.to_period("M")
    for i, dt in enumerate(index):
        if i == len(index) - 1 or periods[i + 1] != periods[i]:
            markers.append(dt)
    return set(markers)


def value_weights(close, dt):
    available = [s for s in VALUE_ETFS if s in close.columns and pd.notna(close.at[dt, s])]
    if not available:
        return {}
    weight = 0.5 / len(available)
    return {s: weight for s in available}


def tactical_weights(close, ma50, ma200, mom63, mom126, dt):
    if pd.isna(close.at[dt, "SPY"]) or pd.isna(ma200.at[dt, "SPY"]):
        return {}
    if close.at[dt, "SPY"] <= ma200.at[dt, "SPY"]:
        return {}

    ranked = []
    for symbol in TACTICAL_ETFS:
        if symbol not in close.columns:
            continue
        fields = [
            close.at[dt, symbol],
            ma50.at[dt, symbol],
            mom63.at[dt, symbol],
            mom126.at[dt, symbol],
        ]
        if any(pd.isna(v) for v in fields):
            continue
        if close.at[dt, symbol] <= ma50.at[dt, symbol]:
            continue
        if mom63.at[dt, symbol] <= 0:
            continue
        score = mom63.at[dt, symbol] + mom126.at[dt, symbol]
        ranked.append((score, symbol))

    ranked.sort(reverse=True)
    selected = [symbol for _score, symbol in ranked[:3]]
    if not selected:
        return {}
    weight = 0.5 / len(selected)
    return {s: weight for s in selected}


def combine_weights(*groups):
    weights = {}
    for group in groups:
        for symbol, weight in group.items():
            weights[symbol] = weights.get(symbol, 0.0) + weight
    return weights


def run_dual_sleeve(close):
    returns = close.pct_change(fill_method=None).fillna(0.0)
    ma50 = close.rolling(50).mean()
    ma200 = close.rolling(200).mean()
    mom63 = close / close.shift(63) - 1.0
    mom126 = close / close.shift(126) - 1.0
    rebalance_dates = month_end_dates(close.index)

    weights = {}
    equity = []
    allocations = []
    value = INITIAL_CAPITAL

    for dt in close.index:
        day_return = 0.0
        for symbol, weight in weights.items():
            if symbol in returns.columns and pd.notna(returns.at[dt, symbol]):
                day_return += weight * returns.at[dt, symbol]
        value *= 1.0 + day_return
        equity.append(value)

        if dt in rebalance_dates:
            v = value_weights(close, dt)
            t = tactical_weights(close, ma50, ma200, mom63, mom126, dt)
            weights = combine_weights(v, t)
            allocations.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "value": "|".join(sorted(v)),
                    "tactical": "|".join(sorted(t)),
                    "cash": max(0.0, 1.0 - sum(weights.values())),
                }
            )

    return pd.Series(equity, index=close.index, name="dual_sleeve_v0"), pd.DataFrame(allocations)


def run_buy_hold(close, weights, name):
    returns = close.pct_change(fill_method=None).fillna(0.0)
    weighted = pd.Series(0.0, index=close.index)
    for symbol, weight in weights.items():
        weighted = weighted.add(returns[symbol].fillna(0.0) * weight, fill_value=0.0)
    return (1.0 + weighted).cumprod().rename(name)


def summarize(name, equity):
    daily_returns = equity.pct_change(fill_method=None).dropna()
    years = (equity.index[-1] - equity.index[0]).days / 365.25
    cagr = equity.iloc[-1] ** (1 / years) - 1 if years > 0 else 0.0
    peak = equity.cummax()
    drawdown = equity / peak - 1.0
    vol = daily_returns.std() * (TRADING_DAYS**0.5)
    sharpe = (daily_returns.mean() * TRADING_DAYS / vol) if vol else 0.0
    downside = daily_returns[daily_returns < 0]
    downside_vol = downside.std() * (TRADING_DAYS**0.5)
    sortino = (daily_returns.mean() * TRADING_DAYS / downside_vol) if downside_vol else 0.0
    wins = daily_returns[daily_returns > 0]
    losses = daily_returns[daily_returns < 0]
    return {
        "name": name,
        "start": equity.index[0].strftime("%Y-%m-%d"),
        "end": equity.index[-1].strftime("%Y-%m-%d"),
        "final_value": float(equity.iloc[-1]),
        "cagr": float(cagr),
        "max_drawdown": float(drawdown.min()),
        "volatility": float(vol),
        "sharpe": float(sharpe),
        "sortino": float(sortino),
        "win_rate": float(len(wins) / len(daily_returns)) if len(daily_returns) else 0.0,
        "avg_win": float(wins.mean()) if len(wins) else 0.0,
        "avg_loss": float(losses.mean()) if len(losses) else 0.0,
    }


def pct(value):
    return f"{value * 100:.2f}%"


def write_outputs(close, curves, allocations):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    equity = pd.concat(curves, axis=1)
    equity.to_csv(RESULTS_DIR / "equity_curve.csv", index_label="date")
    allocations.to_csv(RESULTS_DIR / "monthly_allocations.csv", index=False)

    summaries = [summarize(col, equity[col]) for col in equity.columns]
    (RESULTS_DIR / "summary.json").write_text(
        json.dumps({"summaries": summaries}, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Backtest Summary",
        "",
        f"Period: {close.index[0].strftime('%Y-%m-%d')} to {close.index[-1].strftime('%Y-%m-%d')}",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for s in summaries:
        lines.append(
            f"| {s['name']} | {s['final_value']:.3f} | {pct(s['cagr'])} | "
            f"{pct(s['max_drawdown'])} | {pct(s['volatility'])} | "
            f"{s['sharpe']:.2f} | {s['sortino']:.2f} | {pct(s['win_rate'])} |"
        )

    lines.extend(
        [
            "",
            "## V0 Interpretation Notes",
            "",
            "- Value sleeve is proxied by equal-weight `VTV`, `IWD`, and `SCHD`.",
            "- Hot-industry sleeve rotates monthly into the top 3 eligible ETFs.",
            "- Tactical sleeve moves to cash when SPY is below its 200-day moving average.",
            "- Cash earns 0% in this version.",
            "- Prices use yfinance auto-adjusted daily close data.",
            "- This validates the allocation structure, not the final individual-stock strategy.",
        ]
    )
    (RESULTS_DIR / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summaries


def main():
    close = fetch_close_prices()
    required = ["SPY", "QQQ"]
    missing = [s for s in required if s not in close.columns]
    if missing:
        raise RuntimeError(f"missing benchmark columns: {missing}")

    strategy, allocations = run_dual_sleeve(close)
    curves = [
        strategy,
        run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    ]
    summaries = write_outputs(close, curves, allocations)
    for s in summaries:
        print(
            f"{s['name']}: final={s['final_value']:.3f}, "
            f"CAGR={pct(s['cagr'])}, MDD={pct(s['max_drawdown'])}, "
            f"Sharpe={s['sharpe']:.2f}"
        )


if __name__ == "__main__":
    main()
