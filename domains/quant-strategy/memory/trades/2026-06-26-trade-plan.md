# 2026-06-26 Trade Plan

Run time: 2026-06-26 22:00 Asia/Shanghai.

Scope: U.S. intraday execution checklist. Regular session is open; prices below are live, not official closes.

## Intraday Order Guidelines

The market is experiencing a severe technology and semiconductor sell-off (QQQ -1.54%, SMH -3.80%), raising the Market Fear Gate score to **elevated (6/14)**. Active position protection is our absolute priority.

Amended broker-side checklist:

1. **GLW (Hold 2 Shares; No Add)**: GLW has pulled back to $216.34 (-5.12%). Hold. Trailing profit protection line remains **$210.00** (close-based). If it closes below $210, we will review for profit-taking in the next post-close audit.
2. **TTMI (Hold 3 Shares; No Add)**: TTMI has dropped to $196.03 (-6.91%), breaking below the $200 wind-control line. Hold the 3 shares. Do not average down or buy more. Hard stop remains **$188.00** close-based. If it closes below $200, we will alert the user for a potential risk-reduction next week.
3. **DRAM (Hold 4 Shares; No Add)**: DRAM has dropped to $72.05 (-6.29%). Hold. **CRITICAL:** Confirm if the protective `DRAM 4 @ 70.50 stop-market sell` order is active at the broker. If DRAM trades at or below $70.50 intraday, sell all 4 shares immediately.
4. **Other Candidates (Watch Only)**: MRVL ($269.22), AMD ($512.24), WDC ($617.19), and STX ($956.76) are all under pressure. No new buys are allowed.

## Data Snapshot

| Ticker | Intraday Price | Change | Yesterday Close | Source / time |
| --- | --- | --- | --- | --- |
| SPY | 728.76 | -0.75% | 734.30 | Tencent (Primary), 22:00 BJT |
| QQQ | 705.33 | -1.54% | 716.38 | Tencent (Primary) |
| SMH | 612.66 | -3.80% | 636.88 | Tencent (Primary) |
| VIX | 20.45 | +8.26% | 18.89 | Yahoo Chart, 22:00 BJT |
| VIX3M | 21.26 | +4.57% | 20.33 | Yahoo Chart |
| GLW | 216.34 | -5.12% | 228.01 | Tencent (Primary) |
| TTMI | 196.03 | -6.91% | 210.57 | Tencent (Primary) |
| DRAM | 72.05 | -6.29% | 76.89 | Tencent (Primary) |
| MRVL | 269.22 | -4.28% | 281.26 | Tencent (Primary) |
| AMD | 512.24 | -3.82% | 532.57 | Tencent (Primary) |
| WDC | 617.19 | -8.62% | 675.39 | Tencent (Primary) |
| STX | 956.76 | -6.69% | 1025.36 | Tencent (Primary) |

## Executive Action Checklist

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference price | Trigger | Stop / reduce line | Invalid condition | Strategy reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Hold / profit protection | GLW | Hold `2`; no add | `USD 432.68` / `6.78%` | 216.34 | Keep only while completed close stays at/above `210` | Close `<210` -> reduce/exit review; hard failure `<180` | Fades and close loses `210` | Strongest holding, but vertically extended and same AI-capex theme | `core hold` |
| 2 | Hold / risk review | TTMI | Hold `3`; no add | `USD 588.09` / `9.22%` | 196.03 | Maintain while above `188` close-based stop | Close `<200` -> warning/reduce review; close `<188` -> exit review | Close breaks below $188 | Breached $200 wind-control; no averaging down | `defensive hold` |
| 3 | Hold / protect | DRAM | Hold `4`; no add | `USD 288.20` / `4.52%` | 72.05 | Existing user-confirmed fill only; cancel duplicate buy orders | Protective exit `70.50` for all 4 shares (intraday) | Any additional DRAM/WDC fill | Memory ETF; nearing $70.50 protective exit | `defensive hold` |
| 4 | Watch only | MRVL | No order | `0` | 269.22 | New setup requires completed close `>285` plus SMH > 50-DMA | New plan required | Intraday spike above 285 without close confirmation | Closed position; watch only | `watch only` |
| 5 | Watch only | AMD | No order | `0` | 512.24 | Requires fresh trend-aligned setup | n/a | n/a | Watch only | `watch only` |
| 6 | Watch only | WDC / STX | No order | `0` | 617.19 / 956.76 | Consolidation and theme-crowding review | n/a | n/a | Same-theme crowding and sector sell-off block entry | `watch only` |

