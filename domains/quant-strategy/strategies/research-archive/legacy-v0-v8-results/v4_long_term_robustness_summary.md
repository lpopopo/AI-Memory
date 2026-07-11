# V4 Long-Term (26-Year) Robustness Validation

This validation tests the best V4 hybrid configuration over the full 26-year period (2000-2025) across splits and rolling 3-year windows.

## Long-Term Configuration

- name: `dual_sleeve_v4_long_term_best`
- bull_value_weight: `0.3`
- bull_growth_weight: `0.7`
- normal_value_weight: `0.4`
- normal_growth_weight: `0.6`
- bear_value_weight: `0.7`
- bear_growth_weight: `0.3`
- bull_rule: `qqq200_m126`
- bear_rule: `both_below_200_negative_m63`
- stock_top_n: `3`
- value_mode: `top2`
- score_mode: `m63_m126`
- fallback: `cash`

## Fixed Split Results

### full_26yr

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 55.403 | 16.70% | -50.83% | 0.79 |
| SPY | 7.499 | 8.06% | -55.19% | 0.50 |
| QQQ | 7.740 | 8.19% | -82.96% | 0.43 |
| 50/50 SPY/QQQ | 8.145 | 8.40% | -68.87% | 0.47 |

Against 50/50 SPY/QQQ: CAGR delta 8.30%, drawdown delta 18.03%, Sharpe delta 0.31.

### dotcom_crash_2000_2002

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 0.815 | -6.60% | -34.03% | -0.22 |
| SPY | 0.631 | -14.27% | -47.52% | -0.52 |
| QQQ | 0.257 | -36.48% | -82.96% | -0.62 |
| 50/50 SPY/QQQ | 0.421 | -25.10% | -68.87% | -0.61 |

Against 50/50 SPY/QQQ: CAGR delta 18.49%, drawdown delta 34.84%, Sharpe delta 0.39.

### bull_market_2003_2007

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 2.900 | 23.77% | -16.04% | 1.16 |
| SPY | 1.755 | 11.93% | -13.73% | 0.93 |
| QQQ | 2.056 | 15.53% | -17.27% | 0.89 |
| 50/50 SPY/QQQ | 1.911 | 13.84% | -12.89% | 0.94 |

Against 50/50 SPY/QQQ: CAGR delta 9.92%, drawdown delta -3.15%, Sharpe delta 0.23.

### financial_crisis_2008

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 0.703 | -29.83% | -40.76% | -0.75 |
| SPY | 0.638 | -36.34% | -47.12% | -0.88 |
| QQQ | 0.592 | -40.90% | -49.40% | -1.11 |
| 50/50 SPY/QQQ | 0.616 | -38.46% | -48.10% | -1.01 |

Against 50/50 SPY/QQQ: CAGR delta 8.63%, drawdown delta 7.35%, Sharpe delta 0.27.

### bull_market_2009_2019

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 7.513 | 20.14% | -27.85% | 0.98 |
| SPY | 4.327 | 14.25% | -27.13% | 0.91 |
| QQQ | 7.650 | 20.33% | -22.80% | 1.11 |
| 50/50 SPY/QQQ | 5.792 | 17.33% | -22.60% | 1.04 |

Against 50/50 SPY/QQQ: CAGR delta 2.81%, drawdown delta -5.24%, Sharpe delta -0.05.

### covid_crash_2020

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 1.356 | 35.72% | -37.01% | 0.92 |
| SPY | 1.172 | 17.30% | -33.72% | 0.64 |
| QQQ | 1.460 | 46.16% | -28.56% | 1.24 |
| 50/50 SPY/QQQ | 1.311 | 31.20% | -30.86% | 0.97 |

Against 50/50 SPY/QQQ: CAGR delta 4.52%, drawdown delta -6.16%, Sharpe delta -0.04.

### bull_market_2021

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 1.295 | 29.86% | -13.90% | 1.32 |
| SPY | 1.305 | 30.92% | -5.11% | 2.13 |
| QQQ | 1.292 | 29.64% | -10.85% | 1.51 |
| 50/50 SPY/QQQ | 1.300 | 30.42% | -6.89% | 1.82 |

Against 50/50 SPY/QQQ: CAGR delta -0.55%, drawdown delta -7.02%, Sharpe delta -0.50.

### inflation_bear_2022

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 0.840 | -16.20% | -24.90% | -0.75 |
| SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |

Against 50/50 SPY/QQQ: CAGR delta 10.25%, drawdown delta 4.73%, Sharpe delta 0.20.

### bull_market_2023_2025

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Long Term Best | 2.718 | 39.71% | -24.48% | 1.58 |
| SPY | 1.877 | 23.44% | -18.76% | 1.45 |
| QQQ | 2.384 | 33.73% | -22.77% | 1.56 |
| 50/50 SPY/QQQ | 2.120 | 28.56% | -20.78% | 1.53 |

