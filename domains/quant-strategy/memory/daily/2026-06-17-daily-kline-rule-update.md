# 2026-06-17 Daily K-line Rule Update

Scope: stable process update prompted by user feedback during U.S. open execution.

## Issue

Recent live execution advice used real-time quotes, cost lines, and intraday triggers, but did not consistently include daily K-line context. This made trigger prices such as MRVL `294` too dependent on opening-range behavior rather than daily technical structure.

## Rule Added

Before any real-account buy, add, reduce, or exit recommendation, the strategy must review:

- latest daily close/open/high/low;
- 5/10/20/50-day moving averages;
- 20-day high/low or other nearby daily resistance/support;
- whether price is extended above short/medium moving averages or broken below them;
- fee-adjusted breakeven and cancellation/exit rule.

## Practical Impact

- MRVL: if above 5/10-day averages but far above the 20-day average, default to hold/profit-protection rather than casual add.
- RDW: if below 5/10/20-day averages and only near the 50-day average, do not average down until it reclaims the predefined risk line and market/theme confirmation improves.
- AMZN or other defensive participation candidates: if below 20/50-day averages, do not label them as strong breakout candidates without a clear reclaim.

Updated `decisions.md`.

Not investment advice.
