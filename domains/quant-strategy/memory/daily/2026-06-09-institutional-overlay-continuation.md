# 2026-06-09 Institutional Overlay Continuation

Purpose: absorb the latest Man Institute consumer-fragility research into the institutional overlay system and align the replay todo state with the current ledger.

## What Changed

Updated:

- `references/institutional-overlay-scorecard.md`
- `references/institutional-overlay-data-proxies.md`
- `references/institutional-overlay-replay-protocol.md`
- `memory/todos/2026-06-09-strategy-todos.md`

## New Overlay Dimension

Added two factor-macro flags:

- `consumer_backstop_fragility`
- `K_shaped_consumption_risk`

Interpretation:

- When AI/large-cap leadership is narrow, do not assume broad consumer spending can cushion an AI de-rating shock.
- If consumer stress, energy costs, delinquencies, or equity-wealth concentration worsen, treat them as macro context for market fear and replay analysis.
- These flags are not standalone sell signals and do not override price, stops, fear gate, or concentration rules.

## Replay Status

The 2026-06-05 replay ledger already includes:

- 2026-06-05 close event row.
- 2026-06-08 intraday snapshot.
- 2026-06-08 completed close row.

Next required row:

- 2026-06-09 close after formal post-close audit.

## Decision Status

No update to `decisions.md`. The consumer-backstop overlay is a monitoring and replay dimension until validated.
