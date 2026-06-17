# 2026-06-14 Strategy Todos

Run time: 2026-06-14 23:30 Asia/Shanghai.

## Open

### 1. VIX/VIX3M term structure source

- Problem: Local Tencent VIX remains stale-looking with zero OHLC/volume, while external pages can provide VIX close but not the full synchronized VIX/VIX3M term structure.
- Impact: The market fear gate should stay `elevated / repair watch`, not `normal`, even though the 2026-06-12 tape repaired.
- Possible cause: Local quote source does not provide complete volatility-index fields.
- Repair suggestion: Add or verify a reliable VIX and VIX3M close source for post-close audits.
- Validation method: post-close audit records synchronized VIX, VIX3M, and term-structure interpretation.
- Next step: keep VIX/VIX3M as the highest-priority data gap.

### 2. AMD replay repair confirmation

- Problem: AMD reclaimed the historical replay `492` line in the 2026-06-12 completed-session row, but this is a replay label change, not a real-account action.
- Impact: Treating repair as a new buy signal could rebuild AI compute beta too early.
- Possible cause: Strong semiconductor follow-through after a stress-to-repair sequence.
- Repair suggestion: Keep AMD real-account status as watch-only; require sustained closes above `492-500`, RS versus QQQ/SMH, and a technical entry basis before any candidate ranking.
- Validation method: next formal close and relative-strength review.
- Next step: no real order unless user confirms and entry basis is explicit.

### 3. WDC/STX whipsaw-recovery replay

- Problem: WDC and STX recovered sharply above their historical replay risk lines after near-stop/reduce-review conditions.
- Impact: The overlay replay needs to measure whether the earlier caution reduced drawdown or created avoidable missed rebound.
- Possible cause: Storage and AI capex beta recovered quickly with semiconductor leadership.
- Repair suggestion: Continue replay rows only from completed closes; compare baseline and overlay actions across the stress-to-repair window.
- Validation method: replay ledger notes and follow-through rows.
- Next step: keep WDC/STX real-account watch-only; do not add without support/reclaim basis and small-account sizing check.

### 4. MRVL fresh re-entry rule

- Problem: MRVL remains above the real exit price, creating opportunity-cost pressure, but it is still not a clean technical re-entry.
- Impact: Automatic rebuy would violate the account-size and no-chase discipline.
- Possible cause: Confusion between profit-capture exit and stop-defense exit.
- Repair suggestion: Define fresh setup language: controlled pullback, reclaim, VWAP/support behavior, and QQQ/SMH confirmation.
- Validation method: any future MRVL order plan states technical basis, invalidation, and account-size impact.
- Next step: keep MRVL `watch only / no chase`.

### 5. Theme-crowding overlay follow-through

- Problem: Historical MRVL/AMD/WDC/STX still express overlapping AI capex / semiconductor / storage beta.
- Impact: Buying multiple repaired names together could recreate the same concentrated risk after one rebound.
- Possible cause: Rebound strength is clustered in the same high-beta themes.
- Repair suggestion: If future exposure is allowed, choose one best starter rather than rebuilding the basket.
- Validation method: portfolio construction review shows theme count, overlap, and max single-name impact.
- Next step: keep `theme_overlap_high` active for historical replay basket.

### 6. Institutional checker retry

- Problem: `institutional-research-checker.js` timed out and wrote no completed output in this run.
- Impact: No new AQR/Citadel/GMO/Man item can be promoted or summarized from this run.
- Possible cause: network latency or official-site/Jina reader access slowdown.
- Repair suggestion: Retry with a longer timeout or split by institution if institutional source coverage is required.
- Validation method: completed Markdown and JSON diagnostics.
- Next step: record as source gap, not as evidence of no institutional research.

### 7. Real-account confirmations

- Problem: Real-account cash, settlement, fees, FX, tax, margin status, and any old MRVL broker-side order remain unconfirmed.
- Impact: Equity exposure is confirmed as 0%, but final cash/NAV and open-order state cannot be written.
- Possible cause: No sanitized broker/account confirmation in memory.
- Repair suggestion: Record only user-confirmed non-sensitive facts; keep credentials and private account details out of memory.
- Validation method: user-confirmed sanitized cash/order status.
- Next step: no new real trade or order record without user confirmation.

## Completed / Verified This Run

- Node quote workflow smoke test returned structured Tencent quote objects; Python fallback and Google browser-visible fallback were not required.
- Existing 2026-06-12 replay row is present; no future rows were prefilled.
- Real account remains `cash / no confirmed equity holdings`.
