# Dual-Sleeve Portfolio Strategy

This document defines the improved 50/50 US-stock strategy:

- 50% value-investing sleeve.
- 50% hot-industry momentum sleeve.

The goal is to combine a stable valuation-quality base with a tactical sleeve that can participate in strong market themes without turning the portfolio into unmanaged chasing.

## Core Allocation

Default allocation:

| Sleeve | Target Weight | Role |
| --- | ---: | --- |
| Value Sleeve | 50% | Long-term compounding, valuation discipline, quality filter |
| Industry Momentum Sleeve | 50% | Capture strong sector/theme trends |

Rebalance rule:

- Review sleeve weights monthly.
- Rebalance when either sleeve drifts more than 5 percentage points from target.
- Allow tactical sleeve to hold cash if no industry passes the trend filter.

## Sleeve 1: Value Investing

### Objective

Hold durable US companies at reasonable prices, with enough quality and financial strength to survive market stress.

### Universe

Initial candidates:

- S&P 500 constituents.
- Large and liquid US-listed companies.
- Optional later extension: top US stocks by dollar volume.

Avoid:

- Unprofitable speculative companies.
- Companies with unstable financial reporting.
- Very high debt without strong cash flow.
- Stocks with poor liquidity.

### Selection Factors

Use a multi-factor value-quality score:

1. Valuation
   - Low forward or trailing P/E relative to sector.
   - Low EV/EBITDA relative to sector.
   - Reasonable price/free-cash-flow.
2. Quality
   - Positive free cash flow.
   - Stable or improving margins.
   - Return on invested capital or return on equity above sector median.
3. Balance sheet
   - Debt levels manageable relative to earnings or cash flow.
   - Interest coverage not deteriorating.
4. Shareholder return
   - Buybacks, dividends, or consistent reinvestment at attractive returns.
5. Downside protection
   - Lower drawdown than peers.
   - Earnings stability through cycles.

### Entry Rule

Enter or add when:

1. Company passes quality and balance-sheet filters.
2. Valuation is attractive versus sector peers or its own history.
3. Price trend is not in severe breakdown.
4. No major known event risk blocks entry.

### Exit Rule

Exit or reduce when:

- Valuation becomes excessive versus fundamentals.
- Quality thesis breaks.
- Debt or cash-flow profile deteriorates.
- Price falls below a long-term risk threshold and fundamentals do not justify holding.
- A better value candidate replaces it in ranking.

### Position Rules

- 8 to 15 holdings.
- Position size: 3% to 8% of total portfolio.
- Maximum sector exposure inside value sleeve: 30% of value sleeve unless explicitly approved.
- Review monthly; deep review quarterly after earnings.

## Sleeve 2: Hot-Industry Momentum

### Objective

Capture leading industries that are receiving market attention, capital inflow, earnings acceleration, or policy/technology tailwinds.

### Industry Definition

Use a standard classification system for baseline sector and industry grouping.

Preferred classification:

- GICS sectors, industry groups, industries, and sub-industries.

Implementation proxy:

- Sector ETFs and industry ETFs for first scan.
- Individual stocks only after industry strength is confirmed.

### Industry Scoring

Rank industries using a composite momentum score:

1. Price strength
   - 1-month, 3-month, and 6-month relative return versus SPY and QQQ.
2. Breadth
   - Percentage of stocks in the industry above 50-day and 200-day moving averages.
3. Volume confirmation
   - Industry ETF or leading stocks show rising dollar volume.
4. Earnings or revenue acceleration
   - Optional after data source is stable.
5. News or narrative intensity
   - Optional later input; never enough by itself.

### Industry Entry Rule

An industry becomes eligible when:

1. Its ETF or representative basket outperforms SPY over 1-month and 3-month windows.
2. Industry breadth is positive.
3. The broad market regime is not strongly negative.
4. At least three representative stocks confirm the trend.

### Stock Selection Within Hot Industries

Choose stocks that combine industry strength with individual confirmation:

- Top relative strength inside the industry.
- Strong liquidity.
- Price above 50-day moving average.
- Positive earnings or revenue trend when available.
- Avoid names that are too extended from moving averages.

### Exit Rule

Exit or reduce when:

- Industry relative strength falls below threshold.
- Breadth deteriorates.
- Price breaks below 50-day moving average.
- Market regime turns negative.
- Position hits ATR stop or maximum drawdown rule.

### Position Rules

- 2 to 4 industries active at one time.
- 2 to 5 holdings per active industry, or use ETFs when stock-level conviction is low.
- Maximum one industry exposure: 20% of total portfolio.
- Maximum single tactical position: 5% of total portfolio.
- Review weekly; rebalance monthly or on exit signal.

## Portfolio-Level Risk Controls

### Market Regime

If SPY is below its 200-day moving average:

- Freeze new hot-industry entries.
- Reduce tactical sleeve exposure.
- Value sleeve can remain invested only in high-quality holdings.

If both SPY and QQQ are below long-term trend:

- Tactical sleeve may move partly or fully to cash.
- New value entries require stronger margin of safety.

### Drawdown Controls

Suggested initial limits:

- Portfolio-level soft drawdown alert: -8%.
- Portfolio-level risk reduction trigger: -12%.
- Single-position review trigger: -10% from entry or ATR-based stop.

These are starting points for backtesting, not final rules.

### Correlation Control

The two sleeves must not accidentally become the same bet.

Examples:

- If value sleeve is already heavy in mega-cap technology, tactical sleeve should not add excessive AI/semiconductor concentration without an explicit risk override.
- Track sector and factor exposure across the full portfolio, not only inside each sleeve.

## Rebalancing

Default cadence:

- Weekly scan for tactical exits.
- Monthly rebalance for sleeve weights.
- Quarterly fundamental review for value holdings.

Drift bands:

- Target sleeve weight: 50% / 50%.
- Rebalance if a sleeve moves below 45% or above 55%.

## Backtest Requirements

Backtest both sleeves separately and together.

Required views:

1. Value sleeve only.
2. Hot-industry sleeve only.
3. Combined 50/50 portfolio.
4. SPY benchmark.
5. QQQ benchmark.
6. 50/50 SPY/QQQ benchmark.

Required metrics:

- CAGR.
- Max drawdown.
- Sharpe ratio.
- Sortino ratio.
- Volatility.
- Turnover.
- Win rate.
- Average win/loss.
- Sector concentration.
- Monthly return distribution.

## Why This Improves The Original Strategy

The 50/50 split gives the portfolio two engines:

- Value sleeve reduces the risk of chasing expensive themes at the wrong time.
- Hot-industry sleeve allows participation when the market rewards a specific sector or narrative.

The key improvement is not the 50/50 number by itself. The improvement is making each half follow different rules, different review cycles, and different exit logic.

## Open Parameters To Decide

- Whether value sleeve should use only individual stocks or allow value ETFs.
- Whether tactical sleeve should begin with ETFs before individual stocks.
- Exact valuation metrics and data source.
- Exact industry classification and ETF mapping.
- Maximum acceptable portfolio drawdown.
- Whether cash is allowed when no tactical industry qualifies.
