# RSR2 close-confirmed profit-protection forward preregistration

## Status and separation

- Version: `RSR2-profit-lock-shadow`
- Start: first completed U.S. session on or after `2026-08-17`
- Universe: the same 32-name `ai_capex_broad` scope as RSR1
- Entry rules, target weight, initial stop, maximum hold and costs: identical to RSR1
- Benchmark: frozen `RSR1-shadow`
- Formal V9 change: `false`
- Live-order authorization: `false`
- Ledger: `results/forward_profit_protection_ledger.csv`, separate from RSR1

## Frozen exit challenger

After a position closes at least 15% above its actual entry fill, raise its
resting stop to 5% above that entry fill for the following session. The trigger
uses a completed close only; an intraday high cannot activate the stop on the
same day. Gaps through the stop fill at the next available open under the same
slippage and commission assumptions as RSR1.

No fixed profit target is added. In the retrospective 32-name sample, 14 of 15
winners reached +8% pre-exit MFE, while only one of eight losers did. A fixed
target would sacrifice the strategy's right tail to address one giveback.

## Promotion gate versus RSR1

Do not review for promotion before all are true:

- At least 126 completed sessions and 20 closed RSR2 trades.
- At least three distinct subthemes and no one symbol contributes more than 35%
  of gross profits, aggregated across repeated winning trades.
- RSR2 net return and win rate are not below contemporaneous RSR1.
- RSR2 profit factor is at least 1.30 and Sharpe is not below RSR1.
- RSR2 maximum drawdown is not worse than RSR1 by more than one percentage point.
- RSR2 remains no worse than RSR1 at 20 bps in both full-rerun and fixed-trade-path checks.

Failure of any gate keeps RSR2 in research. RSR2 cannot modify RSR1's ledger or
promotion decision, and neither shadow authorizes a live order.

## Retrospective reason for nomination

At 10 bps, the 15% -> 5% overlay changed the 32-name full result from 15.68%
return, -2.46% drawdown, 1.55 Sharpe and 65.22% win rate to 18.11%, -2.33%,
1.77 and 69.57%. Eight of nine nearby trigger/floor cells were non-worse across
training and 2026 screens. At 20 bps, the challenger returned 14.72% versus
13.45% for RSR1, but the trade path changed from 23 to 24 trades.

The improvement came from only two protected exits (INTC in training and KLAC
in 2026) and uses the same hindsight-selected list. It is therefore a post-hoc
forward challenger, not evidence for a live rule.
