---
name: akshare-us-stock-data
description: AkShare-first resilient U.S. stock quote fetching for AI-Memory quant strategy work. Use when Codex needs current or recent U.S. individual-stock or ETF quotes, ticker snapshots, source-quality labels, AkShare diagnostics, or a fallback quote path for symbols such as NVDA, AMD, MRVL, AAPL, SPY, or QQQ.
---

# AkShare US Stock Data

## Workflow

1. Normalize tickers to uppercase U.S. symbols before fetching.
2. Run `scripts/akshare_us_quote.py` for repeatable quote checks.
3. Treat AkShare as the preferred source, but never as the only required source.
4. If AkShare returns no row, times out, or raises an upstream error, use the built-in Tencent quote fallback.
5. Preserve `source`, `quality`, `observed_at`, and `errors` in every downstream note or strategy file.
6. Do not treat public quote snapshots as broker execution prices. For real orders, require broker or user confirmation.

## Quick Commands

Fetch several quotes and print JSON:

```bash
python scripts/akshare_us_quote.py NVDA AMD MRVL SPY QQQ
```

Write JSON and CSV artifacts:

```bash
python scripts/akshare_us_quote.py NVDA AMD MRVL --json latest-us-quotes.json --csv latest-us-quotes.csv
```

Require AkShare only, with no fallback:

```bash
python scripts/akshare_us_quote.py NVDA AMD --no-fallback
```

## Source Policy

- `AkShare/Eastmoney`: preferred public snapshot when `stock_us_spot_em` succeeds and rows match requested tickers.
- `Tencent`: fallback public snapshot for individual U.S. tickers; useful when AkShare's upstream Eastmoney route is slow, blocked, or empty.
- `quality=high-public-snapshot`: AkShare row matched and numeric price parsed.
- `quality=medium-public-snapshot`: Tencent fallback matched and numeric price parsed.
- `quality=unavailable`: no source returned a usable numeric quote.

For detailed field mapping and failure handling, read `references/source-policy.md`.
