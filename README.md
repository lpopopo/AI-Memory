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

## Current Contents

- `domains/quant-strategy`: 量外策略 research memory.
- `skills/quant-stock-data`: Tencent/Sina resilient stock data-source skill.

## How To Store New Memory

1. Put stable conclusions in `domains/<domain>/memory/decisions.md`.
2. Put running notes and open questions in `domains/<domain>/memory/strategy-log.md`.
3. Put API contracts, field maps, schemas, and external facts in `domains/<domain>/references/`.
4. Put reusable AI workflows and code helpers in `skills/<skill-name>/`.
5. Move obsolete material to `archive/` instead of deleting important history.

## Rules

- Keep secrets, brokerage credentials, cookies, tokens, and personal account data out of this repository.
- Prefer concise entries with links to supporting files.
- Promote useful repeated workflows into skills.
- Commit memory updates with clear messages.
