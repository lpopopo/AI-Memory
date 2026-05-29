# 2026-05-29 Market Fear Data and Strategy Validation

Purpose: Validate whether the market fear framework data is correct, then test the integrated V5 plus market fear gate strategy on 2026 YTD data.

## Data Validation

Report: `experiments/2026-05-29-dual-sleeve-backtest/results/market_fear_data_validation.md`

Validation result:

- Data range: 2025-01-02 to 2026-05-29.
- Returned columns: HYG, IWM, LQD, QQQ, RSP, SMH, SPY, TLT, ^VIX, ^VIX3M.
- Core columns passed: SPY, QQQ, SMH, ^VIX, ^VIX3M.
- Optional columns passed: IWM, RSP, HYG, LQD, TLT.
- Latest value sanity checks passed for SPY, QQQ, SMH, ^VIX, and ^VIX3M.
- Latest regime: `normal`.
- Latest score: `0`.
- No validation warnings.

Latest fear signals:

- VIX around 15.46: calm.
- VIX 5-day change around -7.43%: no spike.
- VIX/VIX3M around 0.82: normal term structure.
- SPY and QQQ are near 63-day highs with intact trend.
- SMH is near its 63-day high with intact trend.
- Breadth and credit proxies are stable.

Conclusion: the latest market fear data is internally consistent and suitable for strategy gating.

## 2026 Integrated Strategy Validation

Report: `experiments/2026-05-29-dual-sleeve-backtest/results/strategy_2026_ytd_fear_integrated_validation.md`

| Strategy | 2026 YTD Return | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: |
| V5 Original | 54.47% | -11.86% | 38.06% | 3.05 | 4.14 |
| V5 + Market Fear Gate | 40.93% | -8.55% | 31.68% | 2.86 | 4.23 |
| SPY | 11.22% | -8.88% | 13.48% | 2.04 | 3.11 |
| QQQ | 20.99% | -11.72% | 18.16% | 2.71 | 4.66 |
| 50/50 SPY/QQQ | 16.03% | -10.30% | 15.63% | 2.45 | 4.07 |

Fear-gated 2026 monthly behavior:

- 2026-01-30: `normal`, score 1, risk multiplier 100%, cash 5%.
- 2026-02-27: `elevated`, score 5, risk multiplier 70%, cash 30%.
- 2026-03-31: `panic`, score 14, risk multiplier 20%, cash 100%.
- 2026-04-30: `normal`, score 2, risk multiplier 100%, cash 5%.
- 2026-05-29: `normal`, score 0, risk multiplier 100%, cash 5%.

## Interpretation

The fear gate is working as a risk governor:

- It reduced return versus original V5 because it forced lower exposure in February and full cash in March.
- It materially improved max drawdown, from -11.86% to -8.55%.
- It reduced volatility, from 38.06% to 31.68%.
- It preserved strong outperformance versus SPY, QQQ, and 50/50 SPY/QQQ.
- Sortino improved slightly, which suggests downside risk was reduced more than upside participation.

Decision: keep the market fear gate in the daily strategy workflow. Treat it as a position-sizing and cash-floor layer, not as a stock selection factor.
