# 2026-06-24 Trade Plan

Run time: 2026-06-24 22:50 Asia/Shanghai.

Scope: U.S. intraday execution checklist. Regular session is open; prices below are live. No broker login, order submission, or unconfirmed fill assumption was made.

## 22:48 BJT Order Amendment

Local Tencent quotes at 2026-06-24 22:48 BJT showed MRVL `274.38`, GLW `212.60`, TTMI `215.97`, SPY `+0.69%`, QQQ `+0.74%`, and SMH `+0.45%`.

Amended broker-side checklist:

1. Cancel all unfilled buy orders, if any, including MRVL, GLW, TTMI, AMD, ALAB, CRDO, MXL, WDC, DRAM, SNOW, DDOG, and DE.
2. If MRVL 1 share is still held, replace any stale MRVL sell limit with an executable sell order for all 1 share. Primary implementation: marketable limit near the live bid/current range, with a short validity window; do not leave a high passive limit that can miss the exit. The completed-close stop below `280` remains triggered.
3. Do not place a new GLW sell order solely because of today's event gap. Hold 2 shares; no add. Reassess profit protection if price loses `205`, and use the completed close rather than an intraday spike for the formal decision.
4. Do not place a new TTMI order. Hold 3 shares; no add. `210` remains the intraday warning area and a completed close below `188` remains the hard stop-review line.
5. Do not submit new opportunity orders today. Market repair is not broad enough to reopen the buy gate while an existing hard stop remains unresolved.

## Data Snapshot

| Ticker | Price | Change | Yesterday Close | Source / time |
| --- | --- | --- | --- | --- |
| SPY | 737.04 | +0.47% | 733.58 | Yahoo Chart Fallback, 2026-06-24 22:44 BJT |
| QQQ | 716.49 | +0.40% | 713.65 | Yahoo Chart Fallback |
| SMH | 621.58 | -0.08% | 622.05 | Yahoo Chart Fallback |
| VIX | 18.81 | - | 19.49 | Yahoo Chart Fallback |
| VIX3M | 20.58 | - | 21.06 | Yahoo Chart Fallback |
| MRVL | 272.19 | -2.45% | 279.04 | Yahoo Chart Fallback |
| GLW | 211.27 | +8.86% | 194.07 | Yahoo Chart Fallback |
| TTMI | 214.14 | +0.46% | 213.17 | Yahoo Chart Fallback |
| AMD | 522.19 | +0.45% | 519.85 | Yahoo Chart Fallback |
| WDC | 654.34 | -2.45% | 670.75 | Yahoo Chart Fallback |
| DRAM | 70.64 | +2.05% | 69.22 | Yahoo Chart Fallback |

## Executive Action Checklist

1.  **MRVL: Mandatory Stop-Loss Exit (Immediate)**
    *   **Action**: Sell **1 share** of MRVL.
    *   **Trigger**: Yesterday's close of $279.04 breached the $280 stop line. Overnight rebound to $285 failed at regular open; stock is currently trading at $272.19. We must execute the stop-loss to protect capital from further decline.
    *   **Limit/Market**: Market or limit order at/near current price (~$272.19) to exit within the session.
2.  **GLW: Core Winner Hold (No Add)**
    *   **Action**: Hold **2 shares** of GLW.
    *   **Rationale**: Corning is surging (+8.86% to $211.27) on massive Nvidia/Meta/Amazon optical fiber deals. Do not add to this position due to high extension, but protect paper profits.
3.  **TTMI: Defensive Hold**
    *   **Action**: Hold **3 shares** of TTMI.
    *   **Rationale**: TTMI is stable above cost at $214.14. Hold with stop-loss below $188 completed close.
4.  **No New Buys (Buy Gate Closed)**
    *   **Action**: All new buys (AMD, ALAB, CRDO, WDC, DRAM, etc.) are blocked.
    *   **Rationale**: Market Fear Gate is **elevated** (score 5/14) and sector flow fragility is **acute** (11/14). Maintain defensive cash posture (>75% cash).

## User Confirmation Needed

*   **MRVL Exit**: Please confirm once you have executed the sell order for MRVL (1 share) and provide the exact filled price and fee details so we can update the ledger.

Not investment advice.

## 23:17 BJT Intraday Refresh

