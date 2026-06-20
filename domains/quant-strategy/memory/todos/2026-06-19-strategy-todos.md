# 2026-06-19 Strategy Todos

Run time: 2026-06-20 08:13 Asia/Shanghai. This list reflects automation-3 holiday / intraday-prep audit after confirming U.S. markets are closed for Juneteenth.

## Open

### 1. RDW exit / stop-review remains first priority

- Problem: RDW's latest completed regular-session close reference is `14.35`, below the `14.50` close stop-review line.
- Impact: stop discipline remains unresolved; do not add RKLB/RDW/space exposure while this is open.
- Possible cause: high-volatility satellite lagged the broad AI / semiconductor repair.
- Fix suggestion: user should choose sell/reduce versus an explicit manual defensive-hold override before any new buy.
- Validation: next regular session should check live broker quote, execution status, and close versus `14.50` / `16.00`.
- Next step: if user confirms execution, record the real broker fill separately; do not infer a fill.

### 2. TTMI and MXL are conditional only, not live orders

- Problem: prior plan language could be misread as execution-ready despite the Juneteenth market holiday.
- Impact: risk of treating conditional plans as broker orders or real fills.
- Possible cause: plan was revised during a non-trading day after account baseline update.
- Fix suggestion: keep TTMI at `conditional / not live`: 3 shares only on `$210-213` pullback or `>$220` confirmed breakout, no chase `>$225`; keep MXL at `conditional / not live`: 2 shares only on `$85-87` pullback or `>$90` confirmed breakout, no chase `>$92`.
- Validation: require next-session market confirmation, live broker quote, spread/liquidity check, and user confirmation before recording any order.
- Next step: reassess at the Monday, June 22 open; do not pre-record fills.

### 3. MRVL and GLW profit-protection review

- Problem: MRVL faded from `329.88` to `310.58`; GLW jumped `11.13%` into/above target zone.
- Impact: both are profitable, but gains can reverse if AI / optical crowding unwinds.
- Possible cause: event / theme-driven rally with elevated flow fragility.
- Fix suggestion: no add; define next-session profit-protection reference lines around MRVL `315` reclaim/rejection and GLW `188-190` support.
- Validation: monitor QQQ/SMH confirmation, stock relative strength, and completed close.
- Next step: update after Monday's live session or formal post-close audit.

### 4. Broker / account reconciliation still needed

- Problem: cash, exact FX, fees, settlement, margin status, and open orders remain estimate-only.
- Impact: NAV, exposure, order capacity, and fee-adjusted breakevens remain approximate.
- Possible cause: no broker login or credentialed account access is allowed in automation.
- Fix suggestion: user can provide sanitized broker-side cash/open-order/fill facts.
- Validation: separate broker-confirmed fields from model estimates in the next portfolio note.
- Next step: do not count TTMI/MXL/RDW changes as real until confirmed.

### 5. Live quote workflow remains usable, but holiday data must be labeled

- Problem: Node returns structured quote objects even on a market holiday, which can be mistaken for live intraday quotes.
- Impact: false intraday trigger interpretation if session context is ignored.
- Possible cause: Tencent/Yahoo style quote fields carry the last completed U.S. session snapshot.
- Fix suggestion: keep using Node workflow first, but always record session status and quote timestamp/source/quality.
- Validation: Node quote workflow returned `Tencent (Primary)` structured objects at `2026-06-20T00:13:17Z`; mark them as 2026-06-18 close/delayed references because NYSE/Nasdaq were closed on 2026-06-19.
- Next step: on Monday, rerun Node workflow during the actual session and compare against broker/browser-visible sanity checks if needed.

### 6. Replay ledger waits for the next completed close

- Problem: institutional overlay replay protocol applies only to completed trading-session rows.
- Impact: adding a 2026-06-19 row would create a false market-data record.
- Possible cause: calendar holiday in the normal daily workflow slot.
- Fix suggestion: do not append a 2026-06-19 close row.
- Validation: NYSE/Nasdaq holiday schedule shows Juneteenth closed on Friday, June 19, 2026.
- Next step: next replay update can use the completed Monday, June 22 close if the post-close audit verifies data.

## Completed / Verified This Run

- Read required memory, references, recent trade/portfolio/todo records, and quote workflow instructions.
- Confirmed local Node quote workflow is usable and returned structured `Tencent (Primary)` quote objects.
- Confirmed U.S. market holiday context from local memory plus official NYSE/Nasdaq holiday references.
- Updated `memory/trades/2026-06-19-trade-plan.md` to remove `Executing` language from non-live items.
- Updated `memory/portfolio/2026-06-19-portfolio-summary.md` to separate confirmed holdings from conditional projection.
- Appended the automation-3 holiday / intraday-prep audit to `memory/daily/2026-06-19-details.md`.
- Did not update `summary.md` or `decisions.md`; no new stable rule was validated.
- Did not update the replay ledger; no 2026-06-19 completed U.S. close exists.

Not investment advice.
