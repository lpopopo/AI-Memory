# V9 Execution Strategy

V9 is the only executable portfolio strategy in this repository. It manages a
single U.S. equity portfolio through three integrated components:

| Component | Maximum allocation | Rule |
| --- | ---: | --- |
| Index core | 70% | SPY/QQQ MA150/MA200 long-term trend allocation |
| Individual stocks | 30% | Rule E evidence, technical, size and stop process |
| Cash | residual | retained whenever a component has no valid authorization |

Read [CURRENT_STRATEGY.md](CURRENT_STRATEGY.md) and
[STRATEGY_OPERATING_MODEL.md](STRATEGY_OPERATING_MODEL.md) before running the
strategy. Index-core market-context checklist (monitor only, not a weight
override):
[../../references/v9-index-core-momentum-monitor.md](../../references/v9-index-core-momentum-monitor.md).
Behavioral-finance and momentum-crash implications, evidence boundaries and
the pre-registered validation backlog are documented in
[BEHAVIORAL_MOMENTUM_SUPPLEMENT.md](BEHAVIORAL_MOMENTUM_SUPPLEMENT.md). That
supplement is research-only and does not authorize a V9 rule change.
Pre-registered validation contracts and experiment outputs live under
[validation/](validation/) and [results/validation/](results/validation/).

## Validation workflow

```powershell
$py = 'D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe'
& $py scripts/download_ff_momentum.py
& $py scripts/build_v9_pit_universe.py
& $py scripts/build_approx_wml_legs.py
& $py scripts/run_v9_validation_experiments.py
& $py scripts/freeze_v9_rule_e.py --replace   # engineering only while dirty
& $py scripts/run_v9_shadow.py --dry-run --initialize
& $py scripts/run_v9_shadow.py --dry-run --as-of YYYY-MM-DD
& $py scripts/audit_shadow_forward_launch.py
& $py scripts/write_v9_plan_completion_audit.py
```

Research monitors (`scripts/v9_research_monitors.py`) feed daily/shadow
`diagnostics` only. They never override MA150/MA200, Fear Gate execution
rails, Rule E, stops, or 70/30 ceilings. Formal forward requires a clean
committed freeze (`forward_eligible=true`).

## Formal append-only forward

First executable completed session after the current freeze: see
[validation/formal-forward-monday-runbook.md](validation/formal-forward-monday-runbook.md).
PIT event gate status and what will **not** close the 18/50 gap:
[validation/pit-event-gap-analysis.md](validation/pit-event-gap-analysis.md).

```powershell
$py = 'D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe'
& $py scripts/preflight_formal_forward.py 2026-07-13
& $py scripts/download_v9_data.py --completed-through 2026-07-13
# Optional new observation (copy validation/event-append-template.json first):
# & $py scripts/append_shadow_event.py --forward --event-json path\to\event.json
& $py scripts/run_v9_shadow.py --as-of 2026-07-13
& $py scripts/report_pit_event_gap.py
& $py scripts/audit_shadow_forward_launch.py
```

Do not backfill dates at or before freeze time. Do not re-freeze after daily
forward states exist unless starting a new versioned genesis.

## Execution workflow

All signals use completed bars and are subject to human review. Nothing here
sends an order to a broker.

```powershell
python scripts/download_v9_data.py --completed-through YYYY-MM-DD
python scripts/run_v9_daily_execution.py
python scripts/v9_signal.py --json
```

The downloader writes atomically only after every required proxy reaches the
declared session. It records per-symbol provenance and uses official Cboe
history for VIX/VIX3M, preventing a stale volatility term structure from
silently entering the Fear Gate.

For the append-only shadow ledger:

```powershell
python scripts/run_v9_shadow.py --as-of YYYY-MM-DD
```

## Active code

- `v9_information_strategy.py`: portfolio rules, sizing, technical exits and
  embedded SPY/QQQ index-core allocation.
- `v9_data.py`: completed-bar data loading.
- `run_v9_daily_execution.py`, `v9_signal.py`: daily human-review outputs.
- `shadow_*.py`, `freeze_v9_rule_e.py`: forward-state integrity controls.
- `test_v9_*.py`, `test_shadow_*.py`, `test_manual_lifecycle.py`: active
  regression coverage.

Historical V0–V8 and V9.1 research is deliberately separated under
`../research-archive/`; it cannot be cited as execution authorization.
