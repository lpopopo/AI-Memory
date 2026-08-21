# Close-confirmed profit-protection audit

## What the trade paths say

The frozen 32-name candidate has `23` trades, `15` winners and `8` losses. Only `1` loss reached +8% pre-exit MFE, and only `1` loss closed at least 8% above entry before later losing. `14/15` eventual winners reached +8% MFE.

A fixed profit target would therefore cap nearly every winner to repair one historical giveback. The tested alternative waits for a completed close to confirm a gain, then raises the stop for the following session. Daily-bar ambiguity is avoided by never activating from the same day's intraday high.

## Frozen versus central 15% -> 5% challenger at 10 bps

| Period | Variant | Return | Max DD | Sharpe | Win rate | Profit factor | Trades | Lock exits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| train_2024_2025 | frozen | 15.01% | -2.46% | 1.89 | 65.00% | 5.92 | 20 | 0 |
| train_2024_2025 | lock_15_to_5 | 17.18% | -1.91% | 2.13 | 70.00% | 8.24 | 20 | 1 |
| 2026 | frozen | 0.62% | -1.88% | 0.33 | 66.67% | 1.67 | 3 | 0 |
| 2026 | lock_15_to_5 | 0.82% | -1.69% | 0.42 | 66.67% | 1.88 | 3 | 1 |
| full | frozen | 15.68% | -2.46% | 1.55 | 65.22% | 4.94 | 23 | 0 |
| full | lock_15_to_5 | 18.11% | -2.33% | 1.77 | 69.57% | 6.49 | 23 | 2 |

## Robustness checks

- `8/9` trigger/floor neighbors pass the non-worse return, drawdown, Sharpe and win-rate screen in both training and 2026 while preserving the paired-filter advantage.
- At 20 bps, the central candidate returns `14.72%` versus `7.14%` for its paired baseline and `13.45%` for frozen RSR1.
- Fixed-path repricing of the unchanged 10-bps trades to 20 bps gives `17.72%` for the central challenger versus `15.30%` for frozen RSR1.
- Full-rerun trade paths at 10/20 bps are not identical (`23` versus `24` trades), so the fixed-path check remains necessary.

## Decision

The 15% close-confirmed trigger with a +5% entry-price floor is a reasonable separate forward challenger, not a replacement for RSR1. Its apparent improvement is driven by only two protected exits (INTC in training and KLAC in 2026), uses the same hindsight-selected watchlist, and was examined after the base strategy. Keep RSR1 frozen; any forward test must use a new version and separate ledger.

Research-only. No live order or formal V9 change is authorized.
