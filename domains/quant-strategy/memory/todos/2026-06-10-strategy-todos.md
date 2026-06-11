# 2026-06-10 Strategy Todos

Run time: 2026-06-10 08:22 Asia/Shanghai.

## Open

### 1. Keep real account and model portfolio strictly separate

- Problem: 2026-06-10 starts the first confirmed real-account MRVL position, while older MRVL/AMD/WDC/STX records are model portfolio notes.
- Impact: mixing them could create false real holdings, false realized P/L, or incorrect order assumptions.
- Possible cause: previous strategy work used a USD 20,000 model ledger before the HKD 20,000 real account was started.
- Repair suggestion: all real trades go under `real account` notes and require user/broker confirmation; model trades remain clearly labeled.
- Validation method: future trade and portfolio files must include account scope.
- Next step: do not record AMD/WDC/STX as real holdings unless user confirms them.

### 2. Formal U.S. post-close audit completed

- Status: completed in `memory/daily/2026-06-10-post-close-audit.md`.
- Result: 2026-06-09 close table, market fear gate, stop-trigger table, institutional overlay scorecard, model NAV, and replay-ledger check were written.
- Remaining data gaps: VIX is still MarketWatch intraday-only, VIX/VIX3M was unavailable, and HYG/LQD had mismatched timestamps.
- Next step: keep future post-close audits separate from intraday/session reviews and continue requiring data-quality labels.

### 3. Confirm MRVL real-position risk state

- Problem: MRVL has a real starter fill at `252`, but latest usable price is only a session snapshot around `261.09`.
- Impact: adding too quickly could overconcentrate the small HKD 20,000 account in one high-volatility AI capex supplier.
- Possible cause: starter position entered during a volatile semiconductor tape.
- Repair suggestion: no add while SMH/QQQ keep weakening; use `<245` close as cut/wait review and `<235` as thesis-failure review.
- Validation method: compare official MRVL close with `245/235` risk levels and SMH/QQQ condition.
- Next step: wait for official close or user-confirmed broker snapshot.

### 4. Resolve AMD close-stop status versus `492`

- Problem: AMD remains the unresolved highest-priority model risk item from prior plans.
- Impact: treating AMD as ordinary hold without official recovery violates stop discipline.
- Possible cause: intraday rebounds have been considered before official close confirmation.
- Repair suggestion: classify the next verified close as still stop-triggered (`<492`) or repaired/override (`>=492` with reason).
- Validation method: official close only; no intraday substitution.
- Next step: keep AMD first in the model execution checklist until closed.

### 5. Keep WDC/STX in near-stop defensive review

- Problem: WDC/STX remain high capex-cycle, same-theme exposures after recent near-stop stress.
- Impact: storage exposure could compound theme-crowding drawdown if AI infrastructure weakens again.
- Possible cause: storage thesis is valid but still synchronized with AI capex flow risk.
- Repair suggestion: require 1-3 verified closes above WDC `500` and STX `835`, with relative strength versus SMH, before upgrading language.
- Validation method: official close table plus storage/SMH relative behavior.
- Next step: no add while this todo is open.

### 6. Add verified replay rows for institutional overlays

- Problem: replay ledger has 2026-06-05 and 2026-06-08 rows, but no later verified close row.
- Impact: theme-crowding overlay cannot be evaluated over the intended T2-T5 window.
- Possible cause: future rows must not be prefilled without data.
- Repair suggestion: append rows only after official close data is available.
- Validation method: every row must include prices, fear state, flow-fragility, trend-aligned state, factor flags, baseline action, overlay action, and data quality.
- Next step: add the next verified close row during the post-close audit.

### 7. Repair and label live quote workflow

- Problem: local Tencent/Sina quote test returned an empty array; Tencent failed and Sina reported `connect EACCES`.
- Impact: intraday quote refresh and model value cannot rely on the local script.
- Possible cause: environment network restrictions and public endpoint fragility.
- Repair suggestion: use an explicit fallback hierarchy: local quote script, public snapshot, manual official close table; label `official close`, `session snapshot`, or `unavailable`.
- Validation method: next run should either return non-empty quote objects or preserve the exact failure path.
- Next step: keep this open and do not treat failed script output as market evidence.

### 8. Confirm whether any old MRVL `315` real-account order exists

- Problem: older notes still mention a possible MRVL `315` real-account limit order, but the new confirmed real position is a separate `1` share buy at `252`.
- Impact: an unmanaged old order could conflict with current starter-position risk controls.
- Possible cause: brokerage order state is intentionally not stored in memory.
- Repair suggestion: user checks broker order page and confirms whether any old `315` sell order exists.
- Validation method: only user or broker report can close this.
- Next step: do not record any real sell or cancellation without confirmation.
