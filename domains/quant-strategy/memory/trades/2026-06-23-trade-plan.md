# 2026-06-23 Trade Plan

Run time: 2026-06-23 23:20 Asia/Shanghai.

Scope: U.S. intraday execution checklist and preliminary review. The U.S. regular session is open; prices below are not formal closes. No broker login, order submission, cancellation, or unconfirmed fill assumption was made.

## Data Snapshot

Local quote workflow was used first as required.

| Layer | Result | Quality |
| --- | --- | --- |
| Node smoke test / `StockService.fetchQuotes` | Returned structured quote objects for holdings, indices, ETFs, and candidates. | Usable intraday data; `source=Tencent (Primary)`. |
| Tencent VIX row | Returned VIX price but zero OHLC/volume. | Rejected for volatility structure. |
| Yahoo chart fallback | Returned 2026-06-23 intraday daily bars, moving-average context, VIX, and VIX3M. | Usable cross-check; not formal close. |
| Python / Google fallback | Not used. | Not needed because Node returned structured quote objects. |

Key intraday references:

| Ticker | Price | Change | Open | High | Low | Source / time |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| SPY | 735.33 | -1.22% | 733.81 | 739.63 | 732.30 | Tencent, 2026-06-23 23:20 BJT |
| QQQ | 716.60 | -2.89% | 715.74 | 723.61 | 713.28 | Tencent |
| SMH | 622.79 | -6.90% | 625.93 | 636.78 | 621.75 | Tencent |
| SOXX | 604.56 | -7.70% | 607.64 | 619.81 | 603.58 | Tencent |
| VIX | 19.38 | +12.15% | n/a | n/a | n/a | Yahoo chart fallback, `regularMarketTime=2026-06-23T15:04:46Z` |
| VIX3M | 21.00 | +7.31% | n/a | n/a | n/a | Yahoo chart fallback, `regularMarketTime=2026-06-23T15:04:46Z` |
| MRVL | 280.22 | -8.98% | 278.82 | 290.95 | 277.22 | Tencent |
| GLW | 186.92 | -10.92% | 192.45 | 194.25 | 186.86 | Tencent |
| TTMI | 209.53 | -5.39% | 202.92 | 213.14 | 200.16 | Tencent |
| AMD | 519.00 | -5.92% | 509.08 | 526.60 | 506.81 | Tencent |
| WDC | 662.47 | -9.58% | 665.21 | 682.53 | 653.00 | Tencent |
| STX | 1010.92 | -7.60% | 984.26 | 1032.70 | 983.00 | Tencent |
| MXL | 87.94 | -8.82% | 84.92 | 92.75 | 84.05 | Tencent |
| ALAB | 399.94 | -9.03% | 399.43 | 419.62 | 395.54 | Tencent |
| DRAM | 70.46 | -12.71% | 69.52 | 73.07 | 68.59 | Tencent |
| CRDO | 266.05 | -12.06% | 277.64 | 284.00 | 265.53 | Tencent |

Daily K-line context from Yahoo chart is intraday only. It shows 2026-06-23 bars in progress, not completed close-stop confirmation.

## Executive Action

The broad market is not in formal panic, but the AI infrastructure / semiconductor theme is experiencing an acute intraday unwind: SMH is down about 6.9%, SOXX about 7.7%, DRAM about 12.7%, CRDO about 12.1%, and current real holdings MRVL/GLW/TTMI are all down sharply. This is a risk-control session, not a buy-the-dip session.

Priority:

1. **No new buys or adds.** Flow fragility has moved from elevated to acute intraday; trend-aligned entry is broken for same-theme adds.
2. **MRVL moves to exit-review / close-stop watch.** Intraday price is near the prior completed-close stop line around 280. Formal action still requires completed close unless the user explicitly wants intraday risk reduction.
3. **GLW moves to defensive hold / near-stop review.** Intraday price broke the raised 203-205 protection band and is near the older 180-181 stop-review zone, but this is not yet a completed close.
4. **TTMI moves to defensive hold / near-stop review.** Intraday low 200.16 broke the 213-214 caution and 210 warning bands, but the formal completed-close stop-review line remains 188.
5. **AMD/WDC/STX remain watch/replay only.** AMD is still above the old 492 replay line; WDC/STX are sharply lower but still far above old replay stops. No real action exists without a real holding.

