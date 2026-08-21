# SMH Relative-Strength Exception Backtest

- Data: `2024-01-02` to `2026-08-07`
- Training: `2024-2025`; held-out test: `2026 YTD`
- Research-only; formal V9 weights changed: `false`
- Promotion gate: `fail`
- Decision: `not_promoted; retain_strict_veto_and_continue_research`

## Default pre-specified configuration

| Period | Variant | Return | CAGR | Max DD | Sharpe | Win rate | Trades | Exception trades | Exposure |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| train | strict_veto | 8.24% | 4.05% | -4.00% | 0.88 | 51.52% | 33 | 0 | 6.34% |
| train | rs_exception | 7.68% | 3.78% | -4.32% | 0.82 | 48.57% | 35 | 2 | 6.50% |
| train | breadth_exception | 6.86% | 3.38% | -4.27% | 0.74 | 48.57% | 35 | 3 | 6.37% |
| train | unrestricted | 14.85% | 7.18% | -3.71% | 1.41 | 54.29% | 35 | 0 | 7.04% |
| test | strict_veto | -1.16% | -1.95% | -2.89% | -0.51 | 25.00% | 8 | 0 | 3.98% |
| test | rs_exception | -1.28% | -2.15% | -3.01% | -0.57 | 22.22% | 9 | 1 | 4.21% |
| test | breadth_exception | -1.66% | -2.79% | -3.45% | -0.73 | 20.00% | 10 | 2 | 4.03% |
| test | unrestricted | -1.26% | -2.10% | -3.21% | -0.55 | 36.36% | 11 | 0 | 4.61% |
| full | strict_veto | 8.86% | 3.33% | -4.00% | 0.76 | 50.00% | 40 | 0 | 5.83% |
| full | rs_exception | 8.18% | 3.07% | -4.32% | 0.70 | 46.51% | 43 | 3 | 6.01% |
| full | breadth_exception | 6.98% | 2.63% | -4.27% | 0.61 | 45.45% | 44 | 5 | 5.87% |
| full | unrestricted | 15.93% | 5.86% | -3.71% | 1.19 | 53.33% | 45 | 0 | 6.61% |

## Train-selected configuration and held-out result

Selected parameters: `{"breadth_count_min": 2.0, "breadth_min": 0.5, "exception_target_weight": 0.03, "max_atr_pct": 1.0, "max_extension": 0.08, "max_hold_days": 30.0, "min_close_location": 0.0, "repair_rs10_min": 0.03, "rs20_min": 0.03, "stop_loss": 0.08, "volume_ratio_min": 1.2}`

| Test variant | Return | Max DD | Sharpe | Win rate | Trades | Exception win rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| strict_veto | -0.24% | -0.41% | -0.72 | 0.00% | 2 | n/a |
| rs_exception | -0.18% | -0.49% | -0.53 | 33.33% | 3 | 100.00% |

## Held-out delta: exception minus strict veto

- Return: `+0.05%`
- CAGR: `+0.09%`
- Max drawdown: `-0.08%` (positive is better)
- Sharpe: `+0.19`
- Trade win rate: `33.33%`

## Breadth-confirmed repair exception

Selected parameters: `{"breadth_count_min": 3.0, "breadth_min": 0.6, "exception_target_weight": 0.05, "max_atr_pct": 1.0, "max_extension": 0.12, "max_hold_days": 20.0, "min_close_location": 0.0, "repair_rs10_min": 0.02, "rs20_min": 0.05, "stop_loss": 0.08, "volume_ratio_min": 1.2}`

| Test variant | Return | Max DD | Sharpe | Win rate | Trades | Exception trades | Exception win rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| strict_veto | -1.16% | -2.89% | -0.51 | 25.00% | 8 | 0 | n/a |
| breadth_exception | -1.66% | -3.45% | -0.73 | 20.00% | 10 | 2 | 0.00% |

Breadth test return delta: `-0.50%`; Sharpe delta: `-0.22`; win-rate delta: `-5.00%`.

## Volatility-adapted strict entry

Selected parameters: `{"breadth_count_min": 2, "breadth_min": 0.5, "exception_target_weight": 0.05, "max_atr_pct": 0.04, "max_extension": 0.12, "max_hold_days": 20, "min_close_location": 0.5, "repair_rs10_min": 0.03, "rs20_min": 0.03, "stop_loss": 0.08, "volume_ratio_min": 1.2}`

| Period | Return | Max DD | Sharpe | Win rate | Trades | Profit factor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024 | 2.13% | -1.43% | 0.68 | 33.33% | 6 | 2.46 |
| 2025 | 12.38% | -1.94% | 3.00 | 73.33% | 15 | 8.46 |
| 2026 | 0.61% | -1.89% | 0.32 | 50.00% | 4 | 1.66 |
| full | 17.81% | -2.33% | 1.77 | 66.67% | 24 | 6.39 |

2026 delta versus default strict: return `+1.78%`, Sharpe `+0.83`, win rate `25.00%`.

This filter is post-hoc because the 2026 loss pattern was inspected before defining it; it requires fresh forward evidence.

## Limitations

- Current watchlist is applied retrospectively and is not a point-in-time universe.
- Earnings are approximated by a >=10% positive opening-gap cooldown because a PIT earnings calendar is unavailable.
- The cached OHLCV dataset ends before the 2026-08-14 review week completed.
- A research pass can only start a forward shadow; it cannot change formal V9 or authorize an order.
