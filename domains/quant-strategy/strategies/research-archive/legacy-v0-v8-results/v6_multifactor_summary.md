# V6 Multi-Factor Strategy Backtest Summary

This version upgrades the selection engine from Raw Momentum to an Aggressive Multi-Factor Model using cross-sectional Z-Score standardization.

## Factor Weighting (Aggressive)

- **+40% Quality Momentum**: `mom126 / vol126` (Rewards high returns with low volatility)
- **+40% Raw Momentum**: `mom63` (Rewards recent strong uptrends)
- **-20% Short-Term Reversal**: `mom21` (Penalizes stocks that spiked too fast in the last month to avoid mean reversion)

## Configuration

- Strategy Name: `dual_sleeve_v6_multifactor_aggressive`
- Risk Management: `30% Trailing Stop-Loss + Bear Market Value Trend Filter`

## Full-Period (26-Year) Comparison (2000-2025)

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V6 Multi-Factor | 35.081 | 14.67% | -35.14% | 18.71% | 0.83 | 1.07 |
| SPY | 7.499 | 8.06% | -55.19% | 19.39% | 0.50 | 0.63 |
| QQQ | 7.740 | 8.19% | -82.96% | 26.89% | 0.43 | 0.56 |
| 50/50 SPY/QQQ | 8.145 | 8.40% | -68.87% | 22.31% | 0.47 | 0.62 |

## Historic Split Periods Performance

| Period | Strategy | Final Value | CAGR | Max DD | Sharpe |
| --- | --- | ---: | ---: | ---: | ---: |
| full_26yr | Dual Sleeve V6 Multi-Factor | 35.081 | 14.67% | -35.14% | 0.83 |
| full_26yr | SPY | 7.499 | 8.06% | -55.19% | 0.50 |
| full_26yr | QQQ | 7.740 | 8.19% | -82.96% | 0.43 |
| full_26yr | 50/50 SPY/QQQ | 8.145 | 8.40% | -68.87% | 0.47 |
| dotcom_crash_2000_2002 | Dual Sleeve V6 Multi-Factor | 0.789 | -7.62% | -23.87% | -0.68 |
| dotcom_crash_2000_2002 | SPY | 0.631 | -14.27% | -47.52% | -0.52 |
| dotcom_crash_2000_2002 | QQQ | 0.257 | -36.48% | -82.96% | -0.62 |
| dotcom_crash_2000_2002 | 50/50 SPY/QQQ | 0.421 | -25.10% | -68.87% | -0.61 |
| bull_market_2003_2007 | Dual Sleeve V6 Multi-Factor | 2.757 | 22.51% | -16.77% | 1.19 |
| bull_market_2003_2007 | SPY | 1.755 | 11.93% | -13.73% | 0.93 |
| bull_market_2003_2007 | QQQ | 2.056 | 15.53% | -17.27% | 0.89 |
| bull_market_2003_2007 | 50/50 SPY/QQQ | 1.911 | 13.84% | -12.89% | 0.94 |
| financial_crisis_2008 | Dual Sleeve V6 Multi-Factor | 0.800 | -20.10% | -22.05% | -1.36 |
| financial_crisis_2008 | SPY | 0.638 | -36.34% | -47.12% | -0.88 |
| financial_crisis_2008 | QQQ | 0.592 | -40.90% | -49.40% | -1.11 |
| financial_crisis_2008 | 50/50 SPY/QQQ | 0.616 | -38.46% | -48.10% | -1.01 |
| bull_market_2009_2019 | Dual Sleeve V6 Multi-Factor | 5.017 | 15.80% | -24.37% | 0.90 |
| bull_market_2009_2019 | SPY | 4.327 | 14.25% | -27.13% | 0.91 |
| bull_market_2009_2019 | QQQ | 7.650 | 20.33% | -22.80% | 1.11 |
| bull_market_2009_2019 | 50/50 SPY/QQQ | 5.792 | 17.33% | -22.60% | 1.04 |
| covid_crash_2020 | Dual Sleeve V6 Multi-Factor | 1.221 | 22.20% | -35.14% | 0.80 |
| covid_crash_2020 | SPY | 1.172 | 17.30% | -33.72% | 0.64 |
| covid_crash_2020 | QQQ | 1.460 | 46.16% | -28.56% | 1.24 |
| covid_crash_2020 | 50/50 SPY/QQQ | 1.311 | 31.20% | -30.86% | 0.97 |
| bull_market_2021 | Dual Sleeve V6 Multi-Factor | 1.473 | 47.93% | -11.13% | 1.86 |
| bull_market_2021 | SPY | 1.305 | 30.92% | -5.11% | 2.13 |
| bull_market_2021 | QQQ | 1.292 | 29.64% | -10.85% | 1.51 |
| bull_market_2021 | 50/50 SPY/QQQ | 1.300 | 30.42% | -6.89% | 1.82 |
| inflation_bear_2022 | Dual Sleeve V6 Multi-Factor | 0.865 | -13.61% | -17.10% | -0.84 |
| inflation_bear_2022 | SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| inflation_bear_2022 | QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| inflation_bear_2022 | 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |
| bull_market_2023_2025 | Dual Sleeve V6 Multi-Factor | 2.508 | 36.00% | -26.28% | 1.52 |
| bull_market_2023_2025 | SPY | 1.877 | 23.44% | -18.76% | 1.45 |
| bull_market_2023_2025 | QQQ | 2.384 | 33.73% | -22.77% | 1.56 |
| bull_market_2023_2025 | 50/50 SPY/QQQ | 2.120 | 28.56% | -20.78% | 1.53 |
