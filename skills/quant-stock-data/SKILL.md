---
name: quant-stock-data
description: Use when working on quant strategy or stock-market data acquisition that needs Tencent Smartbox fuzzy search, Tencent real-time quotes, Yahoo U.S. quote fallback, Sina last-resort fallback quotes, historical daily K-line data, minute data, symbol normalization, GBK decoding, or resilient CN/HK/US quote fetching in JS/TS/Python.
metadata:
  short-description: Tencent/Yahoo/Sina resilient stock data source guide
---

# Quant Stock Data

Use this skill when the user discusses quant-strategy data sources, stock quote fetching, fuzzy stock search, Tencent/Yahoo/Sina quote resilience, or cross-market symbol normalization.

## Workflow

1. Normalize all user symbols before requesting quotes.
2. Prefer Tencent quote endpoints for real-time data.
3. For U.S. tickers, fall back to Yahoo Finance chart data before Sina when Tencent fails or returns unusable data.
4. Use Sina only as the last-resort fallback because some local proxy paths reject Sina with `connect EACCES`.
5. Decode all Tencent/Sina text responses as GBK.
6. For browser JS, do not rely on setting `Referer`; browsers forbid scripts from setting that header. Use Tencent as browser-first, or call Sina through a backend/proxy.
7. Preserve the data-source field in outputs so strategy analysis can trace where a quote came from.

## References

- Read `references/resilient-stock-api.md` for endpoint details, parsing fields, caveats, and usage examples.
- Reuse `scripts/stock_service.js` for JS/TS frontend or Node-side quote/search logic.
- Reuse `scripts/resilient_stock_client.py` for Python backend or scheduled fetching logic. On Windows, run it with a real Python interpreter such as the Codex bundled Python, not the Microsoft Store `python.exe` stub.

## Data Policy Notes

- Treat these endpoints as public web data sources with no formal SLA.
- Add timeout, retry, and source logging before using them in production tasks.
- Keep strategy decisions separate from raw data fetching; data adapters should return normalized quote objects only.
