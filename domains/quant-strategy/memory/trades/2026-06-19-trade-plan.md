# 2026-06-19 Trade Plan

Run time: 2026-06-19 18:55 Asia/Shanghai.
Updated: 2026-06-20 08:13 Asia/Shanghai by automation-3 holiday / intraday-prep audit.

Scope: real-account execution checklist and planning ledger. The U.S. stock market is closed on Friday, June 19, 2026 for Juneteenth, so every action below is next-regular-session preparation for Monday, June 22, 2026. No broker login, order submission, cancellation, or fill assumption was made.

## Data Snapshot

Local Node quote workflow was rerun first per `tools/README.md`.

| Item | Result |
| --- | --- |
| Run time | `2026-06-20T00:13:17.080Z` |
| Node quote workflow | Usable; returned structured quote objects |
| Equity / ETF source | `Tencent (Primary)` |
| Quote reference | 2026-06-18 U.S. regular-session close / delayed snapshot |
| Quote quality | Medium-high for prior-session reference; not a live 2026-06-19 intraday market |
| Volatility reference | Cboe VIX `16.40` / VIX3M `19.57` from the 2026-06-18 formal close audit |
| Account baseline | HKD 50,000, approx. USD 6,410.26 at 7.80 HKD/USD |

## Executive Action

Market state remains `elevated / repair`, not a new normal-risk live session. Broad market and semiconductor/AI leadership repaired strongly on the 2026-06-18 close, but `flow_fragility=elevated` because leadership is crowded and extended. New exposure is allowed only through trend-aligned pullback/reclaim triggers and user confirmation.

Priority:

1. RDW exit-review first: sell/reduce candidate because the latest completed close is `14.35`, below the `14.50` stop-review line.
2. MRVL and GLW: hold and protect gains; no add after event / target-zone extension.
3. TTMI and MXL: conditional plans only; not live broker orders.
4. ALAB / AMD / WDC / STX: watch-only / no chase.

## Execution Checklist

| Priority | Ticker | Direction | Quantity | Target amount | Approx account weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason | Risk point | Status |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | RDW | Sell / exit candidate | 5 shares | USD 71.75 gross | ~1.1% | $14.35 | User confirms next-session sell/reduce after live broker quote; no averaging down | Stop-review already triggered below $14.50 close; reclaim above $16 improves review | User explicitly chooses manual defensive hold with written override | Stop discipline after trend breakdown | Small realized loss; gap/slippage risk | Pending user/broker execution |
| 2 | TTMI | Conditional buy | 3 shares | USD 649.32 gross | ~10.1% | $216.44 | Pullback to $210-213 or confirmed breakout above $220 with QQQ/SMH and stock confirmation | Daily close below $188.00 after entry | Opens above $225 without orderly reset, or QQQ/SMH fail risk-on confirmation | AI data-center PCB / interconnect candidate | New candidate, high beta, crowded theme | Conditional / not live |
| 3 | MXL | Conditional buy | 2 shares | USD 177.52 gross | ~2.8% | $88.76 | Pullback to $85-87 or confirmed breakout above $90 with confirmation | Daily close below $80.00 after entry | Opens above $92 without orderly reset, poor liquidity/spread, or theme fails | Optical / interconnect satellite | Volatility and fee drag | Conditional / not live |
| 4 | MRVL | Hold | 1 share | USD 310.58 | ~4.8% | $310.58 | Hold; monitor reclaim/rejection of $315 | Review below $285; stop below $280 close | Loss of theme support or close below risk line | AI interconnect leader | Event rally faded from $329.88; crowded theme | Core hold / profit-protection review |
| 5 | GLW | Hold | 2 shares | USD 389.84 | ~6.0% | $194.92 | Hold; target zone reached, no add | Caution around $188-190; stop/exit review below $180-181 | Loss of optical/fiber theme support | Optical/fiber starter worked | Profit giveback after 11% jump | Core hold / profit-protection review |
| 6 | ALAB | No buy | 0 | USD 0 | 0% | $417.07 | Re-evaluate only after post-event reset / base | N/A | Chasing index-inclusion extension | Strong theme, but event-risk setup | Event chase / valuation / single-share concentration | Watch only |
| 7 | AMD | No real action | 0 | USD 0 | 0% | $537.37 | Watch only; no real holding | Old replay stop $492 if held in replay context | Chasing after repair extension | AI compute repair | Capex-cycle and theme crowding | Watch only |
| 8 | WDC | No real action | 0 | USD 0 | 0% | $746.23 | Watch only; no real holding | Old replay stop $500 if held in replay context | Chasing extended memory/storage theme | Storage bottleneck leader | Extension and crowding | Watch only |
| 9 | STX | No real action | 0 | USD 0 | 0% | $1070.23 | Watch only; no real holding | Old replay stop $835 if held in replay context | USD 1000-class single-share concentration | Storage leader | Large share price / extension | Watch only |

## Confirmed Real Holdings

Only user-confirmed or broker-confirmed positions are counted as real holdings:

| Ticker | Shares | Expected role | Current status |
| --- | ---: | --- | --- |
| MRVL | 1 | AI interconnect core | Core hold / profit-protection review |
| RDW | 5 | Space / satellite satellite | Exit-review below $14.50 close |
| GLW | 2 | Optical / fiber core | Core hold / profit-protection review |

No TTMI, MXL, or ALAB broker-side open order is recorded unless the user later confirms one.

## Conditional Target Positions

This is a planning projection only if RDW is exited and TTMI/MXL triggers plus user confirmation occur:

| Ticker | Shares | Expected role |
| --- | ---: | --- |
| MRVL | 1 | AI interconnect core hold |
| GLW | 2 | Optical/fiber core hold |
| TTMI | 3 | AI infrastructure PCB core candidate |
| MXL | 2 | AI silicon/interconnect satellite candidate |

Not investment advice.
