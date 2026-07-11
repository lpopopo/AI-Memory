# V7 Full Hybrid Strategy Backtest Summary (20-Year)

This version integrates the V6 Multi-Factor core, the Double-Radar Satellite module (annualized vol), the Market Fear Gate, and 30% Trailing Stop-Loss.

## Configuration
- Core: V6 Aggressive Multi-Factor (75% base)
- Satellite: Double-Radar Top 5 (25% base)
- Risk: Market Fear Gate scaling (20%/50%/75%/100%)
- Stop-Loss: 30% Trailing Stop on individual stocks

## Performance Comparison

| Split | Strategy | Final Value | CAGR | Max DD | Sharpe |
| --- | --- | ---: | ---: | ---: | ---: |
| full_20yr | V7 Hybrid | 26.213 | 17.37% | -31.05% | 0.89 |
| full_20yr | SPY | 7.140 | 10.12% | -55.19% | 0.60 |
| full_20yr | QQQ | 15.345 | 14.33% | -53.40% | 0.72 |
| full_20yr | 50/50 SPY/QQQ | 10.666 | 12.31% | -53.66% | 0.68 |
| dotcom_recovery | V7 Hybrid | 1.319 | 10.66% | -18.93% | 0.65 |
| dotcom_recovery | SPY | 1.332 | 11.05% | -9.05% | 0.97 |
| dotcom_recovery | QQQ | 1.313 | 10.47% | -17.27% | 0.75 |
| dotcom_recovery | 50/50 SPY/QQQ | 1.325 | 10.84% | -10.79% | 0.88 |
| financial_crisis | V7 Hybrid | 0.986 | -0.91% | -16.15% | 0.02 |
| financial_crisis | SPY | 0.534 | -34.19% | -55.19% | -0.90 |
| financial_crisis | QQQ | 0.587 | -29.95% | -53.40% | -0.76 |
| financial_crisis | 50/50 SPY/QQQ | 0.562 | -31.92% | -53.66% | -0.85 |
| post_crisis_bull | V7 Hybrid | 5.495 | 17.18% | -31.05% | 0.89 |
| post_crisis_bull | SPY | 4.927 | 15.99% | -19.35% | 1.06 |
| post_crisis_bull | QQQ | 7.702 | 20.92% | -22.80% | 1.18 |
| post_crisis_bull | 50/50 SPY/QQQ | 6.198 | 18.50% | -20.94% | 1.14 |
| covid_era | V7 Hybrid | 1.966 | 40.32% | -21.00% | 1.47 |
| covid_era | SPY | 1.509 | 22.90% | -33.72% | 0.94 |
| covid_era | QQQ | 1.860 | 36.47% | -28.56% | 1.24 |
| covid_era | 50/50 SPY/QQQ | 1.681 | 29.71% | -30.86% | 1.12 |
| inflation_bear | V7 Hybrid | 0.858 | -14.33% | -15.52% | -1.30 |
| inflation_bear | SPY | 0.814 | -18.84% | -24.50% | -0.74 |
| inflation_bear | QQQ | 0.668 | -33.54% | -34.83% | -1.10 |
| inflation_bear | 50/50 SPY/QQQ | 0.738 | -26.45% | -29.63% | -0.95 |
| ai_bull | V7 Hybrid | 2.115 | 36.66% | -27.04% | 1.42 |
| ai_bull | SPY | 1.592 | 21.38% | -18.76% | 1.28 |
| ai_bull | QQQ | 1.990 | 33.24% | -22.77% | 1.47 |
| ai_bull | 50/50 SPY/QQQ | 1.783 | 27.27% | -20.78% | 1.40 |
