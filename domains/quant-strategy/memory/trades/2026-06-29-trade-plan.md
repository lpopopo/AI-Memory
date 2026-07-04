# 2026-06-29 Trade Plan

Run time: 2026-06-29 23:19 Asia/Shanghai.

Scope: U.S. intraday execution checklist. The regular session is open; all prices are intraday snapshots, not formal close triggers. No brokerage login, order submission, or inferred real fill was performed.

## Data source and quality

Local quote workflow was used first per `tools/README.md`.

| Layer | Result | Quality |
| --- | --- | --- |
| Node `StockService.fetchQuotes` | Returned structured quote objects for indices, ETFs, active holdings, replay names and candidates. | Usable intraday equity/ETF data; `source=Tencent (Primary)`. |
| Tencent VIX | Returned `21.67` with zero OHLC and unchanged prior fields. | Low quality; not used for fear score. |
| Yahoo Chart direct via local `StockService._requestJson` | Returned 2026-06-29 daily/intraday chart rows for `^VIX`, `^VIX3M`, SPY, QQQ, SMH and holdings. | Usable volatility and trend cross-check; still intraday, not official close. |
| Python / Google fallback | Not used. | Not needed because Node returned structured quote objects and Yahoo covered volatility. |

Main intraday snapshots around 23:19 BJT:

| Ticker | Price | Day change | Intraday range | Source | Quality |
| --- | ---: | ---: | --- | --- | --- |
| SPY | 737.11 | +1.11% | 732.11-739.89 | Tencent | Usable intraday |
| QQQ | 715.68 | +1.30% | 705.17-718.66 | Tencent | Usable intraday |
| SMH | 617.91 | +1.03% | 596.29-620.26 | Tencent | Usable intraday; large intraday shakeout |
| VIX | 18.26 | -0.81% vs prior daily bar | n/a | Yahoo Chart | Usable intraday/daily chart |
| VIX3M | 19.82 | -1.54% vs prior daily bar | n/a | Yahoo Chart | Usable intraday/daily chart |
| GLW | 239.08 | +8.16% | 215.13-241.49 | Tencent | Usable intraday |
| TTMI | 181.61 | -5.16% | 174.50-189.06 | Tencent | Usable intraday; below hard line intraday |
| DRAM | 68.45 | -4.77% | 66.47-70.88 | Tencent | Usable intraday; below protective trigger intraday |
| MXL | 101.21 | +4.77% | 94.64-106.20 | Tencent | Usable intraday |
| MU | 1068.68 | -5.62% | 1023.65-1128.70 | Tencent | Usable intraday; below close-risk line intraday |

## Executive action checklist

