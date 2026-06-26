# 2026-06-26 Portfolio Summary

Run time: 2026-06-26 22:00 Asia/Shanghai.

Scope: real-account intraday estimate. The U.S. regular session is open; this is not a broker statement or formal completed-close audit.

## Confirmed holdings

| Ticker | Shares | Cost basis | Intraday price | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| GLW | 2 | `181.50/share`, `363.00 total` | 216.34 | 432.68 | +70.18 | Optical/fiber diversified supplier | `core hold / profit-protection` |
| TTMI | 3 | `213.00/share`, `639.00 total` | 196.03 | 588.09 | -50.91 | PCB/interconnect supplier | `defensive hold` |
| DRAM | 4 | `76.43/share`, `305.72 total` | 72.05 | 288.20 | -24.72 | Memory/storage thematic ETF satellite | `defensive hold` |

MRVL is closed after the user-confirmed sale of `1` share at `USD 272.30`. No unconfirmed holding or fill is included.

## Estimated account metrics

| Metric | Value |
| --- | ---: |
| Working cash after DRAM purchase and fee | USD 5,069.84 |
| Equity market value | USD 1,308.97 |
| Estimated NAV | USD 6,378.81 |
| Estimated change vs USD 6,410.26 baseline | -USD 31.45 / -0.49% |
| Cash ratio | 79.48% |
| Equity exposure | 20.52% |
| Largest position | TTMI, about 9.22% of NAV |
| Active holdings | 3 |
| Active themes | 2 overlapping AI-infrastructure themes: optical/interconnect and memory/storage |

Exact cash, fees, FX, taxes, settlement and open orders require user or broker confirmation.

## Risk state

```text
data_time: 2026-06-26 22:00 Asia/Shanghai
equity_quote_source: Tencent (Primary), local Node workflow
volatility_source: Yahoo Chart (Fallback), local Node workflow
data_quality: usable intraday; not formal close
provisional_fear_regime: elevated, about 6/14
flow_fragility_state: elevated, about 8/14
trend_aligned_entry_state: cheap_but_unconfirmed / gap-rejected for new entries
factor_macro_flags: theme_overlap_high; momentum_reversal_high; AI_capex_cycle_high
new_buy_gate: closed by overlay and concentration controls
```

## Holding controls

- GLW: hold 2; no add. Completed close `<210` requires reduce/exit review.
- TTMI: hold 3; no add. Breaks below $200 wind-control line. Completed close `<200` requires warning and review; `<188` requires exit review.
- DRAM: hold 4; no add. User-side protective exit is `70.50` for all 4 shares (intraday trigger).
- WDC/STX/AMD/MRVL and other candidates: watch only; no live-account position assumed.

Not investment advice.

## 23:17 BJT Intraday Refresh

Run time: 2026-06-26 23:17 Asia/Shanghai. This is an intraday estimate, not a broker statement and not a completed-close audit.

### Data quality

```text
equity_quote_source: Tencent (Primary), local Node quote workflow
volatility_source: Yahoo chart fallback for VIX/VIX3M
data_quality: usable intraday; Tencent VIX low-quality zero-OHLC snapshot excluded from fear score
python_fallback: not used
google_browser_fallback: not used
formal_close_status: unavailable; U.S. session still open
```

### Refreshed holdings

| Ticker | Shares | Cost basis | Intraday price | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| GLW | 2 | `181.50/share`, `363.00 total` | 208.17 | 416.34 | +53.34 | Optical/fiber diversified supplier | `reduce-review / profit-protection watch` |
| TTMI | 3 | `213.00/share`, `639.00 total` | 194.50 | 583.50 | -55.50 | PCB/interconnect supplier | `defensive hold / below wind-control` |
| DRAM | 4 | `76.43/share`, `305.72 total` | 72.86 | 291.44 | -14.28 | Memory/storage thematic ETF satellite | `defensive hold / protective-stop watch` |

MRVL remains closed after the user-confirmed sale of `1` share at `USD 272.30`. AMD, WDC and STX are not real holdings in the current account.

### Refreshed estimated account metrics

