# 2026-06-17 Portfolio Summary

Run time: 2026-06-17 23:03 Asia/Shanghai.

Scope: current real account only for active holdings. This is an intraday execution-prep estimate, not broker-verified NAV and not the formal 04:15 U.S. post-close audit.

## Real Account Holdings

Confirmed active equity holdings after user-confirmed 2026-06-15 fills:

| Ticker | Shares | Fill / cost basis | Latest price | Market value | Gross unrealized P/L | Fee-adjusted read | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| MRVL | 1 | 289.50 gross; about 290.50 after buy fee; 291.50 round-trip breakeven | 291.19 | 291.19 | +1.69 gross | about +0.69 after buy fee, still below round-trip breakeven | AI interconnect / custom silicon starter | reduce-review / risk hold after prior close below 280; no add |
| RDW | 5 | 15.00 gross; 15.20 after buy fee; 15.40 round-trip breakeven | 14.18 | 70.90 | -4.10 gross | about -5.10 after buy fee; below breakeven | space / satellite high-volatility satellite | exit/stop-review below 14.50; no averaging down |

## Real Account NAV Estimate

Broker cash, FX, fees, taxes, and settlement are not independently verified. Estimate uses HKD 20,000 baseline and a simple `7.80 HKD/USD` reference rate, giving about `USD 2,564.10`. The HKD 40,000 sizing baseline remains forward-looking only until user/broker cash availability is confirmed.

| Metric | Gross before unresolved sell-side fees | Fee-adjusted estimate using USD 1 buy fee per trade |
| --- | ---: | ---: |
| USD baseline equivalent | 2,564.10 | 2,564.10 |
| Equity market value | 362.09 | 362.09 |
| Estimated cash | 2,199.60 | 2,197.60 |
| Estimated NAV | 2,561.69 | 2,559.69 |
| Estimated return vs baseline | -0.09% | -0.17% |
| Cash ratio | 85.87% | 85.85% |
| Equity exposure | 14.13% | 14.15% |
| Active holdings count | 2 | 2 |
| Theme count | 2 nominal | 2 nominal |
| Largest single-stock weight | MRVL about 11.37% | MRVL about 11.38% |

If both positions were liquidated immediately, another estimated USD 2 sell-side platform fee would reduce liquidation NAV by about `0.08%` of account value. This is an estimate only, not broker accounting.

## Data Quality

| Item | Status |
| --- | --- |
| Equity / ETF quotes | Local Node quote workflow returned structured Tencent Primary objects during U.S. session; usable but delayed public intraday data |
| Daily K-line / MAs | Yahoo chart API returned daily bars; 2026-06-17 row is incomplete intraday data |
| VIX | Local VIX is low quality; public Cboe / Yahoo / MarketWatch / Investing.com snippets show VIX roughly `16.5-16.6` |
| Broker cash | not independently verified |
| Fees / FX / tax | partially estimated only |
| Session context | intraday / pre-close execution preparation |

## Market / Risk State

```text
market_regime: elevated / repair attempt
fear_score_estimate: about 6/14
risk_multiplier: 70%
cash_floor: 25% framework floor; real estimated cash remains about 86%
flow_fragility_score: about 8-9/14 -> elevated
trend_aligned_entry_state: MRVL partial intraday repair but still reduce-review until completed close confirms; RDW trend_broken; fresh buys cheap_but_unconfirmed or chase-invalid
```

## Position Risk Plan

| Ticker | Current label | Stop / review | Daily technical basis | Action rule |
| --- | --- | --- | --- | --- |
| MRVL | reduce-review / risk hold | review below 285; reduce/exit review below 280 close; priority exit below 275 close | latest price above 5/10D and cost, but prior completed close breached 280; 20D high 324.20 remains far above | no add; user confirms reduce if it fails to close back above 285-289.50; post-close audit may downgrade risk only after completed close confirmation |
| RDW | exit/stop-review | completed close below 14.50 triggers exit/stop-review; reclaim 16 improves hold | below 5/10/20D, only near 50D; latest price still below 14.50 | no averaging down; user confirmation needed before any sell order |
| AMD | watch only; replay repair watch | existing replay stop reference 492 | latest above 5/10/20D and above 492, but not real holding | no real action; if future close below 492, mark reduce-review in replay context |
| WDC | watch only; replay defensive hold / extended | existing replay risk reference 500 | far above 5/10/20D and near 20D high | no real action; no chase |
| STX | watch only; replay defensive hold / extended | existing replay risk reference 835 | far above 5/10/20D and near 20D high | no real action; no chase |
| ORCL | watch only | prior review line 176 | near 5/50D but below 10/20D | no real action |
| RKLB | watch only | prior review line 95 | near 5D/above 50D but below 10/20D | no real action while RDW remains impaired |

## Portfolio Construction

```text
active_real_holdings_count: 2
theme_count: 2 nominal
largest_position: MRVL
cash_state: high but broker-unconfirmed
theme_overlap: current real book is small but high-beta; historical replay basket remains highly correlated AI capex / semiconductor / storage chain
max_new_exposure_allowed_now: 0 operationally until MRVL/RDW risk decisions and broker cash/open-order facts are confirmed
```

## User Confirmation Items

- RDW: sell / reduce after prior close below `14.50`, or explicit manual defensive hold until formal post-close audit.
- MRVL: whether to reduce if it fails to close back above `285-289.50` after the prior completed close below `280`.
- Broker cash, settled USD, FX rate, fees, taxes, and whether HKD 40,000 capital is available.
- Confirmation that no stale real orders remain open.

Not investment advice.
