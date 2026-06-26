# 2026-06-24 Post-Close Audit

Run time: 2026-06-25 Asia/Shanghai.

Scope: formal U.S. regular-session close audit for Wednesday, 2026-06-24. No broker login, no real order submission, and no unconfirmed fill assumption were made. Real account facts rely only on user confirmations already recorded locally.

## 1. Data Sources And Quality

Local quote workflow was used first as required.

| Layer | Result | Quality |
| --- | --- | --- |
| Node smoke test | `StockService.fetchQuotes` returned structured quote objects for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, RSP, HYG, LQD, IWM, GLW, TTMI, and DRAM. | Good for regular-close equity / ETF quotes; `source=Yahoo Chart (Fallback)`. |
| Yahoo chart fallback | Returned daily bars and `regularMarketTime` for equities/ETFs and VIX/VIX3M. | Good cross-check / fallback inside local workflow. |

Official close / reliable close snapshot:

| Ticker | Close | Change | Source | Timestamp / date |
| --- | --- | --- | --- | --- |
| SPY | 733.24 | -0.05% | Yahoo Chart (Fallback) | 2026-06-24 close |
| QQQ | 710.62 | -0.42% | Yahoo Chart (Fallback) | 2026-06-24 close |
| SMH | 618.92 | -0.50% | Yahoo Chart (Fallback) | 2026-06-24 close |
| MRVL | 276.70 | -0.84% | Yahoo Chart (Fallback) | 2026-06-24 close |
| GLW | 205.83 | +6.06% | Yahoo Chart (Fallback) | 2026-06-24 close |
| TTMI | 209.74 | -1.61% | Yahoo Chart (Fallback) | 2026-06-24 close |
| AMD | 519.74 | -0.02% | Yahoo Chart (Fallback) | 2026-06-24 close |
| ALAB | 399.92 | +0.73% | Yahoo Chart (Fallback) | 2026-06-24 close |
| CRDO | 268.99 | -1.11% | Yahoo Chart (Fallback) | 2026-06-24 close |
| RKLB | 85.41 | -10.21% | Yahoo Chart (Fallback) | 2026-06-24 close |
| WDC | 643.83 | -4.01% | Yahoo Chart (Fallback) | 2026-06-24 close |
| DRAM | 69.93 | +1.03% | Yahoo Chart (Fallback) | 2026-06-24 close |
| VIX | 18.63 | -4.41% | Yahoo Chart (Fallback) | 2026-06-24 close |
| VIX3M | 20.37 | -3.28% | Yahoo Chart (Fallback) | 2026-06-24 close |

## 2. Market Fear Gate

Computed from Yahoo chart daily bars:

| Component | Reading | Points | Interpretation |
| --- | --- | ---: | --- |
| VIX Level | 18.63 | 1 | Elevated volatility level (16 to 22). |
| VIX 5-day change | +13.6% | 0 | Normal (<15% change from ~16.40). |
| VIX / VIX3M | 0.915 | 0 | Normal contango (< 1.00). |
| SPY 63-day drawdown | -0.05% | 0 | Normal (0% to -4%). |
| QQQ 63-day drawdown | -0.42% | 0 | Normal (0% to -4%). |
| SMH 63-day drawdown | -7.47% | 1 | Mild drawdown (-4% to -8%). |
| SPY Trend Break | Below 50D ($745.16) | 1 | Caution: SPY below 50-day average. |
| QQQ Trend Break | Above 50D ($676.29) | 0 | Trend intact. |
| SMH Trend Break | Below 50D ($633.45) | 1 | Caution: SMH below 50-day average. |
| IWM/SPY 21-day ratio | +0.50% | 0 | Stable. |
| RSP/SPY 21-day ratio | +1.10% | 0 | Stable. |
| HYG/LQD 21-day ratio | -0.20% | 0 | Stable. |

Formal fear gate: **elevated (borderline normal)**, score **4/14** (shifted from elevated 5/14 yesterday).
*Note: Although the score of 4 technically falls in the "normal" regime, due to SPY and SMH still trading below their 50-day moving averages at the close, we retain a defensive posture until a confirmed breakout/repair occurs.*

## 3. Stop-Trigger Table

Active real holdings:

| Ticker | Close | Existing risk line | Triggered? | Near-stop? | Next state |
| --- | --- | --- | --- | --- | --- |
| GLW | 205.83 | Raised protection `195-200`; stop `<180` | No | No | Core hold / profit-protection. |
| TTMI | 209.74 | Warning `<205`; stop `<188` | No | No | Defensive hold; closed above warning line. |

## 4. Institutional Overlay Scorecard

```text
flow_fragility_score: 8 / 14 -> elevated
flow_fragility_state: elevated
trend_aligned_entry_state: unconfirmed for new buys at close; defensive-hold for existing positions
AI_quality/capex_cycle: GLW diversified supplier (medium sensitivity); TTMI PCB/interconnect supplier (medium-high sensitivity)
factor_macro_flags: theme_overlap_high; semiconductor_basket_correction
action impact: hold GLW/TTMI; no new buys or averaging down allowed at the close
```

## 5. Real-Account Portfolio Audit

Confirmed active holdings:

| Ticker | Shares | Cost basis | Close | Market value | Gross P/L | Status |
| --- | --- | --- | --- | --- | --- | --- |
| GLW | 2 | $181.50 (each) | 205.83 | 411.66 | +$48.66 | Core winner. Hold. |
| TTMI | 3 | $213.00 (each) | 209.74 | 629.22 | -$9.78 | Defensive hold. |

Estimated account metrics:

| Metric | Estimate |
| --- | ---: |
| USD baseline equivalent | 6410.26 |
| Working cash after MRVL sale and fee | 5376.56 |
| Equity market value at 2026-06-24 close | 1040.88 |
| Estimated NAV | 6417.44 |
| Estimated return vs baseline | +0.11% |
| Cash ratio | 83.78% |
| Equity exposure | 16.22% of NAV |
| Active holdings count | 2 |

## 6. Audit Conclusion

What worked:
- Exiting MRVL at $272.30 protected the capital baseline from further intraday drawdown before its modest late-day recovery.
- TTMI successfully defended the $205.00 warning line, closing at $209.74.
- Overall NAV ended positive (+0.11% vs baseline) despite a volatile session.

Not investment advice.