| Metric | Value |
| --- | ---: |
| Working cash after DRAM purchase and fee | USD 5,069.84 |
| Equity market value | USD 1,291.28 |
| Estimated NAV | USD 6,361.12 |
| Estimated change vs USD 6,410.26 baseline | -USD 49.14 / -0.77% |
| Cash ratio | 79.70% |
| Equity exposure | 20.30% |
| Largest position | TTMI, about 9.17% of NAV |
| Active holdings | 3 |
| Active themes | 2 overlapping AI-infrastructure themes: optical/interconnect and memory/storage |

Exact cash, fees, FX, taxes, settlement, live stop orders, open-order cancellation and NAV require user or broker confirmation.

### Updated risk state

```text
data_time: 2026-06-26 23:17 Asia/Shanghai
provisional_fear_regime: elevated, about 5-6/14
flow_fragility_state: elevated / near-acute, about 10/14 by proxy
trend_aligned_entry_state: trend_broken for new correlated-theme entries
factor_macro_flags: theme_overlap_high; sleeve_correlation_high; momentum_reversal_high; AI_capex_cycle_high; semiconductor_basket_unwind
new_buy_gate: closed
```

### Holding controls

- GLW: hold 2; no add. Intraday price is below `210`, but the rule is completed-close based. If the completed close remains below `210`, move to formal reduce/exit review in the post-close audit.
- TTMI: hold 3; no add. It remains below the `$200` wind-control line; completed close `<200` escalates warning/reduce review, and completed close `<188` escalates exit review.
- DRAM: hold 4; no add. Intraday low `71.33` did not touch the `70.50` protective exit, but the broker-side stop-market status still needs user confirmation.
- MRVL: closed; watch only. Re-entry requires completed close `>285` plus trend/relative-strength repair.
- AMD: no real holding; watch only. It is above the old historical `492` line, so no real-account reduce-review is carried forward.
- WDC/STX: no real holdings; watch/replay only. They are above old historical hard lines but same-theme sell-off blocks new buys.

## 23:23 BJT Sync After User-Confirmed MXL Fill

User confirmed a real-account `MXL 6 @ USD 90.70` buy; see `memory/trades/2026-06-26-real-mxl-buy.md`. The local Node quote workflow was rerun after recognizing the fill and returned structured Tencent quotes for active holdings.

### Four-holding portfolio estimate

| Ticker | Shares | Cost basis | Intraday price | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| GLW | 2 | `181.50/share`, `363.00 total` | 209.44 | 418.88 | +55.88 | Optical/fiber diversified supplier | `reduce-review / profit-protection watch` |
| TTMI | 3 | `213.00/share`, `639.00 total` | 195.44 | 586.32 | -52.68 | PCB/interconnect supplier | `defensive hold / below wind-control` |
| DRAM | 4 | `76.43/share`, `305.72 total` | 73.00 | 292.00 | -13.72 | Memory/storage thematic ETF satellite | `defensive hold / protective-stop watch` |
| MXL | 6 | `90.70/share`, `544.20 total` | 91.14 | 546.84 | +2.64 | Optical/InP/interconnect component satellite | `satellite hold / high-beta risk line 86` |

### Four-holding estimated metrics

| Metric | Value |
| --- | ---: |
| Working cash after DRAM and MXL purchases plus estimated fees | USD 4,524.64 |
| Equity market value | USD 1,844.04 |
| Estimated NAV | USD 6,368.68 |
| Estimated change vs USD 6,410.26 baseline | -USD 41.58 / -0.65% |
| Cash ratio | 71.04% |
| Equity exposure | 28.96% |
| Largest position | TTMI, about 9.21% of NAV |
| Active holdings | 4 |
| Active themes | 2, but highly overlapping: optical/interconnect plus memory/storage AI infrastructure |

### Updated controls after MXL

- MXL: hold 6; no add. Risk line `86.00`; if using broker protection, user may place/confirm `MXL sell stop-market, 6 shares, trigger 86.00`. Gross risk to line is `USD 28.20` before fees/slippage.
- Portfolio: equity exposure moved from about `20%` to about `29%`; this is still cash-heavy but increases correlated AI-capex exposure. No further adds before the post-close audit.
- Broker facts still required: exact cash, all fees/FX/taxes, settlement, DRAM stop status, MXL stop status, and residual WDC/DRAM order cancellations.
