# AI-Memory

This repository stores reusable AI working memory, Codex skills, and domain research notes that should travel across machines.

## Memory Design

Read [`docs/memory-architecture.md`](docs/memory-architecture.md) for the full storage model.

Short version:

- `docs/`: Repository-level memory design and operating rules.
- `domains/`: Topic-specific memory, decisions, references, and logs.
- `skills/`: Portable Codex skills and helper scripts.
- `templates/`: Starter files for new memory domains.
- `archive/`: Deprecated or inactive material kept for traceability.
- `docs/automations`: Snapshot of local Codex cron automations for this repository.

## Current Contents

- `domains/quant-strategy`: 量外策略 research memory.
- `skills/quant-stock-data`: Tencent/Sina resilient stock data-source skill.

## How To Store New Memory

1. Put high-level current state in `domains/<domain>/memory/summary.md`.
2. Put daily running notes in `domains/<domain>/memory/daily/<YYYY-MM-DD>-details.md` and append a high-level timeline to `daily-summaries.md`.
3. Put stable conclusions in `domains/<domain>/memory/decisions.md`.
4. Put API contracts, field maps, schemas, and external facts in `domains/<domain>/references/`.
5. Put reusable AI workflows and code helpers in `skills/<skill-name>/`.
6. Move obsolete material to `archive/` instead of deleting important history.

## Rules

- Keep secrets, brokerage credentials, cookies, tokens, and personal account data out of this repository.
- Prefer concise entries with links to supporting files.
- Promote useful repeated workflows into skills.
- Commit memory updates with clear messages.
