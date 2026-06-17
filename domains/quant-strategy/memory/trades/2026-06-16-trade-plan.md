# 2026-06-16 Trade Plan

Run time: 2026-06-16 23:02 Asia/Shanghai.

Scope: daily U.S. stock execution preparation and real-account ledger sync. This is not the 04:15 post-close audit, not broker login, and not real order submission.

## 1. Data Snapshot

Primary local quote workflow: Node `stock_service.js`, Tencent Primary, refreshed at 2026-06-16 23:02 Asia/Shanghai. External cross-check: finance snapshots around 2026-06-16 14:46-14:47 UTC / 22:46-22:47 Beijing. Equity/ETF quote quality is usable but delayed/public. Local Tencent VIX remains low quality because OHLC/volume are zero; external public VIX pages show VIX near `15.9-16.2`, so volatility is not confirming stress, but VIX/VIX3M term structure remains a data gap for this execution-prep run.

| Ticker | Local latest | Local change | Local high/low | External cross-check | Source / quality | Strategy read |
| --- | ---: | ---: | --- | ---: | --- | --- |
| MRVL | 300.55 | -2.70% | 317.00 / 298.42 | 303.15 | Tencent Primary + external finance; usable intraday | still above real cost; profit-protection review, no add |
| RDW | 13.62 | -8.19% | 14.58 / 13.18 | 13.595 | Tencent Primary + external finance; usable intraday | below `14.50` review line intraday; exit-review if confirmed by close |
| AMD | 523.37 | -4.37% | 548.95 / 521.01 | 526.75 | Tencent Primary + external finance; usable intraday | above old `492` replay line but extended/volatile; watch only |
| WDC | 691.10 | +5.75% | 729.92 / 685.00 | 692.60 | Tencent Primary + external finance; usable intraday | storage strength continues; no chase |
| STX | 1052.50 | +3.31% | 1097.00 / 1041.26 | 1057.14 | Tencent Primary + external finance; usable intraday | storage strength continues; no chase |
| SPY | 753.11 | -0.23% | 755.44 / 752.27 | 753.13 | usable intraday | broad market flat/slightly down |
| QQQ | 737.46 | -0.88% | 744.22 / 736.29 | 738.26 | usable intraday | growth risk-on cooled |
| SMH | 633.49 | -2.10% | 648.31 / 632.01 | 637.12 | usable intraday | semiconductor leadership cooling |
| HYG | 80.03 | -0.01% | 80.11 / 80.02 | 80.035 | usable intraday | credit not stressed |
| LQD | 109.12 | +0.11% | 109.17 / 109.05 | 109.075 | usable intraday | rates/credit neutral |
| IWM | 293.39 | -0.42% | 296.79 / 293.02 | 293.75 | usable intraday | small caps not leading |
| RSP | 212.86 | -0.01% | 214.30 / 212.84 | 213.115 | usable intraday | equal weight flat |
| ORCL | 189.25 | -1.76% | 195.30 / 187.67 | 189.55 | usable intraday | watch only; no chase |
| RKLB | 105.00 | -3.89% | 108.49 / 103.07 | 105.16 | usable intraday | watch only; RDW already occupies satellite sleeve |
| VIX | local 21.67 | 0.00% | 0 / 0 | public pages near 15.9-16.2 | local VIX unusable; external public only | not a hard trigger in this file |

## 2. Real Trades / Model Trades / Pending Confirmation

Real-account fills already recorded from user-confirmed information:

| Date | Ticker | Action | Shares | Fill price | Gross notional | Classification | Source |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 2026-06-15 | MRVL | Buy | 1 | 289.50 | 289.50 | pullback starter, core AI infrastructure candidate | user confirmation |
| 2026-06-15 | RDW | Buy | 5 | 15.00 | 75.00 | high-volatility satellite pullback | user confirmation |

Waiting user confirmation:

- Broker cash, FX, fees, tax, settlement, margin status, and any stale open orders.
- Whether RDW should be handled by manual close-review only or a hard broker stop order.

Model / simulation trades: none added today. The retired historical model ledger remains replay/watch context only.

## 3. Institutional Overlay Summary

