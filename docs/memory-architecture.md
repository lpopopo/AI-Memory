# Memory Architecture

This document defines the long-term storage pattern for `AI-Memory`. The goal is to make memory portable across machines, easy for AI agents to load, and stable enough to support long-running research.

## Design Goals

- Keep durable conclusions separate from temporary thinking.
- Make every memory item easy to locate by domain, type, and maturity.
- Store reusable operating knowledge as skills, not as loose notes.
- Keep raw references close to the domain that uses them.
- Avoid secrets, account data, cookies, tokens, and private brokerage credentials.

## Layer Model

`AI-Memory` uses five memory layers.

| Layer | Path | Purpose | Typical files |
| --- | --- | --- | --- |
| L0 Entry Index | `README.md` | Human and AI entry point | Repository map, rules, quick links |
| L1 Domain Memory | `domains/<domain>/memory/` | Stable research memory and daily logs for one topic | `summary.md`, `daily-summaries.md`, `daily/` |
| L2 Domain References | `domains/<domain>/references/` | Source contracts, external docs, field maps, schemas | `data-sources.md`, `api-contracts.md`, `schemas.md` |
| L3 Reusable Skills | `skills/<skill-name>/` | Portable Codex skills and executable helpers | `SKILL.md`, `references/`, `scripts/` |
| L4 Archive | `archive/` | Deprecated or inactive material kept for traceability | Dated snapshots, retired experiments |

## Recommended Directory Shape

```text
AI-Memory/
├── README.md
├── docs/
│   └── memory-architecture.md
├── templates/
│   ├── domain-decisions.md
│   └── domain-strategy-log.md
├── domains/
│   └── <domain>/
│       ├── README.md
│       ├── memory/
│       │   ├── summary.md
│       │   ├── decisions.md
│       │   ├── daily-summaries.md
│       │   └── daily/
│       │       └── YYYY-MM-DD-details.md
│       └── references/
│           └── data-sources.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
└── archive/
```

Not every domain needs every file on day one. Add files only when they have a clear role.

## Memory Types

### Decisions

Use `memory/decisions.md` for stable conclusions that future sessions should trust unless explicitly revised.

Each decision should include:

- Date
- Decision
- Reason
- Impact
- Revision trigger

### Top-level Summary

Use `memory/summary.md` as the main entry point for the AI to understand the current state, primary goal, and latest status of the domain. It provides a high-level overview of the entire domain.

### Daily Summaries

Use `memory/daily-summaries.md` to append a concise summary for each day of work. This provides a fast timeline of progress without needing to read detailed logs.

Good entries include:
- Date
- Key actions taken
- Main conclusion for the day

### Daily Detailed Memory

Use `memory/daily/<YYYY-MM-DD>-details.md` for running notes, open questions, session details, and experiment logs for a specific day. This replaces the old monolithic strategy-log.

Good entries include:
- What changed
- Detailed experiment observations
- What was learned
- What remains uncertain
- Next concrete step

### Hypotheses

Use `memory/hypotheses.md` for unproven ideas that need validation. Promote a hypothesis to `decisions.md` only after evidence or implementation confirms it.

### References

Use `references/` for semi-stable external knowledge: API contracts, endpoint field maps, data dictionaries, provider caveats, formulas, and schemas.

References should be factual and source-oriented. Avoid mixing strategy opinions into reference files.

### Skills

Use `skills/` for reusable AI operating knowledge. A skill is appropriate when the same workflow, API, data source, or coding pattern will be reused across sessions.

Skills should stay portable:

- Keep `SKILL.md` concise.
- Put detailed docs in `references/`.
- Put repeatable code in `scripts/`.
- Do not store machine-specific absolute paths inside skill files unless unavoidable.

## Maturity Flow

Memory should move through maturity stages:

```text
raw note -> strategy log -> hypothesis/reference -> decision/skill -> archive
```

Use this flow:

1. Capture daily detailed thinking in `daily/<date>-details.md`.
2. Append a brief summary to `daily-summaries.md` at the end of the day.
3. Update `summary.md` with any major status changes.
4. Move factual contracts into `references/`.
5. Move reusable workflows into `skills/`.
6. Promote validated conclusions into `decisions.md`.
5. Move obsolete material into `archive/` with a short reason.

## Naming Rules

- Use lowercase kebab-case for directories and files.
- Use domain names that describe the research area, for example `quant-strategy`.
- Use skill names that describe the reusable capability, for example `quant-stock-data`.
- Prefer stable file names over date-heavy names for living memory.
- Use dated files only for snapshots, experiment outputs, or archive records.

## Update Rules

Before adding memory:

1. Decide whether it is a decision, working note, reference, skill, or archive item.
2. Place it in the lowest layer that can serve future retrieval.
3. Keep entries concise and link to supporting files instead of duplicating text.
4. Do not add secrets or credentials.
5. Commit changes with a message that states the memory change, not just "update".

## Retrieval Rules For AI Agents

When starting work:

1. Read root `README.md`.
2. Read this architecture document when unsure where to store something.
3. For a specific topic, read that domain's `memory/summary.md` and `memory/decisions.md` first.
4. Read `memory/daily-summaries.md` to understand recent timeline progress.
5. Read recent `memory/daily/<date>-details.md` files for current open context.
6. Read `references/` only when the task needs factual contracts.
7. Read skill `SKILL.md` only when the task matches that reusable capability.

## Current Domains

| Domain | Path | Status |
| --- | --- | --- |
| 量外策略 / Quant Strategy | `domains/quant-strategy/` | Active |

## Current Skills

| Skill | Path | Purpose |
| --- | --- | --- |
| Quant Stock Data | `skills/quant-stock-data/` | Tencent/Sina resilient stock data source workflow |
