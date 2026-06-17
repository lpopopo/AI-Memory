# 2026-06-12 Strategy Todos

Run time: 2026-06-12 08:51 Asia/Shanghai.

## Open

### 1. Verify follow-through after the 2026-06-11 rebound

- Problem: The dedicated post-close audit already recorded a sharp 2026-06-11 AI/semiconductor rebound, but one repair day does not validate a stable trend repair.
- Impact: Downgrading the fear gate too quickly or chasing MRVL/AI/storage names could turn a whipsaw recovery into a poor entry.
- Possible cause: High-beta themes often rebound hard after synchronized deleveraging.
- Repair suggestion: Track whether QQQ/SMH and the watchlist hold at least part of the rebound on the next completed session; keep new buys dependent on a fresh setup.
- Validation method: next close table and replay note.
- Next step: keep current real-account status as cash / no confirmed equity holdings until user or broker confirms any new trade.

### 2. MRVL re-entry discipline after profitable exit

- Problem: MRVL closed far above the real-account exit price after the confirmed sale.
- Impact: There is regret risk and a temptation to rebuy automatically after a strong close.
- Possible cause: Profit-capture exit and stop-defense exit are currently discussed with similar language.
- Repair suggestion: Treat MRVL as watchlist only; require a fresh setup such as controlled pullback/reclaim or broad SMH/QQQ trend confirmation.
- Validation method: any new MRVL buy plan must state technical basis, risk line, and account-size impact.
- Next step: no automatic rebuy.

### 3. AMD close-stop trigger remains unresolved in historical replay

- Problem: AMD closed `488.45`, still just below the old historical-model `492` line; after-hours near `491.95` is not a formal close reclaim.
- Impact: Replay cannot mark AMD repaired yet.
- Possible cause: Strong semiconductor rebound but incomplete reclaim.
- Repair suggestion: Keep AMD as historical model/replay reduce-review until a completed close reclaims the line or the replay rule is explicitly revised.
- Validation method: next formal close table.
- Next step: do not treat AMD as current real-account exposure unless user confirms a real holding.

### 4. WDC/STX near-stop review should be replayed as whipsaw recovery

- Problem: WDC and STX reclaimed old historical-model risk lines on 2026-06-11 after breaching them on 2026-06-10.
- Impact: The overlay replay should measure whether reduce-review avoided risk or created avoidable whipsaw cost.
- Possible cause: AI/storage theme remained fundamentally crowded but rebounded sharply with semiconductors.
- Repair suggestion: Add a formal replay note comparing baseline and overlay behavior for 2026-06-10 to 2026-06-11 once the audit row is confirmed.
- Validation method: replay ledger row with close prices and action labels.
- Next step: keep WDC/STX out of current holdings tracking unless user asks for historical replay.

### 5. Theme-crowding overlay replay needs follow-through rows

- Problem: The 2026-06-11 rebound row exists, but the overlay still needs follow-through rows to judge whether `flow_fragility=acute/elevated` was too defensive or appropriately cautious.
- Impact: A single rebound row can overstate missed upside or understate residual crowding risk.
- Possible cause: Replay protocol intentionally avoids pre-filling future rows.
- Repair suggestion: Continue filling only completed close rows and explicitly label whipsaw/missed-rebound effects.
- Validation method: replay ledger includes baseline action, overlay action, and follow-through notes.
- Next step: keep as next completed-close confirmation item.

### 6. Repair live quote workflow and Python runtime path

- Status: completed 2026-06-12.
- Problem: Node quote smoke test returned `[]`; Tencent failed with `fetch failed`; Sina failed with `connect EACCES 198.18.0.42:443`. Python smoke test also failed to start with a Windows login-session error.
- Fix: upgraded `quant-stock-data` so empty quote arrays are treated as source failures, Node requests prefer the native HTTPS client instead of fragile global `fetch`, and U.S. tickers now use `Tencent -> Yahoo chart -> Sina`. Python client was rebuilt with the same hierarchy and should be run with the Codex bundled Python path instead of the Windows Store `python.exe` stub.
- Impact: Intraday automations can use local quotes again when at least one public route returns normalized quote objects, while still preserving source labels.
- Possible cause: network sandbox/proxy restriction plus local Python session issue.
- Validation: 2026-06-12 smoke tests returned normalized quote objects for `MRVL`, `AMD`, `SPY`, `QQQ`, and `SMH`; Node and Python both used Tencent primary after the symbol-casing/runtime fixes, and the AkShare skill returned Tencent fallback after AkShare upstream failed.
- Next step: keep source labels in every strategy note; failed quotes remain non-evidence, but the workflow itself is no longer open-broken.

## Completed By Formal Post-Close Audit

- Created `memory/daily/2026-06-12-post-close-audit.md`.
- Created `memory/portfolio/2026-06-12-portfolio-summary.md`.
- Appended the completed 2026-06-11 close row to the institutional overlay replay ledger.
- Confirmed that no `decisions.md` update is justified from this single-day audit.

## 23:32 Intraday Review Update

### 7. 2026-06-12 close confirmation for AMD/WDC/STX repair

- Problem: At 2026-06-12 23:32 Asia/Shanghai / 11:32 ET, Node quotes showed AMD `514.52`, WDC `560.50`, and STX `922.54`, all intraday above their historical replay risk lines.
- Impact: Treating this as a completed repair before the U.S. close would violate the automation rule that formal stop/reduce changes belong to the 04:15 post-close audit.
- Possible cause: High-beta AI/semiconductor/storage rebound after the prior stress window.
- Repair suggestion: Keep AMD as `reduce-review until formal close confirms reclaim above 492`; keep WDC/STX as `defensive hold / repair review` until completed close confirms.
- Validation method: 04:15 post-close audit with official close table and replay-ledger decision.
- Next step: do not update replay ledger from this intraday snapshot.

### 8. Quote workflow verified, VIX term-structure still open

- Status: quote workflow verified for this run.
- Evidence: Node `StockService.fetchQuotes` returned structured Tencent quote objects for `MRVL`, `AMD`, `WDC`, `STX`, `SPY`, `QQQ`, `SMH`, `HYG`, `LQD`, `IWM`, `RSP`, and `VIX`.
- Impact: The old `Tencent fetch failed / Sina EACCES / python.exe login-session` conclusion must not be reused for this run.
- Remaining problem: VIX returned `21.67` with open/high/low/volume all zero, and VIX/VIX3M term structure remains unavailable.
- Repair suggestion: Keep local quote workflow marked usable, but keep synchronized VIX/VIX3M as a separate data-quality gap.
- Validation method: future post-close audit should fetch a reliable VIX and VIX3M close or record an explicit source failure.
- Next step: no Google browser fallback needed unless local quote clients fail or a one-ticker sanity check is required.

### 9. Flow-fragility elevated needs post-close confirmation

- Problem: Breadth improved intraday, but AI/semiconductor/storage leadership is still a crowded high-beta repair.
- Impact: New MRVL/AMD/WDC/STX exposure after an intraday rally could rebuild the same theme basket too early.
- Possible cause: Systematic rebound and semiconductor beta after the 2026-06-10/11 stress-to-repair sequence.
- Repair suggestion: Keep `flow_fragility=elevated`, `trend_aligned_entry=cheap_but_unconfirmed`, and `theme_overlap_high` until the official close and follow-through rows are reviewed.
- Validation method: 04:15 close audit plus next completed-close replay row.
- Next step: keep real account cash / no confirmed equity holdings unless user or broker confirms a new trade.