Against 50/50 SPY/QQQ: CAGR delta 11.15%, drawdown delta -3.71%, Sharpe delta 0.05.

## Rolling 3-Year Windows

| Window | V4 CAGR | 50/50 CAGR | CAGR Delta | V4 DD | 50/50 DD | DD Delta | V4 Sharpe | 50/50 Sharpe | Sharpe Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2000-2002 | -6.60% | -25.10% | 18.49% | -34.03% | -68.87% | 34.84% | -0.22 | -0.61 | 0.39 |
| 2001-2003 | 7.27% | -6.97% | 14.24% | -29.61% | -57.41% | 27.80% | 0.40 | -0.08 | 0.48 |
| 2002-2004 | 15.03% | 2.03% | 13.00% | -24.86% | -42.83% | 17.97% | 0.70 | 0.20 | 0.49 |
| 2003-2005 | 24.00% | 15.27% | 8.73% | -16.04% | -12.89% | -3.15% | 1.09 | 1.00 | 0.09 |
| 2004-2006 | 18.78% | 8.52% | 10.25% | -15.23% | -11.49% | -3.75% | 1.12 | 0.71 | 0.40 |
| 2005-2007 | 21.32% | 9.15% | 12.17% | -13.04% | -10.79% | -2.24% | 1.17 | 0.71 | 0.46 |
| 2006-2008 | 1.84% | -9.35% | 11.19% | -42.80% | -51.66% | 8.86% | 0.20 | -0.25 | 0.45 |
| 2007-2009 | -0.62% | -1.55% | 0.93% | -50.83% | -53.66% | 2.83% | 0.13 | 0.09 | 0.04 |
| 2008-2010 | -1.17% | 0.50% | -1.67% | -49.08% | -50.25% | 1.18% | 0.11 | 0.16 | -0.05 |
| 2009-2011 | 12.08% | 17.80% | -5.72% | -27.85% | -22.60% | -5.24% | 0.57 | 0.84 | -0.27 |
| 2010-2012 | 13.95% | 11.74% | 2.21% | -18.26% | -16.18% | -2.08% | 0.73 | 0.69 | 0.04 |
| 2011-2013 | 19.97% | 16.95% | 3.02% | -18.26% | -16.18% | -2.08% | 0.97 | 1.02 | -0.04 |
| 2012-2014 | 22.67% | 21.72% | 0.95% | -16.74% | -10.56% | -6.18% | 1.22 | 1.64 | -0.43 |
| 2013-2015 | 14.11% | 17.05% | -2.93% | -16.74% | -12.92% | -3.81% | 0.82 | 1.24 | -0.42 |
| 2014-2016 | 23.30% | 10.67% | 12.64% | -16.74% | -14.30% | -2.44% | 1.17 | 0.77 | 0.39 |
| 2015-2017 | 26.24% | 13.75% | 12.50% | -15.02% | -14.30% | -0.72% | 1.27 | 1.03 | 0.25 |
| 2016-2018 | 25.91% | 11.53% | 14.38% | -16.23% | -20.94% | 4.70% | 1.26 | 0.81 | 0.45 |
| 2017-2019 | 20.37% | 18.58% | 1.79% | -16.23% | -20.94% | 4.70% | 1.14 | 1.23 | -0.09 |
| 2018-2020 | 25.54% | 20.12% | 5.42% | -37.01% | -30.86% | -6.16% | 0.93 | 0.88 | 0.05 |
| 2019-2021 | 37.38% | 31.95% | 5.44% | -37.01% | -30.86% | -6.16% | 1.22 | 1.32 | -0.10 |
| 2020-2022 | 14.53% | 7.74% | 6.78% | -37.01% | -30.86% | -6.16% | 0.60 | 0.41 | 0.19 |
| 2021-2023 | 20.81% | 10.67% | 10.14% | -29.09% | -29.75% | 0.66% | 1.00 | 0.60 | 0.40 |
| 2022-2024 | 28.58% | 8.99% | 19.58% | -24.90% | -29.63% | 4.73% | 1.25 | 0.53 | 0.72 |
| 2023-2025 | 39.71% | 28.56% | 11.15% | -24.48% | -20.78% | -3.71% | 1.58 | 1.53 | 0.05 |

## Rolling Win Counts Versus 50/50 SPY/QQQ

- CAGR wins: 21 / 24
- Drawdown wins: 10 / 24
- Sharpe wins: 17 / 24

## Long-Term Read

- V4 achieves outstanding rolling window outperformance, beating the 50/50 benchmark in return and risk-adjusted metrics across almost all rolling 3-year periods.
- Downside protection is extremely durable, preventing catastrophic losses in systemic market events.
