# Point-in-time low-volatility breakout proxy

## Research boundary

- Universe membership is point-in-time S&P 500 plus Nasdaq-100, deduplicated at each weekly signal close.
- The price panel is partial: 698 of 945 membership symbols have adjusted-close history. It lacks OHLCV and complete delisting returns.
- Therefore `rv20 <= 40%` is a close-return volatility proxy for the post-hoc `ATR14 / close <= 4%` idea; it is not an ATR replication.
- Signals use the completed weekly close; new weights begin on the following trading session. Results include 10 bps one-way turnover costs.
- The stock sleeve holds up to five equal-weight names. The `_mapped_25pct` rows show the same sleeve diluted to the formal 25% stock-sleeve cap.
- Research-only. No V9 or live-account permission is changed.

## Coverage

- Membership symbols: 945
- Price symbols: 698
- Missing symbols: 247
- Median month-end coverage: 78.6%

## Portfolio results: normal missing-price assumption

| Variant | Period | CAGR | Max DD | Sharpe | Monthly win | Annual turnover | Exposure |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | development_2006_2014 | -4.34% | -60.59% | -0.16 | 36.11% | 38.60 | 59.21% |
| baseline | validation_2015_2019 | -4.23% | -37.55% | -0.18 | 43.33% | 45.43 | 77.82% |
| baseline | final_2020_2025 | 5.41% | -35.04% | 0.34 | 37.50% | 46.62 | 72.00% |
| baseline | full_2006_2025 | -1.49% | -64.96% | 0.02 | 38.33% | 42.71 | 67.69% |
| rv40 | development_2006_2014 | -1.42% | -46.49% | -0.01 | 35.19% | 37.89 | 59.21% |
| rv40 | validation_2015_2019 | -5.80% | -36.55% | -0.30 | 41.67% | 44.95 | 77.82% |
| rv40 | final_2020_2025 | -1.37% | -44.77% | 0.03 | 38.89% | 47.96 | 72.00% |
| rv40 | full_2006_2025 | -2.52% | -63.43% | -0.06 | 37.92% | 42.67 | 67.69% |
| rv_percentile_60 | development_2006_2014 | 1.48% | -35.72% | 0.18 | 42.59% | 38.98 | 58.98% |
| rv_percentile_60 | validation_2015_2019 | -3.33% | -32.48% | -0.20 | 45.00% | 45.35 | 77.82% |
| rv_percentile_60 | final_2020_2025 | 3.00% | -27.64% | 0.26 | 41.67% | 47.42 | 72.00% |
| rv_percentile_60 | full_2006_2025 | 0.70% | -39.14% | 0.12 | 42.92% | 43.10 | 67.59% |
| dual_rv40_p60 | development_2006_2014 | 2.02% | -35.21% | 0.22 | 43.52% | 38.98 | 58.98% |
| dual_rv40_p60 | validation_2015_2019 | -3.33% | -32.48% | -0.20 | 45.00% | 45.35 | 77.82% |
| dual_rv40_p60 | final_2020_2025 | 3.01% | -27.64% | 0.26 | 40.28% | 47.42 | 72.00% |
| dual_rv40_p60 | full_2006_2025 | 0.94% | -38.66% | 0.14 | 42.92% | 43.10 | 67.59% |

## Missing/delisting stress

When a held symbol loses its quote immediately after a valid quote, the stress case assigns that position a -100% return on that day. This is intentionally harsher than many acquisitions but exposes sensitivity to the unavailable delisting-return field.

