# 2026-06-16 Portfolio Summary

Run time: 2026-06-17 08:46 Asia/Shanghai.

Scope: current real account only for active holdings. This is the formal post-close audit estimate for the 2026-06-16 U.S. regular session, not broker-verified NAV.

## Real Account Holdings

Confirmed active equity holdings after user-confirmed 2026-06-15 fills:

| Ticker | Shares | Fill / cost basis | Post-close price | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | 289.50 gross; about 290.50 after buy fee | 278.67 | 278.67 | -10.83 gross; about -11.83 after buy fee | AI interconnect / custom silicon starter | reduce/exit-review after close below 280; no add |
| RDW | 5 | 15.00 gross; about 15.20 fee-adjusted | 13.50 | 67.50 | -7.50 gross; about -8.50 after buy fee | space / satellite high-volatility satellite | exit/stop-review after close below 14.50; no averaging down |

## Real Account NAV Estimate

Broker cash, FX, fees, taxes, and settlement are not independently verified. The estimate below uses the HKD 20,000 baseline and a simple `7.80 HKD/USD` reference rate. The HKD 40,000 sizing baseline remains forward-looking only until user/broker cash availability is confirmed.

| Metric | Gross before unresolved sell-side fees | Fee-adjusted estimate using USD 1 buy fee per trade |
| --- | ---: | ---: |
| USD baseline equivalent | 2,564.10 | 2,564.10 |
| Equity market value | 346.17 | 346.17 |
| Estimated cash | 2,199.60 | 2,197.60 |
| Estimated NAV | 2,545.77 | 2,543.77 |
| Estimated return vs baseline | -0.71% | -0.79% |
| Cash ratio | 86.40% | 86.39% |
| Equity exposure | 13.60% | 13.61% |
| Active holdings count | 2 | 2 |
| Theme count | 2 nominal | 2 nominal |
| Largest single-stock weight | MRVL about 10.95% | MRVL about 10.95% |

## Data Quality

| Item | Status |
| --- | --- |
| Equity/ETF quotes | Local Node quote workflow returned structured `Tencent (Primary)` objects after U.S. close; usable delayed public close snapshot |
| VIX | Local Tencent VIX low quality with zero OHLC; external Cboe/MarketWatch/Yahoo public close snapshots showed VIX `16.41` |
| VIX3M | Google Finance visible index snapshot showed VIX3M `19.53` |
| Broker cash | not independently verified |
| Fees/FX/tax | partially estimated only |
| Session context | completed U.S. regular-session close audit |

## Market / Risk State

```text
market_regime: elevated
fear_score_estimate: about 6-7 / 14
risk_multiplier: 70%
cash_floor: 25% framework floor; real estimated cash remains about 86%
flow_fragility_score: 9 / 14 -> elevated
trend_aligned_entry_state: MRVL trend_broken / reduce-review; RDW trend_broken / exit-review; fresh buys cheap_but_unconfirmed or chase-invalid
```

## Position Risk Plan

| Ticker | Current label | Stop / review | Action rule |
| --- | --- | --- | --- |
| MRVL | reduce/exit-review | review below 285; reduce/exit review below 280 close; priority exit below 275 close | next actionable window requires user-confirmed risk decision; no add or average-up/down |
| RDW | exit/stop-review | completed close `<14.50` triggers exit/stop-review; reclaim 16 improves hold | no averaging down; user confirmation needed before any sell order |
| AMD | watch only; replay repair watch | existing replay stop reference 492 | no real action; above 492 but volatile and not a real holding |
| WDC | watch only; replay defensive hold / repair confirmed | existing replay risk reference 500 | no real action; still extended |
| STX | watch only; replay defensive hold / repair confirmed | existing replay risk reference 835 | no real action; still extended |
| ORCL | watch only | prior review line 176; recheck 180-186 support/reclaim zone | no real action |
| RKLB | watch only | prior review line 95 | no real action while RDW is below stop-review and occupies satellite sleeve |

## Portfolio Construction

```text
active_real_holdings_count: 2
theme_count: 2 nominal
largest_position: MRVL
cash_state: high but broker-unconfirmed
theme_overlap: current real book is small but high-beta; replay basket remains highly correlated AI capex / storage exposure
max_new_exposure_allowed_now: 0 operationally until MRVL/RDW risk decisions and broker cash/open-order facts are confirmed
```

## Historical Replay Snapshot

This is not the current portfolio. It exists only for institutional overlay diagnostics.

| Ticker | Historical model shares | Post-close price | Historical market value | Replay status |
| --- | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 278.67 | 2,240.03 | reduce/exit-review in real account; replay no add |
| AMD | 4.6083 | 507.29 | 2,337.74 | repair watch above 492 but volatile |
| WDC | 3.6880 | 681.08 | 2,511.82 | defensive hold / repair confirmed |
| STX | 2.2401 | 1031.34 | 2,310.30 | defensive hold / repair confirmed |

| Metric | Value |
| --- | ---: |
| Historical equity market value | about USD 9,399.91 |
| Historical cash placeholder | USD 12,323.96 |
| Historical total NAV | about USD 21,723.87 |
| Historical cash ratio | about 56.73% |
| Historical equity exposure | about 43.27% |
| Historical holdings count | 4 |
| Historical theme count | 3 nominal, highly overlapping AI capex / semiconductor / storage chain |
| Historical largest single-stock weight | WDC about 11.56% |

## User Confirmation Items

- Whether MRVL should be reduced/exited after the completed close below `280`, or reviewed manually against the `275` priority exit line.
- Whether RDW should be exited after the completed close below `14.50`, or only monitored until next session.
- Broker cash after MRVL and RDW fills.
- Exact fees, FX spread, tax, and settlement status.
- Whether any stale real orders remain open.

Not investment advice.
