# RSR1 temporal concentration and regime audit

## Scope and purpose

This is a descriptive audit of the frozen 32-name `ai_capex_broad` shadow universe at 10 bps through 2026-08-07. Buckets use only signal-day information. They are not parameter candidates and do not change RSR1.

## Signal-date concentration

- Candidate trades: `23` across `21` signal dates; maximum same-date trades: `2`.
- Dates with more than one candidate trade: `2`.
- Best signal date contributes `18.26%` of candidate gross profit; top three contribute `48.18%`.
- Best quarter contributes `35.17%` of candidate gross profit.

## Calendar attribution

| Year | Baseline trades | Baseline win | Baseline PnL | Candidate trades | Candidate win | Candidate PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024 | 7 | 42.86% | $88.62 | 6 | 50.00% | $169.69 |
| 2025 | 30 | 46.67% | $351.31 | 14 | 71.43% | $731.16 |
| 2026 | 7 | 28.57% | -$116.65 | 3 | 66.67% | $40.16 |

## Signal-day SMH trend buffer

| SMH above MA50 | Baseline trades | Baseline win | Baseline PnL | Candidate trades | Candidate win | Candidate PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0-3% | 13 | 46.15% | $120.21 | 5 | 60.00% | $187.43 |
| 3-7% | 14 | 42.86% | $265.49 | 10 | 70.00% | $522.84 |
| >7% | 17 | 41.18% | -$62.43 | 8 | 62.50% | $230.73 |

## Signal-day VIX regime

| VIX | Baseline trades | Baseline win | Baseline PnL | Candidate trades | Candidate win | Candidate PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| <15 | 7 | 71.43% | $174.21 | 5 | 100.00% | $274.91 |
| 15-20 | 34 | 35.29% | $1.90 | 17 | 52.94% | $503.07 |
| 20-25 | 3 | 66.67% | $147.16 | 1 | 100.00% | $163.02 |

## Trade-path decomposition

| Path | Trades | Win rate | Average return | Net PnL |
| --- | ---: | ---: | ---: | ---: |
| baseline_common | 19 | 63.16% | 9.57% | $770.92 |
| baseline_only | 25 | 28.00% | -4.01% | -$447.65 |
| candidate_common | 19 | 63.16% | 9.59% | $803.46 |
| candidate_only | 4 | 75.00% | 5.88% | $137.55 |

## Interpretation

- Candidate PnL is positive in `3/3` years and `6/7` active quarters. The only losing candidate quarter is the partial `2026Q3` interval through the data end.
- Candidate PnL and win rate exceed 50% in every SMH/MA50 buffer and observed VIX bucket. Baseline-only trades lose money in every SMH buffer bucket, so the filter benefit is not explained solely by selecting a stronger SMH regime.
- Same-day crowding is low, but profit remains right-skewed: the top three signal dates contribute nearly half of gross profit. This is normal for breakout systems but reinforces the need for the forward profit-concentration gate.
- The 2026 evidence is only three trades. No timing, VIX or SMH-buffer sub-rule is added from these small descriptive cells.

Research-only. This report does not authorize a live order or modify formal V9.
