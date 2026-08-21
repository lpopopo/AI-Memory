# Forward mechanism evidence clock — preregistration

Frozen on 2026-08-21 while all genuine-forward matched-baseline, RSR1 and RSR2
closed-trade counts are zero. This clock is read-only and cannot alter the
original 20-closed-trade / 126-session promotion gates.

## Objective

Repeated daily review can turn a favorable first outcome into an informal rule
change. This clock prevents that by separating continuous accumulation from
interpretation at fixed outcome-count checkpoints. It tracks the two historical
mechanisms that now matter most:

1. entry-quality loss avoidance—baseline trades directly rejected by RSR1;
2. RSR2 exit economics—paired RSR1/RSR2 closed trades and actual changed exits.

## Immutable inputs

- `results/forward_shadow_signals.csv`
- `results/forward_shadow_baseline_trades.csv`
- `results/forward_shadow_ledger.csv`
- `results/forward_profit_protection_ledger.csv`
- `results/forward_shadow_status.json`

Only source-complete rows with signal dates on or after 2026-08-17 and closed
outcomes are admissible. Inputs are hashed before every evaluation.

## Ordering and immutable checkpoint snapshots

- Sort direct exclusions by `exit_date`, then `signal_date`, then `symbol`.
  Sort paired outcomes by the later of the two exit dates (the first date when
  both sides are known), then `signal_date`, then `symbol`.
- Entry-quality checkpoints use the first 5, 10 and 20 closed direct
  exclusions.
- Paired RSR1/RSR2 checkpoints use the first 5, 10 and 20 paired closed trades.
- Changed-exit diagnostic checkpoints use the first 1, 2 and 5 pairs with a
  non-zero direct exit-price effect on frozen RSR1 shares.
- Once a checkpoint is reached, its snapshot is calculated from the first N
  ordered outcomes and must remain unchanged as later rows append.
- Between checkpoints, counts and raw economics update, but the latest fixed
  checkpoint interpretation does not.

## Entry-quality checkpoint metrics

For each checkpoint report avoided losers, missed winners, loss rate, avoided
loss dollars, missed profit dollars, net P&L removed and mean return.

- `supportive_direction`: loss rate is above 50% and net P&L removed is below
  zero.
- `contradictory_direction`: loss rate is below 50% and net P&L removed is
  above zero.
- `mixed_direction`: every other combination.

These are descriptive directions, not p-values or promotion decisions.

## RSR2 paired checkpoint metrics

For each checkpoint report RSR1/RSR2 wins, win-rate delta, total P&L delta,
direct exit effect on RSR1 shares and capital/whole-share residual.

- `supportive_direction`: direct exit effect is positive and win-rate delta is
  non-negative.
- `contradictory_direction`: direct exit effect is negative and win-rate delta
  is non-positive.
- `mixed_direction`: every other combination.

The changed-exit diagnostic separately reports the sign and cumulative direct
effect of the first 1, 2 and 5 non-zero direct effects. It cannot select a new
trigger or floor.

## Status and governance

- `awaiting_sample`: no relevant closed outcome.
- `accumulating_before_first_checkpoint`: at least one outcome, fewer than five.
- `checkpoint_frozen_observing`: at least one 5/10/20 checkpoint is available,
  but the original promotion gates are incomplete.
- `original_gate_review_eligible`: and only if both original immutable gates in
  `forward_shadow_status.json` pass.

No daily result, checkpoint label or changed-exit count may authorize a trade,
modify formal V9, change the real account, weaken the original gates, or add a
historical parameter search.
