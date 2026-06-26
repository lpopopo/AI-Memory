# 2026-06-22 Post-Close Audit

Run time: 2026-06-23 Asia/Shanghai.

Scope: formal U.S. regular-session close audit for Monday, 2026-06-22. No broker login, no real order submission, and no unconfirmed fill assumption were made. Real account facts rely only on user confirmations already recorded locally.

## 1. Data Sources And Quality

Local quote workflow was used first as required.

| Layer | Result | Quality |
| --- | --- | --- |
| Node smoke test | `StockService.fetchQuotes` returned structured quote objects for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, SOXX, RSP, HYG, LQD, IWM, GLW, TTMI, and RDW. | Good for regular-close equity / ETF quotes; `source=Tencent (Primary)`. |
| VIX via Tencent | Returned only low-quality `VIX` row with zero OHLC/volume. | Rejected for formal volatility gate. |
| Yahoo chart fallback | Returned daily bars and `regularMarketTime` for equities/ETFs and VIX/VIX3M. | Good cross-check / fallback inside local workflow hierarchy. |
| Google browser fallback | Not used. | Not needed because local Node + Yahoo chart paths returned structured data. |

Official close / reliable close snapshot:

| Ticker | Close | Change | Source | Timestamp / date |
| --- | ---: | ---: | --- | --- |
| MRVL | 307.86 | -0.88% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `regularMarketTime=2026-06-22T20:00:01Z` |
| AMD | 551.63 | +2.65% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `20:00:01Z` |
| WDC | 732.62 | -1.82% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `20:00:00Z` |
| STX | 1094.04 | +2.22% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `20:00:01Z` |
| SPY | 744.39 | -0.31% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `20:00:00Z` |
| QQQ | 737.95 | -0.36% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `20:00:00Z` |
| SMH | 668.91 | +1.37% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `20:00:00Z` |
| SOXX | 655.01 | +2.43% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close; Yahoo `20:00:00Z` |
| VIX | 17.28 | +5.37% | Yahoo chart daily bars fallback | 2026-06-22 close; Yahoo `20:15:01Z` |
| VIX3M | 19.76 | +0.97% | Yahoo chart daily bars fallback | 2026-06-22 close; Yahoo `20:15:01Z` |
| RSP | 209.61 | -0.17% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close |
| HYG | 79.94 | -0.09% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close |
| LQD | 108.78 | -0.27% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close |
| IWM | 298.18 | +0.88% | Tencent primary, cross-checked by Yahoo chart daily bars | 2026-06-22 close |

## 2. Market Fear Gate

Computed from Yahoo chart daily bars:

| Component | Reading | Interpretation |
| --- | ---: | --- |
| VIX | 17.28 | Elevated volatility level, but below stress. |
| VIX 5-day change | -2.26% | No spike. |
| VIX / VIX3M | 0.8745 | Normal contango, not inverted. |
| SPY 63-day drawdown | -2.00% | Normal. |
| QQQ 63-day drawdown | -1.10% | Normal. |
| SMH 63-day drawdown | 0.00% | New/recent high; semiconductor leadership intact. |
| SPY/QQQ/SMH vs 50D and 200D | All above | Trend risk off not triggered. |
| IWM/SPY 21-day ratio | +6.09% | Small caps improving versus SPY. |
| RSP/SPY 21-day ratio | +2.40% | Equal-weight breadth improving modestly. |
| HYG/LQD 21-day ratio | -0.66% | No material credit deterioration. |

Formal fear gate: `normal`, score about `1/14`.

Risk controls from the fear framework:

```text
risk_multiplier: 100%
max_gross_exposure: 95%
max_new_buy_exposure: 50%
cash_floor: 5%
```

Operational caveat: market fear is normal, but institutional flow fragility and theme overlap remain elevated, so this does not authorize chase buys in AI infrastructure names.

## 3. Stop-Trigger Table

Active real holdings:

| Ticker | Close | Existing line | Triggered? | Near-stop? | Next state |
| --- | ---: | --- | --- | --- | --- |
| MRVL | 307.86 | Guard/profit protect `298-300`; review `<285`; stop `<280` completed close | No | No, but monitor fade from intraday high | Core hold / profit-protection review; no add or event chase. |
| GLW | 209.83 | Raised protection `203-205`; serious review `<200` / `<195`; old stop-review `<180-181` | No | Not stop-near; close is above protection band | Core winner / profit-protection review; protect gains, no add into extension. |
| TTMI | 221.47 | Watch `220`; caution `213-214` / warning `<210`; completed-close stop-review `<188` | No | No | Core hold; support-test fill working; no same-day/next-day chase add. |

Closed today / no longer active:

