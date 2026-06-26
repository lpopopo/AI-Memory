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
