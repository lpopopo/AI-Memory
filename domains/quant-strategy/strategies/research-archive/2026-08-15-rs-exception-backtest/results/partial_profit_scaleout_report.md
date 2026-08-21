# RSR2 whole-share partial-profit audit

## Decision

- Result: `retain_RSR2_without_partial_exit`.
- Advancement status: `insufficient`.
- One closed trade remains one trade after partial and final exits; partial sales cannot inflate hit rate.
- Research only. No formal rule, order or existing forward ledger is changed.

## Advancement screen

| Check | Result |
| --- | --- |
| sufficient_partial_exits | False |
| return_improves_10bps | False |
| sharpe_nonworse | True |
| drawdown_within_1pp | True |
| win_rate_nonworse | False |
| return_improves_20bps | False |
| profit_diversified | True |
| minimum return delta at 10 bps | -2.85% |
| minimum return delta at 20 bps | -1.65% |

## Ten-basis-point results

| NAV | Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Partial exits | Ineligible | Top profit share |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $6,000.00 | development_2024_2025 | RSR2 | 17.18% | -1.91% | 2.13 | 70.00% | 20 | 0 | 0 | 27.84% |
| $6,000.00 | development_2024_2025 | partial_half_at_15 | 14.33% | -1.84% | 2.16 | 66.67% | 21 | 9 | 1 | 22.86% |
| $6,000.00 | heldout_2026 | RSR2 | 0.82% | -1.69% | 0.42 | 66.67% | 3 | 0 | 0 | 82.71% |
| $6,000.00 | heldout_2026 | partial_half_at_15 | 1.10% | -1.57% | 0.57 | 66.67% | 3 | 1 | 1 | 85.13% |
| $6,000.00 | full | RSR2 | 18.11% | -2.33% | 1.77 | 69.57% | 23 | 0 | 0 | 25.43% |
| $6,000.00 | full | partial_half_at_15 | 16.17% | -1.84% | 1.90 | 66.67% | 24 | 11 | 1 | 19.72% |
| $5,751.77 | development_2024_2025 | RSR2 | 16.15% | -1.94% | 2.09 | 70.00% | 20 | 0 | 0 | 24.54% |
| $5,751.77 | development_2024_2025 | partial_half_at_15 | 14.44% | -1.79% | 2.23 | 66.67% | 21 | 8 | 2 | 25.61% |
| $5,751.77 | heldout_2026 | RSR2 | 0.85% | -1.77% | 0.42 | 66.67% | 3 | 0 | 0 | 82.71% |
| $5,751.77 | heldout_2026 | partial_half_at_15 | 1.15% | -1.63% | 0.57 | 66.67% | 3 | 1 | 1 | 85.13% |
| $5,751.77 | full | RSR2 | 17.01% | -2.31% | 1.75 | 69.57% | 23 | 0 | 0 | 22.36% |
| $5,751.77 | full | partial_half_at_15 | 15.59% | -1.79% | 1.85 | 66.67% | 24 | 9 | 3 | 22.86% |

## Full-period P&L attribution at USD 6,000 / 10 bps

| Symbol | Signal | Path | Baseline P&L | Partial P&L | Delta |
| --- | --- | --- | ---: | ---: | ---: |
| MU | 2025-09-05 | common | $253.98 | $170.35 | $-83.63 |
| NOK | 2025-10-10 | common | $166.25 | $123.81 | $-42.45 |
| WDC | 2025-02-18 | candidate_only | $0.00 | $-41.31 | $-41.31 |
| LITE | 2024-11-06 | common | $118.86 | $95.86 | $-23.00 |
| GLW | 2025-08-28 | common | $79.70 | $73.22 | $-6.48 |
| MU | 2025-06-03 | common | $72.57 | $68.20 | $-4.38 |

- Common-trade P&L delta: `$-74.70`.
- Candidate-only P&L delta: `$-41.31`.
- The largest losses come from trimming persistent right-tail winners; released capacity also admitted an additional losing trade.

## Interpretation boundary

- The comparison uses the hindsight-selected current watchlist and previously observed periods. It can reject an operationally weak mechanism but cannot prove a live edge.
- Whole-share feasibility and the extra commission are part of the mechanism, not implementation noise to remove after seeing the result.
- See `../partial-profit-scaleout-preregistration.md` for the frozen design.
