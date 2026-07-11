#!/usr/bin/env python3
"""Best-effort Yahoo backfill for PIT missing membership symbols.

Delisted/acquired names often fail. Successful series are written to a
supplemental panel and later merged by build_v9_pit_universe.py.
This does NOT reconstruct CRSP delisting returns.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
PIT = ROOT / "datasets" / "data_point_in_time"
MISSING = PIT / "missing_symbols.json"
OUT = PIT / "price_backfill_adjusted_close.csv"
REPORT = PIT / "price_backfill_report.json"


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def chunked(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Optional cap for smoke tests")
    parser.add_argument("--batch-size", type=int, default=40)
    parser.add_argument("--start", default="2006-01-01")
    parser.add_argument("--end", default="2025-12-31")
    args = parser.parse_args()

    missing = json.loads(MISSING.read_text(encoding="utf-8"))["symbols"]
    if args.limit > 0:
        missing = missing[: args.limit]

    series_map: dict[str, pd.Series] = {}
    ok: list[str] = []
    empty: list[str] = []
    errors: dict[str, str] = {}
    batches = chunked(missing, max(1, args.batch_size))

    for bi, batch in enumerate(batches, 1):
        print(f"batch {bi}/{len(batches)} size={len(batch)}", flush=True)
        try:
            data = yf.download(
                batch,
                start=args.start,
                end=args.end,
                auto_adjust=True,
                progress=False,
                threads=True,
                group_by="ticker",
            )
        except Exception as exc:  # noqa: BLE001
            for symbol in batch:
                errors[symbol] = str(exc)
            print(f"  batch failed: {exc}", flush=True)
            continue

        if data is None or data.empty:
            empty.extend(batch)
            print(f"  empty batch", flush=True)
            continue

        for symbol in batch:
            try:
                if isinstance(data.columns, pd.MultiIndex):
                    if symbol not in data.columns.get_level_values(0):
                        empty.append(symbol)
                        continue
                    col = data[symbol]["Close"] if "Close" in data[symbol] else None
                else:
                    col = data["Close"] if len(batch) == 1 and "Close" in data else None
                if col is None:
                    empty.append(symbol)
                    continue
                if isinstance(col, pd.DataFrame):
                    col = col.iloc[:, 0]
                col = col.dropna()
                if col.empty:
                    empty.append(symbol)
                else:
                    series_map[symbol] = col
                    ok.append(symbol)
            except Exception as exc:  # noqa: BLE001
                errors[symbol] = str(exc)
        print(f"  cumulative ok={len(ok)} empty={len(empty)} errors={len(errors)}", flush=True)

    if series_map:
        frame = pd.DataFrame(series_map).sort_index()
        frame.index = pd.to_datetime(frame.index).tz_localize(None)
        frame = frame.loc[pd.Timestamp(args.start) : pd.Timestamp(args.end)]
        OUT.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(OUT, index_label="Date")
    elif OUT.exists():
        OUT.unlink()

    report = {
        "requested": len(missing),
        "downloaded": len(ok),
        "empty": len(empty),
        "errors": len(errors),
        "ok_symbols": ok,
        "empty_symbols": empty,
        "error_symbols": errors,
        "output": str(OUT.relative_to(ROOT)) if OUT.exists() else None,
        "output_sha256": file_digest(OUT),
        "note": "Yahoo best-effort only; not CRSP-grade; delisting returns still missing.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("requested", "downloaded", "empty", "errors", "output")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
