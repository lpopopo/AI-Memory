# Matched-baseline risk-filter comparison

This corrects the earlier attribution problem: both variants use the same 3% RS20 minimum, volume, extension, hold and stop settings. They differ only in `ATR14/close <= 4%` and signal-day close location >= 50%.

| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Profit factor |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024 | matched_baseline | 0.78% | -2.18% | 0.25 | 28.57% | 7 | 1.28 |
| 2024 | risk_filter | 2.13% | -1.43% | 0.68 | 33.33% | 6 | 2.46 |
| 2025 | matched_baseline | 5.74% | -3.31% | 0.99 | 48.28% | 29 | 1.86 |
| 2025 | risk_filter | 12.38% | -1.94% | 3.00 | 73.33% | 15 | 8.46 |
| 2026 | matched_baseline | -2.18% | -3.89% | -0.86 | 22.22% | 9 | 0.42 |
| 2026 | risk_filter | 0.61% | -1.89% | 0.32 | 50.00% | 4 | 1.66 |
| train_2024_2025 | matched_baseline | 6.31% | -5.32% | 0.64 | 45.95% | 37 | 1.61 |
| train_2024_2025 | risk_filter | 17.15% | -1.91% | 2.19 | 70.00% | 20 | 8.23 |
| full | matched_baseline | 5.91% | -5.32% | 0.49 | 44.44% | 45 | 1.44 |
| full | risk_filter | 17.81% | -2.33% | 1.77 | 66.67% | 24 | 6.39 |

## Full-period trade-path decomposition

| Group | Trades | Win rate | Average return | Net P&L |
| --- | ---: | ---: | ---: | ---: |
| common | 20 | 65.00% | 9.74% | $830.81 |
| baseline_only | 25 | 28.00% | -4.21% | $-476.27 |
| candidate_only | 4 | 75.00% | 5.88% | $137.55 |

`baseline_only` measures trades absent from the candidate path, usually because ATR/close location rejected them. `candidate_only` measures replacement opportunities made possible by the changed portfolio path; it must not be attributed solely to the filter.

| Baseline-only reason | Trades | Win rate | Average return | Net P&L |
| --- | ---: | ---: | ---: | ---: |
| atr_pct | 14 | 28.57% | -4.91% | $-313.27 |
| portfolio_path | 2 | 0.00% | -8.52% | $-75.94 |
| close_location | 7 | 42.86% | -1.67% | $-53.32 |
| atr_pct+close_location | 2 | 0.00% | -3.95% | $-33.74 |

## Interpretation

On the fixed current watchlist, the exact filter looks materially better than its matched baseline in 2024, 2025 and 2026 YTD. This strengthens the case for the already-frozen forward shadow, but does not override the broader point-in-time proxy result, the watchlist survivorship bias, or the minimum 126-session/20-closed-trade promotion gate.
