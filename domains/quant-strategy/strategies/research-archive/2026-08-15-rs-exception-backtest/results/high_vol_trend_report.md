# High-volatility trend participation event study

## Boundary

The definitions and continuation gate were frozen in `high-vol-trend-preregistration.md` before reading these outputs. The current-list universe is hindsight-selected, and the numerical module was specified after seeing 2026; all results are retrospective and cannot authorize a trade.

## 20-session outcomes

| Period | Variant | Events | Mean | Median | Win rate | Mean excess vs QQQ | Mean MAE | Mean MFE | MFE/|MAE| |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| development_2024_2025 | hv_relaxed | 44 | 10.01% | 4.01% | 65.91% | 8.41% | -12.83% | 22.63% | 1.76 |
| development_2024_2025 | hv_central | 23 | 5.41% | 0.68% | 60.87% | 4.27% | -14.35% | 21.29% | 1.48 |
| development_2024_2025 | hv_strict | 6 | -1.67% | -1.82% | 50.00% | -4.65% | -15.62% | 13.81% | 0.88 |
| development_2024_2025 | rsr1_low_vol_comparator | 33 | 7.88% | 6.41% | 72.73% | 7.22% | -7.18% | 15.84% | 2.20 |
| retrospective_2026 | hv_relaxed | 39 | 12.86% | 2.15% | 51.28% | 11.94% | -16.47% | 35.96% | 2.18 |
| retrospective_2026 | hv_central | 18 | 4.29% | 0.38% | 50.00% | 3.13% | -14.90% | 27.49% | 1.84 |
| retrospective_2026 | hv_strict | 2 | -31.77% | -31.77% | 0.00% | -27.85% | -34.55% | 12.85% | 0.37 |
| retrospective_2026 | rsr1_low_vol_comparator | 3 | 5.26% | -1.20% | 33.33% | 5.83% | -9.66% | 18.88% | 1.95 |

## Continuation gate

- `minimum_event_count`: `True`
- `positive_mean_both`: `True`
- `positive_median_both`: `True`
- `positive_excess_both`: `True`
- `win_rate_ge_50_both`: `True`
- `mfe_mae_ge_1_25_both`: `True`
- `positive_return_concentration_le_35`: `True`
- `two_of_three_neighbors_positive`: `True`
- `positive_return_concentration`: `24.18%`
- `passes_event_continuation_gate`: `True`

## Decision

The event layer passes the preregistered screen and may proceed to a separately specified portfolio simulation. It is still not promotable without genuine forward evidence.
