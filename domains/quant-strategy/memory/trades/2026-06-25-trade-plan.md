# 2026-06-25 Trade Plan

Run time: 2026-06-25 21:48 Asia/Shanghai.

Scope: U.S. intraday execution checklist. Premarket is active; regular session opens in ~40 minutes. No broker login, order submission, or unconfirmed fill assumption was made.

## Premarket Order Guidelines

Premarket quotes show a massive positive gap-up rebound across Nasdaq and semiconductor indices (QQQ +1.64%, SMH +3.73%), catalyzed by Micron's (MU) blockbuster earnings and Qualcomm's CPU update.

Amended broker-side checklist:

1. **No Chasing at the Open**: Do not place any market orders or high limit orders at the open gap-up. Let the initial 15-30 minutes of volatility settle.
2. **GLW (Hold 2 Shares; No Add)**: GLW is gapping to $224.16 (+8.93%). Hold and protect. Raise the trailing close-based protection line to **$210.00** (previously $195-200). If it closes below $210, we will review for profit-taking in the next post-close audit.
3. **TTMI (Hold 3 Shares; No Add)**: TTMI has rebounded to $217.00 (+3.46%), recovering above its cost of $213.00. Hold the 3 shares. No adding on the gap. Intraday warning line is carried forward at **$205.00** and hard stop-loss review at **$188.00** (close-based).
4. **MRVL (Watch Only)**: MRVL has reclaimed $280 in premarket (trading at $281.68) but remains below the **$285.00** technical re-entry trigger. Do not buy back yet.
5. **Conditional Pullback Buys (WDC & DRAM)**: With the Market Fear Gate entering Normal (4/14) and MRVL's stop-loss executed, we authorize conditional pullback limit orders for storage/memory: WDC (1 share limit at $655.00, core sleeve) and DRAM (4 shares limit at $73.00, satellite sleeve). Keep limit prices strict; do not chase.


## Data Snapshot

| Ticker | Premarket Price | Change | Yesterday Close | Source / time |
| --- | --- | --- | --- | --- |
| SPY | 737.03 | +0.51% | 733.24 | Yahoo Chart, 2026-06-25 21:40 BJT |
| QQQ | 722.23 | +1.64% | 710.62 | Yahoo Chart |
| SMH | 643.00 | +3.73% | 618.92 | Yahoo Chart |
| VIX | 17.85 | -4.19% | 18.63 | Yahoo Chart |
| VIX3M | 20.37 | - | 20.37 | Yahoo Chart |
| GLW | 224.16 | +8.93% | 205.83 | Yahoo Chart |
| TTMI | 217.00 | +3.46% | 209.74 | Yahoo Chart |
| MRVL | 281.68 | +1.80% | 276.70 | Yahoo Chart |
| AMD | 547.19 | +5.42% | 519.74 | Yahoo Chart |
| WDC | 700.40 | +8.69% | 643.83 | Yahoo Chart |
| DRAM | 78.77 | +12.64% | 69.93 | Yahoo Chart |

## Executive Action Checklist

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference | Trigger | Stop / reduce line | Invalid condition | Reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Core hold / profit protection | GLW | Hold `2`; no add | `~USD 448.32` / `~6.92%` | 224.16 | Event-driven agreements with NVDA/Meta/Amazon | Raised close-based protection `<210` | Close breaks below $180 (hard stop) | Optical/fiber leader; extremely extended; no chasing | Hold |
| 2 | Core hold | TTMI | Hold `3`; no add | `~USD 651.00` / `~10.05%` | 217.00 | PCB/interconnect player; rebounded above cost | Intraday warning `<205`; close stop `<188` | Close breaks below $188 | Rebound tracks SMH repair; hold current position | Hold |
| 3 | Watch only | MRVL | No order | `0` | 281.68 | Re-entry requires reclaiming $285+ and SMH > 50-DMA | n/a | Close reclaims $285 and SMH > 50-DMA | Wait for right-side confirmation; do not chase premarket bounce | Watch only |
| 4 | Watch only | WDC | No order | `0` | 670.42 | Pullback limit buy at $655 cancelled | n/a | n/a | Memory core position; cancelled limit buy to hold cash | Watch only |
| 5 | Limit Buy | DRAM | Buy `2` shares | `~USD 147.60` / `~2.3%` | 73.80 | Pullback support entry (low was $73.50) | Close stop-review `<70.50` | Intraday price does not touch $73.80 | Memory satellite starter; pullback pending | Pending |

| 6 | Stop Limit Buy | DRAM | Buy `2` shares | `~USD 153.60` / `~2.4%` | 76.50 / 76.80 | Right-side breakout confirmation | Close stop-review `<70.50` | Price does not reclaim $76.50 | Memory satellite add; breakout trigger | Pending |
| 7 | Watch only | Others / TER | No order | `0` | n/a | Market gate is in repair; TER added to watchlist | n/a | n/a | Maintain high cash ratio (~81%-83%) to protect NAV | Watch only |



## Institutional Overlay

