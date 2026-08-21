# RSR filter selection-bias audit

## Bottom line

The registered selection-bias concern is **not contained**.
This result discounts retrospective confidence; it does not modify formal V9, RSR1, RSR2, or live permissions.

## Frozen family and full-path context

- Trial cells: 20
- Frozen interval: 2024-01-02 through 2026-08-18
- Matched baseline: return 5.91%, Sharpe 0.48, trades 45
- Frozen 4%/50%: return 17.81%, Sharpe 1.76, trades 24

## Combinatorially symmetric cross-validation

- Splits: 252
- Probability of backtest overfitting (PBO): 13.1%
- Median selected-cell OOS rank: 95.0%
- Median selected-minus-baseline OOS return: +3.77%
- Median OOS regret versus best cell: +0.53%

Most frequently selected in-sample cells:

- `atr_04_loc_50`: 154/252 splits
- `atr_04_loc_25`: 48/252 splits
- `atr_04_loc_75`: 17/252 splits
- `atr_03_loc_50`: 11/252 splits
- `atr_05_loc_75`: 10/252 splits

## Family-wise block bootstrap

- Best observed cell: `atr_04_loc_50`
- Best annualized mean daily-return advantage: +4.02%
- Family-wise p-value after all 19 challengers: 0.063
- Frozen 4%/50% annualized mean daily-return advantage: +4.02%
- Frozen cell unadjusted paired p-value: 0.022

## Frozen 4%/50% chronological blocks

| Block | Dates | Return delta | Sharpe delta |
| ---: | --- | ---: | ---: |
| 0 | 2024-01-02 to 2024-04-05 | +0.00% | n/a |
| 1 | 2024-04-08 to 2024-07-11 | +0.00% | n/a |
| 2 | 2024-07-12 to 2024-10-14 | +0.00% | n/a |
| 3 | 2024-10-15 to 2025-01-21 | +1.25% | +0.82 |
| 4 | 2025-01-22 to 2025-04-25 | +5.20% | +5.77 |
| 5 | 2025-04-28 to 2025-07-31 | +0.45% | +1.04 |
| 6 | 2025-08-01 to 2025-11-03 | +1.93% | +1.65 |
| 7 | 2025-11-04 to 2026-02-09 | +0.42% | +0.36 |
| 8 | 2026-02-10 to 2026-05-14 | -0.03% | -0.17 |
| 9 | 2026-05-15 to 2026-08-18 | +1.53% | +0.40 |

Positive return blocks: 6/10; positive Sharpe blocks: 6/10.
Descriptively, 7 blocks had nonzero return observations and 6 were positive; 7 had finite Sharpe observations and 6 were positive. The three inactive blocks remain in the registered 10-block denominator and cannot be removed after observation.

## Registered gate

- pbo_below_50pct: pass
- familywise_p_below_10pct: pass
- fixed_positive_return_at_least_7_of_10: fail
- fixed_positive_sharpe_at_least_7_of_10: fail

## Interpretation

The twenty-cell grid and every resample reuse a fixed current watchlist selected with hindsight. Consequently this audit can reveal parameter-selection fragility but cannot establish a live edge. A low unadjusted p-value is not sufficient after inspecting the full family. Genuine forward trades, payoff distribution and profit concentration remain the governing evidence. The adjusted p-value of 0.063 clears the preregistered 10% threshold but not 5%; combined with three inactive chronological blocks, it is suggestive rather than decisive.
