# RSR2 conditional winner-extension audit

## Scope

This post-hoc study changes only the maximum holding period for positions that remain profitable, above MA20 and non-negative in RS20 at the frozen 20-session deadline. RSR2 profit protection and every entry, sizing, cost and risk rule remain unchanged.

## Frozen versus central

| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Profit concentration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train_2024_2025 | rsr2_frozen | 17.18% | -1.91% | 2.13 | 70.00% | 20 | 27.84% |
| retrospective_2026 | rsr2_frozen | 0.82% | -1.69% | 0.42 | 66.67% | 3 | 82.71% |
| full | rsr2_frozen | 18.11% | -2.33% | 1.77 | 69.57% | 23 | 25.43% |
| train_2024_2025 | extend30_gain8 | 15.95% | -2.56% | 1.80 | 65.00% | 20 | 24.20% |
| retrospective_2026 | extend30_gain8 | 2.60% | -1.57% | 1.17 | 66.67% | 3 | 91.45% |
| full | extend30_gain8 | 18.66% | -2.75% | 1.65 | 65.22% | 23 | 20.30% |

## Screen

| variant             | train_2024_2025_total_return_nonworse   | train_2024_2025_max_drawdown_nonworse   | train_2024_2025_sharpe_nonworse   | train_2024_2025_win_rate_nonworse   | retrospective_2026_total_return_nonworse   | retrospective_2026_max_drawdown_nonworse   | retrospective_2026_sharpe_nonworse   | retrospective_2026_win_rate_nonworse   | full_20bps_return_nonworse   | concentration_le_35   | return_improves_both   | two_of_three_return_improve_both   | passes_all   |
|:--------------------|:----------------------------------------|:----------------------------------------|:----------------------------------|:------------------------------------|:-------------------------------------------|:-------------------------------------------|:-------------------------------------|:---------------------------------------|:-----------------------------|:----------------------|:-----------------------|:-----------------------------------|:-------------|
| extend30_any_winner | False                                   | False                                   | False                             | False                               | True                                       | True                                       | True                                 | True                                   | True                         | True                  | False                  | False                              | False        |
| extend30_gain8      | False                                   | False                                   | False                             | False                               | True                                       | True                                       | True                                 | True                                   | True                         | True                  | False                  | False                              | False        |
| extend40_gain8      | False                                   | False                                   | False                             | False                               | True                                       | False                                      | True                                 | True                                   | True                         | True                  | False                  | False                              | False        |

## Decision

The central extension fails the preregistered cross-period screen. Keep frozen RSR2 and do not optimize further on this history.