## Institutional Overlay

```text
flow_fragility_score: 8/14 -> elevated
flow_fragility_state: elevated
trend_aligned_entry_state: cheap_but_unconfirmed / gap-rejected for new entries
factor_macro_flags: theme_overlap_high; momentum_reversal_high; AI_capex_cycle_high
action impact: hold and protect GLW/TTMI/DRAM; cancel duplicate WDC/DRAM buys; block every new correlated-theme buy
```

Not investment advice.

## 23:17 BJT Intraday Refresh

Run time: 2026-06-26 23:17 Asia/Shanghai. U.S. regular session still open; all triggers below are intraday unless explicitly marked completed-close.

### Data update

Local Node quote workflow returned structured quote objects. Equity/ETF quotes are `source=Tencent (Primary)`. VIX from Tencent was low quality with zero OHLC, so volatility inputs use Yahoo chart fallback. Python and Google browser fallback were not needed.

| Ticker | Intraday price | Change | Intraday range | Source / time | Quality |
| --- | ---: | ---: | --- | --- | --- |
| SPY | 732.13 | -0.30% | 726.86-734.24 | Tencent, 23:17 BJT | Usable intraday |
| QQQ | 709.03 | -1.03% | 702.81-714.33 | Tencent, 23:17 BJT | Usable intraday |
| SMH | 611.00 | -4.06% | 609.20-621.67 | Tencent, 23:17 BJT | Usable intraday |
| SOXX | 591.96 | -5.32% | 590.50-605.80 | Tencent, 23:17 BJT | Usable intraday |
| VIX | 19.25 | +1.91% | 19.00-20.72 | Yahoo chart, 23:17 BJT | Usable; not official close |
| VIX3M | 20.58 | latest chart row | 20.44-21.37 | Yahoo chart, 23:17 BJT | Usable; sparse prior row caveat |
| GLW | 208.17 | -8.70% | 207.74-225.80 | Tencent, 23:17 BJT | Usable intraday |
| TTMI | 194.50 | -7.63% | 193.56-204.76 | Tencent, 23:17 BJT | Usable intraday |
| DRAM | 72.86 | -5.24% | 71.33-74.76 | Tencent, 23:17 BJT | Usable intraday |
| MRVL | 263.14 | -6.44% | 262.20-274.20 | Tencent, 23:17 BJT | Usable intraday |
| AMD | 512.17 | -3.83% | 502.61-525.11 | Tencent, 23:17 BJT | Usable intraday |
| WDC | 605.53 | -10.34% | 603.01-647.41 | Tencent, 23:17 BJT | Usable intraday |
| STX | 947.70 | -7.57% | 940.75-996.48 | Tencent, 23:17 BJT | Usable intraday |

### Updated execution checklist

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Reduce-review / protect profits | GLW | Hold `2`; no add; prepare post-close reduce review if close confirms | `USD 416.34` / `6.55%` | 208.17 | Completed close must reclaim/hold `210`; intraday break alone is not formal trigger | Close `<210` -> reduce/exit review; hard failure `<180` | Close back above 210 keeps hold; no add either way | Strongest prior winner but now lost profit-protection line intraday; same AI-capex basket pressure | `reduce-review / profit-protection watch` |
| 2 | Defensive hold | TTMI | Hold `3`; no add | `USD 583.50` / `9.17%` | 194.50 | Hold only while completed close remains above `188`; close `<200` escalates warning | Close `<200` -> reduce review; close `<188` -> exit review | Close reclaims 200 reduces warning but not add ban | Breached wind-control; Russell migration and theme sell-off increase risk | `defensive hold / below wind-control` |
| 3 | Defensive hold / protective stop watch | DRAM | Hold `4`; no add | `USD 291.44` / `4.58%` | 72.86 | Existing position only; confirm broker stop status | Intraday protective exit `70.50` for all 4 shares | Any additional DRAM/WDC fill; broker stop not active | Memory ETF remains above 70.50 but low was 71.33; allocation is complete | `defensive hold` |
| 4 | Watch only | MRVL | No order | `0` | 263.14 | Re-entry requires completed close `>285` plus SMH/stock trend repair | New plan required | Intraday bounce without close confirmation | Closed real position; event rebound failed | `watch only` |
| 5 | Watch only | AMD | No order | `0` | 512.17 | Fresh trend-aligned setup required | Historical old line `492` is not breached; no real holding | n/a | Above old replay stop but sector is weak; no real-position reduce action | `watch only` |
| 6 | Watch only | WDC / STX | No order | `0` | 605.53 / 947.70 | Wait for post-close sector repair and concentration reset | Historical hard lines 500 / 835 not breached intraday | Same-theme sell-off continues | Both above old hard lines but memory/storage crowding is unwinding | `watch only / replay defensive review` |
| 7 | Only observe next-regime queue | MU / CRDO / ALAB / TER / ANET | No order | `0` | 1157.61 / 251.18 / 375.20 / 425.14 / 157.53 | Require normal fear gate plus trend-aligned entry | New plan required | Current sell-off persists | Research queue only; no new buy during elevated flow fragility | `only observe` |

