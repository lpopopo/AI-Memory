# RSR2 conditional winner-extension registration

Frozen before reading the conditional-extension outputs on 2026-08-15. Research-only; RSR1 and RSR2 remain unchanged.

## Motivation and bias boundary

The existing exit grid already showed that a fixed 30-session hold helped the 2026 replay but reduced 2024–2025 RSR return versus the frozen 20-session hold. This study therefore tests a pre-specified conditional extension rather than another unconditional holding-period search. The hypothesis is post-hoc and cannot be promoted without genuine forward evidence.

## Shared contract

- Use the frozen 32-name `ai_capex_broad` RSR risk-filter signal and strict SMH veto.
- Retain RSR2's +15% completed-close trigger and +5% following-session profit stop.
- Base hold remains 20 sessions.
- An extension is active only when the position has reached the base time limit, completed close is at or above the required gain from entry, close remains at or above MA20, and RS20 versus SMH is non-negative.
- A close below MA20, negative RS20 or an intraday stop still exits under the existing rules.
- Costs, next-open execution, whole shares, 8% target, caps and fee floor remain unchanged.

## Fixed variants

| Variant | Maximum hold | Required gain at/after day 20 |
| --- | ---: | ---: |
| `rsr2_frozen` | 20 | n/a |
| `extend30_any_winner` | 30 | >=0% |
| `extend30_gain8` | 30 | >=8% |
| `extend40_gain8` | 40 | >=8% |

`extend30_gain8` is central because +8% was already identified as a common winner threshold before this study. The neighboring variants test threshold and horizon dependence.

## Promotion screen

For a challenger to survive, versus frozen RSR2 it must have non-worse return, maximum drawdown, Sharpe and win rate in both 2024–2025 and 2026, remain non-worse on full-period return at 20 bps per side, and not increase maximum gross-profit symbol concentration above 35%. At least two of the three extension variants must improve return in both periods. Passing remains research-only and requires a separately frozen forward ledger.
