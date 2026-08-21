# Point-in-time exact OHLCV filter audit

## Bottom line

The frozen 4% ATR / 50% close-location pair **failed** the registered cross-period screen.
This is a broad point-in-time transferability audit, not a promotion of RSR1 and not an order authorization.

## Data coverage

- Frozen stock symbols: 633
- Usable OHLCV stock symbols: 631
- Provider failures: 2 (CSRA, EA)
- Median active-membership coverage, development_2015_2019: 99.3%
- Median active-membership coverage, validation_2020_2022: 99.8%
- Median active-membership coverage, final_2023_2025: 100.0%

## Portfolio results

| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Mean trade | PF | Payoff | Exposure |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| development_2015_2019 | matched_baseline | -7.09% | -9.89% | -0.44 | 37.80% | 209 | -0.51% | 0.80 | 1.29 | 15.45% |
| development_2015_2019 | combined_4pct_50pct | -5.83% | -9.38% | -0.35 | 37.96% | 216 | -0.42% | 0.84 | 1.34 | 15.66% |
| validation_2020_2022 | matched_baseline | -8.30% | -10.06% | -0.84 | 34.38% | 96 | -1.19% | 0.58 | 1.13 | 9.83% |
| validation_2020_2022 | combined_4pct_50pct | -7.58% | -9.35% | -0.84 | 34.44% | 90 | -1.22% | 0.58 | 1.09 | 9.67% |
| final_2023_2025 | matched_baseline | 0.11% | -4.66% | 0.03 | 41.73% | 139 | 0.05% | 1.00 | 1.42 | 14.64% |
| final_2023_2025 | combined_4pct_50pct | 1.62% | -4.42% | 0.17 | 42.34% | 137 | 0.28% | 1.07 | 1.53 | 13.90% |

## Registered screen

| Period | Coverage | n>=20 | Return | Sharpe | DD | Win | Expectancy | Pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| validation_2020_2022 | yes | yes | yes | no | yes | yes | no | no |
| final_2023_2025 | yes | yes | yes | yes | yes | yes | yes | yes |

## Baseline trades removed by the quality pair

| Period | Group | Trades | Win rate | Mean trade | Net PnL |
| --- | --- | ---: | ---: | ---: | ---: |
| development_2015_2019 | excluded_by_pair | 35 | 17.14% | -3.35% | $-514.16 |
| development_2015_2019 | passed_pair | 174 | 41.95% | 0.06% | $88.73 |
| final_2023_2025 | excluded_by_pair | 28 | 50.00% | 1.95% | $262.93 |
| final_2023_2025 | passed_pair | 111 | 39.64% | -0.43% | $-256.53 |
| validation_2020_2022 | excluded_by_pair | 15 | 26.67% | -2.41% | $-161.29 |
| validation_2020_2022 | passed_pair | 81 | 35.80% | -0.97% | $-336.68 |

## Interpretation

The experiment uses point-in-time membership but still lacks complete delisting returns and permanent identifiers. The universe is broader than the AI-capex sleeve, so it can test whether the quality pair transfers to another breakout population, not whether formal V9 should change. Development results cannot rescue either registered out-of-sample period. Formal V9, RSR1, RSR2, and the real account remain unchanged.
