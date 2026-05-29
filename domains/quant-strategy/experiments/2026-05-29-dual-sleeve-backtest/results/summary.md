# Backtest Summary

Period: 2016-05-31 to 2026-05-28

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dual_sleeve_v0 | 2.463 | 9.44% | -24.48% | 13.45% | 0.74 | 0.92 | 55.53% |
| SPY | 4.233 | 15.54% | -33.72% | 17.94% | 0.90 | 1.08 | 55.45% |
| QQQ | 7.156 | 21.77% | -35.12% | 22.30% | 1.00 | 1.27 | 56.89% |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 19.79% | 0.97 | 1.20 | 56.45% |

## V0 Interpretation Notes

- Value sleeve is proxied by equal-weight `VTV`, `IWD`, and `SCHD`.
- Hot-industry sleeve rotates monthly into the top 3 eligible ETFs.
- Tactical sleeve moves to cash when SPY is below its 200-day moving average.
- Cash earns 0% in this version.
- Prices use yfinance auto-adjusted daily close data.
- This validates the allocation structure, not the final individual-stock strategy.

## Initial Read

- V0 did not outperform SPY, QQQ, or 50/50 SPY/QQQ over this period.
- V0 reduced drawdown versus SPY and QQQ, but the reduction was not enough to compensate for the lower CAGR and Sharpe ratio.
- The market-regime filter likely left the tactical sleeve in cash during early periods and some rebounds.
- ETF proxy value exposure may be too conservative compared with a real stock-selection value sleeve.
- Next validation should test a more selective value sleeve and a tactical sleeve that ranks industries against both SPY and QQQ with clearer cash-deployment rules.
