#!/usr/bin/env python3
"""Build a best-effort PIT membership panel and coverage manifest for V9 validation.

This does not claim CRSP-grade delisting completeness. Current-constituent price
caches are joined to membership history and coverage gaps are recorded explicitly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import index_constitution as ic
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets" / "data_point_in_time"
UNIVERSE_MASTER = ROOT / "datasets" / "data_universe" / "us_stock_universe_2000_2025.csv"
START = pd.Timestamp("2006-01-01")
END = pd.Timestamp("2025-12-31")


def normalize(symbol: str) -> str:
    return str(symbol).strip().upper().replace(".", "-")


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def membership_history() -> pd.DataFrame:
    frames = []
    for index_name in ("sp500", "nasdaq100"):
        frame = ic.history(index_name).copy()
        frame["index"] = index_name
        frame["symbol"] = frame["symbol"].map(normalize)
        frame["opt-in"] = pd.to_datetime(frame["opt-in"])
        frame["opt-out"] = pd.to_datetime(frame["opt-out"])
        frames.append(frame[["index", "symbol", "name", "opt-in", "opt-out"]])
    return pd.concat(frames, ignore_index=True).sort_values(["symbol", "opt-in", "index"])


def active_members(history: pd.DataFrame, date: pd.Timestamp) -> set[str]:
    mask = (history["opt-in"] <= date) & (history["opt-out"].isna() | (history["opt-out"] > date))
    return set(history.loc[mask, "symbol"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default=str(START.date()))
    parser.add_argument("--end", default=str(END.date()))
    args = parser.parse_args()
    start = pd.Timestamp(args.start)
    end = pd.Timestamp(args.end)

    OUT.mkdir(parents=True, exist_ok=True)
    history = membership_history()
    history_path = OUT / "membership_history.csv"
    history.to_csv(history_path, index=False)

    if not UNIVERSE_MASTER.exists():
        raise FileNotFoundError(f"missing universe master: {UNIVERSE_MASTER}")
    master = pd.read_csv(UNIVERSE_MASTER, index_col=0, parse_dates=True).sort_index().loc[start:end]
    master.columns = [normalize(c) for c in master.columns]

    backfill_path = OUT / "price_backfill_adjusted_close.csv"
    if backfill_path.exists():
        backfill = pd.read_csv(backfill_path, index_col=0, parse_dates=True).sort_index().loc[start:end]
        backfill.columns = [normalize(c) for c in backfill.columns]
        new_cols = [c for c in backfill.columns if c not in master.columns]
        overlap = [c for c in backfill.columns if c in master.columns]
        if new_cols:
            master = pd.concat([master, backfill[new_cols]], axis=1)
        for col in overlap:
            master[col] = master[col].combine_first(backfill[col])
        master = master.copy()

    universe = sorted(set(history["symbol"]))
    available_symbols = [s for s in universe if s in master.columns]
    missing_symbols = sorted(set(universe) - set(master.columns))
    close = master.loc[:, available_symbols].copy()
    close_path = OUT / "adjusted_close.csv"
    close.to_csv(close_path, index_label="Date")

    month_ends = close.groupby(close.index.to_period("M")).tail(1).index
    coverage_rows = []
    for date in month_ends:
        members = active_members(history, date)
        available = {s for s in members if s in close.columns and pd.notna(close.at[date, s])}
        seasoned = {
            s for s in available
            if close.loc[:date, s].notna().sum() >= 252
        }
        coverage_rows.append({
            "date": str(date.date()),
            "members": len(members),
            "price_available": len(available),
            "indicator_ready": len(seasoned),
            "price_coverage": (len(available) / len(members)) if members else 0.0,
            "indicator_coverage": (len(seasoned) / len(members)) if members else 0.0,
            "missing_count": len(members - available),
        })
    coverage = pd.DataFrame(coverage_rows)
    coverage_path = OUT / "coverage_by_month.csv"
    coverage.to_csv(coverage_path, index=False)

    missing_path = OUT / "missing_symbols.json"
    missing_payload = {
        "count": len(missing_symbols),
        "symbols": missing_symbols,
        "note": "Missing from current Yahoo/universe cache; delisting returns not reconstructed.",
    }
    missing_path.write_text(json.dumps(missing_payload, indent=2), encoding="utf-8")

    median_price_coverage = float(coverage["price_coverage"].median()) if not coverage.empty else 0.0
    price_sources = ["datasets/data_universe/us_stock_universe_2000_2025.csv current-cache join"]
    if backfill_path.exists():
        price_sources.append("datasets/data_point_in_time/price_backfill_adjusted_close.csv yahoo best-effort")
    manifest = {
        "status": "partial_pit_membership_with_cached_prices",
        "decision_grade": False,
        "membership_source": "index-constitution (Wikipedia-normalized)",
        "price_source": " + ".join(price_sources),
        "period": [str(start.date()), str(end.date())],
        "membership_symbols": len(universe),
        "price_symbols": len(available_symbols),
        "missing_symbols": len(missing_symbols),
        "median_month_end_price_coverage": median_price_coverage,
        "yahoo_backfill_applied": backfill_path.exists(),
        "files": {
            "membership_history.csv": {"sha256": file_digest(history_path), "rows": int(len(history))},
            "adjusted_close.csv": {"sha256": file_digest(close_path), "cols": int(close.shape[1]), "rows": int(close.shape[0])},
            "coverage_by_month.csv": {"sha256": file_digest(coverage_path), "rows": int(len(coverage))},
            "missing_symbols.json": {"sha256": file_digest(missing_path), "count": len(missing_symbols)},
        },
        "required_before_promotion": [
            "delisting returns for deleted/acquired names",
            "permanent security identifiers",
            "coverage of missing_symbols.json entries",
            ">=50 reliable PIT information events for Rule E statistics",
        ],
        "warning": "Not CRSP-complete. Do not promote WML/Rule E results on this panel alone.",
    }
    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
