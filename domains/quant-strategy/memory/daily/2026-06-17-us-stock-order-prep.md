# 2026-06-17 US Stock Order Prep

Run time: 2026-06-17 20:47 Asia/Shanghai.

Task: `automation-2` daily U.S. stock premarket candidate order-prep. This is candidate preparation only, not a broker instruction and not a record of order placement.

## Inputs

- Read required core memory: `summary.md`, `decisions.md`, `daily-summaries.md`.
- Read recent daily and portfolio records: 2026-06-17 realtime public/institutional monitor, 2026-06-16 formal post-close audit, and 2026-06-16 portfolio summary.
- Read required references: market fear technical framework, portfolio concentration rules, daily market monitoring framework, institutional overlay checklist/scorecard, and AI quality/capex-cycle classification.
- Read `tools/README.md` Quote Workflow Smoke Test.
- Read current 20:33 realtime public/institutional monitor product.

## Quote Workflow

Node quote workflow was run first using `stock_service.js` and returned structured `Tencent (Primary)` quote objects for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, SOXX, RSP, HYG, LQD, IWM, RDW, ORCL, RKLB, NVDA, and MU. Python and Google browser fallback were not required.

Data quality:

- Equity/ETF quotes: usable structured local quote objects, delayed public market data.
- Local VIX: low quality because OHLC/volume fields were zero.
- External VIX sanity check: Cboe visible page showed VIX spot about `16.30` on 2026-06-17, with previous close `16.41`; this supports `elevated`, not `stress` or `panic`.

## Strategy State

- Market gate: `elevated`, with no panic term-structure signal from available public VIX context.
- Operational new-buy gate: closed until MRVL/RDW risk decisions, broker cash, FX, fees, settlement, and open orders are synchronized.
- Cash target: framework cash floor at least `25%`; practical target remains very high cash because confirmed real positions have active risk-review labels.
- Confirmed real-account holdings from memory: MRVL `1` share and RDW `5` shares. AMD, WDC, STX and other historical watch names are not confirmed current real holdings.
- 2026-06-17 realtime institutional overlay added policy-hysteresis, AI listing-window liquidity, AI capex cash-flow pressure, and semiconductor/software monetization separation as monitoring overlays only; no trade signal was promoted.

## Candidate Prep Summary

| Ticker | Direction | Reference prep price | Shares | Order type | Trigger condition | Invalidation | Risk line | Source | Notes |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- |
| RDW | sell candidate / risk review | 13.45-13.60 | 5 confirmed shares, subject to user sync | limit only, no market order by default | User confirms reducing or exiting after completed close below 14.50 stop-review line | Reclaim and hold above 14.50-16.00 before user decision reduces urgency | Below 13.18 prior low area means stop gap risk remains active | Local Node quote workflow, Tencent Primary, price 13.50 | No averaging down; speculative space sleeve already impaired |
| MRVL | sell/reduce candidate / risk review | 278.50-280.00 | 1 confirmed share, subject to user sync | limit only | User confirms risk reduction after close below 280 reduce/exit-review line | Reclaim and hold above 285-289.50 before user decision can move back to manual hold review | Below 275 close remains priority exit-review line | Local Node quote workflow, Tencent Primary, price 278.67 | No add; AI interconnect thesis weakened by semiconductor reversal |
| ORCL | watch only | 187.50-188.50 observation zone | 0; any future size requires account sync | no order prepared | Only reconsider after QQQ stabilizes and ORCL reclaims 190-195 or holds support with relative strength | Break below 176 prior review line or weak QQQ/AI software reaction | 176 review line | Local Node quote workflow, Tencent Primary, price 188.33 | Cloud/AI factory watch; not executable while real-position risk is unresolved |
| RKLB | watch only | 103.00-105.00 observation zone | 0; any future size requires account sync | no order prepared | Only reconsider after RDW risk is resolved and RKLB reclaims 108.50-109.25 with space-theme strength | Break below 95 or continued RDW weakness | 95 review line | Local Node quote workflow, Tencent Primary, price 104.63 | Do not add a second space satellite while RDW is below stop-review |
| AMD | watch only / historical replay context | 500-507 observation zone | 0 real shares confirmed | no order prepared | Only reconsider after QQQ/SMH recover and AMD holds/reclaims with relative strength | Close back below 492 replay risk line | 492 replay risk line | Local Node quote workflow, Tencent Primary, price 507.29 | Not a current real holding; no chase after -7.30% semiconductor unwind |

No stable rule was promoted to `decisions.md`.

Not investment advice.
