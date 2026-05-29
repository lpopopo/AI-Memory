import requests


class ResilientStockClient:
    """Tencent-first, Sina-fallback stock quote client."""

    def __init__(self, timeout=3):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_quotes(self, symbols):
        try:
            return self._fetch_from_tencent(symbols)
        except Exception as primary_err:
            print(f"[警告] 腾讯行情获取失败: {primary_err}。正在自动切换至新浪兜底...")
            try:
                return self._fetch_from_sina(symbols)
            except Exception as secondary_err:
                print(f"[致命] 双行情源均发生故障: {secondary_err}")
                return []

    def _fetch_from_tencent(self, symbols):
        query_str = ",".join(symbols).lower()
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
                    "symbol": fields[2],
                    "name": fields[1],
                    "price": float(fields[3]) if fields[3] else 0.0,
                    "yesterday_close": float(fields[4]) if fields[4] else 0.0,
                    "open": float(fields[5]) if fields[5] else 0.0,
                    "high": float(fields[33]) if fields[33] else 0.0,
                    "low": float(fields[34]) if fields[34] else 0.0,
                    "volume": int(fields[6]) if fields[6] else 0,
                    "change_percent": float(fields[32]) if fields[32] else 0.0,
                    "source": "Tencent",
                }
            )
        return results

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
        return results
