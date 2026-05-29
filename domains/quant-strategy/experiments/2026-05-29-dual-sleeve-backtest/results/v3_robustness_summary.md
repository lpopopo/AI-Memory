# V3 Robustness Validation

This validation fixes the best V3 configuration and tests it across fixed periods and rolling 3-year windows.

## Fixed V3 Configuration

- name: `dual_sleeve_v3_best`
- bull_value_weight: `0.2`
- bull_growth_weight: `0.8`
- normal_value_weight: `0.4`
- normal_growth_weight: `0.6`
- bear_value_weight: `0.7`
- bear_growth_weight: `0.3`
- bull_rule: `qqq100_m63`
- bear_rule: `both_below_200_negative_m63`
- growth_top_n: `2`
- value_mode: `top2`
- score_mode: `m63_m126`

## Fixed Split Results

### full

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3 Best | 5.758 | 19.15% | -33.12% | 0.96 |
| SPY | 4.233 | 15.54% | -33.72% | 0.90 |
| QQQ | 7.156 | 21.77% | -35.12% | 1.00 |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 0.97 |

Against 50/50 SPY/QQQ: CAGR delta 0.43%, drawdown delta -2.26%, Sharpe delta -0.01.

### train_2016_2021

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3 Best | 2.811 | 20.32% | -33.12% | 0.98 |
| SPY | 2.513 | 17.94% | -33.72% | 1.00 |
| QQQ | 3.769 | 26.81% | -28.56% | 1.21 |
| 50/50 SPY/QQQ | 3.094 | 22.41% | -30.86% | 1.14 |

Against 50/50 SPY/QQQ: CAGR delta -2.09%, drawdown delta -2.26%, Sharpe delta -0.15.

### test_2022_2026

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3 Best | 2.022 | 17.37% | -27.10% | 0.90 |
| SPY | 1.674 | 12.44% | -24.50% | 0.76 |
| QQQ | 1.880 | 15.44% | -34.83% | 0.74 |
| 50/50 SPY/QQQ | 1.781 | 14.03% | -29.63% | 0.75 |

Against 50/50 SPY/QQQ: CAGR delta 3.34%, drawdown delta 2.53%, Sharpe delta 0.15.

### bear_2022

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3 Best | 0.788 | -21.41% | -27.10% | -0.87 |
| SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |

Against 50/50 SPY/QQQ: CAGR delta 5.04%, drawdown delta 2.53%, Sharpe delta 0.08.

### post_2023_2026

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3 Best | 2.581 | 32.19% | -18.92% | 1.60 |
| SPY | 2.067 | 23.83% | -18.76% | 1.49 |
| QQQ | 2.835 | 35.89% | -22.77% | 1.66 |
| 50/50 SPY/QQQ | 2.426 | 29.80% | -20.78% | 1.61 |

Against 50/50 SPY/QQQ: CAGR delta 2.39%, drawdown delta 1.86%, Sharpe delta -0.01.

## Rolling 3-Year Windows

| Window | V3 CAGR | 50/50 CAGR | CAGR Delta | V3 DD | 50/50 DD | DD Delta | V3 Sharpe | 50/50 Sharpe | Sharpe Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2016-2018 | 11.10% | 12.16% | -1.06% | -21.16% | -20.94% | -0.22% | 0.79 | 0.87 | -0.08 |
| 2017-2019 | 15.48% | 18.58% | -3.11% | -21.16% | -20.94% | -0.22% | 1.00 | 1.23 | -0.22 |
| 2018-2020 | 15.68% | 20.12% | -4.44% | -33.12% | -30.86% | -2.26% | 0.70 | 0.88 | -0.18 |
| 2019-2021 | 28.88% | 31.95% | -3.07% | -33.12% | -30.86% | -2.26% | 1.13 | 1.32 | -0.19 |
| 2020-2022 | 8.71% | 7.74% | 0.97% | -33.12% | -30.86% | -2.26% | 0.44 | 0.41 | 0.03 |
| 2021-2023 | 13.01% | 10.67% | 2.35% | -27.10% | -29.75% | 2.65% | 0.70 | 0.60 | 0.11 |
| 2022-2024 | 10.80% | 8.99% | 1.80% | -27.10% | -29.63% | 2.53% | 0.61 | 0.53 | 0.08 |
| 2023-2025 | 27.43% | 28.20% | -0.76% | -18.92% | -20.78% | 1.86% | 1.40 | 1.52 | -0.12 |
| 2024-2026 | 31.02% | 26.08% | 4.94% | -18.92% | -20.78% | 1.86% | 1.53 | 1.38 | 0.15 |

## Rolling Win Counts Versus 50/50 SPY/QQQ

- CAGR wins: 4 / 9
- Drawdown wins: 4 / 9
- Sharpe wins: 4 / 9

## Read

- Positive drawdown delta means V3 had a shallower drawdown.
- This is still ETF-proxy validation; individual-stock sleeves remain untested.
- A robust strategy should not depend on only one rolling window.

## Initial Interpretation

- V3 should be treated as improved but not fully proven.
- The key question is whether its rolling-window behavior is consistent enough to justify moving to individual-stock testing.