```text
flow_fragility_state: elevated, about 8/14
trend_aligned_entry_state: existing MRVL hold remains acceptable but no add; RDW is trend_broken intraday; fresh AI/storage/space entries are cheap_but_unconfirmed or chase-invalid
AI_quality/capex_cycle: MRVL cyclical_supplier / bottleneck starter; RDW speculative_space satellite; AMD/WDC/STX high-sensitivity cyclical suppliers; ORCL platform_cloud watch; RKLB speculative_space watch
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high; sleeve_correlation_high for replay basket; token_cost_elasticity; valuation_concentration_pressure; VIX_term_structure_data_gap
action impact: protect existing real positions first; no fresh buy; RDW moves to exit-review if the completed close stays below 14.50; MRVL hold only, no chase/add
```

New buys do not pass `trend_aligned_entry` today because QQQ/SMH cooled, high-beta themes are volatile, and existing account facts are not fully synchronized.

## 4. Execution Checklist

| Priority | Ticker | Direction | Quantity | Target amount | Approx account weight | Reference price | Trigger condition | Stop / review price | Invalid condition | Strategy reason | Main risk | Status |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | RDW | Exit-review / defensive hold until close confirmation | 5 held; possible sell requires user confirmation | about USD 68.10 local value | about 2.65% NAV | 13.62 local; 15.00 gross cost; about 15.20 fee-adjusted cost | If official completed close is `<14.50`, execute user-confirmed exit/stop-review in next actionable window | `14.50` close review; no averaging down | If close reclaims `14.50` and then `16.00`, exit-review can downgrade to defensive hold | high-volatility satellite is below risk line intraday and fee drag is material in small account | selling may lock loss; holding may deepen drawdown / financing-risk exposure | waiting user/close confirmation; no broker order placed |
| 2 | MRVL | Hold / profit-protection review | 1 held | about USD 300.55 local value | about 11.7% NAV | 300.55 local; 289.50 cost | Hold while above 300/298 area and QQQ/SMH do not break sharply; review profit protection on reclaim/hold above 315 | review below 285; reduce/exit review below 280 close; priority exit below 275 close | Fresh add invalid while MRVL is below 303/315 confirmation and SMH is weak | AI interconnect/custom silicon starter remains profitable but event spike is fading | capex-cycle crowding; vertical rally failure | core hold; no add; no real order |
| 3 | AMD | Watch only / replay repair watch | 0 real shares | 0 | 0 | 523.37 local | Only reconsider after pullback/support or confirmed breakout with QQQ/SMH strength | historical replay stop reference `492` | Fresh buy invalid while account has no broker sync and AMD is volatile after vertical repair | AI compute trend repaired above old replay line | capex-cycle sensitivity and chase risk | watch only; not real holding |
| 4 | WDC | Watch only / defensive replay hold | 0 real shares | 0 | 0 | 691.10 local | Reassess only after pullback/support; no new buy during vertical storage rally | replay risk reference `500` | Fresh buy invalid after another large upside extension | storage bottleneck leadership persists | theme crowding and reversal risk | watch only; not real holding |
| 5 | STX | Watch only / defensive replay hold | 0 real shares | 0 | 0 | 1052.50 local | Reassess only after pullback/support; no new buy during vertical storage rally | replay risk reference `835` | Fresh buy invalid after another large upside extension | storage bottleneck leadership persists | theme crowding and reversal risk | watch only; not real holding |
| 6 | ORCL | Watch only | 0 | 0 | 0 | 189.25 local | Recheck near support/reclaim around prior 180-186 zone or clean base | prior plan review line `176` | No entry while extended and without trend-aligned trigger | cloud / AI factory watch candidate | capex burden, debt, margin risk | watch only |
| 7 | RKLB | Watch only | 0 | 0 | 0 | 105.00 local | Recheck only after volatility cools or support is confirmed | prior high-volatility review line `95` | No entry while RDW already represents satellite sleeve | space / satellite watch candidate | high volatility and overlap | watch only |
| 8 | Stale broker orders | Check / cancel if unwanted | n/a | n/a | n/a | n/a | User checks broker open-order screen | n/a | Any stale order remains active | prevent accidental duplicate exposure | unintended real fill | user confirmation required |

## 5. Required User Confirmation

- Confirm whether RDW should be manually exited if the official 2026-06-16 close remains below `14.50`, or only reviewed after the 04:15 audit.
- Confirm no stale MRVL/RDW/RKLB/ORCL/AMD/WDC/STX broker orders remain open.
- Confirm broker cash, USD/HKD conversion, fees, tax, and settlement status.

## 6. Replay Protocol

No replay ledger row was added. This run is intraday execution prep, not a completed-close audit, and the protocol says not to prefill future dates. If the 2026-06-16 completed close is later audited, update `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` with that completed row only.

Not investment advice.
