# 2026 YTD Current Strategy Validation

Data period: `2026-01-02` to `2026-05-29`.

The validation uses the cached S&P 500 and Nasdaq 100 constituent universe in `datasets/data_universe/`, plus SPY/QQQ benchmarks.

## Data Quality

- 2026 trading rows: `102`.
- Effective columns with 2026 data: `518 / 520`.
- Empty 2026 columns: `CRM, RJF`.

## Performance

| Strategy | Period Return | Annualized Return | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 36.22% | 115.56% | -10.39% | 31.03% | 2.64 | 3.87 |
| Dual Sleeve V5 Optimal | 54.47% | 194.58% | -11.86% | 38.06% | 3.05 | 4.14 |
| Dual Sleeve V6 Multi-Factor | 40.79% | 133.95% | -10.79% | 32.69% | 2.78 | 3.70 |
| SPY | 11.22% | 30.25% | -8.88% | 13.48% | 2.04 | 3.11 |
| QQQ | 20.99% | 60.54% | -11.72% | 18.16% | 2.71 | 4.66 |
| 50/50 SPY/QQQ | 16.03% | 44.69% | -10.30% | 15.63% | 2.45 | 4.07 |

## Benchmark Deltas Versus 50/50 SPY/QQQ

| Strategy | Return Delta | Drawdown Delta | Sharpe Delta |
| --- | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 20.19% | -0.09% | 0.19 |
| Dual Sleeve V5 Optimal | 38.44% | -1.55% | 0.59 |
| Dual Sleeve V6 Multi-Factor | 24.76% | -0.49% | 0.33 |
| SPY | -4.81% | 1.42% | -0.42 |
| QQQ | 4.96% | -1.42% | 0.26 |

## 2026 Monthly Signals

### V5 Optimal

| Signal Date | Bull | Bear | Value Sleeve | Growth Sleeve | Cash |
| --- | ---: | ---: | --- | --- | ---: |
| 2026-01-30 | True | False | SCHD|VTV | ALB|CIEN|COHR|LITE|LRCX|MU|SATS|STX|TER|WDC | 0.00% |
| 2026-02-27 | True | False | SCHD|VTV | CIEN|COHR|GLW|LITE|MRNA|MU|SNDK|STX|TER|WDC | 0.00% |
| 2026-03-31 | False | True | SCHD|VTV | APA|CIEN|COHR|DOW|LITE|LYB|MRNA|SNDK|TER|VRT | 0.00% |
| 2026-04-30 | True | False | IWD|SCHD | CIEN|COHR|INTC|KEYS|LITE|MRVL|SNDK|STX|TER|WDC | 0.00% |
| 2026-05-29 | True | False | IWD|SCHD | AMD|ARM|CIEN|DELL|INTC|MRVL|MU|SNDK|STX|WDC | 0.00% |

### V6 Multi-Factor

| Signal Date | Bull | Bear | Value Sleeve | Growth Sleeve | Cash |
| --- | ---: | ---: | --- | --- | ---: |
| 2026-01-30 | True | False | SCHD|VTV | ALB|CHRW|CIEN|LITE|LRCX|MU|SATS|STX|TER|WDC | 0.00% |
| 2026-02-27 | True | False | SCHD|VTV | CIEN|LITE|LRCX|MRNA|MU|SATS|SNDK|STX|TER|WDC | 0.00% |
| 2026-03-31 | False | True | SCHD|VTV | BG|CIEN|COHR|GLW|JNJ|LITE|MRNA|SNDK|TER|TPL | 0.00% |
| 2026-04-30 | True | False | IWD|SCHD | APA|CIEN|DOW|FDX|KEYS|LITE|MRVL|SNDK|TRGP|WDC | 0.00% |
| 2026-05-29 | True | False | IWD|SCHD | AMD|ARM|DELL|INTC|MRVL|MU|ON|SNDK|STX|WDC | 0.00% |

## Interpretation

- The 2026 sample is year-to-date only, so annualized figures are unstable and should not be treated as a full-year result.
- V5 is the strongest 2026 YTD return engine, with much higher return and Sharpe than SPY, QQQ, and 50/50 SPY/QQQ.
- V5 also has the deepest drawdown among the tested strategy versions, slightly worse than QQQ and 50/50 SPY/QQQ, so it is reasonable only for an aggressive mandate.
- V6 lowers return versus V5 without producing a clearly superior drawdown profile in 2026 YTD, so it should remain experimental.
- The 2026 signals are concentrated in semiconductors, storage, networking, and related technology leaders; this confirms the model is capturing the current hot-industry regime, but it also creates sector concentration risk.
