#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

DEFAULT_START = "2025-01-01"
DEFAULT_END = None
MARKET_TICKERS = ["SPY", "QQQ", "SMH", "IWM", "RSP", "HYG", "LQD", "TLT", "^VIX", "^VIX3M"]


@dataclass(frozen=True)
class FearSignal:
    name: str
    value: float | None
    points: int
    note: str


@dataclass(frozen=True)
class FearResult:
    as_of: str
    score: int
    regime: str
    risk_multiplier: float
    max_gross_exposure: float
    max_new_buy_exposure: float
    cash_floor: float
    signals: list[FearSignal]
    action: str


def pct(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    return f"{value * 100:.2f}%"


def fmt(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    return f"{value:.2f}"


def download_market_data(start: str = DEFAULT_START, end: str | None = DEFAULT_END) -> pd.DataFrame:
    import yfinance as yf

    raw = yf.download(
        MARKET_TICKERS,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        threads=True,
        group_by="column",
    )
    if raw.empty:
        raise RuntimeError("failed to download market fear data")
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    close = close.dropna(how="all")
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def latest(series: pd.Series) -> float | None:
    clean = series.dropna()
    if clean.empty:
        return None
    return float(clean.iloc[-1])


def ratio(close: pd.DataFrame, numerator: str, denominator: str) -> pd.Series:
    if numerator not in close.columns or denominator not in close.columns:
        return pd.Series(dtype=float)
    return close[numerator] / close[denominator]


def add_signal(signals: list[FearSignal], name: str, value: float | None, points: int, note: str) -> None:
    signals.append(FearSignal(name=name, value=None if value is None else float(value), points=points, note=note))


def classify_vix_level(vix: float | None) -> tuple[int, str]:
    if vix is None:
        return 0, "VIX unavailable"
    if vix >= 35:
        return 4, "panic volatility"
    if vix >= 30:
        return 3, "high stress volatility"
    if vix >= 22:
        return 2, "stress volatility"
    if vix >= 16:
        return 1, "elevated but controlled volatility"
    return 0, "calm volatility"


def classify_drawdown(dd: float | None, label: str) -> tuple[int, str]:
    if dd is None:
        return 0, f"{label} drawdown unavailable"
    if dd <= -0.12:
        return 3, f"{label} deep drawdown from 63-day high"
    if dd <= -0.08:
        return 2, f"{label} meaningful drawdown from 63-day high"
    if dd <= -0.04:
        return 1, f"{label} mild drawdown from 63-day high"
    return 0, f"{label} near short-term high"


def compute_fear(close: pd.DataFrame) -> FearResult:
    close = close.sort_index()
    as_of = close.index[-1].strftime("%Y-%m-%d")
    signals: list[FearSignal] = []

    vix = latest(close["^VIX"]) if "^VIX" in close.columns else None
    points, note = classify_vix_level(vix)
    add_signal(signals, "vix_level", vix, points, note)

    vix_5d = None
    if "^VIX" in close.columns and close["^VIX"].dropna().shape[0] >= 6:
        v = close["^VIX"].dropna()
        vix_5d = float(v.iloc[-1] / v.iloc[-6] - 1.0)
        if vix_5d >= 0.50:
            points, note = 3, "VIX 5-day spike above 50%"
        elif vix_5d >= 0.30:
            points, note = 2, "VIX 5-day spike above 30%"
        elif vix_5d >= 0.15:
            points, note = 1, "VIX 5-day spike above 15%"
        else:
            points, note = 0, "no major VIX spike"
        add_signal(signals, "vix_5d_change", vix_5d, points, note)

    if "^VIX" in close.columns and "^VIX3M" in close.columns:
        term = ratio(close, "^VIX", "^VIX3M").dropna()
        value = latest(term)
        if value is not None and value >= 1.05:
            points, note = 3, "VIX curve inverted, near-term stress dominant"
        elif value is not None and value >= 1.00:
            points, note = 2, "VIX curve flat/inverted"
        else:
            points, note = 0, "VIX term structure normal"
        add_signal(signals, "vix_vix3m_ratio", value, points, note)

    for symbol in ["SPY", "QQQ", "SMH"]:
        if symbol not in close.columns:
            continue
        c = close[symbol].dropna()
        if c.shape[0] < 63:
            continue
        dd63 = float(c.iloc[-1] / c.iloc[-63:].max() - 1.0)
        points, note = classify_drawdown(dd63, symbol)
        add_signal(signals, f"{symbol.lower()}_drawdown_63d", dd63, points, note)

        ma50 = c.rolling(50).mean().iloc[-1]
        ma200 = c.rolling(200).mean().iloc[-1] if c.shape[0] >= 200 else np.nan
        below50 = c.iloc[-1] < ma50 if pd.notna(ma50) else False
        below200 = c.iloc[-1] < ma200 if pd.notna(ma200) else False
        if below200:
            points, note = 3, f"{symbol} below 200-day trend"
        elif below50:
            points, note = 1, f"{symbol} below 50-day trend"
        else:
            points, note = 0, f"{symbol} trend intact"
        add_signal(signals, f"{symbol.lower()}_trend_break", 1.0 if below50 or below200 else 0.0, points, note)

    for numerator, denominator, name in [
        ("IWM", "SPY", "smallcap_vs_spy_21d"),
        ("RSP", "SPY", "equal_weight_vs_spy_21d"),
        ("HYG", "LQD", "credit_risk_21d"),
    ]:
        rel = ratio(close, numerator, denominator).dropna()
        if rel.shape[0] < 22:
            continue
        change = float(rel.iloc[-1] / rel.iloc[-22] - 1.0)
        if change <= -0.05:
            points, note = 2, f"{name} deteriorating sharply"
        elif change <= -0.025:
            points, note = 1, f"{name} deteriorating"
        else:
            points, note = 0, f"{name} stable"
        add_signal(signals, name, change, points, note)

    score = int(sum(signal.points for signal in signals))
    if score >= 14:
        regime = "panic"
        risk_multiplier = 0.20
        max_gross = 0.35
        max_new_buy = 0.00
        cash_floor = 0.65
        action = "Stop new buys; preserve capital; only consider hedges or forced risk reduction."
    elif score >= 9:
        regime = "stress"
        risk_multiplier = 0.40
        max_gross = 0.55
        max_new_buy = 0.10
        cash_floor = 0.45
        action = "Cut position sizes, avoid weak names, and require reclaim signals before adding."
    elif score >= 5:
        regime = "elevated"
        risk_multiplier = 0.70
        max_gross = 0.75
        max_new_buy = 0.25
        cash_floor = 0.25
        action = "Allow staged buys only near support; keep a meaningful cash buffer."
    else:
        regime = "normal"
        risk_multiplier = 1.00
        max_gross = 0.95
        max_new_buy = 0.50
        cash_floor = 0.05
        action = "Normal staged buying is allowed when stock-level filters agree."

    return FearResult(
        as_of=as_of,
        score=score,
        regime=regime,
        risk_multiplier=risk_multiplier,
        max_gross_exposure=max_gross,
        max_new_buy_exposure=max_new_buy,
        cash_floor=cash_floor,
        signals=signals,
        action=action,
    )


def write_outputs(result: FearResult, results_dir: Path = RESULTS_DIR) -> tuple[Path, Path]:
    results_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / "market_fear_latest.json"
    md_path = results_dir / "market_fear_latest.md"

    payload = asdict(result)
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Market Fear Regime",
        "",
        f"- As of: `{result.as_of}`",
        f"- Score: `{result.score}`",
        f"- Regime: `{result.regime}`",
        f"- Risk multiplier: `{result.risk_multiplier:.0%}`",
        f"- Max gross exposure: `{result.max_gross_exposure:.0%}`",
        f"- Max new buy exposure: `{result.max_new_buy_exposure:.0%}`",
        f"- Cash floor: `{result.cash_floor:.0%}`",
        f"- Action: {result.action}",
        "",
        "## Signals",
        "",
        "| Signal | Value | Points | Note |",
        "| --- | ---: | ---: | --- |",
    ]
    for signal in result.signals:
        value = pct(signal.value) if "change" in signal.name or "drawdown" in signal.name or "21d" in signal.name else fmt(signal.value)
        lines.append(f"| {signal.name} | {value} | {signal.points} | {signal.note} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute market fear regime for strategy analysis.")
    parser.add_argument("--start", default=DEFAULT_START)
    parser.add_argument("--end", default=DEFAULT_END)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    close = download_market_data(start=args.start, end=args.end)
    result = compute_fear(close)
    if not args.no_write:
        _json_path, md_path = write_outputs(result)
        print(f"Wrote {md_path}")
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
