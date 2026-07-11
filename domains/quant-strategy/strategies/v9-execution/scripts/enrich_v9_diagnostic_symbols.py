#!/usr/bin/env python3
"""Merge Fear Gate diagnostic ETFs into datasets/data_v9 without a full re-download."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets" / "data_v9"
SYMBOLS = ("SMH", "IWM", "RSP", "HYG", "LQD")
FIELDS = ("Open", "High", "Low", "Close", "Volume")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    panels = {
        field.lower(): pd.read_csv(OUT / f"{field.lower()}.csv", index_col=0, parse_dates=True).sort_index()
        for field in FIELDS
    }
    downloaded = []
    for symbol in SYMBOLS:
        data = yf.download(symbol, start="2024-01-01", end=None, auto_adjust=True, progress=False)
        if data.empty:
            print(f"Skipping {symbol}: empty")
            continue
        for field in FIELDS:
            col = data[field]
            if isinstance(col, pd.DataFrame):
                col = col.iloc[:, 0]
            panels[field.lower()][symbol] = col
        downloaded.append(symbol)
        print(f"Merged {symbol}")

    for name, frame in panels.items():
        frame.index = pd.to_datetime(frame.index).tz_localize(None)
        frame.sort_index(inplace=True)
        frame.to_csv(OUT / f"{name}.csv", index_label="Date")

    meta_path = OUT / "metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta["symbols"] = sorted(panels["close"].columns)
    meta["diagnostic_symbols"] = list(SYMBOLS)
    meta["diagnostic_downloaded"] = downloaded
    meta["downloaded_at_utc"] = pd.Timestamp.now(tz="UTC").isoformat()
    meta["last_date"] = str(panels["close"].index[-1].date())
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"merged": downloaded, "last_date": meta["last_date"]}, indent=2))


if __name__ == "__main__":
    main()
