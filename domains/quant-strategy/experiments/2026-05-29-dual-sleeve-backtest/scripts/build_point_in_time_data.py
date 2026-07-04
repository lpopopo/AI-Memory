#!/usr/bin/env python3
"""Build a best-effort point-in-time S&P 500 + Nasdaq-100 research dataset.

Membership comes from the MIT-licensed ``index-constitution`` package. Prices
use the existing Yahoo-adjusted cache first and yfinance for historical members
not already cached. Coverage is explicitly measured because free Yahoo data does
not retain every acquired, bankrupt, renamed, or otherwise delisted security.
"""

from __future__ import annotations

import json
from pathlib import Path

import index_constitution as ic
import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets" / "data_point_in_time"
START = pd.Timestamp("2006-01-01")
END = pd.Timestamp("2025-12-31")


def normalize(symbol: str) -> str:
    return str(symbol).strip().upper().replace(".", "-")


def membership_history() -> pd.DataFrame:
    frames = []
    for index_name in ("sp500", "nasdaq100"):
        frame = ic.history(index_name).copy()
        frame["index"] = index_name
        frame["symbol"] = frame["symbol"].map(normalize)
        frame["opt-in"] = pd.to_datetime(frame["opt-in"])
        frame["opt-out"] = pd.to_datetime(frame["opt-out"])
        frames.append(frame[["index", "symbol", "name", "opt-in", "opt-out"]])
    return pd.concat(frames, ignore_index=True).sort_values(["symbol", "opt-in"])


def download_missing(symbols: list[str]) -> pd.DataFrame:
    pieces = []
    for start in range(0, len(symbols), 50):
        batch = symbols[start:start + 50]
        print(f"Yahoo batch {start+1}-{min(start+50, len(symbols))}/{len(symbols)}", flush=True)
        raw = yf.download(
            batch, start=START.strftime("%Y-%m-%d"), end=(END + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
            auto_adjust=True, progress=False, threads=True, group_by="column",
        )
        if raw.empty:
            continue
        if isinstance(raw.columns, pd.MultiIndex):
            if "Close" in raw.columns.get_level_values(0):
                close = raw["Close"]
            else:
                close = raw.xs("Close", axis=1, level=1)
        else:
            close = raw[["Close"]].rename(columns={"Close": batch[0]})
        close.columns = [normalize(c) for c in close.columns]
        pieces.append(close)
    if not pieces:
        return pd.DataFrame()
    return pd.concat(pieces, axis=1).loc[START:END]


def active_members(history: pd.DataFrame, date: pd.Timestamp) -> set[str]:
    mask = (history["opt-in"] <= date) & (history["opt-out"].isna() | (history["opt-out"] > date))
    return set(history.loc[mask, "symbol"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    history = membership_history()
    master_path = ROOT / "datasets" / "data_universe" / "us_stock_universe_2000_2025.csv"
    master = pd.read_csv(master_path, index_col=0, parse_dates=True).sort_index().loc[START:END]
    master.columns = [normalize(c) for c in master.columns]
    universe = sorted(set(history["symbol"]))
    cache_path = OUT / "adjusted_close.csv"
    cached = (pd.read_csv(cache_path, index_col=0, parse_dates=True).sort_index()
              if cache_path.exists() else pd.DataFrame(index=master.index))
    cached.columns = [normalize(c) for c in cached.columns]
    requested_missing = sorted(set(universe) - set(master.columns))
    missing_to_download = sorted(set(requested_missing) - set(cached.columns))
    newly_fetched = download_missing(missing_to_download)
    fetched = cached.join(newly_fetched, how="outer", rsuffix="_new")
    # SPY/master dates are the authoritative US trading calendar. This prevents
    # a partial Yahoo batch row from becoming a fake universe-wide month-end.
    close = master.join(fetched, how="left", rsuffix="_fetched").sort_index()
    # Coalesce rare duplicate columns defensively.
    close = close.T.groupby(level=0).first().T
    close = close.loc[:, [s for s in universe if s in close.columns]]

    month_ends = close.groupby(close.index.to_period("M")).tail(1).index
    coverage = []
    for date in month_ends:
        members = active_members(history, date)
        available = {s for s in members if s in close and pd.notna(close.at[date, s])}
        seasoned = {
            s for s in available
            if close.loc[:date, s].notna().sum() >= 252
        }
        coverage.append({
            "date": str(date.date()), "members": len(members),
            "price_available": len(available), "indicator_ready": len(seasoned),
            "price_coverage": len(available) / len(members) if members else 0,
            "indicator_coverage": len(seasoned) / len(members) if members else 0,
        })

    history.to_csv(OUT / "membership_history.csv", index=False)
    close.to_csv(OUT / "adjusted_close.csv", index_label="Date")
    metadata = {
        "membership_source": "index-constitution 0.6.1 (Wikipedia-normalized; MIT)",
        "price_source": "existing Yahoo cache + yfinance auto_adjust=True",
        "period": [str(START.date()), str(END.date())],
        "membership_symbols": len(universe), "existing_symbols": len(set(universe) & set(master.columns)),
        "requested_missing_symbols": len(requested_missing),
        "fetched_missing_with_any_data": int(sum(fetched[c].notna().any() for c in fetched if c not in master)) if not fetched.empty else 0,
        "price_symbols_with_any_data": int(sum(close[c].notna().any() for c in close)),
        "coverage_by_month": coverage,
        "limitations": [
            "Free Yahoo data omits many delisted/acquired/renamed securities.",
            "S&P membership source has only 457 members at 2006-01-03 and is incomplete early in the sample.",
            "A missing historical security cannot be ranked and therefore residual survivorship bias remains.",
        ],
    }
    (OUT / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in metadata.items() if k != "coverage_by_month"}, indent=2))
    print("coverage first/last", coverage[0], coverage[-1])


if __name__ == "__main__":
    main()
