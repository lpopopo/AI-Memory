# 2026-06-29 Strategy Todos

Run time: 2026-06-29 23:19 Asia/Shanghai.

## Priority 0 - broker/user confirmation

### 0. DRAM protective trigger confirmation
- Issue: DRAM intraday price `68.45`, low `66.47`, below the stated `70.50` protective trigger.
- Impact: if the broker stop-market order was active, `4` DRAM shares may already have sold; if not active, the position is below the intended protection line.
- Possible cause: memory-theme reversal continued despite index rebound.
- Verification: user/broker statement or order history only.
- Next step: confirm whether `DRAM sell stop-market, 4 shares, trigger 70.50` existed and whether it filled. Do not record a real sale until confirmed.

### 0a. MU protection / close-risk confirmation
- Issue: MU intraday price `1068.68`, low `1023.65`, below the `1100` close-risk line and below the optional `1090` hard-protection reference.
- Impact: if a hard broker stop was active, MU may have sold; if not, a completed close below `1100` should trigger risk review in the 04:15 audit.
- Possible cause: post-earnings memory/HBM crowding unwind and T+1/T+2 catalyst digestion.
- Verification: broker order/fill history plus formal completed close.
- Next step: confirm whether `MU sell stop-market, 1 share, trigger 1090` exists or filled; do not add MU.

### 0b. TTMI hard-line close audit
- Issue: TTMI intraday price `181.61`, low `174.50`, below the completed-close hard line `188`.
- Impact: if the stock closes below `188`, the hard-cut priority rule should apply in the next executable session.
- Possible cause: position-specific weakness plus AI-capex basket fragility.
- Verification: 04:15 post-close audit with completed close data.
- Next step: no averaging down; prepare exit-review if completed close confirms.

## Priority 1 - portfolio controls

### 1. Correlated-sleeve freeze
- Issue: if all positions are still open, GLW/TTMI/MXL plus DRAM/MU remain one broad AI-capex chain with about `46.88%` equity exposure.
- Impact: new buys in AI/semiconductor/storage would worsen concentration while stops are unresolved.
- Possible cause: theme-level overlap across optical/interconnect, PCB, memory ETF and HBM leader.
- Verification: recompute holdings after confirmed broker fills/stops.
- Next step: block all new correlated-theme buys/adds until DRAM/MU/TTMI state is reconciled and trend-aligned entry improves.

### 2. MXL role and stop reclassification
- Issue: MXL `6 @ 90.70` is about `9.58%` of current estimated NAV at `101.21`, above satellite size.
- Impact: per 2026-06-27 sizing rule, it should be treated as core-like and should not keep a loose satellite-only risk line.
- Possible cause: position size exceeded satellite band after price appreciation.
- Verification: post-close market value and NAV.
- Next step: in the post-close audit, reclassify MXL as core-like if still above satellite band and review raising protection from `86` toward `91-92`.

### 3. Broker cash/NAV/open-order reconciliation
- Issue: working cash `USD 3,368.64` and NAV `USD 6,341.37` are estimates only.
- Impact: stop fills, fees, FX and settlements can materially change available cash and risk exposure.
- Possible cause: automation cannot access broker state.
- Verification: user/broker statement only.
- Next step: reconcile cash, NAV, open orders, stop orders and cancellations after the session.

## Priority 2 - data and process

### 4. Live quote workflow quality
- Issue: Node workflow returned structured Tencent quotes, but Tencent VIX remained low quality with zero OHLC; VIX3M required Yahoo Chart.
- Impact: do not compute fear gate from Tencent VIX.
- Possible cause: Tencent U.S. volatility index payload is incomplete.
- Verification: rerun Node smoke test and Yahoo Chart volatility pull in the 04:15 post-close audit.
- Next step: keep source-level quality notes; do not write "local quote workflow unavailable."

### 5. Replay ledger handling
- Issue: 2026-06-29 regular session was not complete during this run.
- Impact: adding a replay close row now would prefill incomplete data.
- Possible cause: automation-3 runs intraday.
- Verification: wait for completed close data.
- Next step: update `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` only in the post-close audit if protocol inputs are available.

## Completed / verified

- Read required memory, latest records, references and Quote Workflow Smoke Test instructions.
- Ran Node local quote workflow first; received structured quote objects.
- Used Yahoo Chart via local Node client for VIX/VIX3M cross-check.
- Created 2026-06-29 trade plan, portfolio summary and daily details.
- Left `decisions.md` unchanged because no stable validated rule was promoted.

Not investment advice.
