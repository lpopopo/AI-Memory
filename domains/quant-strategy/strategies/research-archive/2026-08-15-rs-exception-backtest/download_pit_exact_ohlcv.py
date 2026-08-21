from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pandas as pd
import yfinance as yf


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
PIT_DIR = QUANT_ROOT / "strategies" / "v9-execution" / "datasets" / "data_point_in_time"
OUT_DIR = HERE / "datasets" / "pit_exact_ohlcv"

START = pd.Timestamp("2014-01-01")
END = pd.Timestamp("2025-12-31")
EVALUATION_START = pd.Timestamp("2015-01-01")
FIELDS = ("Open", "High", "Low", "Close", "Volume")
MARKET_SYMBOLS = ("SPY", "QQQ", "SMH", "^VIX", "^VIX3M")


def provider_symbol(symbol: str) -> str:
    return symbol.replace(".", "-")


def frozen_symbols(
    membership: pd.DataFrame, adjusted_close: pd.DataFrame
) -> list[str]:
    members = membership.copy()
    members["opt-in"] = pd.to_datetime(members["opt-in"])
    members["opt-out"] = pd.to_datetime(members["opt-out"], errors="coerce").fillna(
        pd.Timestamp.max.normalize()
    )
    overlaps = members.loc[
        (members["opt-in"] <= END) & (members["opt-out"] > EVALUATION_START), "symbol"
    ]
    available = set(adjusted_close.columns)
    selected = sorted(set(overlaps) & available)
    return selected


def extract_series(data: pd.DataFrame, field: str, ticker: str) -> pd.Series:
    if data.empty:
        return pd.Series(dtype=float)
    result: pd.Series | pd.DataFrame
    if isinstance(data.columns, pd.MultiIndex):
        if (field, ticker) in data.columns:
            result = data[(field, ticker)]
        elif (ticker, field) in data.columns:
            result = data[(ticker, field)]
        else:
            return pd.Series(dtype=float)
    elif field in data.columns:
        result = data[field]
    else:
        return pd.Series(dtype=float)
    if isinstance(result, pd.DataFrame):
        result = result.iloc[:, 0]
    result = pd.to_numeric(result, errors="coerce")
    result.index = pd.to_datetime(result.index).tz_localize(None)
    return result.sort_index().loc[START:END].dropna()


def merge_download(
    panels: dict[str, pd.DataFrame],
    data: pd.DataFrame,
    symbols: list[str],
) -> set[str]:
    completed: set[str] = set()
    additions: dict[str, dict[str, pd.Series]] = {field: {} for field in FIELDS}
    for symbol in symbols:
        ticker = provider_symbol(symbol)
        pieces = {field: extract_series(data, field, ticker) for field in FIELDS}
        common = pieces["Close"].index
        for field in FIELDS:
            common = common.intersection(pieces[field].index)
        if len(common) < 30:
            continue
        for field in FIELDS:
            additions[field][symbol] = pieces[field].reindex(common)
        completed.add(symbol)
    for field in FIELDS:
        if not additions[field]:
            continue
        new_frame = pd.DataFrame(additions[field])
        if panels[field].empty:
            panels[field] = new_frame
        else:
            panels[field] = pd.concat([panels[field], new_frame], axis=1)
            panels[field] = panels[field].loc[:, ~panels[field].columns.duplicated(keep="last")]
    return completed


