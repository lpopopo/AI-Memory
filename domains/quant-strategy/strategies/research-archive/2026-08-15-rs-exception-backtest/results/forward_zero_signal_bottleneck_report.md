# Forward zero-signal bottleneck audit

## Bottom line

This audit explains the absence of RSR1 signals without changing any threshold. Counterfactual counts are diagnostics, not trades.

- Period: 2026-08-17 through 2026-08-20
- Sessions / symbols / symbol-days: 4 / 32 / 128
- Binding first-zero steps by session: {'extension_0_to_12pct': 1, 'smh_ma50': 3}
- Stock-level baseline candidates before broad/SMH gates: 0
- With broad gate but ignoring SMH veto: 0
- With strict SMH veto, before quality pair: 0
- Final RSR1 candidates: 0

## Daily market gates and counterfactuals

| Date | Broad | SMH>=MA50 | SMH close | SMH MA50 | Stock baseline | Broad/no-SMH | Strict pre-quality | RSR1 | First zero |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-08-17 | True | True | 594.07 | 590.82 | 0 | 0 | 0 | 0 | extension_0_to_12pct (1) |
| 2026-08-18 | True | False | 569.77 | 590.82 | 0 | 0 | 0 | 0 | smh_ma50 (32) |
| 2026-08-19 | True | False | 560.92 | 590.08 | 0 | 0 | 0 | 0 | smh_ma50 (32) |
| 2026-08-20 | True | False | 562.65 | 589.51 | 0 | 0 | 0 | 0 | smh_ma50 (32) |

## Binding symbols

- 2026-08-17: extension_0_to_12pct — AXTI
- 2026-08-18: smh_ma50 — all 32 frozen shadow symbols
- 2026-08-19: smh_ma50 — all 32 frozen shadow symbols
- 2026-08-20: smh_ma50 — all 32 frozen shadow symbols

## Fixed funnel aggregate

| Condition | Marginal pass | Marginal fail | Sequential survivors |
| --- | ---: | ---: | ---: |
| usable_ohlcv | 128 | 0 | 128 |
| broad_gate | 128 | 0 | 128 |
| smh_ma50 | 32 | 96 | 32 |
| above_ma20 | 84 | 44 | 29 |
| above_ma50 | 39 | 89 | 16 |
| breakout_prior_high20 | 11 | 117 | 8 |
| rs20_at_least_3pct | 54 | 74 | 7 |
| volume_ratio_at_least_1_2 | 14 | 114 | 1 |
| extension_0_to_12pct | 60 | 68 | 0 |
| event_cooldown_clear | 126 | 2 | 0 |
| atr_at_most_4pct | 20 | 108 | 0 |
| close_location_at_least_50pct | 47 | 81 | 0 |

## Decision

Do not relax the SMH veto or the quality pair to manufacture trades. Continue the frozen forward comparison; zero trades provide no win-rate evidence and no order authorization.
