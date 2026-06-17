# 2026-06-16 Strategy Todos

Run time: 2026-06-16 09:01 Asia/Shanghai.

## Open

### 1. RDW near-stop review

- Problem: Latest structured quote / post-close snapshot showed RDW `14.83`, below gross entry `15.00` and below fee-adjusted entry about `15.20`.
- Impact: The satellite position is already under fee-adjusted water and could become a small-account drag.
- Possible cause: high-volatility space/satellite exposure underperformed while AI/semiconductor leaders rallied.
- Repair suggestion: no average-down; review exit/hold if a future completed close is below `14.50`.
- Validation method: close table plus fee-adjusted P/L.
- Next step: keep RDW as first real-account risk item.

### 2. MRVL profit-protection review

- Problem: Latest structured quote / post-close snapshot showed MRVL `308.88`, well above the `289.50` real entry after a sharp move.
- Impact: The position is working, but the account should not turn a starter win into an add/chase decision.
- Possible cause: AI interconnect/custom-silicon theme strength and broad QQQ/SMH risk-on.
- Repair suggestion: hold starter while trend confirms; review if price loses `303/300`; consider profit-protection language if `315+` appears.
- Validation method: completed close and QQQ/SMH confirmation.
- Next step: no add until a separate technical setup appears.

### 3. AMD/WDC/STX whipsaw replay

- Problem: AMD/WDC/STX repaired far above old replay risk lines, but they remain replay/watch context only.
- Impact: Treating the repair as a real-account buy signal would blur the user-confirmed real-account scope.
- Possible cause: high-beta semiconductor/storage rebound.
- Repair suggestion: update replay labels only from completed close rows; compare whether prior caution reduced drawdown or created missed rebound.
- Validation method: replay ledger rows with close prices and baseline/overlay actions.
- Next step: keep AMD/WDC/STX watch-only for real account.

### 4. Theme-crowding overlay replay

- Problem: `flow_fragility=elevated` and `theme_overlap_high` remain active while MRVL/AMD/WDC/STX/RKLB all express related growth or AI/space beta.
- Impact: Adding another hot name could recreate concentrated rebound risk.
- Possible cause: broad risk-on plus AI bottleneck and speculative satellite momentum.
- Repair suggestion: if new exposure is later allowed, choose one best confirmed setup rather than rebuilding a basket.
- Validation method: overlay note records theme count, overlap, and no-chase discipline.
- Next step: keep as post-close follow-through item.

### 5. VIX/VIX3M durable source

- Problem: Local Tencent VIX returned `21.67` with zero OHLC/volume, while the formal audit used external VIX/VIX3M references.
- Impact: Local quote workflow is verified for equities/ETFs but not enough for volatility term-structure scoring.
- Possible cause: local source field quality gap for volatility indexes.
- Repair suggestion: keep a reliable synchronized VIX and VIX3M post-close source path.
- Validation method: audit records VIX, VIX3M, term-structure interpretation, and source quality.
- Next step: keep as top data-quality gap.

### 6. Broker / account reconciliation

- Problem: broker cash, exact fees, FX, tax, settlement, margin status, and stale open orders remain unconfirmed.
- Impact: available buying power and real NAV cannot be finalized beyond estimates.
- Possible cause: sensitive broker data is intentionally excluded from memory.
- Repair suggestion: user provides only sanitized, non-sensitive cash/order facts if needed.
- Validation method: future portfolio note uses user-confirmed non-sensitive fields only.
- Next step: no new order sizing beyond watch-only without confirmation.

## Completed / Verified This Run

- Node quote smoke test returned structured `Tencent (Primary)` quote objects for the required equity/ETF universe.
- Python fallback was not needed.
- Google browser-visible fallback was not needed.
- Public checker completed; institutional checker produced date-filtered output with no post-window verified framework.
- Formal 2026-06-15 post-close audit already recorded close-based stop/NAV/replay status.
- No stable `decisions.md` update was justified.

## 23:30 Intraday Update

Run time: 2026-06-16 23:30 Asia/Shanghai. This is still `盘中初步复盘`, not a formal close trigger.

### Priority Carryover To 04:15 Audit

1. RDW close-confirmed stop / exit-review
   - Problem: Required Node smoke test returned RDW `13.92`, below the `14.50` review line intraday.
   - Impact: The satellite position is now the first real-account risk item and is below gross and fee-adjusted entry.
   - Possible cause: speculative space/satellite beta weakened; RDW also underperformed RKLB.
   - Repair suggestion: no averaging down; if official completed close remains `<14.50`, move to user-confirmed exit/stop-review in the next actionable window.
   - Validation method: 04:15 close audit table and fee-adjusted P/L.
   - Next step: confirm official close before treating this as a formal trigger.

