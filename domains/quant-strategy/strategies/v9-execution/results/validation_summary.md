# V1 Revalidation Summary

This file revalidates the V1 best configuration after optimization.

Fixed V1 configuration:

- Value mode: `top2`
- Tactical top N: `2`
- Regime filter: `spy200_or_qqq100`
- Tactical filter: `positive_m63`
- Score mode: `m63_m126`
- Fallback: `qqq`

## full

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V1 Best | 5.288 | 18.14% | -32.17% | 18.39% | 1.00 | 1.25 | 55.33% |
| SPY | 4.233 | 15.54% | -33.72% | 17.94% | 0.90 | 1.08 | 55.45% |
| QQQ | 7.156 | 21.77% | -35.12% | 22.30% | 1.00 | 1.27 | 56.89% |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 19.79% | 0.97 | 1.20 | 56.45% |

## train_2016_2021

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V1 Best | 2.465 | 17.53% | -32.17% | 19.05% | 0.94 | 1.08 | 56.61% |
| SPY | 2.513 | 17.94% | -33.72% | 18.18% | 1.00 | 1.10 | 56.68% |
| QQQ | 3.769 | 26.81% | -28.56% | 21.55% | 1.21 | 1.41 | 58.66% |
| 50/50 SPY/QQQ | 3.094 | 22.41% | -30.86% | 19.46% | 1.14 | 1.28 | 57.74% |

## test_2022_2026

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V1 Best | 2.136 | 18.84% | -16.85% | 17.53% | 1.08 | 1.57 | 53.67% |
| SPY | 1.674 | 12.44% | -24.50% | 17.64% | 0.76 | 1.04 | 53.85% |
| QQQ | 1.880 | 15.44% | -34.83% | 23.23% | 0.74 | 1.05 | 54.58% |
| 50/50 SPY/QQQ | 1.781 | 14.03% | -29.63% | 20.22% | 0.75 | 1.06 | 54.76% |

## bear_2022

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V1 Best | 0.945 | -5.56% | -16.85% | 23.07% | -0.13 | -0.21 | 47.60% |
| SPY | 0.814 | -18.84% | -24.50% | 24.28% | -0.74 | -1.18 | 43.20% |
| QQQ | 0.668 | -33.54% | -34.83% | 32.20% | -1.10 | -1.83 | 44.00% |
| 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | 28.01% | -0.95 | -1.57 | 44.40% |

## post_2023_2026

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V1 Best | 2.270 | 27.28% | -16.76% | 15.54% | 1.64 | 2.38 | 55.52% |
| SPY | 2.067 | 23.83% | -18.76% | 15.13% | 1.49 | 2.03 | 57.04% |
| QQQ | 2.835 | 35.89% | -22.77% | 19.77% | 1.66 | 2.36 | 57.75% |
| 50/50 SPY/QQQ | 2.426 | 29.80% | -20.78% | 17.23% | 1.61 | 2.24 | 57.86% |

## Read

- Full-period reproduction should match the optimization summary except for tiny rounding differences.
- The train/test split checks whether the optimized rule survives outside the period that visually dominated selection.
- If V1 only looks good in one segment, treat it as a candidate that needs more robust validation.

## Revalidation Conclusion

- Full-period reproduction matches the V1 optimization summary.
- V1 does not beat 50/50 SPY/QQQ over the full 2016-2026 period.
- V1 underperforms during the 2016-2021 bull-market segment.
- V1 outperforms SPY, QQQ, and 50/50 SPY/QQQ during 2022-2026, mainly by reducing 2022 bear-market damage.
- Current evidence suggests V1 is more valuable as a drawdown-control / regime-aware overlay than as a pure return maximizer.
- The next improvement should target bull-market participation without giving up the 2022-style downside protection.
