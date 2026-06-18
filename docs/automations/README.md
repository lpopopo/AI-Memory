# Codex Local Automations

This directory records the local Codex cron automations currently installed on this machine for the AI-Memory quant-strategy workflow.

Source snapshot:

- Host path: `C:\Users\lp\.codex\automations`
- Repository workspace used by the automations: `D:\code\AI-Memory`
- Snapshot date: `2026-06-19`

These files are a portable backup/reference. They do not create, update, pause, or delete the live Codex automations by themselves.

## Active Local Automations

| ID | Name | Schedule | Timezone expectation | Purpose | Config |
| --- | --- | --- | --- | --- | --- |
| `automation-2` | 美股开盘资讯与个股操作建议 | Monday-Friday 21:30 | Beijing / Asia-Shanghai | U.S. stock open prep: public-source checks, institutional research deltas, watchlist review, quote/K-line validation, and candidate operation checklist. | [`automation-2/automation.toml`](automation-2/automation.toml) |
| `automation-3` | 盘中执行清单、持仓记账与策略复盘 | Monday-Friday 23:15 | Beijing / Asia-Shanghai | Intraday execution prep, portfolio ledger sync, preliminary review, todo maintenance, and layered memory updates. | [`automation-3/automation.toml`](automation-3/automation.toml) |
| `automation-5` | 美股盘后正式审计 | Tuesday-Saturday 04:15 | Beijing / Asia-Shanghai | Formal U.S. post-close audit: close triggers, market-fear gate, portfolio risk/NAV audit, replay rows, and memory updates. | [`automation-5/automation.toml`](automation-5/automation.toml) |
| `automation-6` | 四大机构研究周度深度学习 | Sunday 10:00 | Beijing / Asia-Shanghai | Weekly AQR, Citadel Securities, GMO, and Man Institute research study for reusable frameworks, hypotheses, and backtest/replay ideas. | [`automation-6/automation.toml`](automation-6/automation.toml) |

## Not Found Locally

Historical memory notes mention these automation IDs, but they were not present under `C:\Users\lp\.codex\automations` in this snapshot:

- `automation`
- `automation-4`

Treat those as historical/deleted unless the live Codex automation store is later updated.

## Safety Notes

- The task prompts intentionally prohibit broker login, real order submission, and fabricated fills.
- Real account facts must come from user confirmation or broker statements, not from automation inference.
- Keep credentials, cookies, brokerage private data, and account tokens out of this repository.
- Only promote stable, verified strategy rules to `domains/quant-strategy/memory/decisions.md`.

## Restore / Compare

To compare a live automation against this snapshot, inspect the live `automation.toml` for the same ID and diff it against the matching file here.

To restore manually, use Codex's automation management UI/tooling and copy the fields from the relevant TOML:

- `name`
- `prompt`
- `status`
- `rrule`
- `model`
- `reasoning_effort`
- `execution_environment`
- `cwds`

