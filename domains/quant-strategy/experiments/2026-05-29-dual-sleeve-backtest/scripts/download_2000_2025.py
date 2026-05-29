#!/usr/bin/env python3
import json
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

START_LONG = "2000-01-01"
END_LONG = "2025-12-31"

BENCHMARKS = ["SPY", "QQQ"]
VALUE_ETFS = ["VTV", "IWD", "SCHD"]
TACTICAL_ETFS = [
    "XLK", "XLC", "XLY", "XLI", "XLF", "XLV", "XLE", "XLB", "XLU", "XLRE", "XLP", "SMH", "IBB", "ITA"
]
SECTOR_LEADERS = {
    "XLK": ["AAPL", "MSFT", "AVGO"],
    "SMH": ["NVDA", "TSM", "AMD"],
    "XLC": ["META", "GOOGL", "NFLX"],
    "XLY": ["AMZN", "TSLA", "HD"],
    "XLF": ["JPM", "BAC", "MS"],
    "XLV": ["LLY", "UNH", "ABBV"],
    "XLI": ["GE", "CAT", "HON"],
    "XLE": ["XOM", "CVX", "COP"],
    "XLP": ["PG", "COST", "KO"],
    "XLB": ["LIN", "SHW", "APD"],
    "XLU": ["NEE", "SO", "DUK"],
    "XLRE": ["PLD", "AMT", "EQIX"],
    "IBB": ["REGN", "VRTX", "AMGN"],
    "ITA": ["RTX", "LMT", "GD"],
}
ALL_LEADER_STOCKS = sorted(set(s for leaders in SECTOR_LEADERS.values() for s in leaders))
ALL_SYMBOLS = sorted(set(BENCHMARKS + VALUE_ETFS + TACTICAL_ETFS + ALL_LEADER_STOCKS))

ROOT = Path(__file__).resolve().parents[1]
DATA_LONG_DIR = ROOT / "data_long"


def fetch_symbol_close_long(symbol):
    path = DATA_LONG_DIR / f"{symbol}_adjusted_close.csv"
    if path.exists():
        cached = pd.read_csv(path, index_col=0, parse_dates=True)
        if symbol in cached.columns and not cached[symbol].dropna().empty:
            print(f"Loaded {symbol} from long-term cache.")
            return cached[symbol]

    print(f"Downloading {symbol} from yfinance for {START_LONG} to {END_LONG}...")
    last_error = None
    for attempt in range(3):
        try:
            data = yf.download(
                tickers=symbol,
                start=START_LONG,
                end=END_LONG,
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
            close.to_frame().to_csv(path)
            return close
        except Exception as err:
            last_error = err
            print(f"Attempt {attempt+1} failed for {symbol}: {err}")
            time.sleep(2.0 * (attempt + 1))

    raise RuntimeError(str(last_error))


def main():
    DATA_LONG_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = DATA_LONG_DIR / "yfinance_adjusted_close_2000_2025.csv"
    
    series = {}
    failures = {}
    
    print(f"Starting long-term download for {len(ALL_SYMBOLS)} symbols...")
    for symbol in ALL_SYMBOLS:
        try:
            series[symbol] = fetch_symbol_close_long(symbol)
        except Exception as err:
            failures[symbol] = str(err)
            print(f"CRITICAL: Failed to download {symbol}: {err}")
            
    if failures:
        (DATA_LONG_DIR / "download_failures_2000_2025.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
        
    if "SPY" not in series or "QQQ" not in series:
        print("WARNING: Essential benchmark indexes failed to download!")
        
    combined = pd.concat(series.values(), axis=1, keys=series.keys())
    combined = combined.sort_index()
    combined.index = pd.to_datetime(combined.index).tz_localize(None)
    combined.to_csv(cache_path)
    
    print(f"\nLong-term data download complete! Saved to {cache_path}")
    print(f"Total Trading Days: {len(combined)}")
    if failures:
        print(f"Failures recorded for: {list(failures.keys())}")


if __name__ == "__main__":
    main()
