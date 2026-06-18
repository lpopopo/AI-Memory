# 2026-06-18 Portfolio Summary

Run time: 2026-06-18 23:18 Asia/Shanghai.

Scope: current real account only for active holdings after user-confirmed GLW fill. This is an intraday estimate, not broker-verified NAV and not a formal U.S. close audit.

## Real Account Holdings

| Ticker | Shares | Fill / cost basis | Latest reference | Market value estimate | Role | Status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | USD 289.50 gross; about 290.50 after buy fee; 291.50 round-trip breakeven | 324.66 intraday | USD 324.66 | AI interconnect / custom silicon starter | core hold / profit-protection review near 324-326; no add |
| RDW | 5 | USD 15.00 gross; about 15.20 after buy fee; 15.40 round-trip breakeven | 13.81 intraday | USD 69.05 | space / satellite high-volatility satellite | exit-review below 14.50; no averaging down |
| GLW | 2 | USD 181.50 gross; about 182.00 after buy fee; 182.50 round-trip breakeven | 184.62 intraday | USD 369.24 | optical / fiber / AI infrastructure support-test | core hold / support-test starter; review below 181 / stop-review below 180 |

## Cash / Exposure Estimate

Broker cash, FX, fees, taxes, settlement, and margin status remain not independently verified. The HKD 40,000 capital baseline remains user-stated / forward-looking unless a broker cash snapshot is provided; this fill confirms at least enough cash for the GLW order, but does not verify total available funds.

Approximate new GLW entry cash use:

| Item | Amount |
| --- | ---: |
| GLW gross notional | USD 363.00 |
| Estimated buy-side fee | USD 1.00 |
| Estimated cash used | USD 364.00 |

Approximate real equity exposure after GLW fill, using 2026-06-18 23:16 Beijing intraday references:

| Item | Approx value |
| --- | ---: |
| MRVL market value | USD 324.66 |
| RDW market value | USD 69.05 |
| GLW market value | USD 369.24 |
| Total equity market value | about USD 762.95 |

If measured against the old HKD 20,000 baseline at 7.80 HKD/USD, equity exposure is about `29.8%`. If measured against the forward HKD 40,000 baseline, equity exposure is about `14.9%`. Use broker-confirmed cash to resolve the true exposure.

Approximate fee-adjusted NAV using the old HKD 20,000 baseline and USD 1 buy fee per filled order:

| Metric | Approx value |
| --- | ---: |
| USD baseline equivalent | USD 2,564.10 |
| Estimated buy-fee-adjusted cash after MRVL/RDW/GLW | USD 1,833.60 |
| Equity market value | USD 762.95 |
| Estimated NAV before unresolved sell-side fees | USD 2,596.55 |
| Estimated return vs baseline | about +1.27% |
| Cash ratio | about 70.6% |
| Equity exposure | about 29.4% |
| Largest single-stock weight | GLW about 14.2%; MRVL about 12.5% |

## Risk Plan

| Ticker | Action rule |
| --- | --- |
| RDW | First risk item. If it cannot reclaim `14.50`, keep exit / stop-review active. Do not average down. |
| MRVL | Hold only. It is now in the `315-324+` profit-protection zone; no add after event rally. If it loses `285/280`, return to reduce / exit-review. |
| GLW | Support-test starter is working intraday. Below `181` is caution; below `180` and no quick reclaim triggers stop / exit review. Reclaim `187-188` improves hold; `192-198` is initial target / profit-protection zone. |

## Data Quality

| Item | Status |
| --- | --- |
| Equity / ETF quotes | Local Node workflow returned structured `Tencent (Primary)` objects at 2026-06-18 23:16 Beijing; medium-high intraday quality |
| Daily technicals | Yahoo chart daily bars returned current intraday daily candles and 5/10/20/50D references |
| Volatility | Local Tencent VIX remains low quality; Yahoo chart intraday `^VIX` about 17.06 and `^VIX3M` about 19.86, not formal close data |
| Broker cash / fees / FX | Not independently verified; fee estimates use the user's USD 1 per-order rule |
| Session context | U.S. intraday; formal close stop/NAV confirmation deferred to 04:15 audit |

Not investment advice.
