# 2026-06-08 Automation Update

Purpose: update existing Codex automations after the institutional research overlay and 2026-06-05 drawdown replay.

This note records automation workflow changes only. It is not a trading instruction.

## What Changed

Updated existing automations:

- `automation`: realtime public-source and institutional-research monitor. It now tracks social/news sources plus AQR, Citadel Securities, GMO, and Man Group research inputs.
- `automation-2`: daily US stock strategy report. It now must use the US stock daily strategy report template, institutional overlay checklist, scorecard, and AI quality/capex-cycle classification.
- `automation-4`: daily execution checklist and portfolio ledger. It now treats itself as execution preparation, not formal post-close audit, and must label holdings as `core hold`, `defensive hold`, `reduce-review`, `exit-review`, or `watch only`.
- `automation-3`: intraday strategy review and layered memory summary. It now explicitly treats 23:30 Beijing output as intraday preliminary review, not official close-trigger audit.

Created new automation:

- `automation-5`: formal US post-close audit. It runs after the U.S. close and is responsible for formal close-price audit, stop-trigger table, market fear state, institutional overlay scorecard, portfolio value, replay ledger updates, and post-close memory updates.

## Why It Changed

The 2026-06-05 AMD stop breach and AI/semiconductor/storage synchronized drawdown were detected late because the prior "night review" ran during the U.S. session rather than after the official close.

The new workflow separates:

- Premarket strategy generation.
- Intraday execution preparation.
- Intraday preliminary review.
- Formal post-close audit.

## Required Future Behavior

- Formal stop triggers require official or reliable close data.
- Intraday tasks may flag risks but must not treat snapshot prices as final close triggers.
- Daily strategy and execution tasks must include institutional overlays when data permits.
- The post-close audit should update the 2026-06-05 replay ledger when completed close rows become available.

## Stable Decision Status

No new trading rule was promoted to `decisions.md`. The automation workflow changed to improve audit timing and evidence capture; the institutional overlays remain experimental pending replay and validation.
