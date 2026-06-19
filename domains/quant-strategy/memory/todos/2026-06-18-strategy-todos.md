# 2026-06-18 Strategy Todos

Run time: 2026-06-19 08:56 Asia/Shanghai. This list reflects the formal 2026-06-18 U.S. post-close audit.

## Open

### 1. RDW exit / stop-review remains first priority

- Problem: RDW closed at `14.35`, still below the `14.50` close stop-review line and below 5/10/20-day averages.
- Impact: the position remains below gross cost, buy-fee-adjusted cost, and round-trip breakeven while the broader risk-on tape repaired.
- Next step: ask user to confirm sell/reduce versus explicit manual defensive hold; do not average down.
- Validation: next session should check completed close versus `14.50` and `16.00`.

### 2. MRVL profit-protection review after event rally fade

- Problem: MRVL traded as high as `329.88` but closed at `310.58`, below the `315-324+` profit-protection zone.
- Impact: the position is profitable and repaired above downside lines, but the rally remains event/crowding-sensitive.
- Next step: hold current 1 share unless user wants a profit-protection sell plan; no new MRVL buy.
- Validation: watch reclaim or rejection of `315`, plus QQQ/SMH confirmation.

### 3. GLW profit-protection review after support-test success

- Problem: GLW closed at `194.92`, above the `192-198` initial target / profit-protection zone after a `181.50` support-test fill.
- Impact: the entry worked, but GLW is now the largest real-account position near the normal 15% single-stock limit under the old HKD 20,000 baseline.
- Next step: no add; review whether to keep full 2 shares or define a profit-protection line.
- Validation: hold above `187-188` supports the position; below `181` is caution and below `180` is stop/exit review.

### 4. Broker / account reconciliation still needed

- Problem: broker cash, exact fees, FX spread, taxes, settlement, margin status, and stale open orders remain unverified.
- Impact: NAV, exposure, and any new order capacity remain estimates.
- Next step: user can provide sanitized non-sensitive cash/open-order facts if needed.
- Validation: next portfolio note should separate broker-confirmed fields from estimates.

### 5. Crowded AI / memory / semiconductor chase remains blocked

- Problem: SMH/SOXX, WDC, DRAM, GLW, and MRVL repaired strongly, but `flow_fragility=elevated` and theme overlap is high.
- Impact: new AMD/WDC/STX/DRAM/SMCI chase would add correlated beta after the account already holds MRVL and GLW.
- Next step: keep fresh buys blocked until RDW is resolved and any candidate has a support/reclaim plan with defined stop.
- Validation: require trend-aligned entry, daily K-line basis, fee-adjusted breakeven, and cancellation/stop levels before any new order.

## Completed / Verified This Run

- Ran the required local Node Quote Workflow Smoke Test first.
- Confirmed structured `Tencent (Primary)` quote objects for equities/ETFs.
- Confirmed Tencent VIX remains low quality and used Cboe VIX/VIX3M official close data instead.
- Used Yahoo chart daily bars for completed daily OHLC, MAs, and ratio checks.
- Did not run bundled Python fallback because Node succeeded.
- Did not use Google browser-visible fallback because local workflow and Cboe/Yahoo data were sufficient.
- Created `memory/daily/2026-06-18-post-close-audit.md`.
- Updated `memory/portfolio/2026-06-18-portfolio-summary.md` to formal close.
- Appended the completed `2026-06-18,close` replay row.
- Left `decisions.md` unchanged.

Not investment advice.
