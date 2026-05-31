---
name: quant-stock-data
description: Use when working on 量化策略 or stock-market data acquisition that needs Tencent Smartbox fuzzy search, Tencent real-time quotes, Sina fallback quotes, historical daily K-line data, minute data, symbol normalization, GBK decoding, or resilient CN/HK/US quote fetching in JS/TS/Python.
metadata:
  short-description: Tencent/Sina resilient stock data source guide
---

# Quant Stock Data

Use this skill when the user discusses 量化策略 data sources, stock quote fetching, fuzzy stock search, Tencent/Sina quote resilience, or cross-market symbol normalization.

## Workflow

1. Normalize all user symbols before requesting quotes.
2. Prefer Tencent quote endpoints for real-time data.
3. Fall back to Sina quotes only when Tencent fails or returns unusable data.
4. Decode all Tencent/Sina text responses as GBK.
5. For browser JS, do not rely on setting `Referer`; browsers forbid scripts from setting that header. Use Tencent as browser-first, or call Sina through a backend/proxy.
6. Preserve the data-source field in outputs so strategy analysis can trace where a quote came from.

## References

- Read `references/resilient-stock-api.md` for endpoint details, parsing fields, caveats, and usage examples.
- Reuse `scripts/stock_service.js` for JS/TS frontend or Node-side quote/search logic.
- Reuse `scripts/resilient_stock_client.py` for Python backend or scheduled fetching logic.

## Data Policy Notes

- Treat these endpoints as public web data sources with no formal SLA.
- Add timeout, retry, and source logging before using them in production tasks.
- Keep strategy decisions separate from raw data fetching; data adapters should return normalized quote objects only.
