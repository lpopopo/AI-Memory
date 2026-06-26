# 2026-06-23 Portfolio Summary

Run time: 2026-06-24 Asia/Shanghai.

Scope: formal post-close real-account portfolio summary after the 2026-06-23 U.S. regular session. This reflects the HKD 50,000 baseline, the final closes, and local quote workflow close data. The automation did not log in to a broker.

## 1. Current Confirmed State

### Active Holdings

| Ticker | Shares | Cost basis | 2026-06-23 close | Market value | Gross unrealized P/L | Role | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MRVL | 1 | USD 289.50 gross | 279.04 | 279.04 | -10.46 | AI interconnect / custom silicon core | Triggered stop-loss; next-open exit priority |
| GLW | 2 | USD 181.50 gross | 194.07 | 388.14 | +25.14 | Optical / fiber core | Defensive hold; broke protection bands |
| TTMI | 3 | USD 639.00 total ($213.00/sh) | 213.17 | 639.51 | +0.51 | AI PCB / interconnect core-candidate | Defensive hold; closed above cost |

### Current NAV Estimate

| Metric | Fee-adjusted estimate using USD 1 platform fee |
| --- | ---: |
| USD baseline equivalent | 6410.26 |
| Estimated cash after TTMI buy and RDW sale | 5105.26 |
| Equity market value | 1306.69 |
| Estimated NAV | 6411.95 |
| Estimated return vs baseline | +0.026% |
| Cash ratio | 79.62% |
| Equity exposure | 20.38% of NAV / 20.38% of baseline |

Broker cash, exact FX, taxes, settlement, margin status, and open orders are not independently verified by this automation.

## 2. Data Quality

| Item | Source | Quality |
| --- | --- | --- |
| Equity / ETF closes | Local Node `StockService.fetchQuotes`, `source=Yahoo Chart (Fallback)` | Structured quote objects returned. |
| Close cross-check and MAs | Yahoo chart daily bars inside local workflow fallback | Good; returned 2026-06-23 daily bars and regular market timestamps. |
| VIX / VIX3M | Yahoo chart daily bars fallback | Good; Tencent VIX row rejected as low quality because OHLC fields were zero. |
| Google browser fallback | Not used | Local workflow returned usable data. |

## 3. Market And Risk Gate

```text
formal_market_fear_regime: elevated
fear_score: 5 / 14
VIX: 19.49
VIX3M: 21.06
VIX/VIX3M: 0.925
risk_multiplier: 70%
cash_floor: 25%
max_new_buy_exposure: 25%
flow_fragility_score: 11 / 14 -> acute
```

The market fear gate has shifted to **elevated** due to index trend breaks (SPY and SMH below 50-DMA) and rising volatility. Sector flow fragility has risen to **acute**. New same-theme buys are blocked; cash must be preserved above the 25% floor.

## 4. Position Risk Plan

| Ticker | Current label | Stop / review | Daily technical basis | Action rule |
| --- | --- | --- | --- | --- |
| MRVL | exit priority | Completed close below 280 (triggered) | Close 279.04 is below 5D 291.68 and below stop-loss line 280 | **Mandatory exit.** Sell at next open within first 15 minutes. |
| GLW | defensive hold | Serious review below 200 / 195 (active) | Close 194.07 is below 5D 199.12 but above 20D 188.75 and 50D 180.30 | Hold; protect remaining gains; no add |
| TTMI | defensive hold | Stop-review below 188 | Close 213.17 is above 5D 212.18, 20D 193.12, and 50D 168.04 | Hold; no chase add |
| AMD | watch/replay only | Replay risk line 492 | Close 519.85 is above 492 close risk line | No real action |
| WDC | watch/replay only | Replay risk line 500 | Close 670.75 is above 500 replay risk line | No real action |
| STX | watch/replay only | Replay risk line 835 | Close 1038.59 is above 835 replay risk line | No real action |

## 5. Portfolio Construction

```text
active_real_holdings_count: 3
target_holdings_count: 4-6
hard_max_holdings_count: 8
equity_theme_count: 1 dominant AI infrastructure theme, with interconnect/custom silicon, optical/fiber, and PCB/interconnect subthemes
largest_position: TTMI, about 9.97% of NAV
cash_state: high, about 79.62%
theme_overlap: high
correlation_risk_review: completed; theme concentration risk is high, leading to factor-wide selloff exposure.
```

The real account is factor-concentrated in AI infrastructure. MRVL exit will reduce active holdings to 2 and equity exposure to ~16%. Cash will increase to ~84%, which is appropriate for defensive positioning in an elevated risk regime.

Not investment advice.
