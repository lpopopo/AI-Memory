# Exact-filter ablation and robustness

## Boundary

All variants use the same fixed current watchlist, broad/theme gates, RS20 3%, volume, extension, cooldown, sizing, stop and hold rules. Only ATR and signal-day close-location filters change. This is post-hoc, survivorship-biased research and cannot authorize a trade.

## Ten-basis-point ablation

| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Profit factor |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024 | matched_baseline | 0.78% | -2.18% | 0.25 | 28.57% | 7 | 1.28 |
| 2024 | atr_only | 2.13% | -1.43% | 0.68 | 33.33% | 6 | 2.46 |
| 2024 | close_location_only | 0.78% | -2.18% | 0.25 | 28.57% | 7 | 1.28 |
| 2024 | combined | 2.13% | -1.43% | 0.68 | 33.33% | 6 | 2.46 |
| 2025 | matched_baseline | 5.74% | -3.31% | 0.99 | 48.28% | 29 | 1.86 |
| 2025 | atr_only | 8.28% | -3.04% | 1.76 | 56.52% | 23 | 3.01 |
| 2025 | close_location_only | 6.38% | -3.30% | 1.22 | 50.00% | 26 | 1.82 |
| 2025 | combined | 12.38% | -1.94% | 3.00 | 73.33% | 15 | 8.46 |
| 2026 | matched_baseline | -2.18% | -3.89% | -0.86 | 22.22% | 9 | 0.42 |
| 2026 | atr_only | -0.11% | -2.37% | -0.03 | 33.33% | 6 | 0.94 |
| 2026 | close_location_only | -1.46% | -3.41% | -0.59 | 28.57% | 7 | 0.51 |
| 2026 | combined | 0.61% | -1.89% | 0.32 | 50.00% | 4 | 1.66 |
| train_2024_2025 | matched_baseline | 6.31% | -5.32% | 0.64 | 45.95% | 37 | 1.61 |
| train_2024_2025 | atr_only | 12.01% | -2.94% | 1.44 | 57.14% | 28 | 3.38 |
| train_2024_2025 | close_location_only | 9.41% | -3.35% | 1.05 | 50.00% | 32 | 1.94 |
| train_2024_2025 | combined | 17.15% | -1.91% | 2.19 | 70.00% | 20 | 8.23 |
| full | matched_baseline | 5.91% | -5.32% | 0.49 | 44.44% | 45 | 1.44 |
| full | atr_only | 11.89% | -2.94% | 1.15 | 52.94% | 34 | 2.77 |
| full | close_location_only | 10.28% | -3.33% | 0.88 | 48.72% | 39 | 1.81 |
| full | combined | 17.81% | -2.33% | 1.77 | 66.67% | 24 | 6.39 |

## Full-period cost sensitivity

| Cost | Variant | Return | Max DD | Sharpe | Win rate |
| ---: | --- | ---: | ---: | ---: | ---: |
| 10 bps | matched_baseline | 5.91% | -5.32% | 0.49 | 44.44% |
| 10 bps | atr_only | 11.89% | -2.94% | 1.15 | 52.94% |
| 10 bps | close_location_only | 10.28% | -3.33% | 0.88 | 48.72% |
| 10 bps | combined | 17.81% | -2.33% | 1.77 | 66.67% |
| 20 bps | matched_baseline | 5.39% | -5.47% | 0.45 | 44.44% |
| 20 bps | atr_only | 11.39% | -2.96% | 1.10 | 52.94% |
| 20 bps | close_location_only | 9.76% | -3.36% | 0.84 | 48.72% |
| 20 bps | combined | 14.46% | -2.33% | 1.46 | 64.00% |

## Parameter and concentration robustness

- Frozen 4%/50% cell beats the unfiltered baseline in both 2024-2025 and 2026 on return, Sharpe and drawdown: `True`.
- Raw grid cells beating baseline on return, Sharpe and drawdown in both periods: `17/20`.
- After a lenient anti-cash screen of at least 10 training and 4 test trades: `10/20`. This is still far below the promotion sample gate.
- Across 35 leave-one-symbol-out runs, combined beats baseline on return in 100.0%, drawdown in 100.0%, Sharpe in 100.0%, and win rate in 100.0%.
- Leave-one-symbol-out return delta range: +7.97% to +13.27%.
- Across stop-loss 6%/8%/10% and maximum-hold 10/20/30 combinations, the filter beats its paired baseline on return, Sharpe and drawdown in both periods for `9/9` exit cells.

## Paired 20-session block bootstrap

| Period | P(candidate return > baseline) | P(candidate DD better) | Median delta | 5%-95% delta |
| --- | ---: | ---: | ---: | ---: |
| train_2024_2025 | 99.1% | 100.0% | +9.92% | +2.76% to +19.39% |
| 2026 | 97.8% | 99.7% | +2.28% | +0.30% to +5.03% |
| full | 99.8% | 99.9% | +12.00% | +4.30% to +21.85% |

The bootstrap resamples paired realized return blocks from the same post-hoc sample. It describes path consistency; it is not an out-of-sample p-value and cannot cure watchlist selection bias.

## Decision rule

Ablation can identify the likely contributor but cannot promote it. The frozen combined RSR1 shadow remains unchanged. If ATR-only dominates combined across both held-out behavior and parameter neighbors, that finding may seed a separately versioned future challenger only after RSR1 has accumulated genuine forward evidence.

The follow-up family-wise selection-bias audit is in
`selection_bias_audit_report.md`. It finds supportive but non-decisive structure
(PBO 13.1%, family-wise p=0.063) and fails the immutable 7/10 chronological-block
stability gates. This supersedes any interpretation that 17/20 successful raw
grid cells alone establishes an independent edge.
