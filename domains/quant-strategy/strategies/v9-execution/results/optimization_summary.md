# V1 Optimization Summary

Period: 2016-05-31 to 2026-05-28

## Best Configuration

- Value mode: `top2`
- Tactical top N: `2`
- Regime filter: `spy200_or_qqq100`
- Tactical filter: `positive_m63`
- Score mode: `m63_m126`
- Fallback: `qqq`

## Comparison

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V1 Best | 5.288 | 18.14% | -32.17% | 18.39% | 1.00 | 1.25 | 55.33% |
| SPY | 4.233 | 15.54% | -33.72% | 17.94% | 0.90 | 1.08 | 55.45% |
| QQQ | 7.156 | 21.77% | -35.12% | 22.30% | 1.00 | 1.27 | 56.89% |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 19.79% | 0.97 | 1.20 | 56.45% |

## Top 10 Configurations By Composite Score

| Rank | Config | Final | CAGR | Max DD | Sharpe | Value | Top N | Regime | Filter | Score | Fallback |
| ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | --- | --- | --- | --- |
| 1 | v1_0032 | 5.288 | 18.14% | -32.17% | 1.00 | top2 | 2 | spy200_or_qqq100 | positive_m63 | m63_m126 | qqq |
| 2 | v1_0008 | 5.280 | 18.12% | -32.17% | 1.00 | equal | 2 | spy200_or_qqq100 | positive_m63 | m63_m126 | qqq |
| 3 | v1_0044 | 4.999 | 17.48% | -31.88% | 0.99 | top2 | 3 | spy200_or_qqq100 | positive_m63 | m63_m126 | qqq |
| 4 | v1_0020 | 4.991 | 17.46% | -31.87% | 0.99 | equal | 3 | spy200_or_qqq100 | positive_m63 | m63_m126 | qqq |
| 5 | v1_0033 | 4.995 | 17.47% | -33.73% | 0.98 | top2 | 2 | spy200_or_qqq100 | positive_m63 | m63_m126 | spy_qqq |
| 6 | v1_0009 | 4.988 | 17.45% | -33.72% | 0.98 | equal | 2 | spy200_or_qqq100 | positive_m63 | m63_m126 | spy_qqq |
| 7 | v1_0002 | 4.877 | 17.19% | -33.46% | 0.97 | equal | 2 | none | positive_m63 | m63_m126 | qqq |
| 8 | v1_0026 | 4.883 | 17.20% | -33.47% | 0.97 | top2 | 2 | none | positive_m63 | m63_m126 | qqq |
| 9 | v1_0007 | 3.579 | 13.61% | -25.72% | 0.96 | equal | 2 | spy200_or_qqq100 | positive_m63 | m63_m126 | cash |
| 10 | v1_0031 | 3.583 | 13.63% | -25.67% | 0.96 | top2 | 2 | spy200_or_qqq100 | positive_m63 | m63_m126 | cash |

## Caution

- This is an in-sample parameter scan on the same 10-year period.
- Treat the best configuration as a candidate, not proof.
- V2 should use walk-forward or train/test validation before accepting parameter changes.

## Initial Interpretation

- V1 is a major improvement over V0.
- V1 does not clearly beat 50/50 SPY/QQQ because CAGR is lower and drawdown is deeper, though Sharpe is slightly higher.
- The best configuration relies on QQQ fallback, so part of the result comes from growth-index exposure rather than pure hot-industry rotation.
- The next test should use walk-forward validation and then move from ETF proxies to individual-stock selection.
