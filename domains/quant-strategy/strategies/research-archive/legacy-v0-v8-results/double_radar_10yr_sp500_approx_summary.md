# Double-Radar Integration 10-Year S&P 500 Approx Backtest

Data window: 2016-01-04 to 2025-12-30.
Universe: current S&P 500 scraped symbols 503, cached price intersection 501 stocks, plus SPY/QQQ and value ETFs.
Important limitation: this uses current S&P 500 membership with cached adjusted closes, so it has survivorship bias and is not a true point-in-time S&P 500 constituent backtest.

## Performance

| Strategy | Final Value | CAGR | Period Return | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Combined 75% V5 + 25% Radar | 11.851 | 28.09% | 1085.08% | -30.70% | 21.92% | 1.24 | 1.62 |
| V5 S&P500 approx | 10.016 | 25.95% | 901.63% | -30.88% | 21.34% | 1.19 | 1.55 |
| Radar Top5 gated | 17.279 | 33.02% | 1627.88% | -35.77% | 28.42% | 1.15 | 1.41 |
| SPY | 3.976 | 14.82% | 297.60% | -33.72% | 18.01% | 0.87 | 1.04 |
| QQQ | 5.954 | 19.56% | 495.37% | -35.12% | 22.35% | 0.92 | 1.17 |
| 50/50 SPY/QQQ | 4.910 | 17.27% | 390.97% | -30.86% | 19.84% | 0.91 | 1.13 |

## Radar Monthly Picks Sample

| date       | bull   | bear   | allow   | picks                   |   cash |
|:-----------|:-------|:-------|:--------|:------------------------|-------:|
| 2025-01-31 | True   | False  | True    | APP|PLTR|TSLA|HOOD|VST  |    0   |
| 2025-02-28 | True   | False  | True    | HOOD|TPR|SATS|NRG       |    0.2 |
| 2025-03-31 | False  | True   | False   |                         |    1   |
| 2025-04-30 | False  | True   | False   | PLTR                    |    1   |
| 2025-05-30 | True   | False  | True    | PLTR|HOOD|NRG|GEV|CVNA  |    0   |
| 2025-06-30 | True   | False  | True    | PLTR|NRG|CVNA|GEV|STX   |    0   |
| 2025-07-31 | True   | False  | True    | HOOD|PLTR|SMCI|GEV|CVNA |    0   |
| 2025-08-29 | True   | False  | True    | HOOD|LITE|PLTR|FIX|GEV  |    0   |
| 2025-09-30 | True   | False  | True    | HOOD|LITE|PLTR|FIX|STX  |    0   |
| 2025-10-31 | True   | False  | True    | SATS|HOOD|LITE|APP|STX  |    0   |
| 2025-11-28 | True   | False  | True    | SATS|WDC|CIEN|MU|WBD    |    0   |
| 2025-12-30 | True   | False  | True    | LITE|SATS|WDC|CIEN|MU   |    0   |
