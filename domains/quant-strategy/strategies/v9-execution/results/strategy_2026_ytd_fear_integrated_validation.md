# 2026 YTD Fear-Integrated Strategy Validation

This report compares the original V5 strategy with V5 plus the market fear gate.

## Performance

| Strategy | Period Return | Annualized Return | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| V5 Original | 54.47% | 194.58% | -11.86% | 38.06% | 3.05 | 4.14 |
| V5 + Market Fear Gate | 40.93% | 134.54% | -8.55% | 31.68% | 2.86 | 4.23 |
| SPY | 11.22% | 30.25% | -8.88% | 13.48% | 2.04 | 3.11 |
| QQQ | 20.99% | 60.54% | -11.72% | 18.16% | 2.71 | 4.66 |
| 50/50 SPY/QQQ | 16.03% | 44.69% | -10.30% | 15.63% | 2.45 | 4.07 |

## 2026 Fear-Gated Monthly Allocations

| Signal Date | Fear | Score | Risk Multiplier | Bull | Bear | Value | Growth | Cash |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: |
| 2026-01-30 | normal | 1.0 | 100% | True | False | SCHD|VTV | ALB|CIEN|COHR|LITE|LRCX|MU|SATS|STX|TER|WDC | 5.00% |
| 2026-02-27 | elevated | 5.0 | 70% | True | False | SCHD|VTV | CIEN|COHR|GLW|LITE|MRNA|MU|SNDK|STX|TER|WDC | 30.00% |
| 2026-03-31 | panic | 14.0 | 20% | False | True | SCHD|VTV | APA|CIEN|COHR|DOW|LITE|LYB|MRNA|SNDK|TER|VRT | 100.00% |
| 2026-04-30 | normal | 2.0 | 100% | True | False | IWD|SCHD | CIEN|COHR|INTC|KEYS|LITE|MRVL|SNDK|STX|TER|WDC | 5.00% |
| 2026-05-29 | normal | 0.0 | 100% | True | False | IWD|SCHD | AMD|ARM|CIEN|DELL|INTC|MRVL|MU|SNDK|STX|WDC | 5.00% |

## Interpretation

- The fear gate reduced 2026 YTD return versus original V5 because it forced 30% cash in February and 100% cash during the March panic signal.
- The tradeoff was materially lower drawdown and volatility: the gate improved max drawdown while keeping returns far above SPY, QQQ, and 50/50 SPY/QQQ.
- In `normal` months the integrated strategy still keeps the configured 5% cash floor, so it will not exactly match fully invested V5.
- This 2026 test supports using the panic layer as a risk governor rather than as an alpha engine.
