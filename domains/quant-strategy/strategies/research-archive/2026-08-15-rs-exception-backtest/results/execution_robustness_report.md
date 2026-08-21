# Signal-to-execution robustness

## Boundary

Signals remain completed-close only. Delay 1 is the frozen next-open execution; delays 2 and 3 intentionally execute the original signal later without hindsight. Gap caps reject a planned order when its eventual open is too far above the original signal close. This is fixed-watchlist post-hoc research and cannot alter RSR1 or authorize a trade.

## Full-period candidate grid

| Delay | Gap cap | Return | Max DD | Sharpe | Win rate | Trades | Exposure | Filter return delta |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 3.00% | 16.46% | -2.35% | 1.69 | 65.22% | 23 | 4.53% | +9.45% |
| 1 | 5.00% | 17.81% | -2.33% | 1.77 | 66.67% | 24 | 4.86% | +11.90% |
| 1 | 10.00% | 17.81% | -2.33% | 1.77 | 66.67% | 24 | 4.86% | +11.90% |
| 1 | none | 17.81% | -2.33% | 1.77 | 66.67% | 24 | 4.86% | +11.90% |
| 2 | 3.00% | 10.25% | -2.49% | 1.34 | 59.09% | 22 | 3.95% | +2.90% |
| 2 | 5.00% | 11.69% | -2.46% | 1.36 | 62.50% | 24 | 4.48% | +9.22% |
| 2 | 10.00% | 11.69% | -2.46% | 1.36 | 62.50% | 24 | 4.48% | +7.51% |
| 2 | none | 11.34% | -2.47% | 1.32 | 62.50% | 24 | 4.44% | +8.16% |
| 3 | 3.00% | 3.01% | -3.11% | 0.53 | 39.13% | 23 | 2.94% | +2.66% |
| 3 | 5.00% | 7.90% | -2.03% | 0.97 | 52.00% | 25 | 3.99% | +3.30% |
| 3 | 10.00% | 11.22% | -2.15% | 1.29 | 57.69% | 26 | 4.37% | +7.19% |
| 3 | none | 11.61% | -2.14% | 1.26 | 61.54% | 26 | 4.48% | +7.91% |

## Frozen-trade next-open gap attribution

| Entry gap | Trades | Win rate | Average return | Net P&L | Max gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| <=0% | 9 | 88.89% | 14.61% | $694.19 | -0.04% |
| 0-3% | 13 | 53.85% | 6.69% | $396.82 | 2.28% |
| 3-5% | 2 | 50.00% | 0.15% | $-22.23 | 4.57% |
| 5-10% | 0 | n/a | n/a | $0.00 | n/a |
| >10% | 0 | n/a | n/a | $0.00 | n/a |

## Robustness screen

- Cells improving paired baseline return, Sharpe and drawdown in both training and 2026: `11/12`.
- Same result after requiring at least four candidate trades in each period: `9/12`.
- Frozen next-open/no-gap-cap full result: return 17.81%, max DD -2.33%, Sharpe 1.77.
- No new gap threshold is selected from this retrospective grid. A cap that looks better mainly by deleting trades is not evidence of executable alpha.

## Delay-only path

| Delay | Return | Max DD | Sharpe | Win rate | Trades |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 17.81% | -2.33% | 1.77 | 66.67% | 24 |
| 2 | 11.34% | -2.47% | 1.32 | 62.50% | 24 |
| 3 | 11.61% | -2.14% | 1.26 | 61.54% | 26 |
