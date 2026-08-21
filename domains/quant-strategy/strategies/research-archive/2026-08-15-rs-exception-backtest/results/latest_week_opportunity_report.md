# Latest-week missed-opportunity audit

## Boundary

This is a retrospective explanation of completed sessions from 2026-08-10 through 2026-08-14. The RSR1 rules were not yet in genuine forward observation, so no row can authorize or reconstruct a live order.

## Largest watchlist moves

| Rank | Symbol | Aug 7 close | Aug 14 close | Weekly return | RSR1 signal this week |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | SNDK | 1212.21 | 1641.11 | 35.38% | False |
| 2 | SMCI | 31.13 | 39.84 | 27.98% | False |
| 3 | SKHY | 137.91 | 166.33 | 20.61% | False |
| 4 | STX | 812.76 | 973.44 | 19.77% | False |
| 5 | WDC | 434.30 | 508.80 | 17.15% | False |
| 6 | NOK | 9.36 | 10.76 | 14.96% | False |
| 7 | DRAM | 50.60 | 57.32 | 13.28% | False |
| 8 | MXL | 74.98 | 84.84 | 13.15% | False |
| 9 | AAOI | 135.63 | 150.28 | 10.80% | False |
| 10 | MU | 877.57 | 971.66 | 10.72% | False |

## AAOI decision trace

| Date | Close | Daily | From Aug 7 | RS20 | Volume | ATR | Close location | Failed exact conditions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-08-10 | 132.81 | -2.08% | -2.08% | 21.48% | 1.69x | 11.93% | 20% | above_ma50;breakout_20d;extension_le_12pct;atr_le_4pct;close_location_ge_50pct;event_gap_clear |
| 2026-08-11 | 134.33 | 1.14% | -0.96% | 11.64% | 0.80x | 11.82% | 70% | above_ma50;breakout_20d;volume_ge_1_2x;extension_le_12pct;atr_le_4pct;event_gap_clear |
| 2026-08-12 | 138.08 | 2.79% | 1.81% | 27.58% | 1.15x | 11.61% | 66% | breakout_20d;volume_ge_1_2x;extension_le_12pct;atr_le_4pct |
| 2026-08-13 | 130.08 | -5.79% | -4.09% | 26.22% | 0.92x | 12.45% | 3% | above_ma50;breakout_20d;volume_ge_1_2x;extension_le_12pct;atr_le_4pct;close_location_ge_50pct |
| 2026-08-14 | 150.28 | 15.53% | 10.80% | 41.12% | 1.60x | 11.37% | 87% | extension_le_12pct;atr_le_4pct |

## Interpretation

- AAOI returned `10.80%` over the week, but produced `0` exact RSR1 signal days. Its recurring blockers were `extension_le_12pct (5/5), atr_le_4pct (5/5), breakout_20d (4/5), above_ma50 (3/5), volume_ge_1_2x (3/5), close_location_ge_50pct (2/5), event_gap_clear (2/5)`.
- Across all `35` tradable watchlist names there were `0` exact strict-veto signal rows this week. A strong realized return alone is therefore not evidence that the strategy should have bought before the move.
- Classification: AAOI was a missed outcome, not yet a demonstrated rule error. The repair is better ex-ante trigger labeling and forward capture measurement, not retroactively weakening volatility, breakout, volume or market-health gates after seeing the rally.
