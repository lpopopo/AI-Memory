# 2026-06-04 Strategy Todos

Run time: 2026-06-04 23:32 Asia/Shanghai / 11:32 ET.

## Open

### 1. Add or schedule a post-close daily audit

- Problem: the 2026-06-04 review ran at 23:32 Asia/Shanghai / 11:32 ET, before the U.S. close.
- Impact: official close prices, close-based stops, final breadth, final fear inputs, and model-account day-end value remain unverified.
- Possible cause: automation timing is aligned to China evening rather than after the U.S. regular session.
- Repair suggestion: keep this run as an intraday review and add a post-close audit, or move the formal review to after about `04:15` Asia/Shanghai during U.S. daylight-saving time.
- Validation method: the next final daily detail must include official closes for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, breadth/credit proxies, stop checks, and model portfolio value.
- Next step: ask the user whether to split the automation or move the final review time.

### 2. Confirm MRVL real-account execution status

- Problem: the strategy plan authorizes MRVL profit-protection sells, but no user/broker fill confirmation exists.
- Impact: the memory can only maintain a model plan, not an actual execution ledger; if the `>=315` sell was not placed in time, profit protection may have been missed.
- Possible cause: real brokerage data is intentionally unavailable, and memory should not store private account details.
- Repair suggestion: keep real fills, pending plans, and model fills separate; only mark a real trade when the user confirms non-sensitive facts: ticker, direction, quantity, and price.
- Validation method: future portfolio records must reconcile only confirmed real fills or explicitly labeled model fills.
- Next step: user should confirm whether the MRVL `2.50` share sell or `1.50` share defensive trim was submitted or filled.

### 3. Validate a "good news, bad price" AI-crowding filter

- Problem: AVGO/CRWD/NVDA/MRVL-related evidence shows strong AI fundamentals or product news, but price action has punished crowded expectations.
- Impact: without a mechanical filter, the strategy may rotate into AI application names or add AI infrastructure exposure before price confirms.
- Possible cause: the market fear gate handles market-wide stress better than same-theme euphoria and expectation-reset risk.
- Repair suggestion: when a key AI peer sells off after strong news or guidance, block same-theme new buys for at least one trading day and prioritize profit protection on extended holdings.
- Validation method: track AVGO, CRWD, MRVL, NVDA, SMH, IGV, and the active model portfolio over the next 1-5 trading days before promotion to `decisions.md`.
- Next step: continue observation; do not promote to stable rule yet.

### 4. Repair or replace the live quote refresh path

- Problem: local Stooq quote refresh failed again with an inability to connect to the remote server.
- Impact: intraday review and execution plan rely on stale prior-close snapshots, reducing precision for stops, position value, and market-state checks.
- Possible cause: local network restriction or source availability issue.
- Repair suggestion: add a fallback path such as browser-fetched Stooq/Yahoo/StockAnalysis snapshots, cached CSV import, or a small manually supplied quote table for the post-close audit.
- Validation method: next review should either fetch fresh data successfully or explicitly include a verified fallback source and timestamp.
- Next step: test fallback quote workflow before the next formal review.
