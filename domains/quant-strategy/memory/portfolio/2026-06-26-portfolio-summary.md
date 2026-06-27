# 2026-06-26 Portfolio Summary

Run time: 2026-06-27 08:24 Asia/Shanghai.  
Scope: 2026-06-26 completed-close real-account estimate. This is not a broker statement.

## Confirmed holdings at formal close

| Ticker | Shares | Cost basis | Close | Market value | Gross unrealized P/L | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 181.50 | 221.05 | 442.10 | +79.10 | `hold / profit-protection` |
| TTMI | 3 | 213.00 | 191.49 | 574.47 | -64.53 | `reduce-review / near-stop` |
| DRAM | 4 | 76.43 | 71.88 | 287.52 | -18.20 | `defensive hold / near-stop` |
| MXL | 6 | 90.70 | 96.60 | 579.60 | +35.40 | `satellite hold / protect` |
| MU | 1 | 1155.00 | 1132.33 | 1132.33 | -22.67 | `core defensive hold / near-stop` |

MRVL remains closed after the user-confirmed sale. No unconfirmed holding or fill is included.

## Account metrics

| Metric | Value |
| --- | ---: |
| Working cash | USD 3,368.64 |
| Equity market value | USD 3,016.02 |
| Estimated NAV | USD 6,384.66 |
| Change vs USD 6,410.26 baseline | -USD 25.60 / -0.40% |
| Cash / equity exposure | 52.76% / 47.24% |
| Largest position | MU, 17.74% |
| Active holdings / themes | 5 / 2 overlapping AI-capex themes |
| Optical/interconnect sleeve | USD 1,596.17 / 25.00% |
| Memory sleeve | USD 1,419.85 / 22.24% |

Exact cash, fees, FX, taxes, settlement, live orders and NAV require user or broker confirmation.

## Risk state

```text
close_date: 2026-06-26
equity_source: Tencent (Primary) structured quotes + Yahoo Chart completed daily bars
volatility_source: VIX Yahoo Chart completed daily bar; VIX3M Cboe official CSV
data_quality: high equities/ETFs; medium-high VIX; high VIX3M
fear_regime: elevated 6/14
risk_multiplier: 70%
cash_floor: 25%
framework_new_buy_cap: 25%
operational_correlated_theme_buy_cap: 0%
flow_fragility: 10/14 elevated / near-acute
trend_aligned_entry: 1/5 trend_broken
flags: theme_overlap_high; sleeve_correlation_high; momentum_reversal_high;
  AI_capex_cycle_high; memory_concentration_high; semiconductor_basket_unwind
```

## Holding controls

- GLW: close 221.05, above 210; hold/no add.
- TTMI: close 191.49 below 200 but above 188; reduce-review / near-stop, no averaging down.
- DRAM: close 71.88 and day low 71.33, still above 70.50; near-stop, confirm broker protection state.
- MXL: close 96.60, above 86; protect/no add.
- MU: close 1132.33, 2.94% above 1100; near-stop/no add.
- MRVL/AMD/WDC/STX are historical replay/watch context only, not real holdings.

Historical replay model check: estimated NAV `USD 21,050.63`, cash `58.55%`, equity `41.45%`; it remains retired from current holdings tracking.

Not investment advice.
