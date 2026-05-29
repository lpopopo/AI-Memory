# V4.1 Full-Universe Stock Scanner Strategy Backtest Summary

V4.1 upgrades the Tactical Growth Sleeve to dynamically scan the entire constituent list of both the S&P 500 and Nasdaq 100 indexes (~500 stocks) rather than relying on a static pool of pre-defined sector leaders.

## Strategy Mechanics

- **Growth Sleeve (70% Bull / 60% Normal / 30% Bear)**:
  - Filters active constituents at each monthly rebalance.
  - Trend filter: price must be above both its 50-day and 200-day moving averages (`close > ma50` and `close > ma200`).
  - Momentum filter: positive 3-month momentum (`mom63 > 0`).
  - Selection: ranks eligible stocks by momentum score (`mom63 + mom126`) and picks the top 10 stocks.
  - Cash retreat overlay: each stock is allocated exactly 10% of the growth sleeve. If fewer than 10 stocks qualify, the remainder is kept in safe cash.
- **Value Sleeve (30% Bull / 40% Normal / 70% Bear)**:
  - Dynamic allocation into the top 2 Value ETFs (VTV/IWD/SCHD) to maintain a highly diversified defensive base.

## Configuration

- Strategy Name: `dual_sleeve_v4_1_universe`
- Target stocks: `Top 10 individual stocks from the S&P 500 & Nasdaq 100 constituents`
- Bull allocation: `30%` value / `70%` growth
- Normal allocation: `40%` value / `60%` growth
- Bear allocation: `70%` value / `30%` growth

## Full-Period (26-Year) Comparison (2000-2025)

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V4.1 Universe | 551.901 | 27.50% | -55.20% | 23.83% | 1.14 | 1.53 |
| SPY | 7.499 | 8.06% | -55.19% | 19.39% | 0.50 | 0.63 |
| QQQ | 7.740 | 8.19% | -82.96% | 26.89% | 0.43 | 0.56 |
| 50/50 SPY/QQQ | 8.145 | 8.40% | -68.87% | 22.31% | 0.47 | 0.62 |

## Historic Split Periods Performance

| Period | Strategy | Final Value | CAGR | Max DD | Sharpe |
| --- | --- | ---: | ---: | ---: | ---: |
| full_26yr | Dual Sleeve V4.1 Universe | 551.901 | 27.50% | -55.20% | 1.14 |
| full_26yr | SPY | 7.499 | 8.06% | -55.19% | 0.50 |
| full_26yr | QQQ | 7.740 | 8.19% | -82.96% | 0.43 |
| full_26yr | 50/50 SPY/QQQ | 8.145 | 8.40% | -68.87% | 0.47 |
| dotcom_crash_2000_2002 | Dual Sleeve V4.1 Universe | 0.761 | -8.74% | -36.99% | -0.36 |
| dotcom_crash_2000_2002 | SPY | 0.631 | -14.27% | -47.52% | -0.52 |
| dotcom_crash_2000_2002 | QQQ | 0.257 | -36.48% | -82.96% | -0.62 |
| dotcom_crash_2000_2002 | 50/50 SPY/QQQ | 0.421 | -25.10% | -68.87% | -0.61 |
| bull_market_2003_2007 | Dual Sleeve V4.1 Universe | 9.723 | 57.69% | -15.92% | 2.21 |
| bull_market_2003_2007 | SPY | 1.755 | 11.93% | -13.73% | 0.93 |
| bull_market_2003_2007 | QQQ | 2.056 | 15.53% | -17.27% | 0.89 |
| bull_market_2003_2007 | 50/50 SPY/QQQ | 1.911 | 13.84% | -12.89% | 0.94 |
| financial_crisis_2008 | Dual Sleeve V4.1 Universe | 0.636 | -36.48% | -47.34% | -0.90 |
| financial_crisis_2008 | SPY | 0.638 | -36.34% | -47.12% | -0.88 |
| financial_crisis_2008 | QQQ | 0.592 | -40.90% | -49.40% | -1.11 |
| financial_crisis_2008 | 50/50 SPY/QQQ | 0.616 | -38.46% | -48.10% | -1.01 |
| bull_market_2009_2019 | Dual Sleeve V4.1 Universe | 10.887 | 24.26% | -28.78% | 1.10 |
| bull_market_2009_2019 | SPY | 4.327 | 14.25% | -27.13% | 0.91 |
| bull_market_2009_2019 | QQQ | 7.650 | 20.33% | -22.80% | 1.11 |
| bull_market_2009_2019 | 50/50 SPY/QQQ | 5.792 | 17.33% | -22.60% | 1.04 |
| covid_crash_2020 | Dual Sleeve V4.1 Universe | 1.764 | 76.70% | -29.93% | 1.81 |
| covid_crash_2020 | SPY | 1.172 | 17.30% | -33.72% | 0.64 |
| covid_crash_2020 | QQQ | 1.460 | 46.16% | -28.56% | 1.24 |
| covid_crash_2020 | 50/50 SPY/QQQ | 1.311 | 31.20% | -30.86% | 0.97 |
| bull_market_2021 | Dual Sleeve V4.1 Universe | 1.418 | 42.34% | -13.44% | 1.55 |
| bull_market_2021 | SPY | 1.305 | 30.92% | -5.11% | 2.13 |
| bull_market_2021 | QQQ | 1.292 | 29.64% | -10.85% | 1.51 |
| bull_market_2021 | 50/50 SPY/QQQ | 1.300 | 30.42% | -6.89% | 1.82 |
| inflation_bear_2022 | Dual Sleeve V4.1 Universe | 0.972 | -2.85% | -20.20% | -0.01 |
| inflation_bear_2022 | SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| inflation_bear_2022 | QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| inflation_bear_2022 | 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |
| bull_market_2023_2025 | Dual Sleeve V4.1 Universe | 4.185 | 61.42% | -28.78% | 2.07 |
| bull_market_2023_2025 | SPY | 1.877 | 23.44% | -18.76% | 1.45 |
| bull_market_2023_2025 | QQQ | 2.384 | 33.73% | -22.77% | 1.56 |
| bull_market_2023_2025 | 50/50 SPY/QQQ | 2.120 | 28.56% | -20.78% | 1.53 |
