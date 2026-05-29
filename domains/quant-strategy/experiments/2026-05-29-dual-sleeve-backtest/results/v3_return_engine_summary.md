# V3 Return Engine Summary

V3 follows the selected direction: pursue full-cycle return maximization with a stronger bull-market accelerator.

## Best Candidate

- Name: `dual_sleeve_v3_04`
- Bull allocation: `20%` value / `80%` growth
- Normal allocation: `40%` value / `60%` growth
- Bear allocation: `70%` value / `30%` growth
- Bull rule: `qqq100_m63`
- Bear rule: `both_below_200_negative_m63`
- Growth top N: `2`
- Value mode: `top2`

## Full-Period Comparison

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V3 Best | 5.758 | 19.15% | -33.12% | 20.62% | 0.96 | 1.22 |
| SPY | 4.233 | 15.54% | -33.72% | 17.94% | 0.90 | 1.08 |
| QQQ | 7.156 | 21.77% | -35.12% | 22.30% | 1.00 | 1.27 |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 19.79% | 0.97 | 1.20 |

## Top Candidates

| Rank | Name | Full CAGR | Full DD | Sharpe | Train CAGR | Test CAGR | Bear 2022 | Config |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | dual_sleeve_v3_04 | 19.15% | -33.12% | 0.96 | 20.32% | 17.37% | -21.41% | bull 20%/80%, normal 40%/60%, bear 70%/30%, qqq100_m63, top2, value=top2 |
| 2 | dual_sleeve_v3_06 | 18.87% | -32.28% | 0.94 | 21.36% | 15.47% | -20.63% | bull 20%/80%, normal 40%/60%, bear 80%/20%, qqq200_m126, top2, value=top2 |
| 3 | dual_sleeve_v3_07 | 18.57% | -33.12% | 0.94 | 20.68% | 15.63% | -20.63% | bull 20%/80%, normal 40%/60%, bear 80%/20%, spy200_qqq100_m63, top2, value=top2 |
| 4 | dual_sleeve_v3_08 | 18.07% | -33.35% | 0.93 | 19.91% | 15.48% | -19.56% | bull 25%/75%, normal 45%/55%, bear 80%/20%, qqq100_m63, top2, value=top2 |
| 5 | dual_sleeve_v3_01 | 18.36% | -33.12% | 0.93 | 20.30% | 15.63% | -20.63% | bull 20%/80%, normal 40%/60%, bear 80%/20%, qqq100_m63, top2, value=top2 |
| 6 | dual_sleeve_v3_09 | 18.40% | -33.19% | 0.93 | 20.25% | 15.77% | -21.27% | bull 20%/80%, normal 40%/60%, bear 80%/20%, qqq100_m63, top2, value=equal |
| 7 | dual_sleeve_v3_02 | 18.64% | -32.89% | 0.93 | 20.69% | 15.76% | -21.69% | bull 15%/85%, normal 35%/65%, bear 80%/20%, qqq100_m63, top2, value=top2 |
| 8 | dual_sleeve_v3_03 | 18.92% | -32.66% | 0.92 | 21.07% | 15.89% | -22.74% | bull 10%/90%, normal 30%/70%, bear 80%/20%, qqq100_m63, top2, value=top2 |
| 9 | dual_sleeve_v3_05 | 16.55% | -32.48% | 0.88 | 19.01% | 13.11% | -21.07% | bull 20%/80%, normal 40%/60%, bear 80%/20%, qqq100_m63, top3, value=top2 |

## Read

- V3 intentionally prioritizes return more than V2.
- Stronger bull participation may weaken bear-market protection.
- If V3 mainly becomes QQQ-like, it must be compared against QQQ and 50/50 SPY/QQQ, not just V2.

## Initial Interpretation

- V3 does not improve over V2 in the ETF-proxy layer.
- The best V3 candidate matches V2's full-period CAGR but has worse drawdown and lower Sharpe.
- V3 improves the 2016-2021 bull-market CAGR versus V2, but gives up too much in 2022-2026 and especially in 2022.
- This suggests the next return-enhancement attempt should not simply increase ETF growth exposure.
- The better next path is individual-stock leadership selection inside hot industries.
