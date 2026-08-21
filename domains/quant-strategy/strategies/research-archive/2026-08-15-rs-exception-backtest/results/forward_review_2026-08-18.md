# RSR forward review through 2026-08-18

## Current evidence

- Status: `observing`.
- Completed forward sessions: `2` (August 17 and 18).
- Data boundary: completed August 18 session only; August 19 intraday data are
  excluded.
- Universe: frozen 32-name `ai_capex_broad` shadow.
- RSR1 signals/trades: `0 / 0`.
- RSR2 signals/trades: `0 / 0`.
- Matched-baseline signals/trades: `0 / 0`.
- Formal V9 or live account changed: `false`.
- Order authorization: `false`.

The absence of trades is an observation, not a 0% win rate. The forward
expectancy rows remain `awaiting_sample`; no hit-rate, payoff or expectancy
estimate exists until trades close.

## What the filters observed

On August 17, SMH was above its MA50, but no stock passed every frozen RSR1
condition. The opportunity ledger recorded 16 five-session leaders outside the
low-volatility design domain. On August 18, SMH fell back below MA50 and the
theme gate closed; six five-session leaders remained outside RSR1. Across the
two daily rows this is 22 raw observations, or 16 primary event episodes after
grouping repeated same-symbol observations within five sessions.

This does not yet prove that avoiding those leaders was profitable. Their
preregistered outcomes are the exact 5- and 20-session close return, MFE and
MAE. None is mature as of August 18, so every aggregate outcome remains `n/a`.
No one-day decision metric was added after seeing the August 18 semiconductor
selloff.

## Data and integrity work

The local V9 OHLCV cache was advanced atomically from August 14 to August 18.
Every requested non-volatility symbol has complete open, high, low, close and
volume on the declared cutoff. VIX and VIX3M use Cboe official daily history.
The downloader now uses the existing Yahoo Chart daily API as a traceable
auto-adjusted fallback when yfinance fails, and refuses to overwrite the cache
if any requested symbol remains incomplete.

The zero-byte trade-file boundary was also fixed: a completed forward run with
zero trades now enters the scorecard as an empty sample instead of raising a
CSV parser error.

## Decision

Keep formal V9, frozen RSR1 and frozen RSR2 unchanged. Do not relax ATR,
extension or SMH gates because the first two forward sessions produced no
trades. Continue appending completed sessions. The next evidence milestones are
the first actual signal/execution, the first matured five-session opportunity
episodes, 20 closed trades, and 126 completed sessions.
