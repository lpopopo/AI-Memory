# V5, V6, and V7 Performance Comparison (20-Year Backtest)

This report compares the V5, V6, and V7 versions of the quant strategy over a 20-year backtest window from **2006-01-01** to **2025-12-30** (exactly 5030 trading days).

## Performance Table (2006-2025)

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| V5 Universe Optimal | 40.964 | 20.41% | -33.14% | 21.45% | 0.98 | 1.29 |
| V6 Multi-Factor | 19.148 | 15.92% | -35.14% | 19.72% | 0.85 | 1.10 |
| V7 Full Hybrid | 35.648 | 19.58% | -31.05% | 20.78% | 0.97 | 1.22 |
| SPY | 7.855 | 10.86% | -55.19% | 19.39% | 0.63 | 0.77 |
| QQQ | 17.519 | 15.40% | -53.40% | 21.97% | 0.76 | 0.99 |
| 50/50 SPY/QQQ | 11.948 | 13.21% | -53.66% | 20.27% | 0.71 | 0.90 |

## Core Strategy Split Breakdown

- **V5 Universe Optimal**: Baseline dynamic ETF-Stock allocation with a 30% individual stock trailing stop-loss.
- **V6 Multi-Factor**: Replaces the V5 single-indicator momentum score with a multi-factor ranking score (+40% Quality Mom, +40% Raw Mom, -20% Short-term Reversal).
- **V7 Full Hybrid**: Combines the V6 multi-factor selection with a Double-Radar satellite sleeve (25% weight) and dynamic Market Fear Gate exposure scaling.

## Key Observations

1. **CAGR Outperformance**: The **V5** version achieved the highest return over the 20-year period with a CAGR of **20.41%**.
2. **Drawdown Protection**: The **V7** version showed the most resilient risk profile, limiting the maximum drawdown to **-31.05%**.
3. **Benchmark Comparison**: All three versions significantly outperformed the SPY (CAGR: 10.86%) and QQQ (CAGR: 15.40%) on both absolute and risk-adjusted metrics.
