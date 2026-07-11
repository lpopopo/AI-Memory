#!/usr/bin/env python3
"""Causal 0-100 market sentiment oscillator.

Zero means extreme fear and 100 means extreme greed. Components are converted
to rolling empirical percentiles using only observations available on that day.
Missing components are not treated as neutral; at least six are required.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED = ("SPY", "QQQ", "IWM", "RSP", "HYG", "LQD", "TLT", "^VIX", "^VIX3M")


def rolling_percentile(series: pd.Series, window: int = 756, min_periods: int = 252) -> pd.Series:
    def percentile(values: np.ndarray) -> float:
        current = values[-1]
        clean = values[np.isfinite(values)]
        if not np.isfinite(current) or clean.size == 0:
            return np.nan
        return float((clean <= current).sum() / clean.size)
    return series.rolling(window, min_periods=min_periods).apply(percentile, raw=True)


def compute_sentiment(close: pd.DataFrame, put_call: pd.Series | None = None) -> pd.DataFrame:
    missing = sorted(set(REQUIRED) - set(close.columns))
    if missing:
        raise ValueError(f"missing sentiment inputs: {missing}")
    # Vendor calendars can contain volatility-only holiday rows. They must not
    # break rolling equity indicators or create synthetic trading sessions.
    close = close.sort_index().astype(float).dropna(subset=["SPY", "QQQ"])
    raw = pd.DataFrame(index=close.index)
    raw["market_momentum"] = close["SPY"] / close["SPY"].rolling(125).mean() - 1
    raw["market_volatility"] = -(close["^VIX"] / close["^VIX"].rolling(50).mean() - 1)
    raw["volatility_term_structure"] = -(close["^VIX"] / close["^VIX3M"] - 1)
    raw["equal_weight_breadth"] = (close["RSP"] / close["SPY"]).pct_change(20, fill_method=None)
    raw["smallcap_breadth"] = (close["IWM"] / close["SPY"]).pct_change(20, fill_method=None)
    raw["junk_bond_demand"] = (close["HYG"] / close["LQD"]).pct_change(20, fill_method=None)
    raw["safe_haven_demand"] = close["SPY"].pct_change(20, fill_method=None) - close["TLT"].pct_change(20, fill_method=None)
    if put_call is not None:
        raw["put_call_options"] = -put_call.reindex(close.index).rolling(5, min_periods=3).mean()

    components = pd.DataFrame({name: rolling_percentile(raw[name]) * 100 for name in raw})
    available = components.notna().sum(axis=1)
    minimum = 7 if "put_call_options" in components else 6
    score = components.mean(axis=1).where(available >= minimum)
    regime = pd.cut(
        score,
        bins=[-np.inf, 20, 40, 60, 80, np.inf],
        labels=["extreme_fear", "fear", "neutral", "greed", "extreme_greed"],
        right=True,
    )
    out = components.copy()
    out["available_components"] = available
    out["sentiment_score"] = score
    out["sentiment_regime"] = regime.astype("string")
    return out


def confirmed_contrarian_state(close: pd.DataFrame, sentiment: pd.DataFrame) -> pd.DataFrame:
    """Create causal entry/exit flags; execution belongs to the next session."""
    score = sentiment["sentiment_score"]
    armed = score.rolling(10, min_periods=1).min() <= 20
    breadth_5d = (close["RSP"] / close["SPY"]).pct_change(5, fill_method=None)
    confirmation = armed & (score.diff() > 0) & (close["SPY"] > close["SPY"].rolling(5).mean()) & (breadth_5d > 0)
    stop = (score >= 55) | (close["SPY"] < close["SPY"].rolling(20).mean())
    active = []
    days = 0
    holding = False
    for dt in close.index:
        if holding:
            days += 1
            if bool(stop.at[dt]) or days >= 20:
                holding = False
                days = 0
        elif bool(confirmation.at[dt]):
            holding = True
            days = 0
        active.append(holding)
    return pd.DataFrame({"armed": armed, "confirmation": confirmation, "exit": stop, "active": active}, index=close.index)


def latest_payload(close: pd.DataFrame, sentiment: pd.DataFrame) -> dict:
    valid = sentiment.dropna(subset=["sentiment_score"])
    if valid.empty:
        raise ValueError("sentiment score is unavailable")
    dt = valid.index[-1]
    row = valid.loc[dt]
    state = confirmed_contrarian_state(close.reindex(sentiment.index), sentiment).loc[dt]
    component_names = [c for c in sentiment.columns if c not in {"available_components", "sentiment_score", "sentiment_regime"}]
    return {
        "as_of": str(dt.date()),
        "score": float(row.sentiment_score),
        "regime": str(row.sentiment_regime),
        "available_components": int(row.available_components),
        "components": {c: float(row[c]) for c in component_names if pd.notna(row[c])},
        "contrarian": {"armed": bool(state.armed), "confirmed": bool(state.confirmation), "active": bool(state.active)},
        "policy": "research-only; Fear Gate and unresolved-stop veto retain priority",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).resolve().parents[1] / "datasets" / "market_sentiment_close_2009_2026.csv")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "results")
    args = parser.parse_args()
    close = pd.read_csv(args.input, index_col=0, parse_dates=True).sort_index()
    sentiment = compute_sentiment(close)
    payload = latest_payload(close, sentiment)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "market_sentiment_latest.json"
    md_path = args.output_dir / "market_sentiment_latest.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    component_rows = "\n".join(f"| {name} | {value:.1f} |" for name, value in payload["components"].items())
    md_path.write_text(f"""# Market Sentiment Oscillator

- As of: `{payload['as_of']}`
- Score: `{payload['score']:.1f}`
- Regime: `{payload['regime']}`
- Contrarian armed / confirmed / active: `{payload['contrarian']['armed']}` / `{payload['contrarian']['confirmed']}` / `{payload['contrarian']['active']}`
- Policy: {payload['policy']}

| Component | Greed percentile |
| --- | ---: |
{component_rows}
""", encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), **payload}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