This section supersedes earlier intraday prices, but does not convert any checklist item into a real fill.

### Data quality

| Data | Observed time | Source | Quality |
| --- | --- | --- | --- |
| Equities / ETFs | 2026-06-24 23:16 BJT | Local Node quote workflow, `Tencent (Primary)` | Good structured intraday objects |
| VIX / VIX3M | 2026-06-24 23:17 BJT | Local Node workflow, `Yahoo Chart (Fallback)` | Usable intraday volatility snapshot |
| Tencent VIX row | 2026-06-24 23:16 BJT | Tencent | Rejected: zero OHLC/volume and inconsistent price |

Key references: SPY `739.00` (`+0.74%`), QQQ `717.31` (`+0.51%`), IWM `299.44` (`+1.40%`), RSP `211.31` (`+1.16%`), SMH `621.02` (`-0.17%`), SOXX `603.49` (`+0.02%`), VIX `18.05`, VIX3M `20.16`, VIX/VIX3M `0.895`.

### Complete execution checklist

| Priority | Action | Ticker | Direction / quantity | Target amount / NAV weight | Reference | Trigger | Stop / reduce line | Invalid condition | Reason / risk | State |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Exit-review | MRVL | Sell `1` if still held | `~USD 271.08` / `~4.20%` | 271.08 | 2026-06-23 completed close `279.04 < 280` already triggered the stop | Do not wait for a high passive limit; broker execution details control the ledger | Only a user/broker-confirmed prior sale invalidates this task | Stop discipline; stock remains weak despite broad-market rebound | **Pending user/broker confirmation; no fill assumed** |
| 2 | Core hold / profit protection | GLW | Hold `2`; no add | `~USD 428.18` / `~6.64%` | 214.09 | Event-driven strength remains intact | Review on loss of `205`; formal close review remains primary | A completed close that breaks the protection structure | Strong optical/fiber relative strength, but `+10.31%` extension makes chasing unsafe | Hold |
| 3 | Defensive hold | TTMI | Hold `3`; no add | `~USD 645.93` / `~10.01%` | 215.31 | Price remains above `213` cost and outperforms SMH | Intraday warning `210`; completed-close stop-review `<188` | User/broker reports a sale or close breaks the hard line | Relative strength is acceptable, but same-theme correlation remains high | Hold |
| 4 | Hold cash / cancel stale buys | All unfilled buy orders | Cancel if any; quantity depends on broker | `0` new exposure | n/a | Any stale buy order exists | n/a | None without trend-aligned entry and resolved MRVL stop | Existing hard stop unresolved; semiconductor leadership is not broad | Pending user confirmation |
| 5 | Watch only | AMD | No order | `0` | 517.25 | Re-evaluate after a completed-close trend repair | Historical replay line `492`, not a live holding stop | New verified real holding | Above old replay stop, but no trend-aligned entry authorization | Watch only |
| 6 | Watch only | WDC / STX | No order | `0` | 651.44 / 1012.26 | Storage basket must regain relative strength | Historical replay lines `500` / `835`; not live holdings | New verified real holding | Both are below prior close and remain high-cycle / high-price risks | Watch only |
| 7 | Watch only | ALAB / CRDO / MXL / DRAM / TER / ORCL / RKLB / RDW | No order | `0` | See local quote snapshot | Require trend-aligned entry, acceptable concentration, and completed-close confirmation | Candidate-specific review required | Any price-only bounce without trend confirmation | Mixed tape and high flow fragility; no knife-catching or chasing | Watch only |

### Institutional overlay

```text
flow_fragility_state: acute / fragmented rebound
trend_aligned_entry_state: trend_broken or unconfirmed for new correlated-theme buys
AI_quality/capex_cycle: GLW diversified supplier/bottleneck; TTMI medium-high capex sensitivity; MRVL high sensitivity; WDC/STX/DRAM high cyclicality
factor_macro_flags: theme_overlap_high; semiconductor_basket_divergence; momentum_reversal_high; AI_capex_cashflow_pressure; duration_support_from_bonds
bottleneck_watch: optical/fiber confirmed by GLW price action; AEC/optical, PCB and storage remain watch-only
action impact: execute/confirm MRVL exit first; hold GLW/TTMI without adding; block new buys
```

No broker login, order submission, cancellation, or real-fill assumption was made.
