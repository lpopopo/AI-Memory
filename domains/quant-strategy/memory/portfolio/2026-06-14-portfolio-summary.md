# 2026-06-14 Portfolio Summary

Scope: current real account only for active holdings. Historical model figures are included only for institutional overlay replay diagnostics and must not be used as real-account NAV.

## Real Account

| Item | Value |
| --- | ---: |
| Real account baseline | HKD 20,000 |
| Confirmed equity holding | None |
| Confirmed stock exposure | 0% |
| Confirmed holdings count | 0 |
| Confirmed theme count | 0 |
| Largest confirmed single-stock weight | 0 |
| Confirmed cash balance | Unconfirmed by broker/user |
| Fees / FX spread / tax | Unconfirmed |
| Margin / financing | Do not use |

## Confirmed Closed Trade

| Ticker | Buy | Sell | Shares | Gross realized P/L | Gross realized return |
| --- | ---: | ---: | ---: | ---: | ---: |
| MRVL | USD 252.00 | USD 267.020 | 1 | USD +15.020 | +5.96% |

- Fees, FX spread, taxes, settlement cash, and final HKD result remain unconfirmed.
- MRVL's 2026-06-12 local quote snapshot was `USD 279.70`, below the intraday high but still above the real exit. This is opportunity cost, not authorization to rebuy.

## Current Risk Status

```text
real_account_state: cash / no confirmed equity holdings
market_regime: elevated / repair watch
flow_fragility_state: medium / elevated watch
trend_aligned_entry_state: cheap_but_unconfirmed for new real-account buys
new_real_order_status: none
```

Operational stance:

- No immediate buy.
- No sell or reduce action because there is no confirmed real equity holding.
- MRVL remains `watch only / no chase`.
- AMD/WDC/STX are replay/watchlist risk labels only, not real holdings.
- Any new buy must use a technical price basis and user confirmation.

## Historical Replay Snapshot

This is not the current portfolio. It exists only for the institutional overlay replay ledger.

| Ticker | Historical model shares | 2026-06-12 reference price | Historical market value | Historical weight | Replay status |
| --- | ---: | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 279.70 | USD 2,248.31 | 10.66% | watch / no chase |
| AMD | 4.6083 | 511.57 | USD 2,357.47 | 11.18% | repair watch after reclaim above 492 |
| WDC | 3.6880 | 562.93 | USD 2,076.09 | 9.84% | defensive hold / repair confirmed |
| STX | 2.2401 | 931.04 | USD 2,085.62 | 9.89% | defensive hold / repair confirmed |

| Metric | Value |
| --- | ---: |
| Historical equity market value | USD 8,767.49 |
| Historical cash placeholder | USD 12,323.96 |
| Historical total NAV | USD 21,091.45 |
| Historical cash ratio | 58.43% |
| Historical equity exposure | 41.57% |
| Historical holdings count | 4 |
| Historical theme count | 3 nominal, highly overlapping AI capex / semiconductor / storage chain |
| Historical largest single-stock weight | AMD 11.18% |
| Historical cumulative P/L | USD +1,091.45 / +5.46% |

## Data Quality

- Equity and ETF data source: local Node and bundled Python quote clients, both returning Tencent quote objects in this run.
- The quote set appears to reflect the latest completed 2026-06-12 U.S. regular-session values, not Sunday trading.
- VIX source: external public pages show 2026-06-12 close `17.68`; local Tencent VIX remained stale-looking at `21.67` with zero OHLC and is not used for final risk scoring.
- VIX/VIX3M term structure remains unavailable.
- Real-account cash, fees, FX, margin, taxes, settlement, and open-order state remain unconfirmed.

## User Confirmation Items

- Whether any old MRVL broker-side order remains open.
- Final real-account cash and cost details after the MRVL sale.
- Whether future re-entry should prioritize one best confirmed starter rather than rebuilding a correlated basket.