### Six-dimensional decision summary

| Dimension | Current read | Impact |
| --- | --- | --- |
| Market sentiment | QQQ -1.03%, SMH -4.06%, SOXX -5.32%; VIX elevated but not panic. | New-buy gate closed; protect active holdings first. |
| Theme strength | AI semiconductor/memory/interconnect basket is selling off together. | Same-theme additions blocked. |
| Stock relative strength | GLW lost 210 intraday; TTMI below 200; DRAM above 70.50 but weak; MRVL/WDC/STX under pressure. | Existing positions shift to defensive/reduce-review language. |
| Technical entry quality | No candidate has a clean trend-aligned entry during this drawdown. | Buy/add actions invalid. |
| Account constraints | Estimated cash remains high, but active equity sleeve is one correlated AI-capex basket. | Cash protects NAV; do not deploy cash merely because prices are lower. |
| Exit / risk plan | GLW close `<210`, TTMI close `<200`/`<188`, DRAM intraday `70.50`. | Post-close audit must handle formal triggers. |

### Institutional overlay

```text
flow_fragility_score: ~10/14 -> elevated / near-acute
flow_fragility_state: elevated
trend_aligned_entry_state: trend_broken for new correlated-theme entries
AI_quality/capex_cycle:
  - GLW: diversified_supplier / bottleneck, medium capex-cycle sensitivity, now profit-protection watch
  - TTMI: infrastructure_supplier / PCB-interconnect, medium-high capex-cycle sensitivity, below wind-control
  - DRAM: thematic_etf / memory-storage basket, high capex-cycle sensitivity, protective-stop watch
factor_macro_flags: theme_overlap_high; sleeve_correlation_high; momentum_reversal_high; AI_capex_cycle_high; semiconductor_basket_unwind
bottleneck_watch: ALAB/interconnect, HBM upstream, and memory-cost pushback are research fields only; not buy signals
action impact: no new buys/adds; protect GLW/TTMI/DRAM; confirm broker stop/cancel state; defer formal close triggers to 04:15 audit
```

## 23:23 BJT Addendum After User-Confirmed MXL Fill

User-confirmed real trade record exists separately: `memory/trades/2026-06-26-real-mxl-buy.md`.

- Real fill: `MXL buy 6 @ USD 90.70`.
- Estimated gross notional: `USD 544.20`.
- Estimated fee: `USD 1.00`.
- Initial risk line: `86.00`.
- No additional MXL buying today.

Local Node quote workflow was rerun after recognizing the fill and returned structured Tencent quotes. MXL traded at `91.14`, with intraday range `87.13-95.79`, so it remains above the `86.00` risk line.

