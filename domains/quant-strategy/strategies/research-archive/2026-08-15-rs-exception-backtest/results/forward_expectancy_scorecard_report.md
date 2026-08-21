# Forward expectancy scorecard

## Current status

- Forward status: `observing`
- Completed data through: `2026-08-20`
- Completed forward sessions: `4`
- Forward ledger hashes preserved: `True`
- This report is diagnostic-only and does not amend the original promotion gates.

| Scope | Variant | Label | Trades | Win rate (Wilson 95%) | Payoff | Break-even win | Expectancy | PF | Bootstrap p05 / p95 | P(E<=0) | Top-symbol profit |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| genuine_forward | matched_baseline | awaiting_sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| genuine_forward | RSR1-shadow | awaiting_sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| genuine_forward | RSR2-profit-lock-shadow | awaiting_sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| retrospective_calibration | matched_baseline | positive_but_fragile | 44 | 43.18% (29.68%–57.78%) | 1.89 | 34.57% | 1.86% | 1.39 | -1.68% / 5.40% | 20.18% | 22.87% |
| retrospective_calibration | RSR1-shadow | positive_diversified | 23 | 65.22% (44.89%–81.19%) | 2.70 | 27.04% | 8.95% | 4.94 | 3.79% / 14.10% | 0.12% | 22.26% |
| retrospective_calibration | RSR2-profit-lock-shadow | positive_diversified | 23 | 69.57% (49.13%–84.40%) | 2.74 | 26.76% | 9.64% | 6.49 | 4.57% / 14.67% | 0.05% | 25.43% |

## Interpretation

- Forward rows remain `awaiting_sample` until at least 20 trades close. Open or pending positions never enter the denominator.
- The Wilson interval answers how uncertain the hit rate is; payoff and break-even win rate answer whether that hit rate is economically sufficient.
- The cluster bootstrap keeps same-entry-date trades together. It remains descriptive because dates and regimes are not independent.
- Retrospective calibration uses the hindsight-selected current list. It validates calculations and exposes uncertainty, but contributes zero forward evidence.

Research-only. No order or strategy change is authorized.
