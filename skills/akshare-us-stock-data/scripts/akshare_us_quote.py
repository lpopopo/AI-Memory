#!/usr/bin/env python
"""AkShare-first U.S. quote fetcher with Tencent fallback."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from typing import Any
from urllib.request import Request, urlopen


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_ticker(value: str) -> str:
    return re.sub(r"[^A-Z0-9.-]", "", value.strip().upper())


def parse_number(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "").replace("%", "")
    if text in {"", "-", "--", "None", "nan", "NaN"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def compact_error(prefix: str, exc: Exception, limit: int = 360) -> str:
    text = f"{prefix}: {type(exc).__name__}: {exc}"
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return text


def first_number(row: dict[str, Any], candidates: list[str]) -> float | None:
    for key in candidates:
        if key in row:
            value = parse_number(row.get(key))
            if value is not None:
                return value
    return None


def first_text(row: dict[str, Any], candidates: list[str]) -> str:
    for key in candidates:
        value = row.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def row_matches_ticker(row: dict[str, Any], ticker: str) -> bool:
    exact_columns = ["代码", "证券代码", "symbol", "Symbol", "ticker", "Ticker"]
    for key in exact_columns:
        if key in row and normalize_ticker(str(row[key])).endswith(ticker):
            return True

    token_pattern = re.compile(rf"(^|[^A-Z0-9]){re.escape(ticker)}($|[^A-Z0-9])")
    for value in row.values():
        text = normalize_ticker(str(value))
        if text == ticker or token_pattern.search(text):
            return True
    return False


def quote_from_akshare_row(ticker: str, row: dict[str, Any], observed_at: str) -> dict[str, Any]:
    price = first_number(row, ["最新价", "最新", "现价", "price", "Price", "收盘"])
    previous_close = first_number(row, ["昨收", "昨收价", "previous_close", "Previous Close"])
    change_percent = first_number(row, ["涨跌幅", "涨幅", "change_percent", "Change Percent"])
    return {
        "ticker": ticker,
        "name": first_text(row, ["名称", "股票名称", "name", "Name"]),
        "price": price,
        "previous_close": previous_close,
        "open": first_number(row, ["开盘", "开盘价", "open", "Open"]),
        "high": first_number(row, ["最高", "最高价", "high", "High"]),
        "low": first_number(row, ["最低", "最低价", "low", "Low"]),
        "change_percent": change_percent,
        "volume": first_number(row, ["成交量", "volume", "Volume"]),
        "source": "AkShare/Eastmoney stock_us_spot_em",
        "quality": "high-public-snapshot" if price is not None else "unavailable",
        "observed_at": observed_at,
        "errors": [],
    }


def fetch_akshare_quotes(tickers: list[str], observed_at: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors: list[str] = []
    quotes: dict[str, dict[str, Any]] = {}
    try:
        import akshare as ak  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        return {}, [compact_error("AkShare import failed", exc)]

    try:
        df = ak.stock_us_spot_em()
    except Exception as exc:
        return {}, [compact_error("AkShare stock_us_spot_em failed", exc)]

    try:
        rows = df.to_dict(orient="records")
    except Exception as exc:
        return {}, [compact_error("AkShare dataframe conversion failed", exc)]

    for ticker in tickers:
        for row in rows:
            if row_matches_ticker(row, ticker):
                quote = quote_from_akshare_row(ticker, row, observed_at)
                if quote["price"] is not None:
                    quotes[ticker] = quote
                else:
                    errors.append(f"AkShare matched {ticker} but price was empty")
                break
        if ticker not in quotes:
            errors.append(f"AkShare returned no matched row for {ticker}")
    return quotes, errors


def decode_gbk(raw: bytes) -> str:
    try:
        return raw.decode("gbk")
    except UnicodeDecodeError:
        return raw.decode("gb18030", errors="replace")


def fetch_tencent_quotes(tickers: list[str], observed_at: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if not tickers:
        return {}, []

    query = ",".join(f"us{ticker}" for ticker in tickers)
    url = f"https://qt.gtimg.cn/q={query}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=8) as response:
            text = decode_gbk(response.read())
    except Exception as exc:
        return {}, [compact_error("Tencent fallback failed", exc)]

    quotes: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for ticker in tickers:
        match = re.search(rf'v_us{re.escape(ticker)}="([^"]*)"', text, re.IGNORECASE)
        if not match:
            errors.append(f"Tencent returned no line for {ticker}")
            continue
        fields = match.group(1).split("~")
        if len(fields) < 35:
            errors.append(f"Tencent row for {ticker} had only {len(fields)} fields")
            continue
        price = parse_number(fields[3])
        quotes[ticker] = {
            "ticker": ticker,
            "name": fields[1],
            "price": price,
            "previous_close": parse_number(fields[4]),
            "open": parse_number(fields[5]),
            "high": parse_number(fields[33]),
            "low": parse_number(fields[34]),
            "change_percent": parse_number(fields[32]),
            "volume": parse_number(fields[6]),
            "source": "Tencent qt.gtimg.cn fallback",
            "quality": "medium-public-snapshot" if price is not None else "unavailable",
            "observed_at": observed_at,
            "errors": [],
        }
    return quotes, errors


def build_unavailable(ticker: str, observed_at: str, errors: list[str]) -> dict[str, Any]:
    return {
        "ticker": ticker,
        "name": "",
        "price": None,
        "previous_close": None,
        "open": None,
        "high": None,
        "low": None,
        "change_percent": None,
        "volume": None,
        "source": "",
        "quality": "unavailable",
        "observed_at": observed_at,
        "errors": errors,
    }


def fetch_yahoo_chart_quote(ticker: str, observed_at: str) -> tuple[dict[str, Any] | None, str | None]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=1m"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
            result = data.get("chart", {}).get("result", [None])[0]
            if not result:
                return None, f"Yahoo chart returned empty result for {ticker}"
            meta = result.get("meta", {})
            price = parse_number(meta.get("regularMarketPrice"))
            if price is None:
                # Try close price from indicators as fallback
                indicators = result.get("indicators", {})
                quote_list = indicators.get("quote", [{}])
                if quote_list:
                    closes = quote_list[0].get("close", [])
                    for val in reversed(closes):
                        price = parse_number(val)
                        if price is not None:
                            break
            if price is None:
                return None, f"Yahoo chart price was empty for {ticker}"

            previous_close = parse_number(meta.get("chartPreviousClose") or meta.get("previousClose"))
            change_percent = None
            if price is not None and previous_close is not None and previous_close > 0:
                change_percent = round((price - previous_close) / previous_close * 100, 4)

            open_val = parse_number(meta.get("regularMarketDayLow"))
            high_val = parse_number(meta.get("regularMarketDayHigh"))
            low_val = parse_number(meta.get("regularMarketDayLow"))
            volume_val = parse_number(meta.get("regularMarketVolume"))

            indicators = result.get("indicators", {})
            quote_list = indicators.get("quote", [{}])
            if quote_list:
                quote = quote_list[0]
                def get_last_num(lst):
                    if not lst:
                        return None
                    for v in reversed(lst):
                        n = parse_number(v)
                        if n is not None:
                            return n
                    return None
                open_val = get_last_num(quote.get("open")) or open_val
                high_val = get_last_num(quote.get("high")) or high_val
                low_val = get_last_num(quote.get("low")) or low_val
                volume_val = get_last_num(quote.get("volume")) or volume_val

            return {
                "ticker": ticker,
                "name": meta.get("shortName") or meta.get("longName") or ticker,
                "price": price,
                "previous_close": previous_close,
                "open": open_val,
                "high": high_val,
                "low": low_val,
                "change_percent": change_percent,
                "volume": volume_val,
                "source": "Yahoo Finance Chart (0-delay)",
                "quality": "high-public-snapshot",
                "observed_at": observed_at,
                "errors": [],
            }, None
    except Exception as exc:
        return None, compact_error(f"Yahoo chart failed for {ticker}", exc)


def fetch_yahoo_chart_quotes(tickers: list[str], observed_at: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    from concurrent.futures import ThreadPoolExecutor
    quotes: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    
    with ThreadPoolExecutor(max_workers=min(len(tickers), 10)) as executor:
        futures = {executor.submit(fetch_yahoo_chart_quote, ticker, observed_at): ticker for ticker in tickers}
        for future in futures:
            ticker = futures[future]
            try:
                quote, err = future.result()
                if quote:
                    quotes[ticker] = quote
                if err:
                    errors.append(err)
            except Exception as exc:
                errors.append(compact_error(f"Thread execution error for {ticker}", exc))
                
    return quotes, errors


def fetch_quotes(tickers: list[str], allow_fallback: bool) -> dict[str, Any]:
    observed_at = now_iso()
    normalized = [normalize_ticker(item) for item in tickers if normalize_ticker(item)]
    
    # 1. Primary: Yahoo Finance Chart (0-delay)
    yahoo_quotes, yahoo_errors = fetch_yahoo_chart_quotes(normalized, observed_at)
    
    # 2. Check what is missing after Yahoo
    missing = [ticker for ticker in normalized if ticker not in yahoo_quotes]
    
    ak_quotes: dict[str, dict[str, Any]] = {}
    ak_errors: list[str] = []
    if missing:
        ak_quotes, ak_errors = fetch_akshare_quotes(missing, observed_at)
        
    # 3. Check what is still missing after AkShare
    still_missing = [ticker for ticker in missing if ticker not in ak_quotes]
    
    fallback_quotes: dict[str, dict[str, Any]] = {}
    fallback_errors: list[str] = []
    if allow_fallback and still_missing:
        fallback_quotes, fallback_errors = fetch_tencent_quotes(still_missing, observed_at)
        
    results = []
    for ticker in normalized:
        all_errors = yahoo_errors + ak_errors + fallback_errors
        if ticker in yahoo_quotes:
            quote = yahoo_quotes[ticker]
            quote["errors"] = all_errors
            results.append(quote)
        elif ticker in ak_quotes:
            quote = ak_quotes[ticker]
            quote["errors"] = all_errors
            results.append(quote)
        elif ticker in fallback_quotes:
            quote = fallback_quotes[ticker]
            quote["errors"] = all_errors
            results.append(quote)
        else:
            results.append(build_unavailable(ticker, observed_at, all_errors))
            
    return {
        "observed_at": observed_at,
        "requested": normalized,
        "allow_fallback": allow_fallback,
        "results": results,
    }


def write_csv(path: str, rows: list[dict[str, Any]]) -> None:
    fields = [
        "ticker",
        "name",
        "price",
        "previous_close",
        "open",
        "high",
        "low",
        "change_percent",
        "volume",
        "source",
        "quality",
        "observed_at",
        "errors",
    ]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            item = dict(row)
            item["errors"] = " | ".join(item.get("errors") or [])
            writer.writerow(item)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch U.S. stock quotes through AkShare with Tencent fallback.")
    parser.add_argument("tickers", nargs="+", help="U.S. tickers, e.g. NVDA AMD MRVL SPY")
    parser.add_argument("--json", dest="json_path", help="Optional JSON output path")
    parser.add_argument("--csv", dest="csv_path", help="Optional CSV output path")
    parser.add_argument("--no-fallback", action="store_true", help="Disable Tencent fallback")
    args = parser.parse_args()

    payload = fetch_quotes(args.tickers, allow_fallback=not args.no_fallback)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)

    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    if args.csv_path:
        write_csv(args.csv_path, payload["results"])

    return 0 if any(item["quality"] != "unavailable" for item in payload["results"]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
