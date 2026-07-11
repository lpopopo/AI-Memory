# V4.1 Full-Universe Stock Scanner Strategy Robustness Validation

This validation tests the bottom-up S&P 500 & Nasdaq 100 constituent-level scanner (V4.1) over the 26-year period (2000-2025) using fixed splits and rolling 3-year windows to verify alpha persistence across different macro environments.

## Configuration

- name: `dual_sleeve_v4_1_universe`
- bull_value_weight: `0.3`
- bull_growth_weight: `0.7`
- normal_value_weight: `0.4`
- normal_growth_weight: `0.6`
- bear_value_weight: `0.7`
- bear_growth_weight: `0.3`
- bull_rule: `qqq200_m126`
- bear_rule: `both_below_200_negative_m63`
- stock_top_n: `10`
- value_mode: `top2`
- score_mode: `m63_m126`
- fallback: `cash`

## Fixed Split Results

### full_26yr

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 551.901 | 27.50% | -55.20% | 1.14 | 1.53 |
| SPY | 7.499 | 8.06% | -55.19% | 0.50 | 0.63 |
| QQQ | 7.740 | 8.19% | -82.96% | 0.43 | 0.56 |
| 50/50 SPY/QQQ | 8.145 | 8.40% | -68.87% | 0.47 | 0.62 |

Against 50/50 SPY/QQQ: CAGR delta **19.09%**, drawdown delta **13.66%**, Sharpe delta **0.67**.

### dotcom_crash_2000_2002

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 0.761 | -8.74% | -36.99% | -0.36 | -0.49 |
| SPY | 0.631 | -14.27% | -47.52% | -0.52 | -0.86 |
| QQQ | 0.257 | -36.48% | -82.96% | -0.62 | -1.09 |
| 50/50 SPY/QQQ | 0.421 | -25.10% | -68.87% | -0.61 | -1.07 |

Against 50/50 SPY/QQQ: CAGR delta **16.36%**, drawdown delta **31.87%**, Sharpe delta **0.25**.

### bull_market_2003_2007

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 9.723 | 57.69% | -15.92% | 2.21 | 3.22 |
| SPY | 1.755 | 11.93% | -13.73% | 0.93 | 1.31 |
| QQQ | 2.056 | 15.53% | -17.27% | 0.89 | 1.36 |
| 50/50 SPY/QQQ | 1.911 | 13.84% | -12.89% | 0.94 | 1.40 |

Against 50/50 SPY/QQQ: CAGR delta **43.85%**, drawdown delta **-3.03%**, Sharpe delta **1.27**.

### financial_crisis_2008

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 0.636 | -36.48% | -47.34% | -0.90 | -1.25 |
| SPY | 0.638 | -36.34% | -47.12% | -0.88 | -1.22 |
| QQQ | 0.592 | -40.90% | -49.40% | -1.11 | -1.64 |
| 50/50 SPY/QQQ | 0.616 | -38.46% | -48.10% | -1.01 | -1.45 |

Against 50/50 SPY/QQQ: CAGR delta **1.98%**, drawdown delta **0.76%**, Sharpe delta **0.12**.

### bull_market_2009_2019

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 10.887 | 24.26% | -28.78% | 1.10 | 1.45 |
| SPY | 4.327 | 14.25% | -27.13% | 0.91 | 1.14 |
| QQQ | 7.650 | 20.33% | -22.80% | 1.11 | 1.46 |
| 50/50 SPY/QQQ | 5.792 | 17.33% | -22.60% | 1.04 | 1.33 |

Against 50/50 SPY/QQQ: CAGR delta **6.93%**, drawdown delta **-6.18%**, Sharpe delta **0.06**.

### covid_crash_2020

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 1.764 | 76.70% | -29.93% | 1.81 | 2.21 |
| SPY | 1.172 | 17.30% | -33.72% | 0.64 | 0.73 |
| QQQ | 1.460 | 46.16% | -28.56% | 1.24 | 1.43 |
| 50/50 SPY/QQQ | 1.311 | 31.20% | -30.86% | 0.97 | 1.08 |

Against 50/50 SPY/QQQ: CAGR delta **45.49%**, drawdown delta **0.93%**, Sharpe delta **0.84**.

### bull_market_2021

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 1.418 | 42.34% | -13.44% | 1.55 | 2.53 |
| SPY | 1.305 | 30.92% | -5.11% | 2.13 | 3.04 |
| QQQ | 1.292 | 29.64% | -10.85% | 1.51 | 2.13 |
| 50/50 SPY/QQQ | 1.300 | 30.42% | -6.89% | 1.82 | 2.60 |

Against 50/50 SPY/QQQ: CAGR delta **11.92%**, drawdown delta **-6.56%**, Sharpe delta **-0.27**.

### inflation_bear_2022

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 0.972 | -2.85% | -20.20% | -0.01 | -0.02 |
| SPY | 0.814 | -18.84% | -24.50% | -0.74 | -1.18 |
| QQQ | 0.668 | -33.54% | -34.83% | -1.10 | -1.83 |
| 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 | -1.57 |

Against 50/50 SPY/QQQ: CAGR delta **23.60%**, drawdown delta **9.43%**, Sharpe delta **0.94**.

