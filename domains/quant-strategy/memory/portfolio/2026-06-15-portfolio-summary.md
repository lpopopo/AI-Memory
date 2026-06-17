# 2026-06-15 Portfolio Summary

Run time: 2026-06-16 08:59 Asia/Shanghai.

Scope: current real account only for active holdings. Historical model/replay figures are included only for institutional overlay diagnostics and must not be used as real-account NAV.

## Real Account Holdings

Confirmed active equity holdings after user-confirmed 2026-06-15 fills:

| Ticker | Shares | Fill / cost basis | 2026-06-15 close snapshot | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | 289.50 | 308.88 | 308.88 | +19.38 before fees/FX | AI interconnect / custom silicon starter | core hold / starter; no add; profit-protection watch near 315+ |
| RDW | 5 | 15.00 gross; about 15.20 fee-adjusted | 14.83 | 74.15 | -0.85 gross; about -1.85 after buy fee | space / satellite high-volatility satellite | defensive hold / satellite near-stop review |

## Real Account NAV Estimate

Broker cash, FX, fees, taxes, and settlement are not independently verified. The estimate below uses the HKD 20,000 baseline and a simple `7.80 HKD/USD` reference rate.

| Metric | Gross before unresolved sell-side fees | Fee-adjusted estimate using USD 1 buy fee per trade |
| --- | ---: | ---: |
| USD baseline equivalent | 2,564.10 | 2,564.10 |
| Equity market value | 383.03 | 383.03 |
| Estimated cash | 2,199.60 | 2,197.60 |
| Estimated NAV | 2,582.63 | 2,580.63 |
| Estimated return vs baseline | +0.72% | +0.64% |
| Cash ratio | 85.17% | 85.15% |
| Equity exposure | 14.83% | 14.85% |
| Active holdings count | 2 | 2 |
| Theme count | 2 nominal | 2 nominal |
| Largest single-stock weight | MRVL about 11.96% | MRVL about 11.97% |

## Data Quality

| Item | Status |
| --- | --- |
| Equity/ETF quotes | Local Node quote workflow returned structured `Tencent (Primary)` objects after U.S. close; medium-high quality delayed public snapshot |
| VIX | Local Tencent VIX was low quality with zero OHLC; external Cboe/MarketWatch public close snapshot used: 16.20 |
| VIX3M | Local workflow unavailable; Google Finance visible index snapshot used: 19.36 |
| Broker cash | not independently verified |
| Fees/FX/tax | partially estimated only |
| Session context | formal 2026-06-15 U.S. post-close audit |

## Market / Risk State

```text
market_regime: elevated / repair risk-on
fear_score_estimate: 5 / 14
risk_multiplier: 70%
cash_floor: 25%
max_new_buy_exposure: 25%
flow_fragility_score: 7 / 14 -> elevated
trend_aligned_entry_state: held MRVL acceptable; RDW cheap_but_unconfirmed; fresh AI/storage chase invalid
```

## Position Risk Plan

| Ticker | Current label | Stop / review | Action rule |
| --- | --- | --- | --- |
| MRVL | core hold / starter | review below 285; reduce/exit review below 280 close; priority exit below 275 close; profit-protection review near 315+ | hold only; no automatic add after event rebound |
| RDW | defensive hold / satellite near-stop review | exit / stop-review below 14.50 close; reclaim 16 improves hold | hold only; no averaging down |
| AMD | watch only; replay repair watch | existing replay stop reference 492 | no real action; repaired above 492 but too extended to chase |
| WDC | watch only; replay defensive hold / repair confirmed | existing replay risk reference 500 | no real action; too extended |
| STX | watch only; replay defensive hold / repair confirmed | existing replay risk reference 835 | no real action; too extended |

## Portfolio Construction

```text
active_real_holdings_count: 2
theme_count: 2 nominal
largest_position: MRVL
cash_state: high but broker-unconfirmed
theme_overlap: current real book is small but high-beta; historical replay basket remains highly correlated AI capex/storage exposure
max_new_exposure_allowed_now: 0 operationally until broker cash/open-order state is confirmed
```

## Historical Replay Snapshot

This is not the current portfolio. It exists only for the institutional overlay replay ledger.

| Ticker | Historical model shares | 2026-06-15 close snapshot | Historical market value | Replay status |
| --- | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 308.88 | 2,482.07 | no chase / profit-protection watch |
| AMD | 4.6083 | 547.26 | 2,521.82 | repair watch after close above 492 |
| WDC | 3.6880 | 653.53 | 2,410.22 | defensive hold / repair confirmed |
| STX | 2.2401 | 1018.80 | 2,282.36 | defensive hold / repair confirmed |

| Metric | Value |
| --- | ---: |
| Historical equity market value | about USD 9,696.47 |
| Historical cash placeholder | USD 12,323.96 |
| Historical total NAV | about USD 22,020.43 |
| Historical cash ratio | about 55.97% |
| Historical equity exposure | about 44.03% |
| Historical holdings count | 4 |
| Historical theme count | 3 nominal, highly overlapping AI capex / semiconductor / storage chain |
| Historical largest single-stock weight | AMD about 11.45% |

## User Confirmation Items

- Broker cash after MRVL and RDW fills.
- Exact fees, FX spread, tax, and settlement status.
- Whether any stale real orders remain open.
- Whether RDW should use a hard stop order or manual close-review process only.

Not investment advice.
