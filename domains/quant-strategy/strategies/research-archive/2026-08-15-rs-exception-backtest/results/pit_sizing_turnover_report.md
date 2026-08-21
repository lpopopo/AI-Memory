# PIT soft sizing and turnover-buffer exploration

## Boundary

This is a post-hoc exploration on the same partial point-in-time adjusted-close panel. It cannot promote a rule. All variants keep the same eligible names; no low-volatility stock is excluded.

- `equal_weekly`: original top-five equal-weight weekly baseline.
- `soft_vol_weekly`: same five names, blending equal weights 50/50 with inverse-square-root-volatility weights.
- `buffer_equal`: keep an existing name while it remains in the top ten, then fill to five; equal weight.
- `buffer_soft_vol`: combine the top-ten holding buffer and soft volatility tilt.

## Ten-basis-point results

| Variant | Period | CAGR | Max DD | Sharpe | Monthly win | Annual turnover |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| equal_weekly | development_2006_2014 | -4.34% | -60.59% | -0.16 | 36.11% | 38.60 |
| equal_weekly | validation_2015_2019 | -4.23% | -37.55% | -0.18 | 43.33% | 45.43 |
| equal_weekly | final_2020_2025 | 5.41% | -35.04% | 0.34 | 37.50% | 46.62 |
| equal_weekly | full_2006_2025 | -1.49% | -64.96% | 0.02 | 38.33% | 42.71 |
| soft_vol_weekly | development_2006_2014 | -4.54% | -61.08% | -0.17 | 35.19% | 39.22 |
| soft_vol_weekly | validation_2015_2019 | -4.75% | -36.40% | -0.22 | 43.33% | 46.20 |
| soft_vol_weekly | final_2020_2025 | 5.00% | -34.65% | 0.32 | 37.50% | 47.28 |
| soft_vol_weekly | full_2006_2025 | -1.83% | -66.22% | 0.00 | 37.92% | 43.38 |
| buffer_equal | development_2006_2014 | -1.72% | -52.36% | -0.01 | 35.19% | 31.34 |
| buffer_equal | validation_2015_2019 | -6.55% | -38.51% | -0.35 | 41.67% | 37.10 |
| buffer_equal | final_2020_2025 | 7.88% | -30.83% | 0.44 | 37.50% | 38.46 |
| buffer_equal | full_2006_2025 | -0.20% | -58.09% | 0.09 | 37.50% | 34.91 |
| buffer_soft_vol | development_2006_2014 | -1.71% | -51.99% | -0.01 | 33.33% | 31.75 |
| buffer_soft_vol | validation_2015_2019 | -6.87% | -39.32% | -0.38 | 40.00% | 37.57 |
| buffer_soft_vol | final_2020_2025 | 7.49% | -29.47% | 0.42 | 38.89% | 39.07 |
| buffer_soft_vol | full_2006_2025 | -0.39% | -58.56% | 0.08 | 36.67% | 35.40 |

## Final-period cost sensitivity

| Variant | Cost | CAGR | Max DD | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| equal_weekly | 0 bps | 10.44% | -28.81% | 0.53 |
| equal_weekly | 10 bps | 5.41% | -35.04% | 0.34 |
| equal_weekly | 20 bps | 0.60% | -45.95% | 0.15 |
| equal_weekly | 50 bps | -12.57% | -71.26% | -0.41 |
| soft_vol_weekly | 0 bps | 10.08% | -28.10% | 0.52 |
| soft_vol_weekly | 10 bps | 5.00% | -34.65% | 0.32 |
| soft_vol_weekly | 20 bps | 0.15% | -46.30% | 0.13 |
| soft_vol_weekly | 50 bps | -13.14% | -71.65% | -0.45 |
| buffer_equal | 0 bps | 12.11% | -28.86% | 0.59 |
| buffer_equal | 10 bps | 7.88% | -30.83% | 0.44 |
| buffer_equal | 20 bps | 3.81% | -36.38% | 0.28 |
| buffer_equal | 50 bps | -7.54% | -59.27% | -0.20 |
| buffer_soft_vol | 0 bps | 11.77% | -27.44% | 0.59 |
| buffer_soft_vol | 10 bps | 7.49% | -29.47% | 0.42 |
| buffer_soft_vol | 20 bps | 3.37% | -35.60% | 0.26 |
| buffer_soft_vol | 50 bps | -8.11% | -59.26% | -0.24 |

## Rolling three-year comparison versus equal weekly

- `soft_vol_weekly`: higher CAGR 25.0%, better drawdown 56.2%, higher Sharpe 18.8%, higher monthly win rate 18.8% across 16 windows.
- `buffer_equal`: higher CAGR 68.8%, better drawdown 81.2%, higher Sharpe 68.8%, higher monthly win rate 0.0% across 16 windows.
- `buffer_soft_vol`: higher CAGR 68.8%, better drawdown 81.2%, higher Sharpe 68.8%, higher monthly win rate 18.8% across 16 windows.

## Retrospective screen

| Variant | Better CAGR and Sharpe in validation/final at 10/20 bps | Lower turnover | No worse drawdown | Result |
| --- | ---: | ---: | ---: | --- |
| soft_vol_weekly | no | no | no | reject |
| buffer_equal | no | yes | no | reject |
| buffer_soft_vol | no | yes | no | reject |

## Decision standard

A useful successor must improve validation and final-period net return/Sharpe at both 10 and 20 bps, reduce turnover materially, and avoid a worse max drawdown. Passing this retrospective screen would justify only a new preregistered shadow version.

None passed. The soft volatility tilt reduced neither turnover nor return sacrifice. The top-ten holding buffer helped 2020-2025 and lowered turnover, but materially worsened 2015-2019; it is not stable enough to create a second shadow candidate.