2. MRVL profit-protection / entry-line review
   - Problem: Required Node smoke test returned MRVL `296.19`, still above the `289.50` real fill but down from the prior close `308.88`.
   - Impact: The profit cushion narrowed; a starter win should not become a chase/add decision.
   - Possible cause: QQQ/SMH cooled and MRVL failed to sustain the 315+ area.
   - Repair suggestion: hold only; review if completed close loses entry/support, and only discuss profit protection on reclaim/sustain above `303/315`.
   - Validation method: completed close versus `294`, `289.50`, `303`, and `315` markers.
   - Next step: keep no-add status until a separate trend-aligned setup exists.

3. VIX/VIX3M formal-source confirmation
   - Problem: Node smoke test again returned a structured but low-quality VIX object with zero OHLC/volume.
   - Impact: equity/ETF workflow is verified, but market fear scoring still needs external volatility data.
   - Possible cause: Tencent volatility-index field quality gap.
   - Repair suggestion: formal audit should continue using external VIX and VIX3M sources.
   - Validation method: record synchronized VIX, VIX3M, term structure, and source quality.
   - Next step: do not downgrade local quote workflow availability; isolate this as a VIX-specific gap.

4. Theme-crowding replay discipline
   - Problem: `flow_fragility=elevated` and `theme_overlap_high` remain active while AI/storage/space themes are volatile.
   - Impact: converting AMD/WDC/STX/RKLB strength into fresh real buys would violate no-chase and real-account scope rules.
   - Possible cause: high-beta rebound followed by intraday cooling in QQQ/SMH.
   - Repair suggestion: keep AMD/WDC/STX as replay/watch context only; no new RKLB while RDW occupies the space sleeve.
   - Validation method: completed-close replay row only after the 04:15 audit.
   - Next step: no replay ledger prefill during this intraday run.

### Additional Completed / Verified At 23:30

- Node quote smoke test again returned structured Tencent Primary equity/ETF quote objects.
- Python fallback and Google browser-visible fallback were not required.
- Old local quote failure conclusions remain retired for equities/ETFs.
- No broker login, no real order, no model fill, and no replay row were added.

## Formal Post-Close Audit Update

Run time: 2026-06-17 08:46 Asia/Shanghai. This is the formal close-trigger audit for the 2026-06-16 U.S. regular session.

### Priority Carryover To Next Actionable Window

1. MRVL reduce/exit-review
   - Problem: Formal close snapshot showed MRVL `278.67`, below the `285` review line and below the `280` close reduce/exit-review line.
   - Impact: The real starter is now below entry and below the first formal reduce trigger, though still above the `275` priority exit line.
   - Repair suggestion: no add; require user-confirmed reduce/exit decision in the next actionable window.
   - Validation method: next-session price versus `275/280/285` and QQQ/SMH confirmation.

2. RDW exit/stop-review
   - Problem: Formal close snapshot showed RDW `13.50`, below the `14.50` exit/stop-review line.
   - Impact: The satellite position is below gross and fee-adjusted cost, and fee drag is material relative to the small position.
   - Repair suggestion: no averaging down; require user-confirmed exit/hold decision in the next actionable window.
   - Validation method: close table plus fee-adjusted P/L.

3. New-buy block while risk items are unresolved
   - Problem: `flow_fragility=elevated`, MRVL and RDW both triggered review, and AI/semiconductor/space beta sold off.
   - Impact: Opening AMD/WDC/STX/RKLB/ORCL would add complexity before existing risk is handled.
   - Repair suggestion: keep max operational new exposure at `0%` until MRVL/RDW and broker open-order/cash facts are clarified.
   - Validation method: next trade plan explicitly resolves existing-position risk before any new order.

### Completed / Verified At Formal Close

- Node quote smoke test returned structured Tencent Primary equity/ETF quote objects.
- Python fallback and Google browser-visible fallback were not required.
- Local VIX remained low-quality; external VIX `16.41` and VIX3M `19.53` were used for formal fear scoring.
- Added the completed 2026-06-16 close replay row.
- Updated 2026-06-16 portfolio summary and created 2026-06-16 post-close audit.
- No stable `decisions.md` update was justified.
