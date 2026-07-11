# 2026-06-08 Institutional Research Stage 5

Purpose: create a repeatable replay protocol and ledger for comparing baseline rules against the experimental institutional overlays.

This note is research memory only. It does not promote new stable decisions.

## What Changed

Created:

- `references/institutional-overlay-replay-protocol.md`
- `experiments/2026-06-08-institutional-overlay-replay/README.md`
- `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv`

Updated:

- `references/institutional-overlays-backtest-plan.md`
- `memory/todos/2026-06-08-strategy-todos.md`
- `memory/daily-summaries.md`

## Replay Design

The replay now compares:

- `baseline_rules`: market fear gate, existing stops, concentration rules, and daily monitoring.
- `overlay_rules`: baseline plus flow-fragility score, trend-aligned entry score, AI quality/capex-cycle labels, and factor-macro flags.

The first replay window is:

- `T0`: 2026-06-05 close.
- `T1`: 2026-06-08 close or best verified regular-session snapshot.
- `T2-T5`: next four completed trading days after `T1`.

Future rows should not be filled until the data exists.

## Initial Findings From Setup

- The overlay would not have automatically sold all MRVL/AMD/WDC/STX exposure.
- It would have blocked all fresh AI/semiconductor/storage adds after the 2026-06-05 close.
- It would have forced immediate AMD reduce-review because the stop was breached.
- It would have downgraded WDC/STX to defensive near-stop review.
- It would have required correlated-theme portfolio review before relying on single-stock optimism.

## Why This Matters

The main operational failure on 2026-06-05 was not the stock thesis itself. It was timing and workflow: the post-close audit did not immediately catch a stop breach plus theme-wide drawdown. The replay protocol tests whether institutional overlays can make that risk visible earlier without turning into over-defensive selling.

## Next Step

After the next completed U.S. close, append the next row to `replay-ledger-template.csv` with official close data and compare:

- Baseline portfolio value.
- Overlay portfolio value under the explicit execution assumption.
- Drawdown reduction.
- Missed rebound cost.
- Whether AMD/WDC/STX/MRVL decisions were improved or merely delayed.
