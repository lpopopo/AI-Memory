import re

import requests


class ResilientStockClient:
    """Tencent-first quote client with Yahoo and Sina fallbacks."""

    def __init__(self, timeout=8):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_quotes(self, symbols):
        norm_symbols = [self.normalize_symbol(symbol) for symbol in symbols]
        errors = []

        try:
            results = self._fetch_from_tencent(norm_symbols)
            if results:
                return results
            errors.append("Tencent returned no usable rows")
        except Exception as err:
            errors.append(f"Tencent failed: {self._compact_error(err)}")

        us_symbols = [symbol for symbol in norm_symbols if self._is_us_symbol(symbol)]
        if us_symbols:
            try:
                results = self._fetch_from_yahoo(us_symbols)
                if results:
                    return results
                errors.append("Yahoo returned no usable rows")
            except Exception as err:
                errors.append(f"Yahoo failed: {self._compact_error(err)}")

        try:
            results = self._fetch_from_sina(norm_symbols)
            if results:
                return results
            errors.append("Sina returned no usable rows")
        except Exception as err:
            errors.append(f"Sina failed: {self._compact_error(err)}")

        print("[Fatal] quote sources failed: " + " | ".join(errors))
        return []

    @staticmethod
    def normalize_symbol(symbol):
        clean = re.sub(r"[\s.]", "", str(symbol).strip())
        lower = clean.lower()
        if lower.startswith(("sh", "sz", "hk", "us")):
            if lower.startswith("us"):
                return f"us{clean[2:].upper()}"
            return lower
        if re.fullmatch(r"\d{6}", lower):
            return f"sh{lower}" if lower.startswith(("6", "9")) else f"sz{lower}"
        if re.fullmatch(r"\d{1,5}", lower):
            return f"hk{lower.zfill(5)}"
        if re.fullmatch(r"[A-Za-z]+", clean):
            return f"us{clean.upper()}"
        return lower

    @staticmethod
    def _is_us_symbol(symbol):
        return bool(re.fullmatch(r"us[A-Za-z.]+", symbol))

    @staticmethod
    def _to_yahoo_symbol(symbol):
        return symbol[2:].upper() if symbol.lower().startswith("us") else symbol.upper()

    @staticmethod
    def _compact_error(err):
        return re.sub(r"\s+", " ", str(err)).strip()[:240]

    @staticmethod
    def _last_number(values):
        if not isinstance(values, list):
            return 0.0
        for value in reversed(values):
            try:
                if value is not None:
                    return float(value)
            except (TypeError, ValueError):
                continue
        return 0.0

    def _fetch_from_tencent(self, symbols):
        query_str = ",".join(symbols)
        url = f"https://qt.gtimg.cn/q={query_str}"
        resp = requests.get(url, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        resp.encoding = "gbk"

        results = []
        for line in resp.text.strip().split("\n"):
            if '="' not in line:
                continue
            start = line.find('="') + 2
            end = line.rfind('"')
            fields = line[start:end].split("~")
            if len(fields) < 35:
                continue

            results.append(
                {
                    "symbol": fields[2] or "",
                    "name": fields[1],
                    "price": float(fields[3]) if fields[3] else 0.0,
                    "yesterday_close": float(fields[4]) if fields[4] else 0.0,
                    "open": float(fields[5]) if fields[5] else 0.0,
                    "high": float(fields[33]) if fields[33] else 0.0,
                    "low": float(fields[34]) if fields[34] else 0.0,
                    "volume": int(float(fields[6])) if fields[6] else 0,
                    "change_percent": float(fields[32]) if fields[32] else 0.0,
                    "source": "Tencent",
                }
            )
        return [item for item in results if item["price"] > 0]

    def _fetch_from_yahoo(self, symbols):
        results = []
        for symbol in symbols:
            try:
                ticker = self._to_yahoo_symbol(symbol)
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                params = {"range": "1d", "interval": "1m"}
                resp = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                item = ((data.get("chart") or {}).get("result") or [None])[0]
                if not item:
                    continue

                meta = item.get("meta") or {}
                quote = (((item.get("indicators") or {}).get("quote") or [{}])[0]) or {}
                price = float(meta.get("regularMarketPrice") or self._last_number(quote.get("close")))
                previous_close = float(meta.get("previousClose") or meta.get("chartPreviousClose") or 0.0)
                change_percent = ((price - previous_close) / previous_close * 100) if previous_close else 0.0

                results.append(
                    {
                        "symbol": f"US{ticker}",
                        "name": meta.get("shortName") or ticker,
                        "price": price,
                        "yesterday_close": previous_close,
                        "open": self._last_number(quote.get("open")),
                        "high": self._last_number(quote.get("high")),
                        "low": self._last_number(quote.get("low")),
                        "volume": int(self._last_number(quote.get("volume"))),
                        "change_percent": change_percent,
                        "source": "Yahoo Chart",
                    }
                )
            except Exception as err:
                print(f"[Warn] Yahoo failed for {symbol}: {self._compact_error(err)}")
        return [item for item in results if item["price"] > 0]

    def _fetch_from_sina(self, symbols):
        query_str = ",".join(symbols).lower()
        url = f"https://hq.sinajs.cn/list={query_str}"
        sina_headers = self.headers.copy()
        sina_headers["Referer"] = "https://finance.sina.com.cn/"

        resp = requests.get(url, headers=sina_headers, timeout=self.timeout)
        resp.raise_for_status()
        resp.encoding = "gbk"

        results = []
        for index, line in enumerate(resp.text.strip().split("\n")):
            if '="' not in line:
                continue
            start = line.find('="') + 2
            end = line.rfind('"')
            fields = line[start:end].split(",")
            if len(fields) < 10:
                continue

            price = float(fields[3]) if fields[3] else 0.0
            yesterday_close = float(fields[2]) if fields[2] else 0.0
            change_percent = ((price - yesterday_close) / yesterday_close * 100) if yesterday_close > 0 else 0.0

            results.append(
                {
                    "symbol": symbols[index].upper() if index < len(symbols) else "",
                    "name": fields[0],
                    "price": price,
                    "yesterday_close": yesterday_close,
                    "open": float(fields[1]) if fields[1] else 0.0,
                    "high": float(fields[4]) if fields[4] else 0.0,
                    "low": float(fields[5]) if fields[5] else 0.0,
                    "volume": int(int(fields[8]) / 100) if fields[8] else 0,
                    "change_percent": change_percent,
                    "source": "Sina",
                }
            )
        return [item for item in results if item["price"] > 0]