Updated execution checklist including MXL:

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Reduce-review / protect profits | GLW | Hold `2`; no add | `USD 418.88` / `6.58%` | 209.44 | Completed close must reclaim/hold `210` | Close `<210` -> reduce/exit review | Close above 210 keeps hold; no add | Prior winner is now testing protection line | `reduce-review / profit-protection watch` |
| 2 | Defensive hold | TTMI | Hold `3`; no add | `USD 586.32` / `9.21%` | 195.44 | Hold only while completed close remains above `188` | Close `<200` -> reduce review; close `<188` -> exit review | Close reclaims 200 reduces warning but not add ban | Below wind-control; rebalance and theme pressure | `defensive hold` |
| 3 | Defensive hold / protective stop watch | DRAM | Hold `4`; no add | `USD 292.00` / `4.58%` | 73.00 | Existing position only | Intraday protective exit `70.50` | Any additional DRAM/WDC fill | Above 70.50 but still weak | `defensive hold` |
| 4 | Satellite hold / protect | MXL | Hold `6`; no add | `USD 546.84` / `8.59%` | 91.14 | User-confirmed fill only; no automation order | Risk line `86.00`; consider broker stop-market if user chooses | Breaks 86 or same-theme drawdown worsens | High-beta optical/InP/interconnect satellite, not a core add | `satellite hold` |
| 5 | Watch only | MRVL / AMD / WDC / STX | No order | `0` | 263.14 / 512.17 / 605.53 / 947.70 | Fresh post-close setup required | Existing old replay lines only | Intraday rebound without close repair | No current real holdings; same-theme sell-off blocks new buys | `watch only` |

Estimated account after MXL:

```text
working_cash: USD 4,524.64
equity_value: USD 1,844.04
estimated_NAV: USD 6,368.68
cash_ratio: 71.04%
equity_exposure: 28.96%
active_holdings: GLW 2, TTMI 3, DRAM 4, MXL 6
new_buy_gate: closed until post-close audit
```

## 02:21 BJT Addendum After User-Confirmed MU Fill

User-confirmed real trade record exists separately: `memory/trades/2026-06-26-real-mu-buy.md`.

- Real fill: `MU buy 1 @ USD 1,155.00`.
- Estimated gross notional: `USD 1,155.00`.
- Estimated fee: `USD 1.00`.
- Initial risk line: `1,100.00` close-based (50-day simple moving average).
- No additional MU buying today.

Local Node quote workflow was rerun after recognizing the fill and returned structured Tencent quotes. MU traded at `1149.50`, with intraday range `1140.00-1213.56`, so it remains above the `1,100.00` risk line.

Updated execution checklist including MU:

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Reduce-review / protect profits | GLW | Hold `2`; no add | `USD 432.06` / `6.76%` | 216.03 | Completed close must reclaim/hold `210` | Close `<210` -> reduce/exit review | Close above 210 keeps hold; no add | Prior winner testing protection line | `reduce-review / profit-protection watch` |
| 2 | Defensive hold | TTMI | Hold `3`; no add | `USD 590.46` / `9.24%` | 196.82 | Hold only while completed close remains above `188` | Close `<200` -> reduce review; close `<188` -> exit review | Close reclaims 200 reduces warning | Below wind-control; rebalance and theme pressure | `defensive hold` |
| 3 | Defensive hold / protective stop watch | DRAM | Hold `4`; no add | `USD 292.20` / `4.57%` | 73.05 | Existing position only | Intraday protective exit `70.50` | Any additional DRAM/WDC fill | Above 70.50 but still weak | `defensive hold` |
| 4 | Satellite hold / protect | MXL | Hold `6`; no add | `USD 559.08` / `8.75%` | 93.18 | User-confirmed fill only; no automation order | Risk line `86.00`; consider broker stop-market if user chooses | Breaks 86 or same-theme drawdown worsens | High-beta optical/InP/interconnect satellite | `satellite hold` |
| 5 | Core hold / protect | MU | Hold `1`; no add | `USD 1149.50` / `17.98%` | 1149.50 | User-confirmed fill only; no automation order | Close-stop `1,100.00` (or stop-market `1,090.00`) | Breaks 1100 or same-theme drawdown worsens | Core HBM leader, but raises memory concentration | `core hold` |
| 6 | Watch only | MRVL / AMD / WDC / STX | No order | `0` | 263.14 / 518.13 / 605.53 / 927.98 | Fresh post-close setup required | Existing old replay lines only | Intraday rebound without close repair | No current real holdings; same-theme sell-off blocks new buys | `watch only` |

Estimated account after MU:

```text
working_cash: USD 3,368.64
equity_value: USD 3,023.30
estimated_NAV: USD 6,391.94
cash_ratio: 52.70%
equity_exposure: 47.30%
active_holdings: GLW 2, TTMI 3, DRAM 4, MXL 6, MU 1
new_buy_gate: closed (thematic memory limit reached, MU+DRAM ~22.70% of NAV)
```

