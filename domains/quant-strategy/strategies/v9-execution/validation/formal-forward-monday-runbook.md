# Formal Shadow Forward — Monday Runbook

Status: operational checklist for the first append-only formal forward day.  
First executable completed session: **2026-07-13**  
Do **not** backfill `2026-07-10` or any earlier date.

## Preconditions

- [ ] `git status` clean (or only unrelated ignored local data)
- [ ] `results/shadow_portfolio/frozen/code_manifest.json` has `forward_eligible: true`
- [ ] `results/shadow_portfolio/forward/accounts/*/initial_state.json` exist (4 accounts)
- [ ] No dated `20*_state.json` yet, or chain is contiguous through prior session

## Steps (after US cash close)

```powershell
cd D:\code\AI-Memory\domains\quant-strategy\strategies\v9-execution
$py = "D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe"

# 1) Refresh completed bars used by diagnostics / engine
& $py scripts\download_v9_data.py
# or, if only breadth proxies need refresh:
# & $py scripts\enrich_v9_diagnostic_symbols.py

# 2) Optional: append any newly observed information events BEFORE the day run
# & $py scripts\append_shadow_event.py --forward --event-json path\to\event.json

# 3) Advance formal forward exactly one session
& $py scripts\run_v9_shadow.py --as-of 2026-07-13

# 4) Refresh gap / launch audits
& $py scripts\report_pit_event_gap.py
& $py scripts\audit_shadow_forward_launch.py
```

## Pass criteria for the day

- Report written under `results/shadow_portfolio/forward/reports/shadow_report_2026-07-13.json`
- `diagnostics.authorizes_trade == false` for research monitors
- Four account state files hashed and linked to prior genesis
- No tamper alarm

## Explicit non-goals that day

- Do not promote Rule E on statistical grounds (still 18/50 reliable PIT events)
- Do not change MA150/MA200, Fear Gate rails, stops, or 70/30 ceilings
- Do not reclassify retrospective backfill events as PIT
