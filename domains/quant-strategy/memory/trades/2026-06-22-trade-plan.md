# 2026-06-22 Trade Plan

Run time: 2026-06-22 23:19 Asia/Shanghai.

Scope: real-account intraday execution checklist and planning ledger. U.S. regular session is still open. No broker login, order submission, order cancellation, or unconfirmed fill assumption is made.

## Data Snapshot

Local quote workflow was usable. Node `StockService.fetchQuotes` returned structured quote objects for ETFs, holdings, and candidates using `Tencent (Primary)`. VIX and VIX3M were fetched through the same local Node client via Yahoo chart fallback because Tencent did not return those index rows.

| Item | Result |
| --- | --- |
| Run time | `2026-06-22 23:19 Asia/Shanghai` |
| Quote workflow | Usable; structured quote objects returned |
| Equity / ETF source | `Tencent (Primary)` |
| VIX source | `Yahoo Chart (Fallback)` |
| Volatility reference | VIX `17.50`; VIX3M `19.89`; VIX/VIX3M `0.880` |
| Data quality | Good for intraday execution prep; not official close data |
| Account baseline | HKD 50,000, approx. USD 6,410.26 at 7.80 HKD/USD |

Latest intraday quote references:

| Ticker | Price | Change | Open | High | Low | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| SPY | 744.59 | -0.29% | 747.70 | 750.18 | 743.15 | Tencent |
| QQQ | 737.60 | -0.30% | 742.02 | 745.43 | 735.35 | Tencent |
| SMH | 665.60 | +0.87% | 670.35 | 671.83 | 661.52 | Tencent |
| IWM | 297.54 | +0.66% | 297.13 | 299.49 | 296.16 | Tencent |
| MRVL | 301.76 | -2.84% | 313.39 | 314.17 | 298.77 | Tencent |
| RDW | 12.74 | -11.22% | 14.03 | 13.89 | 12.60 | Tencent |
| GLW | 199.26 | +2.23% | 200.48 | 204.48 | 196.87 | Tencent |
| TTMI | 216.93 | +0.23% | 220.84 | 222.93 | 210.74 | Tencent |
| MXL | 95.69 | +7.81% | 92.50 | 97.53 | 89.60 | Tencent |
| ALAB | 428.79 | +2.81% | 425.61 | 440.99 | 420.11 | Tencent |
| AMD | 547.32 | +1.85% | 545.50 | 562.99 | 535.71 | Tencent |
| WDC | 758.99 | +1.71% | 772.75 | 779.80 | 741.55 | Tencent |
| STX | 1103.38 | +3.10% | 1089.00 | 1127.99 | 1080.20 | Tencent |
| DRAM | 80.29 | +4.67% | 80.68 | 81.34 | 79.53 | Tencent |
| RKLB | 97.55 | -9.04% | 106.99 | 107.40 | 96.50 | Tencent |

Daily K-line references are Yahoo chart intraday daily bars for 2026-06-22, not official completed closes. They are usable for execution context, not for formal close-stop confirmation.

## Executive Action

Market state remains `elevated / repair`: VIX is elevated but not inverted versus VIX3M, QQQ/SPY are slightly negative, SMH remains positive, and small caps are firmer. AI infrastructure leadership is still strong but crowded. New exposure is allowed only through already-confirmed fills or trend-aligned pullback/reclaim setups; no new chase buy is valid.

Priority:

1. **RDW exit remains first priority.** RDW is now around `12.74`, below the already-triggered `14.50` close-stop line and below the 5/10/20/50-day averages. This is not a normal hold.
2. **TTMI is now a confirmed real holding.** User confirmed `3` shares bought at `213.00`. The later intraday low `210.74` confirms the planned pullback zone traded. No same-day add.
3. **MRVL and GLW are holds with profit protection.** MRVL is still above daily MA5/10/20 but has faded from the morning high; GLW remains strong and extended.
4. **MXL remains invalidated for entry.** It opened above the no-chase rule and is still extended.
5. **AMD/WDC/STX remain watch/replay context only.** They are not current real holdings.

## Institutional Overlay

