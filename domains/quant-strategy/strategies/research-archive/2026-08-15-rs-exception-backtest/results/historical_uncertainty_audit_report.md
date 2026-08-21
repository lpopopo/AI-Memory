# Historical edge uncertainty audit

## Bottom line

The historical quality filter has a stable avoided-loss signature inside the already-selected current-list sample. RSR2's additional profit-lock benefit is directionally favorable but sparse, and its higher historical win rate is one trade rather than broad evidence.

This strengthens the priority order—validate entry-quality loss avoidance forward before doing more exit optimization—but does not cure survivorship/selection bias or authorize a strategy change.

## Absolute historical expectancy context

| Variant | Trades | Win rate (Wilson 95%) | Mean return/trade | Cluster-bootstrap 5%-95% | P(nonpositive) |
| --- | ---: | --- | ---: | --- | ---: |
| matched_baseline | 44 | 43.18% (29.68%-57.78%) | 1.86% | -1.68% to 5.40% | 20.18% |
| RSR1-shadow | 23 | 65.22% (44.89%-81.19%) | 8.95% | 3.79% to 14.10% | 0.12% |
| RSR2-profit-lock-shadow | 23 | 69.57% (49.13%-84.40%) | 9.64% | 4.57% to 14.67% | 0.05% |

## Entry-quality exclusion robustness

- Direct exclusions: 23 trades / 21 signal-date clusters.
- Observed excluded mean return / P&L: -3.84% / $-17.19 per trade.
- Bootstrap probability both mean return and mean P&L remain negative: 98.43%.
- 95% mean-return interval: -7.01% to -0.39%.
- Every leave-one-signal-date-out estimate remains negative: True.
- Label: `historically_stable_selected_sample`—this is still selected-sample evidence, not transfer proof.

## RSR2 incremental robustness

- Paired trades / signal-date clusters: 23 / 21.
- RSR1 wins versus RSR2 wins: 15 / 16; the hit-rate difference is exactly one trade.
- Aggregate total P&L delta: $145.34; probability bootstrap mean is positive: 99.59%.
- Direct exit effect: $77.95; probability bootstrap mean is positive: 87.72%.
- Probability total P&L, direct effect and win-rate delta are all positive: 64.31%.
- Two largest total deltas explain 86.93%; remaining total delta after both: $19.00.
- Only 2 paired trades have a positive direct exit effect; removing both leaves $0.00.
- Every leave-one-cluster-out total/direct aggregate remains positive: True / True.
- Label: `directional_but_sparse`.

## Decision

1. Treat RSR1's loss-avoidance mechanism as the more important forward question. Its absolute historical expectancy bootstrap is strong, but the exact transfer and 7/10 stability gates still fail.
2. Keep RSR2 as a separate frozen shadow. Its profit direction is favorable, but two direct exits and one win conversion are too sparse for promotion.
3. Do not search a new profit trigger, floor, partial-exit fraction or holding period on this history.
4. Formal V9, the real account and all order states remain unchanged.

No order or live authorization is created by this report.
