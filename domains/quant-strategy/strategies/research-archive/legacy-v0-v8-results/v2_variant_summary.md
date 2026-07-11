# V2 Variant Summary

V2 tests bull-market participation upgrades on top of V1.

## Best Candidate

- Name: `dual_sleeve_v2_05`
- Bull value weight: `35%`
- Bull tactical/growth weight: `65%`
- Normal value weight: `50%`
- Normal tactical weight: `50%`
- Bull rule: `qqq200_m126`
- Tactical top N: `2`
- Fallback: `qqq`
- Include QQQ in bull rank: `True`

## Full-Period Comparison

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V2 Best | 5.759 | 19.15% | -31.04% | 19.06% | 1.02 | 1.29 | 55.41% |
| SPY | 4.233 | 15.54% | -33.72% | 17.94% | 0.90 | 1.08 | 55.45% |
| QQQ | 7.156 | 21.77% | -35.12% | 22.30% | 1.00 | 1.27 | 56.89% |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 19.79% | 0.97 | 1.20 | 56.45% |

## Top Candidates

| Rank | Name | Full CAGR | Full DD | Full Sharpe | Test CAGR | Test DD | Test Sharpe | Train CAGR | Bear 2022 | Config |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | dual_sleeve_v2_05 | 19.15% | -31.04% | 1.02 | 19.97% | -17.46% | 1.08 | 18.44% | -6.79% | bull 35%/65%, qqq200_m126, top2, qqq, qqq_rank=True |
| 2 | dual_sleeve_v2_06 | 18.93% | -32.33% | 1.01 | 20.00% | -17.20% | 1.09 | 18.02% | -6.79% | bull 35%/65%, spy200_qqq100, top2, qqq, qqq_rank=True |
| 3 | dual_sleeve_v2_08 | 18.87% | -32.33% | 1.00 | 19.87% | -17.20% | 1.08 | 18.02% | -6.79% | bull 35%/65%, qqq100_m63, top2, qqq, qqq_rank=False |
| 4 | dual_sleeve_v2_03 | 19.10% | -32.43% | 0.99 | 20.68% | -17.68% | 1.09 | 17.79% | -7.61% | bull 25%/75%, qqq100_m63, top2, qqq, qqq_rank=True |
| 5 | dual_sleeve_v2_02 | 18.89% | -32.38% | 0.99 | 20.34% | -17.37% | 1.09 | 17.68% | -7.20% | bull 30%/70%, qqq100_m63, top2, qqq, qqq_rank=True |
| 6 | dual_sleeve_v2_01 | 18.67% | -32.33% | 0.99 | 20.00% | -17.20% | 1.09 | 17.56% | -6.79% | bull 35%/65%, qqq100_m63, top2, qqq, qqq_rank=True |
| 7 | dual_sleeve_v2_09 | 18.45% | -32.28% | 1.00 | 19.65% | -17.02% | 1.09 | 17.44% | -6.38% | bull 40%/60%, qqq100_m63, top2, qqq, qqq_rank=True |
| 8 | dual_sleeve_v2_07 | 17.99% | -33.87% | 0.97 | 19.21% | -17.19% | 1.07 | 16.97% | -5.93% | bull 35%/65%, qqq100_m63, top2, spy_qqq, qqq_rank=True |
| 9 | dual_sleeve_v2_04 | 17.72% | -32.24% | 0.97 | 17.41% | -17.72% | 1.00 | 17.88% | -8.40% | bull 35%/65%, qqq100_m63, top3, qqq, qqq_rank=True |

## Read

- V2 is still an ETF-proxy strategy, not the final individual-stock version.
- The goal is to improve bull-market participation while watching whether 2022 protection degrades.
- If V2 mostly becomes QQQ exposure, compare it skeptically against 50/50 SPY/QQQ and QQQ.

## Initial Interpretation

- V2 improves on V1: full-period CAGR rises from 18.14% to 19.15%, max drawdown improves from -32.17% to -31.04%, and Sharpe improves from 1.00 to 1.02.
- V2 slightly beats 50/50 SPY/QQQ on full-period CAGR and Sharpe, while its max drawdown is slightly worse.
- V2 still trails QQQ on full-period CAGR, but with lower volatility and lower drawdown.
- V2 gives up some 2022 bear-market protection versus V1, but still protects far better than SPY, QQQ, or 50/50 SPY/QQQ.
- Current best interpretation: V2 is the strongest ETF-proxy candidate so far, but it still needs walk-forward and individual-stock validation.
