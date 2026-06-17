# 2026-06-15 Trade Plan

Run time: 2026-06-15 23:04 Asia/Shanghai.

Scope: daily U.S. stock execution preparation and real-account ledger sync. This is not a formal U.S. post-close audit and is not broker order submission.

## Data Snapshot

Latest local quote workflow source: Tencent Primary, refreshed during this run.

| Ticker | Latest price | Change | Open | High | Low | Source | Quality |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 295.10 | +5.51% | 296.71 | 302.40 | 288.09 | Tencent Primary | usable intraday |
| RDW | 15.00 | -0.83% | 15.96 | 15.99 | 14.96 | Tencent Primary | usable intraday, high volatility |
| AMD | 551.13 | +7.73% | 535.75 | 558.37 | 530.50 | Tencent Primary | usable intraday |
| WDC | 647.00 | +14.94% | 618.78 | 658.80 | 612.00 | Tencent Primary | usable intraday, extended |
| STX | 1006.04 | +8.05% | 1032.52 | 1032.52 | 990.78 | Tencent Primary | usable intraday, extended |
| SPY | 754.64 | +1.74% | 751.85 | 754.76 | 751.76 | Tencent Primary | usable intraday |
| QQQ | 742.18 | +2.89% | 738.10 | 742.38 | 737.38 | Tencent Primary | usable intraday |
| SMH | 643.86 | +3.85% | 643.50 | 648.00 | 639.25 | Tencent Primary | usable intraday |
| HYG | 80.12 | +0.23% | 80.14 | 80.17 | 80.06 | Tencent Primary | usable intraday |
| LQD | 109.17 | +0.14% | 109.28 | 109.34 | 109.15 | Tencent Primary | usable intraday |
| IWM | 295.10 | +0.97% | 296.56 | 297.90 | 294.77 | Tencent Primary | usable intraday |
| RSP | 213.51 | +0.88% | 213.60 | 214.29 | 213.20 | Tencent Primary | usable intraday |
| ORCL | 193.26 | +4.96% | 187.39 | 194.40 | 186.21 | Tencent Primary | usable intraday |
| RKLB | 107.03 | +4.53% | 107.96 | 110.62 | 105.80 | Tencent Primary | usable intraday, high volatility |
| VIX | 21.67 | 0.00% | 0.00 | 0.00 | 0.00 | Tencent Primary | low quality; do not use as hard trigger |

Data gaps:

- VIX local quote remains low quality because OHLC and volume are zero.
- VIX/VIX3M term structure is unavailable.
- Broker cash, final FX rate, full commission, taxes, and settlement cash are not independently verified.
- All prices are intraday snapshots, not official close prices.

## Real Trades Confirmed

These are real-account fills already recorded from user-confirmed information. No additional broker action was performed by this automation.

| Date | Ticker | Action | Shares | Fill price | Gross notional | Classification | Source |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 2026-06-15 | MRVL | Buy | 1 | 289.50 | 289.50 | pullback starter, core AI infrastructure candidate | user confirmation |
| 2026-06-15 | RDW | Buy | 5 | 15.00 | 75.00 | high-volatility satellite pullback | user confirmation |

Estimated fee notes:

- RDW buy-side platform fee estimate is USD 1.00, making effective entry cost about USD 15.20 per share.
- MRVL should also include broker fees/FX in the real account, but only the USD 289.50 fill is confirmed.

## Institutional Overlay Summary

```text
flow_fragility_state: medium / elevated watch
trend_aligned_entry_state: trend_aligned for market and selected held starters; chase entries invalid
AI_quality/capex_cycle: MRVL cyclical_supplier / bottleneck, RDW speculative_space satellite, AMD/WDC/STX cyclical high sensitivity
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high; token_cost_elasticity; VIX_term_structure_data_gap
action impact: hold confirmed starters; no additional AI/storage chase buys; require pullback or confirmed breakout for any new buy
```

Flow-fragility score estimate: 7 / 14, `elevated watch`.