def download_chunk(symbols: list[str]) -> pd.DataFrame:
    tickers = [provider_symbol(symbol) for symbol in symbols]
    return yf.download(
        tickers,
        start=START.strftime("%Y-%m-%d"),
        end=(END + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        auto_adjust=True,
        actions=False,
        progress=False,
        group_by="column",
        threads=True,
        timeout=30,
    )


def atomic_csv(frame: pd.DataFrame, path: Path) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    frame.to_csv(temporary, index_label="Date")
    temporary.replace(path)


def atomic_json(payload: dict, path: Path) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


def load_existing() -> dict[str, pd.DataFrame]:
    panels: dict[str, pd.DataFrame] = {}
    for field in FIELDS:
        path = OUT_DIR / f"{field.lower()}.csv"
        if path.exists():
            panels[field] = pd.read_csv(path, index_col=0, parse_dates=True).sort_index()
        else:
            panels[field] = pd.DataFrame()
    return panels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk-size", type=int, default=32)
    parser.add_argument("--retry-pause", type=float, default=0.25)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    membership = pd.read_csv(PIT_DIR / "membership_history.csv")
    adjusted_close = pd.read_csv(PIT_DIR / "adjusted_close.csv", index_col=0, parse_dates=True)
    stock_symbols = frozen_symbols(membership, adjusted_close)
    all_symbols = stock_symbols + [symbol for symbol in MARKET_SYMBOLS if symbol not in stock_symbols]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    symbol_frame = pd.DataFrame(
        {
            "symbol": all_symbols,
            "role": ["stock" if symbol in stock_symbols else "market" for symbol in all_symbols],
            "provider_symbol": [provider_symbol(symbol) for symbol in all_symbols],
        }
    )
    symbol_frame.to_csv(OUT_DIR / "frozen_symbols.csv", index=False)

    panels = {field: pd.DataFrame() for field in FIELDS} if args.refresh else load_existing()
    already_complete = set.intersection(
        *(set(panels[field].columns) for field in FIELDS)
    ) if all(not panels[field].empty for field in FIELDS) else set()
    pending = [symbol for symbol in all_symbols if symbol not in already_complete]
    status: dict[str, dict[str, str | int | None]] = {
        symbol: {"status": "cached", "provider_symbol": provider_symbol(symbol)}
        for symbol in already_complete
    }

    for offset in range(0, len(pending), args.chunk_size):
        chunk = pending[offset : offset + args.chunk_size]
        try:
            data = download_chunk(chunk)
            completed = merge_download(panels, data, chunk)
        except Exception as error:
            completed = set()
            for symbol in chunk:
                status[symbol] = {
                    "status": "batch_error",
                    "provider_symbol": provider_symbol(symbol),
                    "error": str(error),
                }
        for symbol in chunk:
            if symbol in completed:
                count = int(panels["Close"][symbol].notna().sum())
                status[symbol] = {
                    "status": "downloaded",
                    "provider_symbol": provider_symbol(symbol),
                    "rows": count,
                }
            elif status.get(symbol, {}).get("status") != "batch_error":
                status[symbol] = {
                    "status": "missing_after_batch",
                    "provider_symbol": provider_symbol(symbol),
                }
        print(
            f"chunk {offset // args.chunk_size + 1}: "
            f"{len(completed)}/{len(chunk)} symbols with usable OHLCV"
        )

    failed = [
        symbol for symbol in pending if status.get(symbol, {}).get("status") != "downloaded"
    ]
    for number, symbol in enumerate(failed, start=1):
        try:
            data = download_chunk([symbol])
            completed = merge_download(panels, data, [symbol])
            if symbol in completed:
                status[symbol] = {
                    "status": "downloaded_individual_retry",
                    "provider_symbol": provider_symbol(symbol),
                    "rows": int(panels["Close"][symbol].notna().sum()),
                }
            else:
                status[symbol]["retry"] = "no_usable_ohlcv"
        except Exception as error:
            status[symbol]["retry_error"] = str(error)
        if number % 25 == 0:
            print(f"individual retries {number}/{len(failed)}")
        time.sleep(max(args.retry_pause, 0.0))

    common_symbols = sorted(
        set.intersection(*(set(panels[field].columns) for field in FIELDS))
    )
    market_missing = sorted(set(MARKET_SYMBOLS) - set(common_symbols))
    if market_missing:
        raise RuntimeError(f"required market OHLCV missing: {market_missing}")

    for field in FIELDS:
        frame = panels[field].loc[START:END, common_symbols].sort_index()
        atomic_csv(frame, OUT_DIR / f"{field.lower()}.csv")

    downloaded_stocks = sorted(set(stock_symbols) & set(common_symbols))
    manifest = {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "preregistration": "pit-exact-filter-preregistration.md",
        "start": str(START.date()),
        "end": str(END.date()),
        "adjustment": "Yahoo Finance auto_adjust=True; volume unadjusted",
        "frozen_stock_symbols": len(stock_symbols),
        "usable_stock_symbols": len(downloaded_stocks),
        "failed_stock_symbols": sorted(set(stock_symbols) - set(downloaded_stocks)),
        "market_symbols": list(MARKET_SYMBOLS),
        "symbol_status": status,
        "downloaded_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
    }
    atomic_json(manifest, OUT_DIR / "manifest.json")
    print(
        json.dumps(
            {
                "frozen_stock_symbols": len(stock_symbols),
                "usable_stock_symbols": len(downloaded_stocks),
                "failed_stock_symbols": len(stock_symbols) - len(downloaded_stocks),
                "output": str(OUT_DIR),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