| Ticker | Close | Real-account status | Next state |
| --- | ---: | --- | --- |
| RDW | 13.02 | User-confirmed sale: 5 shares at 13.30 | Closed; any future RDW action is a new setup, not a continuation. |

Replay/watch context:

| Ticker | Close | Existing replay risk line | Triggered? | Status |
| --- | ---: | --- | --- | --- |
| AMD | 551.63 | 492 close risk line | No. Close is above 492, so no reduce-review is required. | Watch/replay repair; no real holding. |
| WDC | 732.62 | 500 replay risk line | No; not near stop. | Watch/replay extended leader; no real chase. |
| STX | 1094.04 | 835 replay risk line | No; not near stop. | Watch/replay extended leader; USD 1000-class share price remains too large for small-account satellite role. |

## 4. Institutional Overlay Scorecard

```text
flow_fragility_score: 7 / 14 -> elevated
flow_fragility_state: elevated
trend_aligned_entry_score: 4 / 5 for existing MRVL/GLW/TTMI holds, but extended/chase-invalid for new adds
trend_aligned_entry_state: trend_aligned_hold / no_chase_add
AI_quality/capex_cycle: MRVL cyclical_supplier/bottleneck high sensitivity; GLW diversified_supplier/bottleneck medium sensitivity; TTMI infrastructure_supplier/PCB-interconnect medium-high sensitivity
factor_macro_flags: theme_overlap_high; growth_duration_high; momentum_reversal_high; AI_capex_cashflow_pressure; flow_rebalancing_risk
bottleneck_watch: optical/interconnect and PCB remain active; memory/storage strong but WDC/STX are extended and not real-account entries
action impact: hold current winners, protect gains, block same-theme chase buys, and require portfolio-level correlation review before adding another AI infrastructure name
```

Portfolio-level correlated-risk review is required and completed because `flow_fragility=elevated` and current holdings all express the AI infrastructure / capex-chain theme. The issue is not single-name size; it is common-factor exposure.

## 5. Real-Account Portfolio Audit

Confirmed active holdings after the user-confirmed RDW sale:

| Ticker | Shares | Close | Market value | Gross P/L vs gross fill | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| MRVL | 1 | 307.86 | 307.86 | +18.36 | Core hold / profit-protection review |
| GLW | 2 | 209.83 | 419.66 | +56.66 | Core winner / profit-protection review |
| TTMI | 3 | 221.47 | 664.41 | +25.41 | Core hold / support-test fill working |

Estimated account metrics:

| Metric | Estimate |
| --- | ---: |
| USD baseline equivalent | 6410.26 |
| Estimated cash after TTMI buy and RDW sale | 5105.26 |
| Equity market value at 2026-06-22 close | 1391.93 |
| Estimated NAV | 6497.19 |
| Estimated return vs baseline | +1.36% |
| Cash ratio | 78.58% |
| Equity exposure | 21.42% of NAV / 21.71% of baseline |
| Active holdings count | 3 |
| Equity theme count | 1 dominant theme, with 3 subthemes: interconnect/custom silicon, optical/fiber, PCB/interconnect |
| Largest single-stock weight | TTMI about 10.23% of NAV |

Broker cash, exact FX, tax, settlement, margin status, and open orders are not independently verified by this automation.

Historical replay model check:

| Ticker | Historical model shares | Close | Historical market value |
| --- | ---: | ---: | ---: |
| MRVL | 8.0383 | 307.86 | 2474.67 |
| AMD | 4.6083 | 551.63 | 2542.08 |
| WDC | 3.6880 | 732.62 | 2701.90 |
| STX | 2.2401 | 1094.04 | 2450.76 |

Using the replay cash placeholder `12323.96`, historical replay NAV is about `22493.37`. This is not the current real account.

## 6. Audit Conclusion

What worked:

- RDW stop discipline was resolved by the user-confirmed sale; the open stop item is no longer active.
- TTMI pullback fill closed above cost and above short-term moving-average support.
- MRVL and GLW remain profitable holds.
- AMD repaired far above the old 492 replay risk line; WDC/STX are no longer near old replay stops.

What remains risky:

- The current real-account book is concentrated in one effective AI infrastructure factor despite only three active holdings.
- GLW and TTMI had strong upside moves; profit giveback risk is higher than stop-loss risk today.
- Formal market fear is normal, but flow fragility is elevated; new same-theme chase buys should remain blocked.

Memory actions:

- Created this post-close audit.
- Updated `memory/portfolio/2026-06-22-portfolio-summary.md`.
- Updated `memory/todos/2026-06-22-strategy-todos.md`.
- Appended the 2026-06-22 close row to the institutional overlay replay ledger.
- Appended one line to `memory/daily-summaries.md`.
- Left `memory/decisions.md` unchanged because no new stable rule was validated.

Not investment advice.
