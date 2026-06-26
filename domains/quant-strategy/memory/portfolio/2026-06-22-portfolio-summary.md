# 2026-06-22 Portfolio Summary

Run time: 2026-06-23 Asia/Shanghai.

Scope: formal post-close real-account portfolio summary after the 2026-06-22 U.S. regular session. This reflects the HKD 50,000 baseline, the user-confirmed TTMI purchase, the user-confirmed RDW sale, and local quote workflow close data. The automation did not log in to a broker.

## 1. Current Confirmed State

### Active Holdings

| Ticker | Shares | Cost basis | 2026-06-22 close | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | USD 289.50 gross | 307.86 | 307.86 | +18.36 | AI interconnect / custom silicon core | Core hold; profit-protection review |
| GLW | 2 | USD 181.50 gross | 209.83 | 419.66 | +56.66 | Optical / fiber core | Core winner; protect gains |
| TTMI | 3 | USD 213.00 gross | 221.47 | 664.41 | +25.41 | AI PCB / interconnect core-candidate | Core hold; support-test fill working |

### Closed Today

| Ticker | Shares | Buy cost | Sell fill | Gross proceeds | Gross realized P/L | Estimated net realized P/L | Reason |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| RDW | 5 | USD 15.00 gross | USD 13.30 | USD 66.50 | -8.50 | about -10.50 | Stop-discipline exit below 14.50 |

### Current NAV Estimate

| Metric | Fee-adjusted estimate using USD 1 platform fee |
| --- | ---: |
| USD baseline equivalent | 6410.26 |
| Estimated cash after TTMI buy and RDW sale | 5105.26 |
| Equity market value | 1391.93 |
| Estimated NAV | 6497.19 |
| Estimated return vs baseline | +1.36% |
| Cash ratio | 78.58% |
| Equity exposure | 21.42% of NAV / 21.71% of baseline |

Broker cash, exact FX, taxes, settlement, margin status, and open orders are not independently verified by this automation.

## 2. Data Quality

| Item | Source | Quality |
| --- | --- | --- |
| Equity / ETF closes | Local Node `StockService.fetchQuotes`, `source=Tencent (Primary)` | Structured quote objects returned. |
| Close cross-check and MAs | Yahoo chart daily bars inside local workflow fallback | Good; returned 2026-06-22 daily bars and regular market timestamps. |
| VIX / VIX3M | Yahoo chart daily bars fallback | Good; Tencent VIX row rejected as low quality because OHLC fields were zero. |
| Google browser fallback | Not used | Local workflow returned usable data. |

## 3. Market And Risk Gate

```text
formal_market_fear_regime: normal
fear_score: about 1 / 14
VIX: 17.28
VIX3M: 19.76
VIX/VIX3M: 0.8745
risk_multiplier: 100%
cash_floor: 5%
max_new_buy_exposure: 50%
flow_fragility_score: 7 / 14 -> elevated
```

The market fear gate is normal, but flow fragility and theme overlap are elevated. Operationally, new same-theme chase buys remain blocked; only clean support or reclaim setups should be considered.

## 4. Position Risk Plan

| Ticker | Current label | Stop / review | Daily technical basis | Action rule |
| --- | --- | --- | --- | --- |
| MRVL | core hold / profit-protection review | Guard/profit-protect 298-300; review below 285; stop below 280 completed close | Close 307.86 is above 5D 299.11, 10D 286.43, 20D 263.46, and 50D 201.70 | Hold only; no add or event chase |
| GLW | core winner / profit-protection review | Raised protection 203-205; serious review below 200 / 195; old stop-review below 180-181 | Close 209.83 is far above 5D 189.09, 10D 183.09, 20D 186.46, and 50D 180.00 | Hold; protect gains; no add into extension |
| TTMI | core hold / support-test filled | Watch 220; caution 213-214; warning below 210; completed-close stop-review below 188 | Close 221.47 is above 5D 209.37, 10D 195.25, 20D 189.28, and 50D 163.97 | Hold; no chase add |
| AMD | watch/replay only | Replay risk line 492 | Close 551.63 is above the 492 line and above key MAs | No reduce-review needed; no real action |
| WDC | watch/replay only | Replay risk line 500 | Close 732.62 is far above the 500 line, but extended | No real action; no chase |
| STX | watch/replay only | Replay risk line 835 | Close 1094.04 is far above the 835 line, but extended and USD 1000-class | No real action; no small-account satellite entry |

## 5. Portfolio Construction

```text
active_real_holdings_count: 3
target_holdings_count: 4-6
hard_max_holdings_count: 8
equity_theme_count: 1 dominant AI infrastructure theme, with interconnect/custom silicon, optical/fiber, and PCB/interconnect subthemes
largest_position: TTMI, about 10.23% of NAV
cash_state: high, about 78.58%
theme_overlap: high
correlation_risk_review: required and completed because flow_fragility=elevated and theme_overlap_high
```

The real account remains below concentration limits by single-name weight and holding count, but the active equity book is factor-concentrated. New adds should diversify only if the setup is independently strong; do not add merely to deploy cash.

## 6. Historical Replay Model

This is not the current real account. It exists only for institutional overlay diagnostics.

| Ticker | Historical model shares | 2026-06-22 close | Historical market value | Replay status |
| --- | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 307.86 | 2474.67 | repaired, profit-protection / no chase |
| AMD | 4.6083 | 551.63 | 2542.08 | repaired above 492; no reduce-review |
| WDC | 3.6880 | 732.62 | 2701.90 | extended leader; no near-stop |
| STX | 2.2401 | 1094.04 | 2450.76 | extended leader; no near-stop |

| Metric | Value |
| --- | ---: |
| Historical equity value | 10169.41 |
| Historical cash placeholder | 12323.96 |
| Historical total NAV | about 22493.37 |
| Historical cash ratio | about 54.79% |
| Historical equity exposure | about 45.21% |
| Historical holdings count | 4 |
| Historical largest single-stock weight | WDC about 12.01% |

Not investment advice.
