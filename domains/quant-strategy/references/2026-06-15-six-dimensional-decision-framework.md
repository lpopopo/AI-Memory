# 2026-06-15 Six-Dimensional Decision Framework

Purpose: repair the real-account decision workflow after the strategy discussion showed that multi-dimensional analysis was present but not consistently compressed into a clear trade action.

## Rule Added

Every real-account buy/sell recommendation must explicitly evaluate six dimensions:

1. Market sentiment:
   - SPY, QQQ, SMH, VIX, breadth, credit / risk appetite if available.
2. Theme strength:
   - AI compute, AI interconnect / optical, memory / storage, cloud / AI factory, AI application, or defensive sectors.
3. Stock relative strength:
   - Stock versus QQQ, SMH, and direct same-theme peers.
4. Technical entry quality:
   - Moving averages, intraday VWAP, prior support / low, opening range, ATR pullback, or breakout trigger.
5. Account constraints:
   - HKD 20,000 real capital, single-share sizing, USD cash availability, FX / fees, and no margin / financing.
6. Exit / risk plan:
   - Stop line, no-chase line, failed-trigger rule, and profit-taking level.

## Required Output

The final action must map the above dimensions into one of:

- `buy`
- `conditional buy`
- `wait`
- `watch only`
- `reduce`
- `exit`

If live data is unreliable or a dimension is missing, the trade should default to `conditional buy`, `wait`, or `watch only`.

## Files Updated

- `memory/decisions.md`
- `references/us-stock-daily-strategy-report-template.md`

## Practical Impact

For strong repair/risk-on days, the strategy must not stop at "do not chase." It should also define whether a smaller breakout / confirmation entry is valid, invalid, or already beyond the no-chase line.
