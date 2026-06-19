---
name: ai-memory-loader
description: Load the user's local AI-Memory repository from D:\code\AI-Memory. Use when the user says to load AI-MEMORY, AI-Memory, memory, strategy memory, quant-strategy memory, or asks to continue US stock, portfolio, trading, quant, market monitoring, or investment strategy work from prior memory.
---

# AI Memory Loader

Use this skill to load the user's portable AI working memory before answering strategy, market, portfolio, or quant-research requests.

## Default Path

The memory repository is:

```text
D:\code\AI-Memory
```

If the path is missing, search `D:\code` for `AI-Memory` before asking the user.

## Loading Order

Read only the files needed for the current task, in this order:

1. `D:\code\AI-Memory\README.md`
2. `D:\code\AI-Memory\docs\memory-architecture.md`
3. For the active domain, usually `quant-strategy`:
   - `D:\code\AI-Memory\domains\quant-strategy\memory\summary.md`
   - `D:\code\AI-Memory\domains\quant-strategy\memory\decisions.md`
   - `D:\code\AI-Memory\domains\quant-strategy\memory\daily-summaries.md`
   - the most recent relevant files under `memory\daily\`
4. Read `hypotheses.md` when evaluating unproven strategy ideas.
5. Read `references\` files only when their rules are needed for the current request.

For US stock strategy work, the most commonly needed references are:

- `references\market-fear-technical-framework.md`
- `references\portfolio-concentration-rules.md`
- `references\daily-market-monitoring-framework.md`
- `references\us-stock-strategy-blueprint.md`

## Operating Rules

- Treat stable conclusions in `memory\decisions.md` as the default strategy rules unless the user explicitly revises them.
- Treat daily notes as historical context, not automatically current market recommendations.
- For prices, news, market regime, earnings, and daily recommendations, refresh current data before acting because those facts change.
- Do not load large experiment datasets unless the user asks for backtesting, validation, or data inspection.
- Keep secrets, brokerage credentials, cookies, tokens, and personal account data out of memory updates.

## Expected Strategy Defaults

When continuing US stock strategy work:

- Prioritize US-listed equities and ETFs.
- Use the market fear gate before stock-level buy recommendations.
- Prefer concentrated portfolios: target 4 to 6 active stocks, hard maximum 8.
- Prefer 2 to 3 clear themes at one time.
- Separate core positions from speculative satellite positions.
- Map hot news to macro, sector, theme, and ticker catalysts, then confirm against price action and risk controls.

## Updating Memory

When the user asks to save or update memory:

- Put stable process changes in `memory\decisions.md`.
- Put daily observations in `memory\daily\YYYY-MM-DD-*.md`.
- Append one concise line to `memory\daily-summaries.md`.
- Put factual source contracts or reusable frameworks in `references\`.
- Use concise entries and link to supporting files instead of duplicating large content.