## Institutional Overlay

```text
flow_fragility_score: about 11 / 14 -> acute intraday
flow_fragility_state: acute
trend_aligned_entry_state: trend_broken for new AI infrastructure adds; defensive-hold review for existing holdings
AI_quality/capex_cycle: MRVL high sensitivity; GLW medium; TTMI medium-high; WDC/STX/DRAM high cyclicality
factor_macro_flags: theme_overlap_high; momentum_reversal_high; growth_duration_high; AI_capex_cashflow_pressure; semiconductor_basket_unwind
bottleneck_watch: optical/interconnect, PCB, and memory/storage remain valid watch themes, but price action rejects chase entries today
action impact: block all new AI/semiconductor/storage buys; protect existing gains; wait for completed-close audit before formal stop/NAV decisions
```

## Execution Checklist

| Priority | Action | Ticker | Direction | Quantity | Target amount | Approx NAV weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason | Risk point | Status |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | Hold / exit-review watch | MRVL | Sell only if user chooses intraday risk cut; otherwise wait for close audit | 1 | ~USD 280.22 | ~4.4% | 280.22 | Completed close below 280 would trigger formal stop/exit review; intraday break may justify discretionary risk cut | Profit guard already failed intraday; review below 285; stop below 280 completed close | Reclaim and hold back above 298-300 with SMH repair | Existing AI interconnect core, but trend is broken intraday | High beta and crowded capex-chain unwind | Needs user decision if acting intraday; formal review at close |
| 2 | Defensive hold / near-stop review | GLW | Hold; no add | 2 | ~USD 373.84 | ~5.9% | 186.92 | Intraday break of 203-205 protection band and 200/195 serious review area | Old stop-review below 180-181 completed close | Close recovery above 200 and theme repair | Optical/fiber core winner, but today gave back protection zone | Profit giveback and same-theme correlation | Hold for close audit unless user wants discretionary trim |
| 3 | Defensive hold / near-stop review | TTMI | Hold; no add | 3 | ~USD 628.59 | ~9.8% | 209.53 | Intraday break of 213-214 caution and 210 warning; low 200.16 | Completed-close stop-review below 188 | Close recovery above 213-214 and hold above 220 later | Pullback entry worked previously, but theme shock invalidates add logic | New position, crowded PCB/interconnect exposure | Hold for close audit; no averaging down |
| 4 | No buy / no add | AMD | Watch only | 0 | 0 | 0% | 519.00 | None | Old replay line 492 only applies to historical replay | Any new buy needs trend reclaim and non-acute flow state | AI compute repair watch | Not a real holding; theme drawdown | Watch only |
| 5 | No buy / defensive replay watch | WDC | Watch only | 0 | 0 | 0% | 662.47 | None | Old replay line 500, not near today | New entry invalid while DRAM/storage basket unwinds | Storage bottleneck leader | Large price, extension, cyclicality | Watch only |
| 6 | No buy / defensive replay watch | STX | Watch only | 0 | 0 | 0% | 1010.92 | None | Old replay line 835, not near today | USD 1000-class single share remains too large | Storage leader | Size and extension | Watch only |
| 7 | No buy | MXL / ALAB / DRAM / CRDO / TER / ORCL / RKLB / RDW | Watch only | 0 | 0 | 0% | See snapshot | Re-evaluate only after close audit or trend reclaim | n/a | Intraday knife-catch invalid while theme is breaking | Candidate-pool context only | Flow fragility acute | Watch only |

## User Confirmation Needed

- Confirm whether any broker-side stop, trim, or manual sell is desired intraday for MRVL, GLW, or TTMI. The automation did not submit orders.
- Confirm broker cash/NAV/open orders if different from the estimated HKD 50,000 baseline ledger.
- Confirm whether any RDW position remains; local memory treats RDW as closed from the user-confirmed 2026-06-22 sale.

Not investment advice.
