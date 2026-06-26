# 2026-06-25 Portfolio Summary

Run time: 2026-06-26 21:54 Asia/Shanghai.

Scope: formal completed-close estimate for the 2026-06-25 U.S. regular session. No broker login, order submission, cancellation, or unconfirmed fill assumption was made.

## Confirmed holdings

| Ticker | Shares | Cost basis | Close price | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| GLW | 2 | `181.50/share`, `363.00 total` | 228.01 | 456.02 | +93.02 | Optical/fiber diversified supplier | `core hold / profit-protection` |
| TTMI | 3 | `213.00/share`, `639.00 total` | 210.57 | 631.71 | -7.29 | PCB/interconnect supplier | `defensive hold` |
| DRAM | 4 | `76.43/share`, `305.72 total` | 76.89 | 307.56 | +1.84 | Memory/storage thematic ETF satellite | `defensive hold` |

MRVL is closed after the user-confirmed sale of `1` share at `USD 272.30`. No unconfirmed holding or fill is included.

## NAV metrics

| Metric | Value |
| --- | ---: |
| Working cash after DRAM purchase and fee | USD 5,069.84 |
| Equity market value | USD 1,395.29 |
| Estimated NAV | USD 6,465.13 |
| Estimated return vs USD 6,410.26 baseline | +USD 54.87 / +0.86% |
| Cash ratio | 78.42% |
| Equity exposure | 21.58% |
| Largest position | TTMI, about 9.77% of NAV |
| Active holdings | 3 |
| Active themes | 2 overlapping AI-infrastructure themes: optical/interconnect and memory/storage |

Exact cash, fees, FX, taxes, settlement and open orders require user or broker confirmation.

## Risk state

```text
data_time: 2026-06-25 completed regular-session close
equity_quote_source: local Node Yahoo chart daily bars, after local StockService smoke test
volatility_source: Yahoo chart daily VIX; FRED VXVCLS / Yahoo visible snapshot VIX3M fallback
data_quality: completed close; VIX3M source-level fallback noted
formal_fear_regime: normal, 2/14
flow_fragility_score: 8/14
flow_fragility_state: elevated
trend_aligned_entry_state: cheap_but_unconfirmed / gap-rejected for new correlated-theme entries
factor_macro_flags: theme_overlap_high; sleeve_correlation_high; momentum_reversal_high; AI_capex_cycle_high; opening_gap_rejection
new_buy_gate: closed by overlay and concentration controls for AI/semiconductor/storage adds
```

## Holding controls

- GLW: hold 2; no add. Completed close `<210` requires reduce/exit review.
- TTMI: hold 3; no add. Reclaimed warning line ($210.57 vs $205 warning). Hard stop remains `<188` close-based.
- DRAM: hold 4; no add. User-side protective exit is `70.50` for all 4 shares.
- WDC/STX/AMD/MRVL and other candidates: watch only; no live-account position assumed.
- Confirm every residual DRAM buy and the WDC `655` buy are cancelled; user-side confirmation remains pending.

The retired USD 20,000 model ledger is not a current portfolio. MRVL/AMD/WDC/STX values are tracked only where the institutional overlay replay protocol requires historical diagnostics.

Not investment advice.