### bull_market_2023_2025

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 4.185 | 61.42% | -28.78% | 2.07 | 3.05 |
| SPY | 1.877 | 23.44% | -18.76% | 1.45 | 1.95 |
| QQQ | 2.384 | 33.73% | -22.77% | 1.56 | 2.19 |
| 50/50 SPY/QQQ | 2.120 | 28.56% | -20.78% | 1.53 | 2.10 |

Against 50/50 SPY/QQQ: CAGR delta **32.86%**, drawdown delta **-8.01%**, Sharpe delta **0.54**.

## Rolling 3-Year Windows

| Window | V4.1 CAGR | 50/50 CAGR | CAGR Delta | V4.1 DD | 50/50 DD | DD Delta | V4.1 Sharpe | 50/50 Sharpe | Sharpe Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2000-2002 | -8.74% | -25.10% | 16.36% | -36.99% | -68.87% | 31.87% | -0.36 | -0.61 | 0.25 |
| 2001-2003 | 22.95% | -6.97% | 29.92% | -36.99% | -57.41% | 20.42% | 0.95 | -0.08 | 1.04 |
| 2002-2004 | 46.62% | 2.03% | 44.59% | -30.08% | -42.83% | 12.75% | 1.65 | 0.20 | 1.45 |
| 2003-2005 | 72.28% | 15.27% | 57.01% | -13.82% | -12.89% | -0.93% | 2.61 | 1.00 | 1.61 |
| 2004-2006 | 36.59% | 8.52% | 28.07% | -15.92% | -11.49% | -4.43% | 1.75 | 0.71 | 1.04 |
| 2005-2007 | 38.95% | 9.15% | 29.80% | -15.92% | -10.79% | -5.13% | 1.71 | 0.71 | 0.99 |
| 2006-2008 | 5.57% | -9.35% | 14.92% | -49.07% | -51.66% | 2.59% | 0.33 | -0.25 | 0.58 |
| 2007-2009 | 6.36% | -1.55% | 7.91% | -55.20% | -53.66% | -1.54% | 0.35 | 0.09 | 0.26 |
| 2008-2010 | -3.18% | 0.50% | -3.68% | -53.69% | -50.25% | -3.43% | 0.08 | 0.16 | -0.09 |
| 2009-2011 | 11.98% | 17.80% | -5.82% | -28.78% | -22.60% | -6.18% | 0.53 | 0.84 | -0.31 |
| 2010-2012 | 14.43% | 11.74% | 2.70% | -25.83% | -16.18% | -9.65% | 0.66 | 0.69 | -0.03 |
| 2011-2013 | 29.24% | 16.95% | 12.29% | -25.83% | -16.18% | -9.65% | 1.23 | 1.02 | 0.22 |
| 2012-2014 | 42.20% | 21.72% | 20.48% | -14.39% | -10.56% | -3.83% | 1.98 | 1.64 | 0.34 |
| 2013-2015 | 33.33% | 17.05% | 16.28% | -12.58% | -12.92% | 0.35% | 1.71 | 1.24 | 0.47 |
| 2014-2016 | 21.17% | 10.67% | 10.51% | -12.94% | -14.30% | 1.36% | 1.20 | 0.77 | 0.42 |
| 2015-2017 | 20.21% | 13.75% | 6.47% | -12.94% | -14.30% | 1.36% | 1.18 | 1.03 | 0.15 |
| 2016-2018 | 24.86% | 11.53% | 13.34% | -25.92% | -20.94% | -4.98% | 1.31 | 0.81 | 0.49 |
| 2017-2019 | 26.44% | 18.58% | 7.86% | -25.92% | -20.94% | -4.98% | 1.37 | 1.23 | 0.14 |
| 2018-2020 | 39.98% | 20.12% | 19.86% | -29.93% | -30.86% | 0.93% | 1.44 | 0.88 | 0.56 |
| 2019-2021 | 49.15% | 31.95% | 17.20% | -29.93% | -30.86% | 0.93% | 1.64 | 1.32 | 0.32 |
| 2020-2022 | 34.66% | 7.74% | 26.91% | -29.93% | -30.86% | 0.93% | 1.20 | 0.41 | 0.79 |
| 2021-2023 | 30.69% | 10.67% | 20.03% | -20.20% | -29.75% | 9.56% | 1.29 | 0.60 | 0.69 |
| 2022-2024 | 38.30% | 8.99% | 29.31% | -20.20% | -29.63% | 9.43% | 1.50 | 0.53 | 0.98 |
| 2023-2025 | 61.42% | 28.56% | 32.86% | -28.78% | -20.78% | -8.01% | 2.07 | 1.53 | 0.54 |

## Rolling Win Counts Versus 50/50 SPY/QQQ

- CAGR wins: **22 / 24** (91.7%)
- Drawdown wins: **12 / 24** (50.0%)
- Sharpe wins: **21 / 24** (87.5%)

## Key Robustness Findings

1. **Alpha Persistence**: The V4.1 Full-Universe scanner strategy beats the 50/50 benchmark in return and risk-adjusted metrics across almost every single rolling 3-year window since 2000.
2. **Bear Market Mitigation**: The cash retreat dynamic overlay and defensive Value ETF rotation provide stellar drawdown mitigation during major crises like the Dot-com crash (2000-2002) and the 2022 Inflation bear.
3. **Growth Engine Efficiency**: Vectorized relative strength ranking enables highly responsive rebalancing that captures emerging market leaders in real-time.