Trend-aligned entry score estimate: 4 / 5 for already-filled MRVL starter, 3 / 5 for RDW satellite, 3 / 5 for fresh AI/storage adds.

Replay protocol:

- No replay-ledger row was added. The 2026-06-15 data is intraday and the replay protocol should only add completed close rows or explicitly labeled snapshots without pre-filling future dates.

## Execution Checklist

| Priority | Ticker | Direction | Quantity | Target amount | Approx account weight | Reference price | Trigger condition | Stop / review price | Invalid condition | Strategy reason | Main risk | Status |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | MRVL | Hold | 1 | 295.10 market value | about 11%-12% baseline | 295.10 latest; 289.50 cost | Hold while above 285 intraday support and broad QQQ/SMH stays risk-on | Review below 285; reduce/exit review below 280 close; prioritize exit below 275 close | Close below 280 without SMH/QQQ offset | AI interconnect/custom silicon starter with pullback entry already confirmed | capex-cycle crowding; event rally may fail | core hold / starter, no add |
| 2 | RDW | Hold | 5 | 75.00 market value | about 3% baseline | 15.00 latest; 15.00 fill | Hold only if it stabilizes above 15 and can reclaim 16 | Exit / stop-review below 14.50 close | Failure to hold 15 with weak volume/market | small satellite exposure to space/satellite infrastructure | high volatility, financing/execution risk, fee drag | defensive hold / satellite near-stop review |
| 3 | AMD | No buy | 0 | 0 | 0 | 551.13 | Only reconsider after pullback/reclaim setup, not during vertical extension | Historical close stop line remains 492 for replay context | Fresh add invalid while extended after +7.73% intraday | Trend has repaired above old stop, but move is stretched | high capex-cycle sensitivity and chase risk | watch only; historical reduce-review no longer active on intraday price, pending formal close audit |
| 4 | WDC | No buy | 0 | 0 | 0 | 647.00 | Only reassess after pullback to support or formal close review | Historical replay risk line 500 | Fresh add invalid after +14.94% intraday move | Storage theme leadership is strong | same-theme crowding and large extension | defensive hold / near-stop review in replay context; no real order |
| 5 | STX | No buy | 0 | 0 | 0 | 1006.04 | Only reassess after pullback to support or formal close review | Historical replay risk line 835 | Fresh add invalid after +8.05% intraday move | Storage theme leadership is strong | same-theme crowding and large extension | defensive hold / near-stop review in replay context; no real order |
| 6 | ORCL | No buy | 0 | 0 | 0 | 193.26 | Recheck only after support/reclaim near prior 180-186 zone or clean breakout base | 176 prior plan review line | No entry while extended without a new base | AI factory/cloud watch name | capex burden and debt/margin risk | watch only |
| 7 | RKLB | No buy | 0 | 0 | 0 | 107.03 | Recheck only after volatility cools or support is confirmed | 95 prior high-volatility review line | No entry while account already has RDW satellite | space satellite theme already represented by RDW | high volatility and overlap | watch only |
| 8 | Existing stale orders | Cancel/check | n/a | n/a | n/a | n/a | User must verify broker open-order screen | n/a | Any unneeded stale order remains active | Avoid unintended real fills | accidental duplicate exposure | user confirmation required |

## Orders Needing User Confirmation

- Confirm whether any stale MRVL, RDW, RKLB, ORCL, AMD, WDC, or STX broker-side limit orders remain open.
- Confirm current USD/HKD cash and whether the MRVL and RDW buy-side fees match the USD 1 minimum rule.
- No new buy, sell, reduce, or add order is recommended without a fresh user check.

## Model / Simulation Distinction

- Real trades: MRVL 1 share at USD 289.50; RDW 5 shares at USD 15.00.
- Waiting user confirmation: broker cash, fees, FX, taxes, settlement, and stale open orders.
- Model/replay trades: none added today.
- No real order was logged in or submitted by this automation.

Not investment advice.
