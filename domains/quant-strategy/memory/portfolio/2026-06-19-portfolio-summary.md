# 2026-06-19 Portfolio Summary

Run time: 2026-06-19 18:55 Asia/Shanghai.
Updated: 2026-06-20 08:13 Asia/Shanghai by automation-3 holiday / intraday-prep audit.

Scope: current real-account active holdings. This summary reflects the HKD 50,000 baseline and separates confirmed holdings from conditional next-session projections. The U.S. market is closed on Friday, June 19, 2026 for Juneteenth, so there is no 2026-06-19 regular-session fill or intraday trigger.

## 1. Current Confirmed State

### Active Holdings

| Ticker | Shares | Cost basis | Last close reference | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | USD 289.50 gross | $310.58 | $310.58 | +$21.08 | AI interconnect core | Core hold / profit-protection review |
| RDW | 5 | USD 15.00 gross | $14.35 | $71.75 | -$3.25 | Space / satellite satellite | Exit-review below $14.50 close |
| GLW | 2 | USD 181.50 gross | $194.92 | $389.84 | +$26.84 | Optical / fiber core | Core hold / profit-protection review |

### Current NAV Estimate

| Metric | Fee-adjusted estimate using USD 1 platform fee |
| --- | ---: |
| USD baseline equivalent | 6,410.26 |
| Equity market value | 772.17 |
| Estimated cash, including new baseline capital | 5,679.76 |
| Estimated NAV | 6,451.93 |
| Estimated return vs baseline | +0.65% |
| Cash ratio | 88.03% |
| Equity exposure | 11.97% |

Broker cash, exact FX, taxes, settlement, margin status, and open orders are not independently verified by this automation.

## 2. Conditional Next-Session Projection

This projection assumes RDW is sold and TTMI/MXL are bought at 2026-06-18 reference prices. It is not a real-account ledger until the user or broker confirms fills.

### Projected Holdings

| Ticker | Shares | Expected cost basis | Reference price | Projected market value | Expected role |
| --- | ---: | ---: | ---: | ---: | --- |
| MRVL | 1 | USD 289.50 | $310.58 | $310.58 | AI interconnect core hold |
| GLW | 2 | USD 181.50 | $194.92 | $389.84 | Optical/fiber core hold |
| TTMI | 3 | USD 216.44 | $216.44 | $649.32 | AI infrastructure PCB core candidate, conditional / not live |
| MXL | 2 | USD 88.76 | $88.76 | $177.52 | AI silicon / interconnect satellite candidate, conditional / not live |

### Projected NAV Estimate

| Metric | Projected value |
| --- | ---: |
| Projected equity market value | 1,527.26 |
| Projected cash | 4,921.67 |
| Projected NAV | 6,448.93 |
| Projected cash ratio | 76.32% |
| Projected equity exposure | 23.68% |

## 3. Position Risk Plan

| Ticker | Current label | Stop / review | Daily technical basis | Action rule |
| --- | --- | --- | --- | --- |
| MRVL | core hold / profit-protection review | Review below 285; stop below 280 close; profit-protection review around 315 reclaim/rejection | Close 310.58 is above 5/10/20/50D but below 315 after fading from 329.88 | Hold only; no add or chase |
| GLW | core hold / profit-protection review | Caution around 188-190; stop/exit review below 180-181 | Close 194.92 is above 5/10/20/50D; target zone reached after 11% jump | Hold; review profit protection; no add |
| RDW | exit-review | Stop triggered below 14.50 close | Close 14.35 is below 5/10/20D and review line | Sell/reduce candidate after user/broker confirmation; no averaging down |
| TTMI | conditional buy candidate / not live | Stop/exit review below 188.00 close if entered | Close 216.44 is extended after a 6.78% day | Buy only on $210-213 pullback or >$220 confirmed breakout; no chase >$225 |
| MXL | conditional buy candidate / not live | Stop/exit review below 80.00 close if entered | Close 88.76 is extended after a 7.11% day | Buy only on $85-87 pullback or >$90 confirmed breakout; no chase >$92 |

## 4. Data Quality And Market Session

- Local Node quote workflow returned structured `Tencent (Primary)` quote objects at `2026-06-20T00:13:17Z`.
- Source quality: usable for prior-session close / delayed reference values; not usable as a 2026-06-19 live U.S. intraday market because NYSE and Nasdaq are closed for Juneteenth.
- Volatility reference remains the 2026-06-18 post-close audit: Cboe VIX `16.40`, VIX3M `19.57`.
- Replay ledger is not updated for 2026-06-19 because there is no completed U.S. regular-session close row.

Not investment advice.
