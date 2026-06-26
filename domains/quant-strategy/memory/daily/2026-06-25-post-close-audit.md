# 2026-06-25 Post-Close Audit

Run time: 2026-06-26 Asia/Shanghai.

Scope: formal U.S. regular-session close audit for Thursday, 2026-06-25. No broker login, no real order submission, and no unconfirmed fill assumption were made. Real account facts rely only on user confirmations already recorded locally.

## 1. Data Sources And Quality

Local quote workflow was used as required.

| Layer | Result | Quality |
| --- | --- | --- |
| Node smoke test | `StockService.fetchQuotes` returned structured quote objects for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, RSP, HYG, LQD, IWM, GLW, TTMI, and DRAM. | Good for regular-close equity / ETF quotes; `source=Tencent (Primary)`. |
| Yahoo chart fallback | Returned daily bars and `regularMarketTime` for VIX/VIX3M. | Good cross-check / fallback inside local workflow. |

Official close / reliable close snapshot:

| Ticker | Close | Change | Source | Timestamp / date |
| --- | --- | --- | --- | --- |
| SPY | 734.30 | +0.14% | Tencent (Primary) | 2026-06-25 close |
| QQQ | 716.38 | +0.81% | Tencent (Primary) | 2026-06-25 close |
| SMH | 636.88 | +2.90% | Tencent (Primary) | 2026-06-25 close |
| MRVL | 281.26 | +1.65% | Tencent (Primary) | 2026-06-25 close |
| GLW | 228.01 | +10.78% | Tencent (Primary) | 2026-06-25 close |
| TTMI | 210.57 | +0.40% | Tencent (Primary) | 2026-06-25 close |
| AMD | 532.57 | +2.47% | Tencent (Primary) | 2026-06-25 close |
| WDC | 675.39 | +4.90% | Tencent (Primary) | 2026-06-25 close |
| STX | 1025.36 | +3.23% | Tencent (Primary) | 2026-06-25 close |
| DRAM | 76.89 | +9.95% | Tencent (Primary) | 2026-06-25 close |
| VIX | 18.89 | +1.40% | Yahoo Chart (Fallback) | 2026-06-25 close |
| VIX3M | 20.33 | -0.20% | Yahoo Chart (Fallback) | 2026-06-25 close |

## 2. Market Fear Gate

Computed from Yahoo chart daily bars:

| Component | Reading | Points | Interpretation |
| --- | --- | ---: | --- |
| VIX Level | 18.89 | 1 | Elevated volatility level (16 to 22). |
| VIX 5-day change | +2.44% | 0 | Normal (<15% change from 18.44). |
| VIX / VIX3M | 0.929 | 0 | Normal contango (< 1.00). |
| SPY 63-day drawdown | -1.36% | 0 | Normal (0% to -4%). |
| QQQ 63-day drawdown | -3.71% | 0 | Normal (0% to -4%). |
| SMH 63-day drawdown | -4.79% | 1 | Mild drawdown (-4% to -8%). |
| SPY Trend Break | Above 50D ($732.07) | 0 | Trend intact. |
| QQQ Trend Break | Above 50D ($700.70) | 0 | Trend intact. |
| SMH Trend Break | Above 50D ($563.27) | 0 | Trend intact. |
| IWM/SPY 21-day ratio | +5.15% | 0 | Stable. |
| RSP/SPY 21-day ratio | +4.38% | 0 | Stable. |
| HYG/LQD 21-day ratio | -0.90% | 0 | Stable. |

Formal fear gate: **normal**, score **2/14** (shifted from elevated 4/14 yesterday).
*Stance: Although the score improved to normal, new buys remain governed by theme-crowding and sector overlay rules. Staged entry is permitted only on high-quality technical setups.*

## 3. Stop-Trigger Table

Active real holdings:

| Ticker | Close | Existing risk line | Triggered? | Near-stop? | Next state |
| --- | --- | --- | --- | --- | --- |
| GLW | 228.01 | Raised protection `$210` | No | No | Core hold / profit-protection. |
| TTMI | 210.57 | Warning `<205`; stop `<188` | No | No | Defensive hold. Rebounded above warning level. |
| DRAM | 76.89 | Protective stop `<70.50` | No | No | Defensive hold. |

## 4. Institutional Overlay Scorecard

```text
flow_fragility_score: 8 / 14 -> elevated
flow_fragility_state: elevated
trend_aligned_entry_state: cheap_but_unconfirmed
factor_macro_flags: theme_overlap_high; momentum_reversal_high; AI_capex_cycle_high
action impact: hold GLW/TTMI/DRAM; block new AI/semiconductor adds due to high theme overlap
```

## 5. Real-Account Portfolio Audit

Confirmed active holdings:

| Ticker | Shares | Cost basis | Close | Market value | Gross P/L | Status |
| --- | --- | --- | --- | --- | --- | --- |
| GLW | 2 | $181.50 (each) | 228.01 | 456.02 | +$93.02 | Core winner. Hold. |
| TTMI | 3 | $213.00 (each) | 210.57 | 631.71 | -$7.29 | Defensive hold. |
| DRAM | 4 | $76.43 (each) | 76.89 | 307.56 | +$1.84 | Satellite hold. |

Estimated account metrics:

| Metric | Estimate |
| --- | ---: |
| USD baseline equivalent | 6410.26 |
| Working cash after DRAM buy and fee | 5069.84 |
| Equity market value at 2026-06-25 close | 1395.29 |
| Estimated NAV | 6465.13 |
| Estimated return vs baseline | +0.86% |
| Cash ratio | 78.42% |
| Equity exposure | 21.58% of NAV |
| Active holdings count | 3 |

## 6. Audit Conclusion

What worked:
- Rebounding indices and semiconductor/AI theme led to a positive daily return (+0.86% NAV vs baseline).
- TTMI repaired its prior breakdown, reclaiming the $210 level and removing immediate stop-review pressure.
- DRAM ETF buy filled at $76.43 and closed at $76.89, providing a diversified memory play.
- GLW surged over +10% on Nvidia/Meta/Amazon datacenter fiber catalysts, now trading at $228.01.

Not investment advice.
