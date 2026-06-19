# 2026-06-18 Portfolio Summary

Run time: 2026-06-19 08:56 Asia/Shanghai.

Scope: current real account only for active holdings after the 2026-06-18 U.S. close. This is a formal post-close estimate, not broker-verified NAV.

## Real Account Holdings

| Ticker | Shares | Fill / cost basis | Post-close price | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | USD 289.50 gross; about 290.50 after buy fee; 291.50 round-trip breakeven | 310.58 | 310.58 | +21.08 | AI interconnect / custom silicon starter | core hold / profit-protection review; no add |
| RDW | 5 | USD 15.00 gross; about 15.20 after buy fee; 15.40 round-trip breakeven | 14.35 | 71.75 | -3.25 | space / satellite high-volatility satellite | exit/stop-review below 14.50; no averaging down |
| GLW | 2 | USD 181.50 gross; about 182.00 after buy fee; 182.50 round-trip breakeven | 194.92 | 389.84 | +26.84 | optical / fiber / AI infrastructure support-test | core hold / profit-protection review; no same-day add |

## Real Account NAV Estimate

Broker cash, FX, fees, taxes, settlement, margin status, and stale open orders are not independently verified. The estimate below uses the old HKD 20,000 baseline and a simple `7.80 HKD/USD` reference rate. The HKD 40,000 sizing baseline remains forward-looking only until user/broker cash availability is confirmed.

| Metric | Fee-adjusted estimate using USD 1 buy fee per trade |
| --- | ---: |
| USD baseline equivalent | 2,564.10 |
| Equity market value | 772.17 |
| Estimated buy-fee-adjusted cash after MRVL/RDW/GLW | 1,833.60 |
| Estimated NAV before unresolved sell-side fees | 2,605.77 |
| Estimated return vs baseline | +1.62% |
| Cash ratio | 70.37% |
| Equity exposure | 29.63% |
| Active holdings count | 3 |
| Theme count | 2 nominal; AI infrastructure overlap is high |
| Largest single-stock weight | GLW about 14.96%; MRVL about 11.92% |

If measured against the forward HKD 40,000 baseline at 7.80 HKD/USD, equity exposure is about `15.06%`. Use broker-confirmed cash to resolve the true exposure.

If all three positions were liquidated immediately, another estimated USD 3 sell-side platform fee would reduce liquidation NAV by about `0.12%` of account value. This is an estimate only, not broker accounting.

## Data Quality

| Item | Status |
| --- | --- |
| Equity / ETF quotes | Local Node quote workflow returned structured `Tencent (Primary)` objects after the U.S. close; usable delayed public close snapshot |
| Daily OHLC / MAs | Yahoo chart daily bars returned 2026-06-18 completed daily bars |
| VIX | Local Tencent VIX low quality with zero OHLC; Cboe VIX historical CSV showed VIX `16.40` |
| VIX3M | Cboe VIX3M historical CSV showed VIX3M `19.57` |
| Broker cash | not independently verified |
| Fees / FX / tax | partially estimated only |
| Session context | completed U.S. regular-session close audit |

## Market / Risk State

```text
market_regime: elevated
fear_score_estimate: about 5 / 14
risk_multiplier: 70%
cash_floor: 25% framework floor; real estimated cash remains about 70%
flow_fragility_score: 8 / 14 -> elevated
trend_aligned_entry_state: MRVL trend_aligned but extended/profit-protection; GLW trend_aligned/support-test working; RDW trend_broken; fresh buys cheap_but_unconfirmed or chase-invalid
max_new_exposure_allowed_now: 0 operationally until RDW risk and broker cash/open-order facts are confirmed
```

## Position Risk Plan

| Ticker | Current label | Stop / review | Daily technical basis | Action rule |
| --- | --- | --- | --- | --- |
| MRVL | core hold / profit-protection review | review below 285; reduce/exit review below 280 close; priority exit below 275 close; profit-protection near 315-324+ | close 310.58 is above 5/10/20/50D but below the intraday high and below 315 after fading from 329.88 | hold only; no add after event rally; review profit protection if it fails to reclaim 315 |
| RDW | exit/stop-review | completed close below 14.50 triggers exit/stop-review; reclaim 16 improves hold | close 14.35 remains below 5/10/20D and below the 14.50 review line | no averaging down; user confirmation needed before any real sell order |
| GLW | core hold / support-test working | caution below 181; stop/exit review below 180; profit-protection zone 192-198 | close 194.92 is above 5/10/20/50D and above round-trip breakeven; target zone reached | hold; review profit protection; no same-day add |
| AMD | watch only; replay repair watch | existing replay stop reference 492 | close 537.37 is above 5/10/20/50D and above old risk line | no real action; if future close below 492, mark reduce-review in replay context |
| WDC | watch only; trend participation candidate in replay | existing replay risk reference 500 | close 746.23 is far above 20D and 50D, at a fresh 20D/63D high | no real action; no chase |
| STX | watch only; replay defensive hold / extended | existing replay risk reference 835 | close 1070.23 is far above 20D and 50D, but faded from intraday high | no real action; no USD 1000-class real entry without explicit approval |

## Portfolio Construction

```text
active_real_holdings_count: 3
theme_count: 2 nominal
largest_position: GLW
cash_state: high but broker-unconfirmed
theme_overlap: MRVL and GLW both express AI infrastructure / optical-interconnect adjacency; RDW is separate but high-volatility satellite
correlation_risk_review: required and completed because flow_fragility=elevated and theme_overlap_high remains active
```

## Historical Replay Snapshot

This is not the current portfolio. It exists only for institutional overlay diagnostics.

| Ticker | Historical model shares | Post-close price | Historical market value | Replay status |
| --- | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 310.58 | 2,496.54 | repaired, profit-protection / no chase |
| AMD | 4.6083 | 537.37 | 2,476.36 | repair watch above 492 |
| WDC | 3.6880 | 746.23 | 2,752.10 | defensive hold / extended leader |
| STX | 2.2401 | 1070.23 | 2,397.42 | defensive hold / extended leader |

| Metric | Value |
| --- | ---: |
| Historical equity market value | about USD 10,122.42 |
| Historical cash placeholder | USD 12,323.96 |
| Historical total NAV | about USD 22,446.38 |
| Historical cash ratio | about 54.90% |
| Historical equity exposure | about 45.10% |
| Historical holdings count | 4 |
| Historical theme count | 3 nominal, highly overlapping AI capex / semiconductor / storage chain |
| Historical largest single-stock weight | WDC about 12.26% |

## User Confirmation Items

- RDW: confirm sell/reduce after another completed close below `14.50`, or explicitly keep as manual defensive hold.
- MRVL: confirm whether to place any profit-protection plan after the event rally faded below `315`.
- GLW: confirm whether to protect profit after the support-test starter reached the `192-198` target zone.
- Broker cash after MRVL/RDW/GLW fills.
- Exact fees, FX spread, tax, settlement status, margin status, and whether any stale real orders remain open.

Not investment advice.