```text
trend_aligned_entry_state:
- TTMI: trend_aligned for the already-filled pullback entry; no add after fill.
- RDW: trend_broken; exit-review / stop execution.
- MRVL/GLW: trend valid but extended/profit-protection, not add candidates.
- MXL/ALAB/AMD/WDC/STX: watch only because current prices are chase/extension setups or not real holdings.

flow_fragility_state:
- elevated. AI/semiconductor/storage and optical/interconnect leadership is strong, but theme overlap and momentum extension are high.

AI_quality/capex_cycle:
- MRVL: cyclical_supplier / bottleneck, high capex-cycle sensitivity.
- GLW: diversified_supplier / bottleneck, medium capex-cycle sensitivity.
- TTMI: infrastructure_supplier / PCB-interconnect, medium-high capex-cycle sensitivity.
- RDW: speculative_space / satellite_infrastructure, high risk, satellite/watch class only.

factor_macro_flags:
- growth_duration_high; momentum_reversal_high; theme_overlap_high; AI_capex_cashflow_pressure; flow_rebalancing_risk.

bottleneck_watch:
- Optical/interconnect and PCB/infrastructure remain active; storage/memory is strong but too extended for new single-name entry.

action impact:
- Resolve RDW stop first, hold TTMI/MRVL/GLW, protect gains, block all new chase buys.
```

## Execution Checklist

| Priority | Ticker | Direction | Quantity | Target amount | Approx account weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason | Risk point | Status |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | RDW | Sell / exit | 5 shares | USD 63.70 gross at reference | ~1.0% | $12.74 | Immediate broker-side exit; prior close-stop below $14.50 already triggered | Already triggered; current intraday bar below MA5/10/20/50 and 20-day low | Only user-written manual override can defer | Stop discipline and trend-broken satellite | Slippage already widened; do not average down | Pending user/broker execution |
| 2 | TTMI | Hold | 3 shares | USD 650.79 market value | ~10.1% | $216.93 | User-confirmed fill at $213.00 already occurred; no same-day add | Caution below $205; stop/exit review below completed daily close $188.00 | Failed support with close below $188, or theme reversal | AI data-center PCB / interconnect core candidate; pullback zone traded | New position, medium-high capex-cycle sensitivity, crowded AI infra theme | Confirmed real holding / hold |
| 3 | MRVL | Hold | 1 share | USD 301.76 market value | ~4.7% | $301.76 | Hold; no add; monitor $298-$301 behavior after fade from high | Review below $285; stop below $280 close; profit-protection around $295-$298 | Loss of AI interconnect theme support or close below risk line | Existing AI interconnect core | High beta, capex-cycle/crowding, intraday fade | Core hold / profit-protection review |
| 4 | GLW | Hold | 2 shares | USD 398.52 market value | ~6.2% | $199.26 | Hold; no add into extension | Caution $188-$190; stop/exit review below $180-$181 | Loss of optical/fiber theme support | Optical/fiber core starter worked | Profit giveback after vertical extension | Core hold / profit-protection review |
| 5 | MXL | No buy | 0 | USD 0 | 0% | $95.69 | N/A | N/A | Already invalidated: opened above $92 and remains above no-chase zone | Optical/interconnect candidate only after reset | Chasing extended move; no technical support entry | Invalidated / do not buy |
| 6 | ALAB | No buy | 0 | USD 0 | 0% | $428.79 | Re-evaluate only after event reset/base | N/A | Chasing index-inclusion/event extension | Strong interconnect theme | Single-share concentration, valuation/event risk | Watch only |
| 7 | AMD | No real action | 0 | USD 0 | 0% | $547.32 | Watch only; no real holding | Old replay stop line $492 only applies to replay context | Chasing after repair extension | AI compute repair | Capex cycle and theme crowding | Watch only |
| 8 | WDC | No real action | 0 | USD 0 | 0% | $758.99 | Watch only; no real holding | Old replay stop line $500 only applies to replay context | Chasing extended storage theme | Storage bottleneck leader | Extension and crowding | Watch only |
| 9 | STX | No real action | 0 | USD 0 | 0% | $1103.38 | Watch only; no real holding | Old replay stop line $835 only applies to replay context | USD 1000-class single-share concentration | Storage leader | Share price and extension too large | Watch only |
| 10 | RKLB | No buy | 0 | USD 0 | 0% | $97.55 | Watch only after sharp drop | N/A | Space theme weakness today | Space / satellite read-through | Theme pressure confirms RDW caution | Watch only |

## Confirmed Real Holdings

Only user-confirmed or broker-confirmed positions are counted as real holdings:

| Ticker | Shares | Expected role | Current status |
| --- | ---: | --- | --- |
| MRVL | 1 | AI interconnect core | Core hold / profit-protection review |
| RDW | 5 | Space / satellite satellite | Exit triggered; pending execution |
| GLW | 2 | Optical / fiber core | Core hold / profit-protection review |
| TTMI | 3 | AI PCB / interconnect core | Core hold / support-test filled |

## User Confirmation Needed

- Confirm whether the RDW sell was executed, including shares, fill price, time, and fee.
- Confirm whether any broker-side open orders remain after the TTMI fill.
- Confirm broker cash/NAV if it differs from the HKD 50,000 / USD 6,410.26 baseline estimate.

Not investment advice.
