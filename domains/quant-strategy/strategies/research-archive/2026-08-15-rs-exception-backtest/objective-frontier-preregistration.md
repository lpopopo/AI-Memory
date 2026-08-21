# Multi-objective evidence frontier preregistration

## Purpose

This is a synthesis layer over already completed, preregistered experiments. It
does not search a new threshold, holding period, allocation or universe. Its
purpose is to keep four distinct questions visible at the same time:

1. historical total return;
2. trade or monthly win rate, when the source experiment defines one;
3. drawdown and risk-adjusted return;
4. the strength and transferability of the evidence.

The output is research-only. It cannot modify formal V9, the real account or
authorize an order.

## Frozen inputs

Only the following existing result files may be read:

- `profit_protection_metrics.csv`
- `partial_profit_scaleout_metrics.csv`
- `winner_extension_metrics.csv`
- `capital_constrained_ranking_metrics.csv`
- `shared_capital_architecture_metrics.csv`
- `high_vol_portfolio_metrics.csv`
- `core_allocation_frontier_metrics.csv`
- `combined_v9_portfolio_metrics.csv`

No strategy engine is rerun and no unregistered alternative is constructed.

## Comparability rule

Pareto dominance is evaluated only inside a `comparable_group`. A group fixes
the experiment family, time period, cost assumption and starting NAV where the
source experiment varies it. Periods and families are never pooled merely
because their columns have the same names.

The metrics are fixed by family:

| Family | Pareto metrics |
| --- | --- |
| Stock selection / exit | return, trade win rate, max drawdown, Sharpe, profit factor |
| Profit realization | return, trade win rate, max drawdown, Sharpe, profit factor |
| Winner extension | return, trade win rate, max drawdown, Sharpe, profit factor |
| Entry ranking | return, trade win rate, max drawdown, Sharpe, profit factor |
| Shared capital | return, monthly win rate, max drawdown, Sharpe |
| High-volatility sleeve | return, trade win rate, max drawdown, Sharpe, profit factor |
| Core-only allocation | return, monthly win rate, max drawdown, Sharpe |
| Combined 2026 architecture | return, max drawdown, Sharpe |

Higher is better for every stored metric, including max drawdown: a value of
`-0.02` is better than `-0.05`. Candidate A dominates B only if A is no worse
on every registered metric and strictly better on at least one. A single
candidate in a group is labeled descriptive rather than selected.

## Decision rule

Pareto membership is descriptive, not authorization. The synthesis decision
also applies the already documented cross-period and evidence results:

- RSR2 is the historical stock-sleeve leader but remains a frozen shadow.
- Whole-position RSR2 is retained over half-position scale-out because the
  latter gives up return and win rate for smoother drawdown.
- Conditional winner extension is rejected because its full-period return
  edge fails the development period.
- Formal entry ranking and formal 70/30 shared-capital architecture remain.
- The high-volatility sleeve remains rejected because development evidence is
  weak and inconsistent with 2026.
- Core-only 80% may sit on a local frontier but is superseded by the
  shared-capital replay.
- Residual-cash yield remains operationally conditional on broker, tax,
  settlement and liquidity facts.

The best historical candidate must therefore be reported separately from the
best deployable architecture. Genuine-forward zero-signal/zero-trade evidence
through the latest completed session cannot be converted into a zero effect or
used to promote RSR1/RSR2.

