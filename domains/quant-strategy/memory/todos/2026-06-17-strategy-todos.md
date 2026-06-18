# 2026-06-17 Strategy Todos

Run time: 2026-06-18 08:45 Asia/Shanghai. This list reflects the formal post-close audit for the 2026-06-17 U.S. regular session.

## Open

### 1. RDW exit / stop-review remains active

- Problem: RDW closed at `14.36`, still below the `14.50` stop-review line despite an intraday rebound.
- Impact: the position remains below gross cost, buy-fee-adjusted cost, and round-trip breakeven.
- Repair suggestion: no averaging down; require user-confirmed sell/reduce or explicit manual defensive hold.
- Validation method: next completed close versus `14.50` and `16.00`, plus fee-adjusted P/L.
- Next step: carry as the first real-account risk item.

### 2. MRVL repaired prior trigger only marginally

- Problem: MRVL closed at `289.54`, above `285` and barely above the `289.50` gross fill, but below the estimated `291.50` round-trip breakeven.
- Impact: the 2026-06-16 reduce trigger is repaired by completed close, but the repair is not strong enough for add/pyramid logic.
- Repair suggestion: downgrade to manual risk hold / no add; if it loses `285` or `280` again, return to reduce/exit-review.
- Validation method: completed close versus `285/280/275`, plus SMH/QQQ confirmation.
- Next step: keep in hold review, not chase.

### 3. Volatility source hygiene

- Problem: local Node quote workflow is usable for equities/ETFs, but local Tencent VIX remains low quality with zero OHLC/volume.
- Impact: formal market fear scoring still needs Cboe/Yahoo/Google-visible volatility confirmation.
- Repair suggestion: continue recording VIX/VIX3M from Cboe CSV or equivalent public close data while preserving local source labels for equities/ETFs.
- Validation method: audit records VIX, VIX3M, ratio, timestamp, and source quality.

### 4. Theme-crowding / correlation risk review

- Problem: `flow_fragility=elevated`, `theme_overlap_high`, and replay `sleeve_correlation_high` remain active.
- Impact: a new AMD/WDC/STX/MU/RKLB chase would add correlated high-beta exposure before RDW is resolved.
- Repair suggestion: keep fresh buys blocked operationally; allow only observation levels until existing risk items and broker facts are synchronized.
- Validation method: next trade plan resolves RDW/MRVL before adding any new exposure.

### 5. Broker / account reconciliation

- Problem: broker cash, exact fees, FX, tax, settlement, margin status, and stale open orders remain unconfirmed.
- Impact: real NAV and executable order capacity remain estimates only.
- Repair suggestion: user can provide sanitized non-sensitive cash/order facts if needed; do not log credentials.
- Validation method: future portfolio note uses confirmed non-sensitive fields only.

## Completed / Verified This Run

- Ran the required local Node Quote Workflow Smoke Test first.
- Confirmed structured `Tencent (Primary)` quote objects for required equities/ETFs.
- Did not run bundled Python fallback because Node succeeded.
- Did not use Google browser-visible fallback because local equity/ETF data succeeded and Cboe supplied VIX/VIX3M.
- Recorded formal Cboe VIX `18.44` and VIX3M `20.62` for 2026-06-17.
- Classified market gate as `elevated`, risk multiplier `70%`, framework cash floor `25%`, operational new-buy exposure `0%`.
- Updated the 2026-06-17 portfolio summary and created the 2026-06-17 post-close audit.
- Appended the completed 2026-06-17 replay ledger close row without prefilling future dates.
- Left `decisions.md` unchanged because no stable rule was newly validated.

Not investment advice.
