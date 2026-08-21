# Economic edge decomposition preregistration

Status: frozen on 2026-08-21 before producing the decomposition. Research-only;
no formal/live rule or order authorization.

## Question

Determine whether the historical RSR advantage comes mainly from avoiding
losses, retaining winners, path-dependent replacement trades, or a very small
number of outliers. The analysis must disclose both avoided losses and missed
winners. It cannot propose or test another entry threshold.

## Frozen sample and mechanics

- Data boundary: 2024-01-02 through the completed 2026-08-18 session.
- Universe: frozen 32-name `ai_capex_broad` universe.
- Initial NAV USD 6,000; whole shares; USD 1 commission; 10 bps slippage.
- Matched baseline: same RS20, volume, extension, hold, stop, ranking, sizing and
  market gates as RSR1, without the 4% ATR / 50% close-location pair.
- RSR1: frozen 4% ATR / 50% close-location pair.
- RSR2: RSR1 plus the frozen +15% close-confirmed / +5% next-session profit
  lock.
- Historical period endpoints use the existing convention. The integrity audit
  already established that no current-list trade is a terminal liquidation.

## Frozen attribution

Trade identity is `(symbol, signal_date)`. Report:

1. Common baseline/RSR1 trades, baseline-only trades and RSR1-only replacement
   trades.
2. Among baseline-only trades, separate direct quality-filter exclusions from
   portfolio-path displacement using signal-day ATR and close location.
3. For direct exclusions, report avoided losing trades and dollars, missed
   winning trades and dollars, net P&L removed, win rate and mean return.
4. For RSR1 and RSR2, report gross profit, gross loss, net P&L and the shares of
   gross profit/net P&L contributed by the largest one, two and three winners.
5. Report leave-top-1/2/3 net P&L without rescaling the portfolio or claiming a
   counterfactual return path.
6. Pair common RSR1/RSR2 trades and report per-trade P&L deltas, improved,
   worsened and unchanged counts, and the share of aggregate overlay improvement
   attributable to the largest one and two positive deltas.

## Interpretation rules

- `avoided loss` is not profit earned; it is a historical path attribution.
- `missed winner` is the explicit opportunity cost of the quality filter.
- Replacement trades are path-dependent and cannot be attributed solely to the
  filter.
- Leave-out P&L is a concentration diagnostic, not a tradable portfolio return.
- No result may reopen high-volatility, change 4%/50%, promote RSR1/RSR2, or
  authorize a trade. Only genuine forward observations may resolve the existing
  evidence conflict.
