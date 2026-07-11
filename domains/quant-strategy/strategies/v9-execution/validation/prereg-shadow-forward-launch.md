# Pre-registration: Shadow Forward Launch

Frozen date: 2026-07-11  
Status: launch checklist; formal forward remains blocked until prerequisites pass.

## Prerequisites

1. Clean git worktree for freeze artifacts.
2. `freeze_v9_rule_e.py` succeeds and writes `results/shadow_portfolio/frozen/`.
3. `v9_research_monitors.py` included in code manifest.
4. Baseline event snapshot hash recorded.
5. Reliable PIT events counted; Rule E statistical promotion still requires >=50.
6. Append-only `forward/` directory empty or verified untampered.

## Launch steps

```powershell
& 'D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe' scripts/freeze_v9_rule_e.py
& 'D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe' scripts/init_forward_accounts.py
& 'D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe' scripts/run_v9_shadow.py --as-of YYYY-MM-DD
```

Use `--dry-run` for rehearsals. Formal forward forbids historical backfill.

## Initial audit gate

- at least 3 months of append-only states
- at least 10 independent information-stock decisions or explicit zero-trade log
- diagnostics present each day without authorizing trades

## Promotion gate

Unchanged from `results/v9_goal_completion_audit.md`. Behavioral / momentum
overlays cannot promote without incremental net evidence over Fear Gate + MA.
