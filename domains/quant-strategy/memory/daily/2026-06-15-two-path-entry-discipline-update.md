# 2026-06-15 Two-Path Entry Discipline Update

Purpose: repair the entry framework after the strategy over-emphasized pullback entries during a strong repair/risk-on open.

## Issue

The strategy correctly avoided chasing unsupported prices after the MRVL USD 252 starter-order review, but it over-corrected by treating pullback entry as the only valid path.

On 2026-06-15, QQQ, SMH, and several AI infrastructure names opened strongly. The correct framework should have evaluated a separate breakout / confirmation starter path in addition to the pullback path.

## Rule Added

Every actionable buy candidate must evaluate:

1. Pullback entry:
   - Requires MA / VWAP / prior support / gap level / ATR / risk-line basis.
   - Designed to avoid overpaying.

2. Breakout / confirmation entry:
   - Requires broad-market confirmation such as QQQ and SMH risk-on behavior.
   - Requires stock-level confirmation such as reclaiming a trigger level, holding above opening range / VWAP, or outperforming SMH for 15-30 minutes.
   - Must use a smaller starter size for the real HKD 20,000 account.

3. No-chase line:
   - Defines when even a strong stock is too extended for the account size.

4. Failure / stop condition:
   - Defines when the confirmation entry is invalidated intraday or by close.

## Real Account Impact

For the real HKD 20,000 account:

- Breakout entries are allowed only as small starter positions.
- Each breakout order should generally stay around 5%-10% account exposure.
- No margin / financing.
- If the trigger fails intraday, cancel or reassess rather than averaging down.

## Files Updated

- `memory/decisions.md`
- `references/us-stock-daily-strategy-report-template.md`
