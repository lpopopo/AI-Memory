# Forward expectancy scorecard preregistration

Frozen on 2026-08-15 before the first eligible RSR1/RSR2 forward session.

## Purpose

The shared-capital audit demonstrated that a higher observed win rate can still
produce lower total profit when capacity removes a large winner. The forward
review therefore needs to separate hit rate from economic expectancy. This
scorecard is a read-only evidence diagnostic layered on the existing frozen
promotion gates; it does not change those gates or authorize a trade.

## Inputs and immutability

- RSR1: `results/forward_shadow_ledger.csv`.
- RSR2: `results/forward_profit_protection_ledger.csv`.
- Matched baseline: `results/forward_shadow_baseline_trades.csv` when it exists.
- Session/status metadata: `results/forward_shadow_status.json`.
- Opportunity context: `results/forward_opportunity_diagnostics_ledger.csv`.
- Only rows with a completed exit and finite net PnL/return enter trade metrics.
- Open and pending rows are reported but never imputed as wins or losses.
- The scorecard may overwrite only its derived JSON/CSV/Markdown outputs. It may
  not write, reorder or backfill any forward ledger.

## Frozen economic metrics

For matched baseline, RSR1 and RSR2 report:

1. Closed trades, wins, losses and observed win rate.
2. Wilson 95% interval for the win rate.
3. Average winner, average loser, payoff ratio and break-even win rate.
4. Mean net return per trade (expectancy) and edge above the break-even win rate.
5. Gross profit, gross loss, profit factor and cumulative net PnL.
6. Top-symbol share of gross profits, number of winning symbols and themes.
7. Worst trade and longest consecutive losing streak ordered by exit date.
8. Entry-date-cluster bootstrap of mean trade return: 10,000 samples, fixed seed
   `20260815`, percentile 5%/50%/95%, and probability that expectancy is zero or
   negative. Trades sharing an entry date remain in the same resampled cluster.

Cluster bootstrap is descriptive, not a proof of independence. With fewer than
five entry-date clusters the interval is reported but evidence is labelled too
small.

## Frozen evidence labels

- `awaiting_sample`: fewer than 20 closed trades.
- `observed_negative`: at least 20 trades and observed expectancy is not positive.
- `positive_but_fragile`: positive observed expectancy, but bootstrap 5th
  percentile is not above zero or profit factor is below 1.30.
- `positive_concentrated`: positive bootstrap lower bound and profit factor at
  least 1.30, but one symbol exceeds 35% of gross profits.
- `positive_diversified`: positive bootstrap lower bound, profit factor at least
  1.30 and no symbol exceeds 35% of gross profits.

These labels cannot promote or reject RSR1/RSR2 by themselves. The original
126-session, 20-trade, relative-performance, drawdown, Sharpe, cost and theme
gates remain decisive.

## Historical calibration

The same calculations may be shown for the frozen 2024 through latest-cached
current-watchlist backtests solely to verify implementation and demonstrate the
scale of sampling uncertainty. Those rows are explicitly retrospective,
survivorship-biased and never count toward forward evidence.

## Governance

Research-only. Formal V9, RSR1, RSR2, live holdings, orders and all append-only
forward ledgers remain unchanged.
