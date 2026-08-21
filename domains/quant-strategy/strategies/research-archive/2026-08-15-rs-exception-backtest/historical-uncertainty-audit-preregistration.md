# Historical edge uncertainty audit — preregistration

Frozen on 2026-08-21 after the aggregate economic decomposition was already
known, but before generating the resampling and leave-cluster-out results in
this audit. This is a read-only robustness layer. It does not search a new
entry threshold, exit, holding period, allocation, rank or universe.

## Known facts before this audit

- The matched baseline has 44 closed trades, RSR1 has 23 and RSR2 has 23.
- RSR1 directly excludes 23 baseline trades: 16 losers and seven winners.
- RSR2 adds USD 145.34 versus RSR1 in the historical account path.
- Only two paired trades have a non-zero direct exit effect; path and
  whole-share sizing explain part of the aggregate RSR2 delta.
- The exact point-in-time transfer screen failed and the parameter-selection
  bias screen did not contain the retrospective concern.

These known results make this audit confirmatory only in the narrow sense of
measuring sampling fragility. It cannot supply independent validation.

## Frozen inputs

The evaluator may read only:

- `results/economic_edge_trade_attribution.csv`
- `results/economic_edge_profit_lock_deltas.csv`
- `results/forward_expectancy_scorecard.csv`
- `results/selection_bias_audit_summary.json`

The source hashes must be recorded. No backtest engine is rerun.

## Resampling unit and seed

- Cluster on the immutable `signal_date`; same-day signals are not treated as
  independent observations.
- Draw the observed number of signal-date clusters with replacement.
- Concatenate all trades belonging to each selected cluster and evaluate the
  mean across the resulting trade rows.
- Use exactly 20,000 samples and NumPy seed `20260821`.
- Report 2.5%, 5%, median, 95% and 97.5% quantiles.
- Tail probabilities use the plus-one correction `(count + 1) / (B + 1)`.

## Test A — direct quality-filter exclusions

Use only `baseline_only` rows whose reason is not `portfolio_path`. For every
bootstrap sample calculate mean excluded-trade P&L and mean excluded-trade
return. The historical filter direction is favorable only when both means are
negative. Report:

- probability mean P&L is negative;
- probability mean return is negative;
- probability both are negative;
- the full quantiles for both metrics;
- leave-one-signal-date-cluster-out minima/maxima and whether every omission
  leaves both metrics negative.

This test measures the stability of the already-selected filter's avoided-loss
mechanism. It does not correct the known family-wise selection problem.

## Test B — RSR2 paired economic delta

Use all paired RSR1/RSR2 rows. For every bootstrap sample calculate:

- mean total P&L delta per paired trade;
- mean direct exit effect per paired trade on frozen RSR1 shares;
- mean capital-path/whole-share residual per paired trade;
- win-rate delta from the paired P&L signs.

Report the probability each delta is positive and the probability that total
P&L, direct exit effect and win-rate delta are all positive. Total P&L delta is
not interpreted as a pure exit effect because it contains path/sizing.

## Test C — concentration and omission sensitivity

Without rescaling quantities, remove the largest one and largest two positive
paired deltas and report the remaining aggregate total delta. Repeat for the
direct exit-effect column. Also perform a leave-one-signal-date-cluster-out
jackknife and report whether every omission leaves the total/direct effects
positive.

## Interpretation

- `historically_stable_selected_sample`: Test A has at least 90% bootstrap
  probability that both excluded P&L and return are negative, and every
  leave-one-cluster-out estimate remains negative.
- `directional_but_sparse`: the RSR2 direct-effect probability is at least 80%,
  but fewer than five observed paired trades have a non-zero direct effect or
  removing the two largest direct effects eliminates the aggregate effect.
- `not_stable`: the relevant probability is below 80% or a single-cluster
  omission reverses the sign.

Even the strongest label is retrospective and selection-contaminated. The
decision remains: no formal V9 change, no real-account change, no order, and no
RSR1/RSR2 promotion without the existing genuine-forward gates.

