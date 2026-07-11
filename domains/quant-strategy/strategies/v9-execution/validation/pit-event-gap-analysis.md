# PIT Event Gap Analysis

Frozen date: 2026-07-12  
Status: research / promotion-blocker analysis. Does **not** change formal V9 weights.

## Counts

| Bucket | N |
| --- | ---: |
| All events in `datasets/v9_information_events.json` | 50 |
| Marked `retrospective_backfill` (not PIT-eligible) | 31 |
| `source_completeness >= 15` and PIT-eligible (**reliable**) | 18 |
| Completeness 10–14 near-miss (non-backfill) | 1 |
| Gate for Rule E statistical split | **50** reliable PIT |
| Remaining gap | **32** |

## What will not close the gap

1. **Reclassifying retrospective backfill as PIT** — forbidden. Those posts were discovered after publication (`archive_observed_at` 2026-07-04) and remain research-only.
2. **Raising completeness scores on thin sources** — only one non-backfill event sits below 15; score inflation is not evidence.
3. **Yahoo PIT price backfill** — improves WML/universe coverage, not information-event counts.

## What will close the gap

Collect **new** observations with:

- real `first_seen_at` at discovery time (UTC or offset-aware ISO)
- `source_completeness >= 15`
- unique `event_id` / `content_hash`
- symbols already in the watchlist/data panel when possible

Two tracks:

| Track | Where | Counts toward |
| --- | --- | --- |
| Formal shadow forward | `results/shadow_portfolio/forward/shared/event_append_log.jsonl` via `scripts/append_shadow_event.py` | live Rule E decisions in append-only forward |
| Statistical archive | append to `datasets/v9_information_events.json` only when source health supports live capture, then re-freeze baseline when appropriate | `chronological_split` / >=50 gate |

Forward append events do **not** automatically inflate the frozen baseline count. Do not edit historical baseline events.

## Source health

- `2026-05-29` → `2026-06-26`: `healthy_archived`
- `2026-06-27` → present: `partial_live`

Until source health returns to healthy live capture, treat new Xiaohongshu items as carefully timestamped observations; do not backdate `first_seen_at`.

## Next operational actions

1. On each trading day after 2026-07-13 close: refresh `data_v9`, run formal forward once.
2. When a new qualified information item is observed: append with `append_shadow_event.py --forward`.
3. Periodically recompute reliable PIT count; only after >=50, re-open Rule E statistical promotion tests.
