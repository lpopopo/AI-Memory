# 2026-06-11 Entry Price Discipline Update

Purpose: record the strategy repair after reviewing the real MRVL USD 252 starter order.

## Issue

The MRVL USD 252 buy level was a starter-test price based on a discount from the current quote and the USD 245 risk-review line. It was not explicitly derived from moving averages, VWAP, prior support, or ATR.

## Rule Added

Future buy-limit recommendations must state their technical price basis:

- 5 / 10 / 20 / 50-day moving average.
- Intraday VWAP.
- Prior low / support.
- Gap level.
- ATR-derived pullback range.
- Explicit risk-line offset.

If the limit is merely a small-account starter-test price, it must be labeled that way and not described as a support-based entry.

## Files Updated

- `memory/decisions.md`
- `references/us-stock-daily-strategy-report-template.md`

## Real Account Impact

The real HKD 20,000 account should favor fewer, technically justified orders over higher-probability fills, because one U.S. share can consume around 10% or more of capital. New orders must also avoid margin / financing.
