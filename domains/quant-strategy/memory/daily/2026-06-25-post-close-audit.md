# 2026-06-25 Post-Close Audit

Run time: 2026-06-26 21:54 Asia/Shanghai.

Scope: formal U.S. regular-session close audit for Thursday, 2026-06-25. The 2026-06-26 U.S. session had already started when this audit ran, so 2026-06-26 intraday bars were excluded. No broker login, no real order submission, no cancellation, and no unconfirmed fill assumption were made.

## 1. Data Sources And Quality

Local quote workflow was used first as required.

| Layer | Result | Quality |
| --- | --- | --- |
| Node smoke test / `StockService.fetchQuotes` | Returned structured quote objects for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, SOXX, RSP, HYG, LQD, IWM, GLW, TTMI, and DRAM. | Workflow available; `source=Tencent (Primary)`. At run time, latest quote fields had begun reflecting 2026-06-26 activity, so they were used to verify workflow availability, not as 2026-06-25 formal closes. |
| Local Node Yahoo chart daily-bar request | Returned completed daily bars for equities, ETFs, and VIX. The series was truncated to bars dated `<= 2026-06-25`. | Reliable completed daily close cross-check for equities, ETFs, and VIX. |
| VIX3M fallback | Yahoo chart daily data had a 2026-06-25 gap for `^VIX3M`. FRED `VXVCLS` / Yahoo visible snapshot showed `VIX3M 20.33` at the 2026-06-25 close. | Usable official/public volatility fallback; source caveat recorded. |
| Python / Google browser fallback | Not used. | Not needed because local Node path returned structured quote objects and Yahoo daily bars were usable. |

Formal completed-close references:

| Ticker | 2026-06-25 close | Change vs prior close | Source | Data quality |
| --- | ---: | ---: | --- | --- |
| MRVL | 281.26 | +1.65% | Local Node Yahoo chart daily bar | Completed close |
| AMD | 532.57 | +2.47% | Local Node Yahoo chart daily bar | Completed close |
| WDC | 675.39 | +4.90% | Local Node Yahoo chart daily bar | Completed close |
| STX | 1025.36 | +3.23% | Local Node Yahoo chart daily bar | Completed close |
| SPY | 734.30 | +0.14% | Local Node Yahoo chart daily bar | Completed close |
| QQQ | 716.38 | +0.81% | Local Node Yahoo chart daily bar | Completed close |
| SMH | 636.88 | +2.90% | Local Node Yahoo chart daily bar | Completed close |
| SOXX | 625.20 | +3.94% | Local Node Yahoo chart daily bar | Completed close |
| VIX | 18.89 | +1.40% | Local Node Yahoo chart daily bar | Completed close |
| VIX3M | 20.33 | -0.20% | FRED `VXVCLS` / Yahoo visible snapshot fallback | Completed close fallback |
| RSP | 211.75 | +0.65% | Local Node Yahoo chart daily bar | Completed close |
| HYG | 79.88 | +0.04% | Local Node Yahoo chart daily bar | Completed close |
| LQD | 109.50 | +0.08% | Local Node Yahoo chart daily bar | Completed close |
| IWM | 298.91 | +0.75% | Local Node Yahoo chart daily bar | Completed close |
| GLW | 228.01 | +10.78% | Local Node Yahoo chart daily bar | Completed close |
| TTMI | 210.57 | +0.40% | Local Node Yahoo chart daily bar | Completed close |
| DRAM | 76.89 | +9.95% | Local Node Yahoo chart daily bar | Completed close |

## 2. Market Fear Gate

Computed from 2026-06-25 completed daily bars.

| Component | Reading | Points | Interpretation |
| --- | ---: | ---: | --- |
| VIX level | 18.89 | 1 | Elevated volatility band, but below stress. |
| VIX 5-day change | +2.44% | 0 | No volatility spike. |
| VIX / VIX3M | 0.929 | 0 | Normal contango. |
| SPY 63-day drawdown | -3.33% | 0 | Normal. |
| QQQ 63-day drawdown | -3.99% | 0 | Borderline normal, not below -4%. |
| SMH 63-day drawdown | -4.79% | 1 | Mild semiconductor drawdown. |
| SPY trend | Close 734.30 vs 50D 733.77 | 0 | Barely above 50D. |
| QQQ trend | Close 716.38 vs 50D 701.41 | 0 | Above 50D. |
| SMH trend | Close 636.88 vs 50D 563.27 | 0 | Above 50D. |
| IWM/SPY 21-day ratio | +5.17% | 0 | Improved. |
| RSP/SPY 21-day ratio | +4.24% | 0 | Improved breadth. |
| HYG/LQD 21-day ratio | -1.03% | 0 | Mild, not deterioration threshold. |

Formal fear gate: `normal`, score `2/14`.

Risk controls from the framework: risk multiplier `100%`, max gross exposure `95%`, max new buy exposure `50%`, cash floor `5%`. This does not reopen same-theme buys by itself because the institutional overlay and concentration review remain restrictive.

## 3. Stop-Trigger Table

Active real-account holdings:

