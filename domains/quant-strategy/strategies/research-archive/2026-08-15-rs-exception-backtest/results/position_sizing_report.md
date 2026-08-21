# Exact-filter position-sizing study

## Boundary

This changes only the normal target weight of the fixed exact-filter strategy. Initial NAV remains $6,000, whole shares and the $200 fee floor remain active, single-name max is 15%, stock-sleeve max is 25%, and maximum names is three. Weights above 8% may reduce concurrent diversification because three full targets no longer fit inside the 25% sleeve. Research-only; frozen RSR1 remains 8%.

## Candidate at 10 bps

| Period | Target | Return | Max DD | Sharpe | Win rate | Trades | Exposure | Peak names | Max profit share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| train_2024_2025 | 4.00% | 4.23% | -1.62% | 1.18 | 52.63% | 19 | 2.69% | 3 | 20.88% |
| train_2024_2025 | 6.00% | 10.17% | -1.92% | 1.83 | 66.67% | 21 | 4.02% | 3 | 23.50% |
| train_2024_2025 | 8.00% | 17.15% | -1.91% | 2.19 | 70.00% | 20 | 5.26% | 3 | 27.88% |
| train_2024_2025 | 10.00% | 16.77% | -2.21% | 1.93 | 75.00% | 16 | 5.44% | 2 | 24.61% |
| train_2024_2025 | 12.00% | 20.25% | -2.97% | 1.91 | 75.00% | 16 | 6.75% | 2 | 24.71% |
| train_2024_2025 | 15.00% | 16.26% | -2.64% | 1.55 | 63.64% | 11 | 5.21% | 2 | 27.18% |
| 2026 | 4.00% | -0.24% | -1.24% | -0.29 | 33.33% | 3 | 1.72% | 2 | 100.00% |
| 2026 | 6.00% | -0.18% | -1.67% | -0.13 | 50.00% | 4 | 2.48% | 2 | 92.20% |
| 2026 | 8.00% | 0.61% | -1.89% | 0.32 | 50.00% | 4 | 3.64% | 2 | 93.15% |
| 2026 | 10.00% | 0.67% | -2.34% | 0.30 | 75.00% | 4 | 4.27% | 2 | 90.42% |
| 2026 | 12.00% | 1.46% | -2.57% | 0.49 | 75.00% | 4 | 5.25% | 2 | 91.46% |
| 2026 | 15.00% | -0.67% | -3.67% | -0.24 | 66.67% | 3 | 4.32% | 1 | 95.04% |
| full | 4.00% | 3.98% | -1.62% | 0.90 | 50.00% | 22 | 2.45% | 3 | 18.85% |
| full | 6.00% | 10.00% | -1.92% | 1.46 | 64.00% | 25 | 3.65% | 3 | 22.17% |
| full | 8.00% | 17.81% | -2.33% | 1.77 | 66.67% | 24 | 4.86% | 3 | 25.78% |
| full | 10.00% | 18.22% | -2.76% | 1.57 | 75.00% | 20 | 5.22% | 2 | 21.78% |
| full | 12.00% | 21.76% | -3.26% | 1.58 | 75.00% | 20 | 6.33% | 2 | 22.26% |
| full | 15.00% | 15.65% | -3.54% | 1.19 | 64.29% | 14 | 4.99% | 2 | 26.74% |

## Full-period 10/20 bps sensitivity

| Cost | Target | Return | Max DD | Sharpe | Exposure | Return / DD |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 bps | 4.00% | 3.98% | -1.62% | 0.90 | 2.45% | 2.45 |
| 10 bps | 6.00% | 10.00% | -1.92% | 1.46 | 3.65% | 5.21 |
| 10 bps | 8.00% | 17.81% | -2.33% | 1.77 | 4.86% | 7.66 |
| 10 bps | 10.00% | 18.22% | -2.76% | 1.57 | 5.22% | 6.59 |
| 10 bps | 12.00% | 21.76% | -3.26% | 1.58 | 6.33% | 6.68 |
| 10 bps | 15.00% | 15.65% | -3.54% | 1.19 | 4.99% | 4.42 |
| 20 bps | 4.00% | 2.76% | -1.66% | 0.59 | 2.46% | 1.67 |
| 20 bps | 6.00% | 8.27% | -1.93% | 1.16 | 3.67% | 4.27 |
| 20 bps | 8.00% | 14.46% | -2.33% | 1.46 | 4.79% | 6.21 |
| 20 bps | 10.00% | 17.82% | -2.82% | 1.53 | 5.23% | 6.32 |
| 20 bps | 12.00% | 22.02% | -2.69% | 1.63 | 6.05% | 8.20 |
| 20 bps | 15.00% | 15.20% | -3.61% | 1.16 | 5.00% | 4.21 |

## Execution-path stability between 10 and 20 bps

| Target | Trades 10bps | Trades 20bps | Only at 10bps | Only at 20bps | Jaccard | Stable |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 4.00% | 22 | 23 | 0 | 1 | 0.96 | False |
| 6.00% | 25 | 26 | 0 | 1 | 0.96 | False |
| 8.00% | 24 | 25 | 0 | 1 | 0.96 | False |
| 10.00% | 20 | 20 | 0 | 0 | 1.00 | True |
| 12.00% | 20 | 19 | 1 | 0 | 0.95 | False |
| 15.00% | 14 | 14 | 0 | 0 | 1.00 | True |

| Target | 10bps return | 20bps rerun | 20bps fixed-path | Fixed-path cost drag |
| ---: | ---: | ---: | ---: | ---: |
| 4.00% | 3.98% | 2.76% | 3.77% | -0.22% |
| 6.00% | 10.00% | 8.27% | 9.69% | -0.31% |
| 8.00% | 17.81% | 14.46% | 17.41% | -0.40% |
| 10.00% | 18.22% | 17.82% | 17.81% | -0.42% |
| 12.00% | 21.76% | 22.02% | 21.25% | -0.51% |
| 15.00% | 15.65% | 15.20% | 15.23% | -0.43% |

A higher-cost result can look better when slippage pushes one whole-share order over the 15% single-name cap and removes a losing trade. That is a sizing cliff, not cost robustness; a challenger must preserve its trade set across the tested cost levels.

## Decision

- Frozen 8% full-period result: return 17.81%, max DD -2.33%, Sharpe 1.77, peak names 3, max symbol gross-profit share 25.78%.
- Higher/lower weights that beat 8% on return in both training and 2026 while keeping both drawdowns within 5%: `none` after requiring an unchanged trade path between 10 and 20 bps.
- A larger historical dollar return is not enough if it reduces diversification, breaches the profit-concentration gate, or fails one period. No sizing parameter is changed before genuine forward evidence.
