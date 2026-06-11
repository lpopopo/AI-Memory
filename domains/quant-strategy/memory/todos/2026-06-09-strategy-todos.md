# 2026-06-09 Strategy Todos

Run time: 2026-06-09 23:30 Asia/Shanghai / 11:30 ET.

## Open

### 1. Complete the formal U.S. post-close audit

- Problem: this 23:30 run is still U.S. intraday and cannot finalize close-trigger rules.
- Impact: AMD close-stop, WDC/STX near-stop, MRVL risk/profit-protection levels, model NAV, and replay ledger remain provisional.
- Possible cause: intraday review and post-close audit are separate automations.
- Repair suggestion: the 04:15 post-close task must write the official close table and stop-trigger status.
- Validation method: include MRVL/AMD/WDC/STX/SPY/QQQ/SMH/VIX closes, fear state, stop table, model value, and action classification.
- Next step: close or carry this item after the 04:15 audit.

### 2. Confirm AMD close-stop status versus `492`

- Problem: AMD previously closed below `492` on 2026-06-05 and remains the first-priority risk item.
- Impact: if the next official close fails to reclaim `492`, treating AMD as ordinary hold-only would violate the existing stop review process.
- Possible cause: delayed post-close review and reliance on intraday recovery snapshots.
- Repair suggestion: classify the next official close as either still stop-triggered (`<492`) or delayed-trigger override (`>=492`, with documented reason).
- Validation method: use official close, not intraday price; record whether model reduction or explicit override is required.
- Next step: keep AMD at the top of the execution checklist until resolved.

### 3. Keep WDC/STX defensive until 1-3 closes confirm recovery

- Problem: WDC/STX rebounded intraday on 2026-06-08 but had recently approached stop zones (`500` and `835`).
- Impact: one intraday rebound could falsely restore strong-hold language and increase theme-overlap risk.
- Possible cause: storage theme remains fundamentally interesting, but flow fragility and synchronized selloff risk are still elevated.
- Repair suggestion: require 1-3 official closes above risk lines and relative strength versus SMH before upgrading from defensive hold.
- Validation method: track WDC `500`, STX `835`, storage relative strength, and whether SMH confirms or fades.
- Next step: do not add storage exposure while this todo is open.

### 4. Add post-close replay rows for the institutional overlay

- Problem: the replay ledger now has T0 2026-06-05 close, a 2026-06-08 intraday snapshot, and a completed 2026-06-08 close row, but it still needs 2026-06-09 and later verified close rows.
- Impact: H7-H9 and the theme-crowding overlay still cannot be evaluated over a multi-day window.
- Possible cause: future close rows must not be invented before data exists.
- Repair suggestion: append official close rows only after data is verified; keep baseline and overlay action assumptions explicit.
- Validation method: every row must include timestamp, data quality, prices, fear state, flow-fragility state, trend-aligned state, factor flags, and baseline/overlay action.
- Next step: add 2026-06-09 close after the post-close audit, then continue the T2-T5 replay window without pre-filling future data.

### 5. Repair and label the live quote fallback workflow

- Problem: Tencent/Sina quote fetch returned no quotes; Sina failed with `connect EACCES`.
- Impact: intraday model value and fear proxies cannot be reliably refreshed from local scripts.
- Possible cause: environment network restrictions and public endpoint fragility.
- Repair suggestion: maintain a fallback hierarchy: local quote script, browser/public snapshot, manual close table; label each datapoint as `official close`, `intraday snapshot`, or `unavailable`.
- Validation method: next audit must cite one repeatable source path or explicit data-gap label for each active ticker and index proxy.
- Next step: test quote workflow again during post-close audit and avoid using failed fetches as market evidence.

### 6. Confirm MRVL old `315` real-account limit order status

- Problem: local memory still cannot verify whether the user's real account has an old MRVL `315` limit sell order.
- Impact: an unmanaged old order may execute contrary to the current no-chase/no-new-order plan.
- Possible cause: real brokerage state is intentionally not stored in memory.
- Repair suggestion: user should confirm in the broker whether the order exists and whether to cancel/modify it.
- Validation method: only user or broker execution/order report can close this item.
- Next step: keep this as user-confirmation item; do not record any real fill without explicit confirmation.
