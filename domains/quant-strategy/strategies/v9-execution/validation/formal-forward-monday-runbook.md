# Formal Shadow Forward — Monday Runbook

Status: operational checklist; the former 2026-07-13 launch artifact is historical only.
Current status (2026-08-09): formal forward is blocked because the repository is not clean, so no current generation can be forward-eligible.
After a new clean, versioned freeze/genesis, use the first completed session strictly after that freeze. **Do not backfill missing dates as forward evidence.**

The latest rehearsal generation `v9-readiness-20260809-r1` is engineering-only. It must not be promoted or reused because its manifest records a dirty worktree.

## Preconditions

- [ ] Readiness audit reports `formal_freeze_allowed: true` (the complete repository is clean)
- [ ] A new, never-used generation ID has been selected
- [ ] `results/shadow_portfolio/generations/<generation-id>/frozen/code_manifest.json` has `forward_eligible: true`
- [ ] `results/shadow_portfolio/generations/<generation-id>/forward/accounts/*/initial_state.json` exist (4 accounts)
- [ ] No dated `20*_state.json` yet, or chain is contiguous through prior session
- [ ] `preflight_formal_forward.py` and `audit_shadow_forward_launch.py` agree on manifest identity, state-file count and completed-session count
- [ ] Full regression suite passes with forward-integrity tests running only in an isolated temporary directory

## Steps (after US cash close)

```powershell
cd D:\code\AI-Memory\domains\quant-strategy\strategies\v9-execution
$py = "D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe"
$generationId = "v9-formal-YYYYMMDD-r1"
$generationRoot = Join-Path $PWD "results\shadow_portfolio\generations\$generationId"

# 0) Refresh completed bars used by diagnostics / engine
& $py scripts\download_v9_data.py --completed-through YYYY-MM-DD
# or, if only breadth proxies need refresh:
# & $py scripts\enrich_v9_diagnostic_symbols.py

# 1) Prove the complete repository is clean, then create the immutable generation and genesis
& $py scripts\generation_readiness.py --require-clean
& $py scripts\prepare_forward_generation.py $generationId --initialize-forward

# 2) Point all formal operations at this generation
$env:V9_SHADOW_DIR = $generationRoot
$env:V9_FROZEN_DIR = Join-Path $generationRoot "frozen"
$env:V9_FORWARD_DIR = Join-Path $generationRoot "forward"
$env:V9_VALIDATION_DIR = Join-Path $generationRoot "validation"

# 3) Preflight (freeze hashes, genesis, data freshness vs as-of)
& $py scripts\preflight_formal_forward.py YYYY-MM-DD

# 4) Optional: append any newly observed information events BEFORE the day run
# Copy validation/event-append-template.json, fill real fields, then:
# & $py scripts\append_shadow_event.py --forward --event-json path\to\event.json

# 5) Advance formal forward exactly one session
& $py scripts\run_v9_shadow.py --as-of YYYY-MM-DD

# 6) Refresh gap / launch audits
& $py scripts\report_pit_event_gap.py
& $py scripts\audit_shadow_forward_launch.py
```

## Pass criteria for the day

- Report written under `results/shadow_portfolio/generations/<generation-id>/forward/reports/shadow_report_YYYY-MM-DD.json`
- `diagnostics.authorizes_trade == false` for research monitors
- Four account state files hashed and linked to prior genesis
- No tamper alarm

## Explicit non-goals that day

- Do not promote Rule E on statistical grounds (still 18/50 reliable PIT events)
- Do not change MA150/MA200, Fear Gate rails, stops, or 70/30 ceilings
- Do not reclassify retrospective backfill events as PIT
