# Forward validation power and duration audit

## Bottom line

Twenty closed trades can be a useful economic falsification screen, but it cannot establish the historical 65%-70% hit-rate headline with high confidence.
The original gate is unchanged; larger values below are second-stage confidence benchmarks only.

## Exact one-sample power

| Variant | Null | Power at 20 | Wins needed at 20 | n for 80% power |
| --- | --- | ---: | ---: | ---: |
| RSR1-shadow | candidate_breakeven (27.0%) | 94.9% | 10 | 11 |
| RSR1-shadow | matched_baseline_rate (43.2%) | 60.9% | 13 | 32 |
| RSR1-shadow | majority_50pct (50.0%) | 25.2% | 15 | 69 |
| RSR2-profit-lock-shadow | candidate_breakeven (26.8%) | 98.1% | 10 | 10 |
| RSR2-profit-lock-shadow | matched_baseline_rate (43.2%) | 75.9% | 13 | 22 |
| RSR2-profit-lock-shadow | majority_50pct (50.0%) | 40.0% | 15 | 42 |

## Equal-sample relative comparison versus the 43.18% baseline

| Variant | Power at 20+20 | Equal n per arm for 80% power |
| --- | ---: | ---: |
| RSR1-shadow | 37.6% | 59 |
| RSR2-profit-lock-shadow | 49.4% | 43 |

## Wilson 95% confidence events

| Variant | Event | Probability at 20 | n for 80% probability |
| --- | --- | ---: | ---: |
| RSR1-shadow | lower_bound_above_candidate_breakeven | 94.9% | 11 |
| RSR1-shadow | lower_bound_above_matched_baseline_rate | 60.9% | 37 |
| RSR1-shadow | lower_bound_above_majority_50pct | 25.2% | 80 |
| RSR1-shadow | half_width_at_most_10pct | 0.0% | 88 |
| RSR2-profit-lock-shadow | lower_bound_above_candidate_breakeven | 98.1% | 10 |
| RSR2-profit-lock-shadow | lower_bound_above_matched_baseline_rate | 75.9% | 27 |
| RSR2-profit-lock-shadow | lower_bound_above_majority_50pct | 40.0% | 48 |
| RSR2-profit-lock-shadow | half_width_at_most_10pct | 0.1% | 84 |

## Historical-rate duration calibration

Planning rate: 23 trades / 659 sessions = 0.0349 trades/session.

| Target trades | Expected sessions | Expected years | Median sessions | 80% completion | P(reach by 126 sessions) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 287 | 1.1 | 278 | 359 | 1.5% |
| 11 | 315 | 1.3 | 306 | 392 | 0.6% |
| 20 | 573 | 2.3 | 564 | 678 | <0.01% |
| 22 | 630 | 2.5 | 621 | 740 | <0.01% |
| 27 | 774 | 3.1 | 765 | 896 | <0.01% |
| 32 | 917 | 3.6 | 908 | 1050 | <0.01% |
| 37 | 1060 | 4.2 | 1051 | 1204 | <0.01% |
| 42 | 1203 | 4.8 | 1194 | 1357 | <0.01% |
| 43 | 1232 | 4.9 | 1223 | 1387 | <0.01% |
| 48 | 1375 | 5.5 | 1366 | 1539 | <0.01% |
| 59 | 1690 | 6.7 | 1681 | 1873 | <0.01% |
| 69 | 1977 | 7.8 | 1968 | 2175 | <0.01% |
| 80 | 2292 | 9.1 | 2283 | 2505 | <0.01% |
| 84 | 2407 | 9.6 | 2398 | 2625 | <0.01% |
| 88 | 2521 | 10.0 | 2512 | 2745 | <0.01% |

## Interpretation

At twenty trades, strong power against the candidate's low break-even hit rate can show that the payoff distribution is economically plausible. It is a different claim from proving that future win rate exceeds 50% or reproduces the retrospective advantage over baseline. The break-even comparison is conditional on the historical average-win/average-loss relationship; forward payoff and expectancy must still be measured directly. The arrival model also shows that the 20-trade condition, not 126 sessions, is likely to be the binding clock. Do not expand the universe or loosen filters to accelerate that clock; doing so would create a different strategy and invalidate the frozen comparison.

Research-only. No order is authorized and no promotion gate is changed.
