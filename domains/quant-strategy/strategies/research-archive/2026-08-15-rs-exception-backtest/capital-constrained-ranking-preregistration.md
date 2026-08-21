# Capital-constrained RSR2 ranking preregistration

## Status and purpose

- Frozen before reading any ranking-comparison result.
- Research only; no formal V9, RSR1, RSR2, order, holding or forward-ledger change.
- Objective: determine whether the ordering of already-qualified RSR1 entries can
  improve RSR2 economic expectancy when the three-name or stock-capacity limit
  prevents every valid signal from being filled.
- This study does not add a signal, relax a filter, alter position size, or use
  future returns in the ranking.

## Invariants

Use the frozen 32-name `ai_capex_broad` universe and all existing RSR1 entry
rules: broad and SMH gates, breakout, RS20 >= 3%, volume >= 1.2x, extension <=
12%, ATR14/close <= 4%, close location >= 50%, event-gap cooldown, next-session
open execution, whole shares, minimum USD 200 notional, 8% target, 15%
single-name maximum, 25% stock-sleeve maximum and three simultaneous names.

Use the frozen RSR2 exit: 8% initial stop, 20-session maximum, MA20/negative-RS
exit and the close-confirmed +15% trigger that raises the next-session stop to
+5%. Charge USD 1 per order. Do not use SGOV or any cash-yield overlay.

Rank only the candidates that pass every frozen signal rule at a completed
close. When capacity can accept all candidates, every policy must submit the
same orders. Ties use reverse lexical symbol order, preserving the current
implementation exactly and making every comparison deterministic.

## Frozen ranking policies

1. `formal_composite`: current implementation, descending
   `RS20 * 100 + min(volume_ratio, 5)`.
2. `rs_only`: descending RS20.
3. `low_atr_first`: ascending ATR14/close.
4. `balanced_rank`: equal-weight mean of same-day percentile ranks for higher
   RS20, higher volume ratio, higher close location and lower ATR14/close.

No policy or weight may be added after results are viewed. The equal weights in
`balanced_rank` are structural, not fitted.

## Periods and stresses

- Development: 2024-01-02 through 2025-12-31.
- Held-out monitor: 2026-01-02 through the latest locally completed session.
- Full descriptive period: 2024-01-02 through the latest locally completed
  session.
- Initial NAV: USD 6,000 and USD 5,751.77.
- Slippage: 10 bps and 20 bps per side, each as a full rerun.

The 2026 monitor has already been observed elsewhere and is not genuinely new
out-of-sample evidence. It is a frozen cross-period consistency check only.

## Advancement gate

A challenger may become a separate forward-ranking shadow only if all are true:

- At least five capacity-contention decisions occur in development and at least
  two occur in the 2026 monitor. If not, label the comparison `insufficient`.
- At 10 bps, total return exceeds `formal_composite` in both periods and at both
  NAVs.
- Sharpe is not below `formal_composite` in either period at either NAV.
- Maximum drawdown is not worse by more than one percentage point.
- Closed-trade win rate is not lower by more than five percentage points.
- The direction of the return advantage survives 20 bps at both NAVs and in
  both periods.
- At least three symbols contribute gross profit and no one symbol contributes
  more than 35% of gross profit in the full 10 bps run.

If more than one challenger passes, select the one with the highest minimum
return improvement across the four 10 bps period/NAV cells. This selection rule
is frozen here and is not a license to tune the policy.

Passing creates only a versioned forward-ranking shadow beginning after this
study. It cannot replace the already-frozen Aug 17 RSR1/RSR2 ledgers. Failure or
insufficient contention retains `formal_composite` and closes this branch until
new independent capacity conflicts exist.
