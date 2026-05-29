#!/usr/bin/env python3
import json
import re
import time
import urllib.request
from pathlib import Path

import pandas as pd
import yfinance as yf

START_LONG = "2000-01-01"
END_LONG = "2025-12-31"

ROOT = Path(__file__).resolve().parents[1]
DATA_UNIVERSE_DIR = ROOT / "data_universe"


# Robust Fallback tickers list in case scraping Wikipedia fails
FALLBACK_TICKERS = [
    # Mega-caps & Tech Leaders
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "BRK-B", "LLY", "AVGO",
    "JPM", "TSLA", "UNH", "XOM", "V", "MA", "PG", "COST", "HD", "JNJ",
    "ABBV", "MRK", "BAC", "NFLX", "AMD", "ORCL", "ADBE", "CRM", "CVX", "WMT",
    # Financials
    "MS", "GS", "SCHW", "AXP", "C", "BLK", "CB", "SPGI", "MMC", "WFC",
    # Technology / Semiconductors
    "ASML", "TSM", "QCOM", "TXN", "INTC", "AMAT", "MU", "LRCX", "ADI", "KLAC",
    # Communications / Discretionary
    "DIS", "CMCSA", "TMUS", "VZ", "T", "CHTR", "NKE", "SBUX", "TJX", "LOW",
    # Industrials & Defense
    "GE", "CAT", "HON", "UNP", "UPS", "LMT", "RTX", "BA", "GD", "NOC",
    # Healthcare
    "ABT", "ISRG", "PFE", "TMO", "MDT", "SYK", "REGN", "VRTX", "AMGN", "GILD",
    # Consumer Staples / Energy / Materials
    "PEP", "KO", "PM", "EL", "CL", "MO", "SLB", "COP", "EOG", "PXD",
    "LIN", "SHW", "APD", "FCX", "NEM", "DD", "DOW", "ALB", "FMC", "EMN",
    # Real Estate & Utilities
    "PLD", "AMT", "CCI", "EQIX", "SPG", "NEE", "SO", "DUK", "D", "AEP"
]


def scrape_sp500_tickers():
    print("Scraping S&P 500 constituents from Wikipedia...")
    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        table_match = re.search(r'<table[^>]*id="constituents"[^>]*>(.*?)</table>', html, re.DOTALL)
        if not table_match:
            table_match = re.search(r'<table class="wikitable sortable"[^>]*>(.*?)</table>', html, re.DOTALL)
            
        table_html = table_match.group(1) if table_match else html
        
        tickers = []
        rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        for row in rows[1:]:
            cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if cols:
                first_col = cols[0]
                ticker_match = re.search(r'<a[^>]*>(.*?)</a>', first_col)
                ticker = ticker_match.group(1) if ticker_match else first_col
                ticker = ticker.strip().replace('\n', '').replace('\r', '')
                ticker = ticker.replace('.', '-')
                if ticker and (ticker.isalpha() or '-' in ticker):
                    tickers.append(ticker)
        print(f"Scraped {len(tickers)} S&P 500 symbols.")
        return tickers
    except Exception as err:
        print(f"Failed to scrape S&P 500: {err}. Using fallback.")
        return []


def scrape_nasdaq100_tickers():
    print("Scraping Nasdaq 100 constituents from Wikipedia...")
    try:
        url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        table_match = re.search(r'<table[^>]*id="constituents"[^>]*>(.*?)</table>', html, re.DOTALL)
        if not table_match:
            tables = re.findall(r'<table class="wikitable sortable"[^>]*>(.*?)</table>', html, re.DOTALL)
            table_html = tables[0] if tables else html
        else:
            table_html = table_match.group(1)
            
        tickers = []
        rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        for row in rows[1:]:
            cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cols) >= 2:
                ticker = ""
                for col in cols[:2]:
                    col_cleaned = re.sub(r'<[^>]*>', '', col).strip()
                    if col_cleaned.isupper() and col_cleaned.isalpha() and len(col_cleaned) <= 5:
                        ticker = col_cleaned
                        break
                if not ticker:
                    first_col_clean = re.sub(r'<[^>]*>', '', cols[0]).strip()
                    second_col_clean = re.sub(r'<[^>]*>', '', cols[1]).strip()
                    if len(second_col_clean) <= 5 and second_col_clean.isupper():
                        ticker = second_col_clean
                    elif len(first_col_clean) <= 5 and first_col_clean.isupper():
                        ticker = first_col_clean
                ticker = ticker.replace('.', '-')
                if ticker:
                    tickers.append(ticker)
        print(f"Scraped {len(tickers)} Nasdaq 100 symbols.")
        return tickers
    except Exception as err:
        print(f"Failed to scrape Nasdaq 100: {err}. Using fallback.")
        return []


def download_symbol_close(symbol):
    path = DATA_UNIVERSE_DIR / f"{symbol}_adjusted_close.csv"
    if path.exists():
        try:
            cached = pd.read_csv(path, index_col=0, parse_dates=True)
            if symbol in cached.columns and not cached[symbol].dropna().empty:
                return cached[symbol]
        except Exception:
            pass

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
            time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(str(last_error))


def main():
    DATA_UNIVERSE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = DATA_UNIVERSE_DIR / "us_stock_universe_2000_2025.csv"
    
    # 1. Scrape tickers
    sp500 = scrape_sp500_tickers()
    nasdaq100 = scrape_nasdaq100_tickers()
    
    # 2. Combine and union tickers
    tickers = sorted(set(sp500 + nasdaq100))
    if len(tickers) < 200:
        print("Scraped list too small or failed. Using fallback full high-quality list.")
        tickers = sorted(set(FALLBACK_TICKERS))
        
    print(f"\nFinal Stock Universe Symbol Count: {len(tickers)} stocks.")
    
    # 3. Add benchmark indexes SPY and QQQ
    all_symbols = sorted(set(["SPY", "QQQ"] + tickers))
    
    # 4. Ingest/download data
    series = {}
    failures = {}
    
    total = len(all_symbols)
    print(f"\nStarting Ingestion Pipeline for {total} symbols...")
    
    for idx, symbol in enumerate(all_symbols, start=1):
        try:
            series[symbol] = download_symbol_close(symbol)
            if idx % 10 == 0 or idx == total:
                print(f"[{idx}/{total}] Downloaded {symbol} successfully.")
            # Tiny sleep to avoid Yahoo rate-limits
            time.sleep(0.05)
        except Exception as err:
            failures[symbol] = str(err)
            print(f"[{idx}/{total}] Failed to download {symbol}: {err}")
            
    if failures:
        (DATA_UNIVERSE_DIR / "download_failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
        
    # 5. Consolidate into a single master index-aligned CSV
    print("\nConsolidating dataset columns...")
    combined = pd.concat(series.values(), axis=1, keys=series.keys())
    combined = combined.sort_index()
    combined.index = pd.to_datetime(combined.index).tz_localize(None)
    combined.to_csv(cache_path)
    
    print(f"\nIngestion Pipeline Complete! Master dataset saved to: {cache_path}")
    print(f"Total Trading Days: {len(combined)}")
    print(f"Total Cached Stocks: {len(combined.columns)}")
    if failures:
        print(f"Total Failures: {len(failures)} (Details in data_universe/download_failures.json)")


if __name__ == "__main__":
    main()
