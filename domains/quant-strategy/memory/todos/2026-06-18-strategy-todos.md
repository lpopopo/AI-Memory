# 2026-06-18 Strategy Todos

Run time: 2026-06-18 23:18 Asia/Shanghai. This list reflects an intraday review, not the formal 04:15 post-close audit.

## Open

### 1. RDW exit / stop-review remains first priority

- Problem: RDW traded around `13.81` intraday, still below the `14.50` stop-review line and below 5/10/20-day averages.
- Impact: the position remains below gross cost, buy-fee-adjusted cost, and round-trip breakeven while the rest of the risk-on tape improved.
- Possible reason: space / satellite theme is weaker than AI / semiconductor / optical leaders; RDW remains a high-volatility satellite rather than core.
- Fix / next step: ask user to confirm sell/reduce versus explicit manual defensive hold; do not average down.
- Validation: formal 04:15 audit should check completed close versus `14.50` and `16.00`.

### 2. MRVL profit-protection review after event rally

- Problem: MRVL rallied to about `324.66`, reaching the prior `315-324` profit-protection zone.
- Impact: unrealized P/L improved sharply, but the move is event/crowding-sensitive and should not become an add/chase signal.
- Possible reason: AI interconnect / custom silicon strength and broader SMH risk-on move.
- Fix / next step: hold current 1 share unless user wants a profit-protection sell plan; no new MRVL buy.
- Validation: watch rejection or hold above `324-326`, plus formal close and SMH/QQQ confirmation.

### 3. GLW new support-test needs next-session risk tracking

- Problem: GLW fill at `181.50` is working intraday around `184.62`, but it is a same-day support-test starter.
- Impact: it raises real equity exposure to about `29%` of the old HKD 20,000 baseline, or about `15%` of the forward HKD 40,000 baseline.
- Possible reason: optical / fiber / AI infrastructure rotation offered lower single-name risk than chasing WDC.
- Fix / next step: no same-day add; keep caution below `181`, stop/exit review below `180`, and target/profit-protection review near `192-198`.
- Validation: completed close versus `181/180/187-188`, then next-session behavior.

### 4. Broker / account reconciliation still needed

- Problem: broker cash, exact fees, FX spread, taxes, settlement, margin status, and stale open orders remain unverified.
- Impact: NAV, exposure, and any new order capacity remain estimates.
- Possible reason: automation does not log in to broker and only records user-confirmed fills.
- Fix / next step: user can provide sanitized non-sensitive cash/open-order facts if needed.
- Validation: next portfolio note should separate broker-confirmed fields from estimates.

### 5. Volatility source hygiene

- Problem: local Node quote workflow is usable for equities/ETFs, but Tencent `VIX` remains low quality with zero OHLC / volume.
- Impact: market fear scoring should not rely on the local Tencent VIX object.
- Possible reason: Tencent index mapping quality issue for volatility symbols.
- Fix / next step: use Yahoo/Cboe/Google-visible volatility confirmation in the formal close audit while preserving source labels.
- Validation: record VIX, VIX3M, ratio, timestamp, source, and quality in the 04:15 audit.

### 6. WDC / DRAM / SMCI trend participation needs discipline

- Problem: WDC, DRAM, MU, SMCI, INTC and QCOM are strong intraday, but several are extended or high-concentration if bought as single shares.
- Impact: chasing would add crowded AI / memory / semiconductor beta after the account already added GLW.
- Possible reason: broad semiconductor and memory/storage risk-on rotation.
- Fix / next step: keep as watch-only unless user explicitly accepts a controlled participation plan and concentration risk.
- Validation: require trend-aligned entry, daily K-line basis, fee-adjusted breakeven, and cancellation/stop levels before any new order.

## Completed / Verified This Run

- Ran the required local Node Quote Workflow Smoke Test first.
- Confirmed structured `Tencent (Primary)` quote objects for real holdings and watchlist equities/ETFs.
- Did not run bundled Python fallback because Node succeeded.
- Did not use Google browser-visible fallback because local quote workflow succeeded for equities/ETFs.
- Recorded volatility as a source-quality gap rather than calling the whole quote workflow unavailable.
- Created `memory/trades/2026-06-18-trade-plan.md`.
- Updated `memory/portfolio/2026-06-18-portfolio-summary.md`.
- Created `memory/daily/2026-06-18-details.md`.
- Did not append replay ledger because this is not a completed close row.
- Left `summary.md` and `decisions.md` unchanged.

Not investment advice.
