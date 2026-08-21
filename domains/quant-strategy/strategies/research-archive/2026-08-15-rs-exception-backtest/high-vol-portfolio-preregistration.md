# High-volatility trend portfolio simulation registration

Frozen after the event layer passed and before reading portfolio outputs on 2026-08-15. Research-only; no order authorization.

## Signal

Use only the already-frozen `hv_central` signal from `high-vol-trend-preregistration.md`. Do not search signal thresholds in this stage.

## Portfolio contract

- Initial NAV: USD 6,000.
- Entry: next-session open, 10 bps slippage and USD 1 commission per side.
- Reject an entry if the next-open gap exceeds 5% from the signal close.
- Rank simultaneous orders by RS20, then volume ratio, then symbol.
- Maximum two positions; maximum aggregate high-volatility sleeve 15% NAV.
- Stop distance: `min(15%, max(8%, 1.25 * signal ATR14/close))`.
- Target weight: `min(8%, 0.75% NAV risk / stop distance)`.
- Whole shares only. A one-share exception is allowed only when the share remains within the 15% sleeve and 15% single-name ceiling.
- Resting intraday stop; a gap through the stop executes at the opening price, otherwise at the stop, with sell slippage and commission.
- After a completed close reaches +15% from entry, the next-session stop rises to at least +5% from entry and never moves down.
- Ordinary exit: next-session open after either 20 sessions held or a completed close below MA10.
- Re-entry cooldown: 10 sessions after exit.
- Liquidate remaining positions at the report end close for comparable period metrics.

## Cost checks

Run both 10 bps and 20 bps per side. The entry identity path must remain unchanged between costs; otherwise cost and selection effects cannot be conflated.

## Continuation gate

Proceed to V9/RSR combination only if the 10 bps central portfolio satisfies all of the following in both `development_2024_2025` and `retrospective_2026`:

1. At least 10 and 5 closed trades, respectively.
2. Positive total return and Sharpe at least 0.50.
3. Win rate at least 50% and profit factor at least 1.20.
4. Maximum drawdown no worse than -10%.
5. Return remains positive at 20 bps in both periods.
6. Entry identity path is unchanged between 10 and 20 bps.
7. Across both periods, no symbol contributes more than 35% of gross winning PnL.

Failure stops portfolio promotion and leaves the module as a non-trading diagnostic.
