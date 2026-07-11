# 2026-07-12 Formal Forward Ready + PIT Event Gap

## Status

Formal V9 shadow forward is initialized and freeze-eligible. First executable completed session is **2026-07-13**. Historical backfill is forbidden.

## PIT event gap (Rule E statistical gate)

- Archive events: 50
- Retrospective backfill (not PIT): 31
- Reliable PIT (`source_completeness >= 15` and not backfill): **18**
- Gate: 50 → gap **32**
- Cannot close the gap by reclassifying backfill or inflating scores
- Closing path: newly observed events with real `first_seen_at`, via `scripts/append_shadow_event.py` for live forward and curated archive updates only when live capture is honest

See `strategies/v9-execution/validation/pit-event-gap-analysis.md` and `formal-forward-monday-runbook.md`.

## Monday close checklist

1. Refresh `data_v9`
2. Append any new observed info events (`--forward`)
3. `run_v9_shadow.py --as-of 2026-07-13`
4. `report_pit_event_gap.py` + `audit_shadow_forward_launch.py`

## Non-changes

Formal MA150/MA200, Fear Gate rails, Rule E thresholds, stops, and 70/30 ceilings remain unchanged.