| Ticker | Close | Existing stop / reduce line | Triggered? | Near-stop? | Next state |
| --- | ---: | --- | --- | --- | --- |
| GLW | 228.01 | Profit-protection review on completed close `<210`; hard failure `<180` | No | No | `core hold / profit-protection`; no add after vertical extension. |
| TTMI | 210.57 | Reduce review on close `<200`; hard exit review `<188` | No | No, but rebalance/AI-theme risk remains | `defensive hold`; no averaging down or add. |
| DRAM | 76.89 | Protective exit `70.50` for all 4 shares | No | No; close is about 8.3% above line | `defensive hold`; allocation complete, no further DRAM/WDC buy. |

Replay/watch-only controls:

| Ticker | Close | Existing historical / watch line | Triggered? | Next state |
| --- | ---: | --- | --- | --- |
| MRVL | 281.26 | Closed real position; re-entry requires completed close `>285` plus trend/RS repair | No re-entry trigger | `watch only`; event rebound must not cause automatic chase. |
| AMD | 532.57 | Historical replay risk line `492` | No | `watch only`; no real holding and no reduce-review needed. |
| WDC | 675.39 | Historical replay hard line `500`; cancelled real-account buy line `655` | No stop trigger; buy line should remain cancelled | `watch only`; memory/storage overlap blocks new buy. |
| STX | 1025.36 | Historical replay hard line `835` | No | `watch only`; USD 1000-class sizing and theme overlap keep it off the real-account action list. |

## 4. Institutional Overlay Scorecard

```text
flow_fragility_score: 8 / 14 -> elevated
flow_fragility_state: elevated
trend_aligned_entry_score: 3 / 5 -> cheap_but_unconfirmed for new correlated-theme entries
AI_quality/capex_cycle:
  - GLW: diversified_supplier / bottleneck, medium capex-cycle sensitivity
  - TTMI: infrastructure_supplier / PCB-interconnect, medium-high capex-cycle sensitivity
  - DRAM: thematic_etf / memory-storage basket, high capex-cycle sensitivity
factor_macro_flags: theme_overlap_high; sleeve_correlation_high; momentum_reversal_high; AI_capex_cycle_high; opening_gap_rejection
bottleneck_watch: optical/fiber strongest; memory/storage demand evidence strong but crowded after MU-driven gap
action impact: hold and protect GLW/TTMI/DRAM; confirm residual DRAM/WDC buys are cancelled; block every new correlated-theme buy despite normal market fear score
```

Portfolio-level correlated-risk review: active holdings are only 3 names, but all express AI infrastructure / capex-chain exposure. GLW and TTMI are optical/interconnect/PCB infrastructure; DRAM is memory/storage. Treat the equity sleeve as one correlated AI-capex basket for risk, not as three independent diversifiers.

## 5. Real-Account Portfolio Audit

Working cash uses the prior local estimate after the user-confirmed DRAM buy and assumed USD 1 buy fee: `USD 5,069.84`. This is not a broker statement.

| Ticker | Shares | Cost basis | Close | Market value | Gross unrealized P/L | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 181.50 | 228.01 | 456.02 | +93.02 | Core winner / profit-protection. |
| TTMI | 3 | 213.00 | 210.57 | 631.71 | -7.29 | Defensive hold. |
| DRAM | 4 | 76.43 | 76.89 | 307.56 | +1.84 | Defensive hold; no add. |

Estimated metrics:

| Metric | Estimate |
| --- | ---: |
| Working cash | USD 5,069.84 |
| Equity market value | USD 1,395.29 |
| Estimated NAV | USD 6,465.13 |
| Change vs USD 6,410.26 baseline | +USD 54.87 / +0.86% |
| Cash ratio | 78.42% |
| Equity exposure | 21.58% |
| Active holdings | 3 |
| Active themes | 2, but highly overlapping: optical/interconnect and memory/storage AI infrastructure |
| Largest single position | TTMI, about 9.77% of NAV |

Current-account scope remains real-account only. The retired USD 20,000 strategy-tracking model is not a live portfolio; its MRVL/AMD/WDC/STX values are used only for the replay ledger.

## 6. Replay Ledger

Replay protocol is applicable because the 2026-06-08 overlay replay ledger already tracks MRVL/AMD/WDC/STX through completed closes. Appended the completed 2026-06-25 row. No future date was prefilled, and overlay portfolio value remains blank because there is no explicit model execution assumption.

## 7. Audit Conclusion

- The market fear gate improved to `normal 2/14`, but the portfolio action stance remains defensive because flow fragility is still `elevated` and the real equity sleeve is thematically correlated.
- No active holding triggered a close-based stop on 2026-06-25. GLW remains the strongest holding, TTMI avoided the `<200` reduce line, and DRAM closed above the 70.50 protective line.
- MRVL is closed and remains watch-only; the 281.26 close is below the 285 re-entry condition.
- AMD/WDC/STX are watch/replay context only and did not breach their old risk lines.
- Do not add more DRAM or WDC. Confirm residual buy orders are cancelled and whether the DRAM 70.50 protective stop-market sell is active on the user/broker side.

Not investment advice.
