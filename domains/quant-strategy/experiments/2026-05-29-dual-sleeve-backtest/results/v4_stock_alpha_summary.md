# V4 Stock Alpha (V4.0) Backtest Summary

V4 upgrades the Tactical Growth Sleeve from sector/theme ETFs to a dynamic selection of individual mega-cap leaders inside those hot sectors.

## Configuration

- Name: `dual_sleeve_v4_best`
- Fallback strategy: `cash`
- Bull allocation: `30%` value / `70%` growth
- Normal allocation: `40%` value / `60%` growth
- Bear allocation: `70%` value / `30%` growth
- Stock top N: `3`

## Full-Period Comparison

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4 Best | 10.263 | 26.25% | -37.01% | 23.35% | 1.12 | 1.46 |
| SPY | 4.233 | 15.54% | -33.72% | 17.94% | 0.90 | 1.08 |
| QQQ | 7.156 | 21.77% | -35.12% | 22.30% | 1.00 | 1.27 |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 19.79% | 0.97 | 1.20 |

## Split Periods Performance

| Period | Strategy | Final Value | CAGR | Max DD | Sharpe |
| --- | --- | ---: | ---: | ---: | ---: |
| full | Dual Sleeve V4 Best | 10.263 | 26.25% | -37.01% | 1.12 |
| full | SPY | 4.233 | 15.54% | -33.72% | 0.90 |
| full | QQQ | 7.156 | 21.77% | -35.12% | 1.00 |
| full | 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 0.97 |
| train_2016_2021 | Dual Sleeve V4 Best | 3.567 | 25.57% | -37.01% | 1.06 |
| train_2016_2021 | SPY | 2.513 | 17.94% | -33.72% | 1.00 |
| train_2016_2021 | QQQ | 3.769 | 26.81% | -28.56% | 1.21 |
| train_2016_2021 | 50/50 SPY/QQQ | 3.094 | 22.41% | -30.86% | 1.14 |
| test_2022_2026 | Dual Sleeve V4 Best | 2.833 | 26.72% | -24.90% | 1.18 |
| test_2022_2026 | SPY | 1.674 | 12.44% | -24.50% | 0.76 |
| test_2022_2026 | QQQ | 1.880 | 15.44% | -34.83% | 0.74 |
| test_2022_2026 | 50/50 SPY/QQQ | 1.781 | 14.03% | -29.63% | 0.75 |
| bear_2022 | Dual Sleeve V4 Best | 0.840 | -16.20% | -24.90% | -0.75 |
| bear_2022 | SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| bear_2022 | QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| bear_2022 | 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |
| post_2023_2026 | Dual Sleeve V4 Best | 3.368 | 42.96% | -24.48% | 1.70 |
| post_2023_2026 | SPY | 2.067 | 23.83% | -18.76% | 1.49 |
| post_2023_2026 | QQQ | 2.835 | 35.89% | -22.77% | 1.66 |
| post_2023_2026 | 50/50 SPY/QQQ | 2.426 | 29.80% | -20.78% | 1.61 |
