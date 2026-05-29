# V3.1 Refined Robustness Validation

This validation fixes the best V3.1 refined configuration (with dynamic cash fallback) and tests it across fixed periods and rolling 3-year windows.

## Fixed V3.1 Configuration

- name: `dual_sleeve_v3_refined_best`
- bull_value_weight: `0.3`
- bull_growth_weight: `0.7`
- normal_value_weight: `0.4`
- normal_growth_weight: `0.6`
- bear_value_weight: `0.7`
- bear_growth_weight: `0.3`
- bull_rule: `qqq200_m126`
- bear_rule: `both_below_200_negative_m63`
- growth_top_n: `2`
- value_mode: `top2`
- score_mode: `m63_m126`
- fallback: `cash`

## Fixed Split Results

### full

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3.1 Best | 5.232 | 18.01% | -32.46% | 0.99 |
| SPY | 4.233 | 15.54% | -33.72% | 0.90 |
| QQQ | 7.156 | 21.77% | -35.12% | 1.00 |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 0.97 |

Against 50/50 SPY/QQQ: CAGR delta -0.71%, drawdown delta -1.60%, Sharpe delta 0.02.

### train_2016_2021

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3.1 Best | 2.645 | 19.02% | -32.46% | 0.98 |
| SPY | 2.513 | 17.94% | -33.72% | 1.00 |
| QQQ | 3.769 | 26.81% | -28.56% | 1.21 |
| 50/50 SPY/QQQ | 3.094 | 22.41% | -30.86% | 1.14 |

Against 50/50 SPY/QQQ: CAGR delta -3.39%, drawdown delta -1.60%, Sharpe delta -0.16.

### test_2022_2026

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3.1 Best | 1.955 | 16.48% | -17.06% | 0.98 |
| SPY | 1.674 | 12.44% | -24.50% | 0.76 |
| QQQ | 1.880 | 15.44% | -34.83% | 0.74 |
| 50/50 SPY/QQQ | 1.781 | 14.03% | -29.63% | 0.75 |

Against 50/50 SPY/QQQ: CAGR delta 2.45%, drawdown delta 12.58%, Sharpe delta 0.23.

### bear_2022

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3.1 Best | 0.872 | -12.92% | -17.06% | -0.72 |
| SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |

Against 50/50 SPY/QQQ: CAGR delta 13.53%, drawdown delta 12.58%, Sharpe delta 0.23.

### post_2023_2026

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V3.1 Best | 2.255 | 27.04% | -14.82% | 1.50 |
| SPY | 2.067 | 23.83% | -18.76% | 1.49 |
| QQQ | 2.835 | 35.89% | -22.77% | 1.66 |
| 50/50 SPY/QQQ | 2.426 | 29.80% | -20.78% | 1.61 |

Against 50/50 SPY/QQQ: CAGR delta -2.77%, drawdown delta 5.96%, Sharpe delta -0.11.

## Rolling 3-Year Windows

| Window | V3.1 CAGR | 50/50 CAGR | CAGR Delta | V3.1 DD | 50/50 DD | DD Delta | V3.1 Sharpe | 50/50 Sharpe | Sharpe Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2016-2018 | 10.63% | 12.16% | -1.53% | -12.78% | -20.94% | 8.15% | 0.90 | 0.87 | 0.03 |
| 2017-2019 | 15.49% | 18.58% | -3.09% | -12.78% | -20.94% | 8.15% | 1.13 | 1.23 | -0.10 |
| 2018-2020 | 14.14% | 20.12% | -5.99% | -32.46% | -30.86% | -1.60% | 0.67 | 0.88 | -0.21 |
| 2019-2021 | 26.81% | 31.95% | -5.14% | -32.46% | -30.86% | -1.60% | 1.09 | 1.32 | -0.23 |
| 2020-2022 | 11.33% | 7.74% | 3.59% | -32.46% | -30.86% | -1.60% | 0.56 | 0.41 | 0.14 |
| 2021-2023 | 14.11% | 10.67% | 3.44% | -17.06% | -29.75% | 12.70% | 0.86 | 0.60 | 0.26 |
| 2022-2024 | 11.31% | 8.99% | 2.32% | -17.06% | -29.63% | 12.58% | 0.71 | 0.53 | 0.19 |
| 2023-2025 | 22.65% | 28.20% | -5.55% | -14.82% | -20.78% | 5.96% | 1.31 | 1.52 | -0.21 |
| 2024-2026 | 27.32% | 26.08% | 1.24% | -14.82% | -20.78% | 5.96% | 1.51 | 1.38 | 0.13 |

## Rolling Win Counts Versus 50/50 SPY/QQQ

- CAGR wins: 4 / 9
- Drawdown wins: 6 / 9
- Sharpe wins: 5 / 9

## Read

- V3.1 with cash fallback significantly reduces bear-market drag versus standard V3.
- Drawing comparison against V2 Best, V3.1 shows a much healthier return profile in recovery and growth periods while controlling downside.