No new buy/add order is valid while the current real sleeve remains one correlated AI-capex basket and several holdings are near or below risk lines intraday.

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 0 | Confirm possible protective execution | DRAM | User/broker confirmation needed for `4` shares | If still held: `USD 273.80` / `4.32%` | 68.45 | Intraday low `66.47` is below the stated `70.50` protective exit trigger | `70.50` intraday protective exit | Do not record a sale until user/broker confirms fill | If the broker stop-market order was active, it may already have triggered; automation cannot infer real execution | `exit-confirmation-needed` |
| 1 | Confirm possible protective execution / close review | MU | User/broker confirmation needed for `1` share | If still held: `USD 1068.68` / `16.85%` | 1068.68 | Intraday price and low are below `1100`; hard protection reference was `1090` if user set it | Completed close `<1100` triggers risk review; possible broker stop `1090` must be confirmed | Do not add; do not call this a formal close trigger yet | Event-day/T+1 chase risk is materializing; memory theme concentration remains high | `core defensive hold / close-risk review` |
| 2 | Reduce / exit review | TTMI | Hold `3` only if no broker stop exists; no add | `USD 544.83` / `8.59%` | 181.61 | Intraday price and low are below the `188` hard completed-close line | Close `<188` -> hard exit review; close `<200` -> reduce-review | Any averaging down | TTMI remains below wind-control and now below hard line intraday; formal close audit must decide | `exit-review intraday / not formal close` |
| 3 | Hold / protect gains | GLW | Hold `2`; no add | `USD 478.16` / `7.54%` | 239.08 | Strong intraday rebound above 210 protection | Close `<210` -> reduce/exit review; hard failure `<180` | Close loses `210` again | Strongest holding, but still part of same AI-capex basket | `core hold` |
| 4 | Hold / protect | MXL | Hold `6`; no add | `USD 607.26` / `9.58%` | 101.21 | Above 86 and above 91-92 upgraded core-style stop zone | Risk line was `86`; 2026-06-27 sizing rule suggests reclassify as core and raise protection to about `91-92` | Breaks upgraded risk zone or same-theme selloff resumes | Position size is core-like, not satellite-like; do not average down | `core/reclassified hold pending post-close` |
| 5 | Watch only | MRVL | No order | `0` | 263.32 | Re-entry requires completed close `>285` plus SMH/stock trend repair | New plan required | Intraday bounce without close confirmation | Closed real position; event rebound has not repaired trend | `watch only` |
| 6 | Watch only | AMD | No order | `0` | 522.00 | Fresh trend-aligned setup required | Old replay line `492`; current price is above it | n/a | Not a real holding; no reduce action. Do not chase. | `watch only` |
| 7 | Watch / replay defensive review | WDC / STX | No order | `0` | 621.38 / 922.00 | Wait for sector repair and concentration reset | Old replay lines `500` / `835` | Same-theme crowding persists | Both bounced but remain volatile after severe drawdown | `watch only / defensive review` |
| 8 | Only observe next-regime queue | CRDO / ALAB / TER / ANET / QCOM | No order | `0` | 238.51 / 422.25 / 453.34 / 162.65 / 189.44 | Require normal fear gate plus trend-aligned entry and portfolio room | New plan required | Current portfolio risk unresolved | Research queue only; no new exposure before stops and concentration are reconciled | `only observe` |

## Six-dimensional decision summary

| Dimension | Current read | Impact |
| --- | --- | --- |
| Market sentiment | SPY/QQQ/SMH are rebounding, VIX/VIX3M are easing, but SMH had a deep intraday shakeout. | Provisional fear gate improves, but not enough to add while position-level stops are unresolved. |
| Theme strength | GLW/MXL rebound while TTMI/DRAM/MU remain weak; AI-capex leadership is internally divergent. | Treat the sleeve as fragile, not repaired. |
| Stock relative strength | GLW and MXL outperform; TTMI, DRAM and MU underperform the theme. | Weakest duplicate exposures need priority review. |
| Technical entry quality | No new candidate clears trend-aligned entry after portfolio-level risk review. | All buys/adds are invalid today. |
| Account constraints | Estimated NAV if all positions still held is about `USD 6,341.37`; cash about `53.12%`. | Cash is adequate, but correlated exposure is still too high. |
| Exit / risk plan | DRAM intraday `70.50`, TTMI close `<188`, MU close `<1100`, MXL upgraded `91-92`, GLW close `<210`. | Confirm broker stops first; formal close audit handles completed-close triggers. |

## Institutional overlay

```text
flow_fragility_score: ~9/14 -> elevated
flow_fragility_state: elevated / internally divergent rebound
trend_aligned_entry_score: 1/5 for new correlated entries -> trend_broken
AI_quality/capex_cycle:
  GLW: diversified_supplier / bottleneck, medium sensitivity, core hold
  TTMI: infrastructure_supplier / PCB-interconnect, medium-high sensitivity, exit-review intraday
  DRAM: thematic_etf / memory-storage basket, high sensitivity, protective-trigger confirmation needed
  MXL: speculative_bottleneck / optical component, high sensitivity, position size now core-like
  MU: cyclical_supplier / HBM-memory leader, high sensitivity, close-risk review
factor_macro_flags: theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high;
  memory_concentration_high; momentum_reversal_high; semiconductor_intraday_shakeout
bottleneck_watch: Cerebras / memory-substitution / Optical HBM / GB300 software optimization are research fields only, not buy signals
action impact: freeze all new buys; verify DRAM/MU protective order status; prepare TTMI close-stop audit
```

Not investment advice.
