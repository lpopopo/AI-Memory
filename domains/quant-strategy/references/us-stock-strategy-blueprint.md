# US Stock Strategy Blueprint

This document defines the initial strategy direction for 量外策略 with US equities as the primary target market.

## Scope

Primary market:

- US-listed equities and ETFs.

Initial universe:

- Start with large and liquid names.
- Prefer S&P 500, Nasdaq 100, and highly liquid sector ETFs for the first version.
- Exclude penny stocks, illiquid microcaps, leveraged ETFs, and instruments with unstable data.

Working definition of 量外策略:

- A systematic strategy that starts from price-volume behavior, then adds external confirmation such as fundamentals, events, macro regime, institutional behavior, or news/sentiment only after the baseline is validated.

## Strategy Objective

Build a medium-frequency strategy that can identify stronger US stocks during favorable market regimes while controlling drawdown during weak regimes.

Primary goal:

- Outperform SPY or QQQ on risk-adjusted return.

Secondary goals:

- Keep drawdown controlled.
- Avoid excessive turnover.
- Keep rules explainable enough for manual review.

## Time Horizon

Default holding period:

- 5 to 30 trading days.

Signal frequency:

- Daily scan after market close.

Execution assumption:

- Next trading day open or volume-weighted execution model during backtest.

## Core Signal Stack

### 1. Market Regime Filter

Only allow long positions when the broad market is healthy.

Candidate rules:

- SPY close above 200-day moving average.
- QQQ close above 100-day moving average for growth-heavy exposure.
- VIX or volatility proxy below a defined risk threshold.

If regime is negative:

- Reduce position count.
- Raise cash.
- Disable new long entries except defensive ETF tests.

### 2. Trend Filter

Require stock-level trend confirmation.

Candidate rules:

- Close above 50-day and 200-day moving averages.
- 20-day moving average above 50-day moving average.
- Recent price near 3-month or 6-month highs.

### 3. Relative Strength

Prefer stocks outperforming the market.

Candidate rules:

- 3-month return greater than SPY return.
- 6-month return ranks in the top 20% of the universe.
- Avoid stocks with strong absolute return but weak benchmark-relative return.

### 4. Volume and Liquidity

Avoid signals that cannot be executed cleanly.

Candidate rules:

- Average dollar volume above a fixed threshold.
- Breakout day volume above 20-day average volume.
- Exclude stocks with abnormal single-day volume caused by splits or bad data.

### 5. Risk Filter

Block entries with poor risk/reward.

Candidate rules:

- ATR-based stop distance must be within allowed range.
- Avoid stocks with earnings date too close for the first version.
- Avoid gap-up entries if price is too extended from moving averages.

## Entry Rule V0

A candidate enters the buy list when all are true:

1. Market regime is positive.
2. Stock close is above 50-day and 200-day moving averages.
3. 3-month or 6-month relative strength ranks in the top 20% of the universe.
4. Average dollar volume passes the liquidity threshold.
5. Price is not excessively extended from the 20-day moving average.

Rank candidates by:

1. Relative strength rank.
2. Trend quality.
3. Liquidity.
4. Lower volatility among otherwise similar candidates.

## Exit Rule V0

Exit when any are true:

- Close falls below 50-day moving average.
- Relative strength rank drops below the allowed threshold.
- ATR stop is hit.
- Market regime turns negative.
- Maximum holding period is reached and momentum has faded.

## Portfolio Construction

Default version (V5 Architecture):

- Long-only, highly concentrated.
- Dual-sleeve portfolio: Value/Cash defensive sleeve vs Hot-industry momentum sleeve.
- Target active holdings: 4 to 6 stocks (Hard max 8).
- Target themes: 2 to 3 themes (Hard max 55% broad theme concentration).
- Core positions: 8% to 15% (Max 20% for high conviction).
- Satellite/Speculative positions: 3% to 6% (Max price $300 for satellite).
- Speed Limit: Max 15% new portfolio exposure per day (8% in elevated regime).

Risk controls:

- Use cash when not enough qualified candidates exist.
- Do not force full investment.
- Rebalance weekly or when exit signals trigger.
- Track sector and factor exposure across both sleeves so the portfolio does not accidentally become one concentrated bet.

See `dual-sleeve-portfolio-strategy.md` for the detailed 50/50 design.

## Backtest Metrics

Required metrics:

- CAGR
- Max drawdown
- Sharpe ratio
- Sortino ratio
- Win rate
- Average win/loss
- Turnover
- Exposure percentage
- Benchmark-relative return versus SPY and QQQ

Required checks:

- Include transaction costs and slippage.
- Avoid look-ahead bias.
- Avoid using same-day close signal with same-day close execution.
- Test across bull, bear, and sideways regimes.

## Development Phases

### Phase 1: Baseline

Build daily OHLCV pipeline, universe, indicators, and V0 backtest.

### Phase 2: Robustness

Add transaction costs, sector caps, benchmark comparison, and parameter sensitivity tests.

### Phase 3: External Signals

Add fundamentals, earnings calendar, macro regime, options activity, or news/sentiment only if they improve out-of-sample behavior.

### Phase 4: Monitoring

Build daily scan output with candidate list, current holdings, exit warnings, and risk status.

## Open Questions

- Should the first benchmark be SPY, QQQ, or both?
- Should the initial universe be S&P 500, Nasdaq 100, or the top N by dollar volume?
- Should strategy be long-only first, or allow hedging with ETFs?
- What maximum drawdown is acceptable?
- What account size and transaction-cost assumptions should backtest use?
