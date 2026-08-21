# Economic edge and opportunity-cost decomposition

## Bottom line

The historical RSR1 edge is primarily an avoided-loss effect, but it also rejects profitable trades. RSR2's incremental benefit is sparse and must not be treated as a broad improvement until forward protected exits accumulate.

## Variant economics

| Variant | Trades | Win rate | Gross profit | Gross loss | Net P&L | PF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| matched_baseline | 44 | 43.18% | $1148.13 | $824.87 | $323.25 | 1.39 |
| RSR1-shadow | 23 | 65.22% | $1179.66 | $238.70 | $940.96 | 4.94 |
| RSR2-profit-lock-shadow | 23 | 69.57% | $1284.15 | $197.85 | $1086.30 | 6.49 |

## Direct quality-filter exclusions

- Directly excluded trades: 23
- Avoided losers: 16, historical losses avoided $554.79
- Missed winners: 7, historical profit missed $159.37
- Net P&L removed from the baseline path: $-395.43
- Excluded-trade win rate / mean return: 30.43% / -3.84%

Avoided losses are not earned profit, and RSR1-only replacements remain path-dependent. This decomposition cannot be converted into a new threshold.

## Winner concentration

| Variant | Top winners removed | Share gross profit | Share net P&L | Remaining net P&L |
| --- | ---: | ---: | ---: | ---: |
| RSR1-shadow | 1 | 16.10% | 20.19% | $750.97 |
| RSR1-shadow | 2 | 29.92% | 37.52% | $587.96 |
| RSR1-shadow | 3 | 40.00% | 50.15% | $469.10 |
| RSR2-profit-lock-shadow | 1 | 19.78% | 23.38% | $832.32 |
| RSR2-profit-lock-shadow | 2 | 32.72% | 38.68% | $666.07 |
| RSR2-profit-lock-shadow | 3 | 41.98% | 49.63% | $547.21 |

## RSR2 incremental attribution

- Paired trades: 23
- Improved / worsened / unchanged: 5 / 0 / 18
- Aggregate P&L delta versus RSR1: $145.34
- Direct exit effect on frozen RSR1 shares: $77.95 (53.63%)
- Capital-path and whole-share sizing residual: $67.39 (46.37%)
- Trades with a nonzero direct exit effect: 2
- Largest positive delta share: 44.03%
- Two largest positive deltas share: 86.93%
- Profit-lock activations / exits: 12 / 2

## Decision

Keep RSR1 and RSR2 unchanged as separate forward shadows. Forward reviews must report avoided-loss behavior and missed-winner opportunity cost together, and must identify whether RSR2 improvement remains concentrated in one or two protected exits. No order is authorized.
