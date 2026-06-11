# 2026-06-11 Strategy Todos

Run time: 2026-06-11 08:25 Asia/Shanghai.

## Open

### 1. Confirm MRVL real-position risk state versus 245 and 235

- Problem: MRVL official close was `252.59`, but after-hours traded around `244.55`, below the existing 245 review line.
- Impact: a confirmed official close below 245 would require cut-or-wait review for the only real holding.
- Possible cause: renewed AI/semiconductor selloff, elevated VIX, and weak SMH/QQQ tape.
- Repair suggestion: no add; use official close only for the formal trigger and monitor 235 with QQQ/SMH weakness as thesis-failure review.
- Validation method: next official close table; do not substitute after-hours for close trigger.
- Next step: keep for the 04:15 post-close audit or next official close review.

### 2. Real account is the only current portfolio scope

- Problem: user clarified that the historical model ledger should no longer be tracked in routine work.
- Impact: including model AMD/WDC/STX in daily audit tables creates confusion and distracts from the actual real-account risk.
- Possible cause: prior automation prompt still asked to audit the model portfolio after the user had retired it.
- Repair suggestion: future portfolio files should list only user-confirmed real holdings; historical model/replay notes should be omitted unless explicitly requested.
- Validation method: every trade/portfolio file includes account scope.
- Next step: daily execution/post-close audit should focus on MRVL real holding and any later broker-confirmed real positions only.

### 3. Historical model stop/replay cleanup for AMD, WDC, and STX

- Status: closed for routine daily work by user instruction.
- Result: do not track AMD/WDC/STX model stop state in current daily execution or post-close audit.
- Reopen condition: user explicitly asks for historical model replay, backtest diagnostics, or old ledger reconciliation.

### 4. Repair and label live quote workflow

- Problem: local Tencent/Sina quote workflow returned an empty array again.
- Impact: intraday automation cannot depend on local quotes for triggers or NAV.
- Possible cause: Tencent `fetch failed`; Sina fallback blocked with `connect EACCES 198.18.0.42:443`.
- Repair suggestion: add explicit source-level health output and keep public snapshot/manual close fallback.
- Validation method: next smoke test returns normalized quote objects or exact source failures.
- Next step: keep open; do not treat failed output as market evidence.

### 5. Confirm whether any old MRVL 315 real-account order exists

- Problem: older notes mention a possible MRVL `315` real-account sell limit, but the only confirmed real fill is 1 MRVL at 252.
- Impact: an unmanaged old order could conflict with current starter-position risk controls.
- Possible cause: brokerage order state is intentionally not stored in memory.
- Repair suggestion: user checks broker order page and confirms whether the old order exists.
- Validation method: only user/broker report can close this.
- Next step: do not record any real sell, cancellation, or amendment without confirmation.

### 6. Confirm VIX/VIX3M and credit proxies in formal audit

- Problem: VIX was refreshed only from live coverage around 21, while VIX/VIX3M and HYG/LQD official close data were not reliably captured.
- Impact: risk regime cannot be downgraded from `elevated, stress-leaning`.
- Possible cause: public-data access limits and mismatched timestamps.
- Repair suggestion: use official close/consistent timestamp sources in the post-close audit.
- Validation method: record timestamp and source quality for each proxy.
- Next step: keep elevated risk until confirmed otherwise.

## Completed By Formal Post-Close Audit

- Created `memory/daily/2026-06-11-post-close-audit.md`.
- Appended the completed 2026-06-10 close row to the institutional overlay replay ledger.
- Updated `memory/portfolio/2026-06-11-portfolio-summary.md` with formal post-close NAV and risk state.
- Confirmed that no `decisions.md` update is justified from this single-day audit.