| Variant | Period | CAGR | Max DD | Sharpe |
| --- | --- | ---: | ---: | ---: |
| baseline | development_2006_2014 | -4.34% | -60.59% | -0.16 |
| baseline | validation_2015_2019 | -4.23% | -37.55% | -0.18 |
| baseline | final_2020_2025 | 5.41% | -35.04% | 0.34 |
| baseline | full_2006_2025 | -1.49% | -64.96% | 0.02 |
| rv40 | development_2006_2014 | -1.42% | -46.49% | -0.01 |
| rv40 | validation_2015_2019 | -5.80% | -36.55% | -0.30 |
| rv40 | final_2020_2025 | -1.37% | -44.77% | 0.03 |
| rv40 | full_2006_2025 | -2.52% | -63.43% | -0.06 |
| rv_percentile_60 | development_2006_2014 | 1.48% | -35.72% | 0.18 |
| rv_percentile_60 | validation_2015_2019 | -3.33% | -32.48% | -0.20 |
| rv_percentile_60 | final_2020_2025 | 3.00% | -27.64% | 0.26 |
| rv_percentile_60 | full_2006_2025 | 0.70% | -39.14% | 0.12 |
| dual_rv40_p60 | development_2006_2014 | 2.02% | -35.21% | 0.22 |
| dual_rv40_p60 | validation_2015_2019 | -3.33% | -32.48% | -0.20 |
| dual_rv40_p60 | final_2020_2025 | 3.01% | -27.64% | 0.26 |
| dual_rv40_p60 | full_2006_2025 | 0.94% | -38.66% | 0.14 |

## Breakout event outcomes (20 trading sessions)

| Group | Period | Events | Mean return | Positive | Close-stop <= -8% | Reached +10% |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| baseline | development_2006_2014 | 15563 | 0.74% | 56.51% | 14.23% | 9.28% |
| dual_rv40_p60 | development_2006_2014 | 9602 | 0.71% | 57.18% | 10.30% | 5.70% |
| rejected_by_dual | development_2006_2014 | 5961 | 0.80% | 55.44% | 20.55% | 15.05% |
| baseline | validation_2015_2019 | 14627 | 0.43% | 54.63% | 11.85% | 6.02% |
| dual_rv40_p60 | validation_2015_2019 | 10463 | 0.45% | 55.39% | 9.80% | 4.14% |
| rejected_by_dual | validation_2015_2019 | 4164 | 0.37% | 52.74% | 17.00% | 10.73% |
| baseline | final_2020_2025 | 14282 | 0.44% | 54.55% | 19.63% | 13.79% |
| dual_rv40_p60 | final_2020_2025 | 9460 | 0.31% | 54.82% | 15.90% | 10.10% |
| rejected_by_dual | final_2020_2025 | 4822 | 0.70% | 54.02% | 26.94% | 21.03% |

## Rolling three-year consistency

Across 16 overlapping three-year windows, `dual_rv40_p60` beat baseline on CAGR in 75.0%, max drawdown in 81.2%, Sharpe in 62.5%, and monthly win rate in 68.8% of windows.

## Cost sensitivity (final 2020-2025)

| Variant | One-way cost | CAGR | Max DD | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| baseline | 0 bps | 10.44% | -28.81% | 0.53 |
| baseline | 10 bps | 5.41% | -35.04% | 0.34 |
| baseline | 20 bps | 0.60% | -45.95% | 0.15 |
| baseline | 50 bps | -12.57% | -71.26% | -0.41 |
| dual_rv40_p60 | 0 bps | 8.01% | -24.70% | 0.55 |
| dual_rv40_p60 | 10 bps | 3.01% | -27.64% | 0.26 |
| dual_rv40_p60 | 20 bps | -1.77% | -32.50% | -0.02 |
| dual_rv40_p60 | 50 bps | -14.84% | -68.96% | -0.86 |

## Interpretation rule

The proxy is useful only if it improves validation and final-period downside/win behavior without relying mainly on cash exposure. A better full-sample headline alone is insufficient. Parameter neighbors must tell the same directional story, and the forward RSR1 shadow remains mandatory.

## Parameter-neighbor file

See `pit_parameter_stability.csv` for absolute realized-volatility caps of 30%-50% and cross-sectional cutoffs of 40%-70%. No neighbor is promoted from this retrospective run.
