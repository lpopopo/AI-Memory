# Forward economic-edge attribution preregistration

Status: frozen on 2026-08-21 before any closed RSR1/RSR2 forward trade exists.
Research-only; read-only inputs; no gate or order authorization.

## Objective

Carry the historical avoided-loss, missed-winner and profit-lock path
decomposition into genuine forward observation. The scorecard prevents a higher
headline win rate or later whole-share compounding from being mistaken for a
repeatable economic mechanism.

## Immutable inputs

- `results/forward_shadow_signals.csv`
- `results/forward_shadow_baseline_trades.csv`
- `results/forward_shadow_ledger.csv`
- `results/forward_profit_protection_ledger.csv`
- `results/forward_shadow_status.json`

The evaluator may read but never modify these ledgers. Only rows on or after
2026-08-17 with complete sources and actual closed outcomes may enter economic
totals.

## Frozen outputs

1. Closed matched-baseline trades whose signal is present in the signal ledger
   and rejected by RSR1 are direct quality exclusions. Split them into avoided
   losers and missed winners without changing the filter.
2. Baseline and RSR1 trades are paired by `(symbol, signal_date)`. Common,
   baseline-only and RSR1-only path counts are reported separately.
3. Closed RSR1 and RSR2 trades are paired by `(symbol, signal_date)`. Report
   aggregate observed P&L delta, direct changed-exit effect on RSR1 shares, and
   residual capital/whole-share path effect using the already frozen addendum
   formula.
4. Report profit-lock activations and actual profit-lock exits, plus the share
   of incremental P&L supplied by the largest one and two positive deltas.
5. Historical calibration is labeled retrospective and contributes zero
   forward evidence.

## Status rules

- `awaiting_closed_baseline_exclusion`: no directly excluded baseline trade has
  closed; avoided-loss and missed-winner statistics are unavailable, not zero.
- `awaiting_paired_rsr_exit`: no common closed RSR1/RSR2 pair exists; overlay
  attribution is unavailable, not zero.
- `observing`: at least one relevant closed outcome exists but the original
  20-trade/126-session gate is incomplete.
- `review_eligible`: original immutable gates are met; this scorecard still
  cannot promote a strategy by itself.

No sample-dependent threshold, backfill, active-block deletion, universe
expansion or reinterpretation of an open trade is permitted.