```text
flow_fragility_state: elevated / recovery rebound
trend_aligned_entry_state: unconfirmed for new entries due to gap-up extension; hold existing
AI_quality/capex_cycle: GLW diversified supplier; TTMI interconnect supplier; MU/WDC/DRAM memory suppliers
factor_macro_flags: theme_overlap_high; semiconductor_basket_gap_up; momentum_repair
bottleneck_watch: optical/fiber confirmed; memory/storage and PCB/interconnect in sharp recovery
action impact: hold GLW/TTMI; execute conditional limit buys for WDC/DRAM on pullback; block all chase buys
```

Not investment advice.

## 23:18 BJT Intraday Execution Refresh

Session status: U.S. regular session remains open. The following is an intraday checklist, not a completed-close trigger and not a broker order record.

Data quality:

- Equities and ETFs: local Node quote workflow, `Tencent (Primary)`, observed 2026-06-25 23:17-23:18 BJT; structured objects, usable intraday quality.
- VIX / VIX3M: local Node Yahoo chart fallback, observed 2026-06-25 23:17-23:18 BJT; usable index snapshot, zero-volume index fields ignored.
- Provisional fear gate: about `normal 3/14`; formal close audit remains assigned to the 04:15 post-close task.

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference price | Trigger / condition | Stop / reduce line | Invalid condition | Strategy reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Hold / profit protection | GLW | Hold `2`; no add | `USD 446.40` / `6.93%` | 223.20 | Keep only while completed close stays at/above `210` | Close `<210` -> reduce/exit review; hard failure `<180` | Event gap fades and close loses `210` | Strongest holding, but vertically extended and same AI-capex theme | `core hold` |
| 2 | Hold / risk review | TTMI | Hold `3`; no add | `USD 625.35` / `9.71%` | 208.45 | Maintain while above `200` wind-control and no formal hard-stop trigger | Close `<200` -> reduce review; close `<188` -> exit review | Russell rebalance pressure persists with close below `200` | Recovered from intraday low but remains below cost; no averaging down | `defensive hold` |
| 3 | Hold / protect | DRAM | Hold `4`; no add | `USD 300.52` / `4.66%` | 75.13 | Existing user-confirmed fill only; cancel duplicate buy orders | Protective exit `70.50` for all 4 shares | Any additional DRAM/WDC fill would violate completed allocation | Memory ETF reduced single-name risk, but entry followed a crowded earnings gap and is below cost | `defensive hold` |
| 4 | Cancel | WDC | Cancel any `1 @ 655` buy | `0` | 671.49 | User-side cancellation confirmation required | n/a | Order remains live and later fills | DRAM allocation is complete; avoid duplicate memory-theme exposure | `pending user confirmation` |
| 5 | Cancel | DRAM | Cancel every remaining buy order | `0` | 75.13 | User-side cancellation confirmation required | Keep only protective sell at `70.50` | Duplicate buy remains live | Prevent accidental over-allocation after full 4-share fill | `pending user confirmation` |
| 6 | Watch only | MRVL | No order | `0` | 271.97 | New setup requires completed close `>285` plus confirmed trend/RS repair | New plan required | Intraday spike above 285 without close confirmation | Position is closed; failed gap and weak close trajectory prohibit chase | `watch only` |
| 7 | Watch only | AMD | No order | `0` | 515.52 | Existing historical `492` close-stop is not breached; any new entry needs fresh trend-aligned setup | No active-account stop | Close loses `492` or relative strength deteriorates | Not held; do not inherit stale model-position instructions | `watch only` |
| 8 | Watch only | WDC / STX | No order | `0` | 671.49 / 1013.03 | Re-evaluate only after post-gap consolidation and theme-crowding review | Old near-stop levels are not active holdings rules | Chasing earnings-driven gap or adding correlated exposure | Both are above old stop zones, but same-theme crowding and opening-gap fade block entry | `watch only` |
| 9 | Watch only | MRVL / ALAB / CRDO / RKLB / TER | No order | `0` | See quote log | Require `trend_aligned_entry >=4/5`, acceptable valuation and concentration | New setup required | Weak RS, gap rejection, or market gate deterioration | Candidate universe only; no executable order | `watch only` |

Institutional overlay:

```text
flow_fragility_score: about 8/14 -> elevated
flow_fragility_state: elevated
trend_aligned_entry_state: cheap_but_unconfirmed / gap-rejected for new AI-memory and semiconductor entries
AI_quality/capex_cycle: GLW diversified supplier; TTMI medium-high sensitivity interconnect supplier; DRAM high-sensitivity thematic ETF
factor_macro_flags: theme_overlap_high; momentum_reversal_high; AI_capex_cycle_high; opening_gap_rejection
bottleneck_watch: optical/fiber remains strongest; memory demand evidence is strong but short-term price crowding is visible
action impact: hold and protect GLW/TTMI/DRAM; cancel duplicate WDC/DRAM buys; block every new correlated-theme buy
```

No real order was submitted, cancelled, or assumed filled by this automation.
