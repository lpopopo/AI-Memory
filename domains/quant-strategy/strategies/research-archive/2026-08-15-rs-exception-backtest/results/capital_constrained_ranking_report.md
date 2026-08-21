# Capital-constrained RSR2 ranking audit

## Decision

- Result: `retain_formal_composite`.
- Selected forward challenger: `none`.
- Every policy uses identical frozen RSR1 entries and RSR2 exits; only ordering among simultaneously eligible names changes.
- This retrospective current-list audit cannot modify formal V9 or the already-frozen RSR1/RSR2 forward ledgers.

## Advancement screen

| Policy | Status | Min return delta 10bps | Min return delta 20bps | Contention | Sharpe | DD | Win rate | Diversified |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| rs_only | insufficient | -3.82% | -3.10% | False | False | True | True | True |
| low_atr_first | insufficient | -3.61% | -2.60% | False | False | True | True | True |
| balanced_rank | insufficient | -0.13% | -0.14% | False | True | True | True | True |

## Ten-basis-point results

| NAV | Period | Policy | Return | Max DD | Sharpe | Win rate | Trades | Contention | Top profit share |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $6,000.00 | development_2024_2025 | formal_composite | 17.18% | -1.91% | 2.13 | 70.00% | 20 | 6 | 27.84% |
| $6,000.00 | development_2024_2025 | rs_only | 13.36% | -2.07% | 1.85 | 65.00% | 20 | 6 | 26.92% |
| $6,000.00 | development_2024_2025 | low_atr_first | 13.57% | -1.93% | 1.83 | 65.00% | 20 | 7 | 22.48% |
| $6,000.00 | development_2024_2025 | balanced_rank | 17.05% | -1.91% | 2.16 | 65.00% | 20 | 6 | 28.36% |
| $6,000.00 | heldout_2026 | formal_composite | 0.82% | -1.69% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $6,000.00 | heldout_2026 | rs_only | 0.82% | -1.69% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $6,000.00 | heldout_2026 | low_atr_first | 0.82% | -1.69% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $6,000.00 | heldout_2026 | balanced_rank | 0.82% | -1.69% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $6,000.00 | full | formal_composite | 18.11% | -2.33% | 1.77 | 69.57% | 23 | 6 | 25.43% |
| $6,000.00 | full | rs_only | 14.17% | -2.30% | 1.55 | 65.22% | 23 | 6 | 24.31% |
| $6,000.00 | full | low_atr_first | 14.39% | -2.30% | 1.54 | 65.22% | 23 | 7 | 20.23% |
| $6,000.00 | full | balanced_rank | 17.98% | -2.33% | 1.78 | 65.22% | 23 | 6 | 25.86% |
| $5,751.77 | development_2024_2025 | formal_composite | 16.15% | -1.94% | 2.09 | 70.00% | 20 | 6 | 24.54% |
| $5,751.77 | development_2024_2025 | rs_only | 13.05% | -2.06% | 1.87 | 65.00% | 20 | 6 | 28.50% |
| $5,751.77 | development_2024_2025 | low_atr_first | 13.56% | -1.96% | 1.86 | 65.00% | 20 | 7 | 23.38% |
| $5,751.77 | development_2024_2025 | balanced_rank | 16.05% | -1.94% | 2.12 | 65.00% | 20 | 6 | 25.02% |
| $5,751.77 | heldout_2026 | formal_composite | 0.85% | -1.77% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $5,751.77 | heldout_2026 | rs_only | 0.85% | -1.77% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $5,751.77 | heldout_2026 | low_atr_first | 0.85% | -1.77% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $5,751.77 | heldout_2026 | balanced_rank | 0.85% | -1.77% | 0.42 | 66.67% | 3 | 0 | 82.71% |
| $5,751.77 | full | formal_composite | 17.01% | -2.31% | 1.75 | 69.57% | 23 | 6 | 22.36% |
| $5,751.77 | full | rs_only | 13.90% | -2.34% | 1.55 | 65.22% | 23 | 6 | 25.59% |
| $5,751.77 | full | low_atr_first | 14.41% | -2.34% | 1.56 | 65.22% | 23 | 7 | 20.96% |
| $5,751.77 | full | balanced_rank | 16.91% | -2.32% | 1.77 | 65.22% | 23 | 6 | 22.75% |

## Interpretation boundary

- A higher retrospective return is not enough: the preregistered gate requires cross-period, two-NAV and two-cost consistency plus adequate contention and profit diversification.
- The 2026 segment has been seen in prior studies. It is a consistency monitor, not genuine out-of-sample evidence.
- See `capital-constrained-ranking-preregistration.md` for the frozen rules and gate.
