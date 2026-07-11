# Strategy Version Registry

| Version | Status | Role | Authoritative entry point |
| --- | --- | --- | --- |
| V0-V4 | Archived research | Early ETF and return-engine experiments | Historical scripts and reports only |
| V5-V7 | Rejected for promotion | Scanners; historical claims are affected by universe limitations | Point-in-time reports only |
| V8 | **Promoted baseline** | Defensive SPY/QQQ core | `scripts/v8_signal.py --version v8` |
| V8.1-V8.7 | Rejected/research-only | Attempted V8 enhancements | Version-specific tests and reports |
| V9-A | Forward control | Strict information-strategy baseline | Official shadow runner |
| V9-E | **Frozen forward experiment** | Rule E waitlist/state-machine challenger | `scripts/run_v9_shadow.py` |

## Directory policy

- `scripts/`: reproducible source and tests. Historical scripts remain for auditability.
- `datasets/`: source snapshots and point-in-time event records.
- `results/`: reports and audit evidence; generated CSV/JSON and live forward state are ignored where configured.
- `results/shadow_portfolio/forward/`: immutable official forward state.
- `results/shadow_portfolio/dry_run/`: disposable isolated rehearsals.
- `task.md` and `walkthrough.md`: retained experiment audit trails.

Do not delete a rejected strategy merely because it failed. Delete only caches,
temporary logs, scratch work, and reproducible generated artifacts. A failed
strategy and its report are evidence against repeating the same experiment.

