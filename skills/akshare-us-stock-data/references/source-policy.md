# AkShare U.S. Quote Source Policy

## Purpose

This skill is for AI-Memory strategy monitoring, not broker execution. It should produce traceable public quote snapshots with explicit source and quality labels.

## Primary Path

Use AkShare first:

- Import `akshare`.
- Prefer `ak.stock_us_spot_em()` for U.S. stock spot snapshots.
- Match requested tickers against likely code columns such as `代码`, `symbol`, `代码简称`, or any column whose values contain exact ticker-like tokens.
- Accept a row only when a numeric latest price can be parsed.

Known fragility:

- AkShare wraps public upstream sites. Interface names, field names, network paths, and anti-bot behavior can change.
- The Eastmoney route may return proxy errors, remote disconnects, timeouts, or empty tables.
- A successful AkShare import is not evidence that the quote fetch succeeded.

## Fallback Path

Use Tencent when AkShare fails or misses specific tickers:

- Endpoint: `https://qt.gtimg.cn/q=usNVDA,usAMD`
- Decode as GBK.
- Parse `~`-separated payloads.
- Preserve the source as `Tencent`.

Tencent fallback quality is lower than a successful AkShare row because it is a separate public web endpoint with no formal SLA, but it is often faster for individual U.S. tickers.

## Required Output Fields

Every result should include:

- `ticker`
- `name`
- `price`
- `previous_close`
- `open`
- `high`
- `low`
- `change_percent`
- `volume`
- `source`
- `quality`
- `observed_at`
- `errors`

Downstream strategy notes must not quote prices without also preserving `source` and `quality`.

## Recommended Decision Rules

- Use AkShare rows as normal public quote snapshots.
- Use Tencent fallback rows for intraday monitoring and watchlist triage.
- Use official close data or broker/user-confirmed data before recording real trade execution.
- If all public routes fail, write an explicit data gap instead of carrying forward stale prices.
