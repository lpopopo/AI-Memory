# V2 Robustness Validation

This validation fixes the best V2 configuration and tests it across fixed periods and rolling 3-year windows.

## Fixed V2 Configuration

- name: `dual_sleeve_v2_best`
- bull_value_weight: `0.35`
- bull_tactical_weight: `0.65`
- normal_value_weight: `0.5`
- normal_tactical_weight: `0.5`
- bull_rule: `qqq200_m126`
- tactical_top_n: `2`
- fallback: `qqq`
- include_qqq_in_bull_rank: `True`

## Fixed Split Results

### full

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V2 Best | 5.759 | 19.15% | -31.04% | 1.02 |
| SPY | 4.233 | 15.54% | -33.72% | 0.90 |
| QQQ | 7.156 | 21.77% | -35.12% | 1.00 |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 0.97 |

Against 50/50 SPY/QQQ: CAGR delta 0.43%, drawdown delta -0.18%, Sharpe delta 0.05.

### train_2016_2021

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V2 Best | 2.574 | 18.44% | -31.04% | 0.96 |
| SPY | 2.513 | 17.94% | -33.72% | 1.00 |
| QQQ | 3.769 | 26.81% | -28.56% | 1.21 |
| 50/50 SPY/QQQ | 3.094 | 22.41% | -30.86% | 1.14 |

Against 50/50 SPY/QQQ: CAGR delta -3.97%, drawdown delta -0.18%, Sharpe delta -0.17.

### test_2022_2026

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V2 Best | 2.227 | 19.97% | -17.46% | 1.08 |
| SPY | 1.674 | 12.44% | -24.50% | 0.76 |
| QQQ | 1.880 | 15.44% | -34.83% | 0.74 |
| 50/50 SPY/QQQ | 1.781 | 14.03% | -29.63% | 0.75 |

Against 50/50 SPY/QQQ: CAGR delta 5.95%, drawdown delta 12.17%, Sharpe delta 0.33.

### bear_2022

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V2 Best | 0.933 | -6.79% | -17.06% | -0.19 |
| SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |

Against 50/50 SPY/QQQ: CAGR delta 19.66%, drawdown delta 12.57%, Sharpe delta 0.77.

### post_2023_2026

| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| Dual Sleeve V2 Best | 2.397 | 29.35% | -17.46% | 1.63 |
| SPY | 2.067 | 23.83% | -18.76% | 1.49 |
| QQQ | 2.835 | 35.89% | -22.77% | 1.66 |
| 50/50 SPY/QQQ | 2.426 | 29.80% | -20.78% | 1.61 |

Against 50/50 SPY/QQQ: CAGR delta -0.46%, drawdown delta 3.32%, Sharpe delta 0.02.

## Rolling 3-Year Windows

| Window | V2 CAGR | 50/50 CAGR | CAGR Delta | V2 DD | 50/50 DD | DD Delta | V2 Sharpe | 50/50 Sharpe | Sharpe Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2016-2018 | 8.48% | 12.16% | -3.68% | -20.73% | -20.94% | 0.20% | 0.68 | 0.87 | -0.19 |
| 2017-2019 | 11.09% | 18.58% | -7.50% | -20.73% | -20.94% | 0.20% | 0.82 | 1.23 | -0.41 |
| 2018-2020 | 12.66% | 20.12% | -7.46% | -31.04% | -30.86% | -0.18% | 0.62 | 0.88 | -0.26 |
| 2019-2021 | 27.72% | 31.95% | -4.23% | -31.04% | -30.86% | -0.18% | 1.15 | 1.32 | -0.17 |
| 2020-2022 | 15.52% | 7.74% | 7.77% | -31.04% | -30.86% | -0.18% | 0.69 | 0.41 | 0.27 |
| 2021-2023 | 16.32% | 10.67% | 5.65% | -17.94% | -29.75% | 11.82% | 0.89 | 0.60 | 0.29 |
| 2022-2024 | 13.40% | 8.99% | 4.41% | -17.06% | -29.63% | 12.57% | 0.77 | 0.53 | 0.25 |
| 2023-2025 | 23.77% | 28.20% | -4.42% | -17.46% | -20.78% | 3.32% | 1.34 | 1.52 | -0.17 |
| 2024-2026 | 30.82% | 26.08% | 4.74% | -17.46% | -20.78% | 3.32% | 1.66 | 1.38 | 0.28 |

## Rolling Win Counts Versus 50/50 SPY/QQQ

- CAGR wins: 4 / 9
- Drawdown wins: 6 / 9
- Sharpe wins: 4 / 9

## Read

- Positive drawdown delta means V2 had a shallower drawdown.
- This is still ETF-proxy validation; individual-stock sleeves remain untested.
- A robust strategy should not depend on only one rolling window.

## Initial Interpretation

- V2 should be treated as improved but not fully proven.
- The key question is whether its rolling-window behavior is consistent enough to justify moving to individual-stock testing.
- Rolling windows show that V2's most consistent edge is drawdown control, not return dominance.
- V2 underperformed 50/50 SPY/QQQ in early bull-market windows, especially 2017-2019 and 2018-2020.
- V2 outperformed in windows that include or follow the 2022 bear market.
- The next design question is whether to keep V2 as a defensive overlay or add a separate bull-market accelerator.
