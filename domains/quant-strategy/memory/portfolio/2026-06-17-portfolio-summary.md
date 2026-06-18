# 2026-06-17 Portfolio Summary

Run time: 2026-06-18 08:45 Asia/Shanghai.

Scope: current real account only for active holdings. This is the formal post-close audit estimate for the 2026-06-17 U.S. regular session, not broker-verified NAV.

## Real Account Holdings

Confirmed active equity holdings after user-confirmed 2026-06-15 fills:

| Ticker | Shares | Fill / cost basis | Post-close price | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | 289.50 gross; about 290.50 after buy fee; 291.50 round-trip breakeven | 289.54 | 289.54 | +0.04 gross; about -0.96 after buy fee | AI interconnect / custom silicon starter | manual risk hold / repaired reduce trigger; no add |
| RDW | 5 | 15.00 gross; about 15.20 buy-fee-adjusted; 15.40 round-trip breakeven | 14.36 | 71.80 | -3.20 gross; about -4.20 after buy fee | space / satellite high-volatility satellite | exit/stop-review below 14.50; no averaging down |

## Real Account NAV Estimate

Broker cash, FX, fees, taxes, settlement, margin status, and stale open orders are not independently verified. The estimate below uses the HKD 20,000 baseline and a simple `7.80 HKD/USD` reference rate. The HKD 40,000 sizing baseline remains forward-looking only until user/broker cash availability is confirmed.

| Metric | Gross before unresolved sell-side fees | Fee-adjusted estimate using USD 1 buy fee per trade |
| --- | ---: | ---: |
| USD baseline equivalent | 2,564.10 | 2,564.10 |
| Equity market value | 361.34 | 361.34 |
| Estimated cash | 2,199.60 | 2,197.60 |
| Estimated NAV | 2,560.94 | 2,558.94 |
| Estimated return vs baseline | -0.12% | -0.20% |
| Cash ratio | 85.89% | 85.88% |
| Equity exposure | 14.11% | 14.12% |
| Active holdings count | 2 | 2 |
| Theme count | 2 nominal | 2 nominal |
| Largest single-stock weight | MRVL about 11.31% | MRVL about 11.31% |

If both positions were liquidated immediately, another estimated USD 2 sell-side platform fee would reduce liquidation NAV by about `0.08%` of account value. This is an estimate only, not broker accounting.

## Data Quality

| Item | Status |
| --- | --- |
| Equity/ETF quotes | Local Node quote workflow returned structured `Tencent (Primary)` objects after U.S. close; usable delayed public close snapshot |
| Daily OHLC / MAs | Yahoo chart daily bars returned 2026-06-17 completed daily bars |
| VIX | Local Tencent VIX low quality with zero OHLC; Cboe VIX historical CSV showed VIX `18.44` |
| VIX3M | Cboe VIX3M historical CSV showed VIX3M `20.62` |
| Broker cash | not independently verified |
| Fees/FX/tax | partially estimated only |
| Session context | completed U.S. regular-session close audit |

## Market / Risk State

```text
market_regime: elevated
fear_score_estimate: about 6 / 14
risk_multiplier: 70%
cash_floor: 25% framework floor; real estimated cash remains about 86%
flow_fragility_score: 8 / 14 -> elevated
trend_aligned_entry_state: MRVL cheap_but_unconfirmed / manual risk hold; RDW trend_broken; fresh buys cheap_but_unconfirmed or chase-invalid
max_new_exposure_allowed_now: 0 operationally until RDW risk and broker cash/open-order facts are confirmed
```

## Position Risk Plan

| Ticker | Current label | Stop / review | Daily technical basis | Action rule |
| --- | --- | --- | --- | --- |
| MRVL | manual risk hold / repaired reduce trigger | review below 285; reduce/exit review below 280 close; priority exit below 275 close; profit-protection near 315+ | close 289.54 is above 5/10/20/50D and barely above gross cost, but below fee-adjusted round-trip breakeven | no add; hold review only; if it loses 285/280 again, return to reduce/exit-review |
| RDW | exit/stop-review | completed close below 14.50 triggers exit/stop-review; reclaim 16 improves hold | close 14.36 remains below 5/10/20D and below the 14.50 review line, only above 50D | no averaging down; user confirmation needed before any real sell order |
| AMD | watch only; replay repair watch | existing replay stop reference 492 | close 512.48 is above 10/20/50D but slightly below 5D; no real holding | no real action; if future close below 492, mark reduce-review in replay context |
| WDC | watch only; replay defensive hold / extended | existing replay risk reference 500 | close 712.13 is far above 5/10/20/50D and near 20D high | no real action; no chase |
| STX | watch only; replay defensive hold / extended | existing replay risk reference 835 | close 1066.07 is far above 5/10/20/50D and near 20D high | no real action; no chase |
| ORCL | watch only | prior review line 176 | below 5/10/20D and near 50D | no real action |
| RKLB | watch only | prior review line 95 | above 5D and 50D, below 10/20D | no real action while RDW remains triggered |

## Portfolio Construction

```text
active_real_holdings_count: 2
theme_count: 2 nominal
largest_position: MRVL
cash_state: high but broker-unconfirmed
theme_overlap: current real book is small but high-beta; historical replay basket remains highly correlated AI capex / semiconductor / storage chain
correlation_risk_review: required and completed because flow_fragility=elevated and theme_overlap_high remains active
```

## Historical Replay Snapshot

This is not the current portfolio. It exists only for institutional overlay diagnostics.

| Ticker | Historical model shares | Post-close price | Historical market value | Replay status |
| --- | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 289.54 | 2,327.41 | repaired above 285/280, but no chase |
| AMD | 4.6083 | 512.48 | 2,361.66 | repair watch above 492 |
| WDC | 3.6880 | 712.13 | 2,626.34 | defensive hold / extended leader |
| STX | 2.2401 | 1066.07 | 2,388.10 | defensive hold / extended leader |

| Metric | Value |
| --- | ---: |
| Historical equity market value | about USD 9,703.51 |
| Historical cash placeholder | USD 12,323.96 |
| Historical total NAV | about USD 22,027.47 |
| Historical cash ratio | about 55.95% |
| Historical equity exposure | about 44.05% |
| Historical holdings count | 4 |
| Historical theme count | 3 nominal, highly overlapping AI capex / semiconductor / storage chain |
| Historical largest single-stock weight | WDC about 11.92% |

## User Confirmation Items

- RDW: confirm sell/reduce after a second completed close below `14.50`, or explicitly keep as manual defensive hold.
- MRVL: confirm whether the marginal reclaim above `289.50` is enough to keep manual hold, given fee-adjusted breakeven remains above the close.
- Broker cash after MRVL and RDW fills.
- Exact fees, FX spread, tax, settlement status, margin status, and whether any stale real orders remain open.

Not investment advice.
