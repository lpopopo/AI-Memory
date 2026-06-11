# 2026-06-10 Post-Close Portfolio Summary

Audit object: 2026-06-09 U.S. regular-session close.

This file is the formal close snapshot for the existing `2026-06-10-portfolio-summary.md`. It does not replace user/broker real-account records.

## Real Account

Confirmed by user:

| Ticker | Shares | Cost | Close | Market value | Unrealized P/L | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| MRVL | 1 | USD 252.00 | USD 266.88 | USD 266.88 | USD +14.88 / +5.90% | core hold / starter defensive review |

Real-account caveats: HKD cash, FX, fees, taxes, buying power, and open orders remain unconfirmed. Any old MRVL `315` order must be confirmed by the user or broker before it is recorded.

## Model Portfolio

| Ticker | Shares | Close | Market value | Weight | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 266.88 | 2,145.26 | 10.48% | core hold / profit-protection review |
| AMD | 4.6083 | 475.51 | 2,191.29 | 10.71% | reduce-review |
| WDC | 3.6880 | 517.72 | 1,909.35 | 9.33% | defensive hold / near-stop review |
| STX | 2.2401 | 846.01 | 1,895.15 | 9.26% | defensive hold / near-stop review |

| Item | Value |
| --- | ---: |
| Equity market value | USD 8,141.05 |
| Cash | USD 12,323.96 |
| Total assets | USD 20,465.01 |
| Cash ratio | 60.22% |
| Stock exposure | 39.78% |
| Holdings count | 4 |
| Theme count | 3, highly overlapped in AI capex |
| Largest single position | AMD, 10.71% |
| Cumulative return | USD 465.01 / +2.33% |

## Portfolio Risk

```text
fear_regime: elevated, stress-leaning
estimated_fear_score: 8/14
risk_multiplier: 70%
framework_cash_floor: 25%
operational_cash_target: 60%-70%
max_new_buy_exposure: 0%
flow_fragility_score: 11/14
flow_fragility_state: elevated / acute watch
trend_aligned_entry_score: 1/5
trend_aligned_entry_state: trend_broken
```

Portfolio-level correlation review is required because `theme_overlap_high` and `sleeve_correlation_high` are both active. The four model holdings are separate tickers but one effective AI capex / semiconductor / storage risk cluster.

## Stop State

| Ticker | Close | Risk line | Triggered | Next state |
| --- | ---: | --- | --- | --- |
| MRVL real | 266.88 | close `<245`; thesis failed near `235` with SMH/QQQ weakness | No | starter defensive hold |
| MRVL model | 266.88 | close `<260` reduce-review; profit-protection only after 310-315 repair | No | hold, no chase |
| AMD model | 475.51 | close `<492` | Yes | reduce-review |
| WDC model | 517.72 | close `<500` | No, near | defensive hold / near-stop review |
| STX model | 846.01 | close `<835` | No, near | defensive hold / near-stop review |

