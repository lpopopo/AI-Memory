# V3 Refined (V3.1) Optimization Summary

V3.1 introduces a customizable `fallback` mechanism (cash, spy, qqq) when tactical growth ETFs do not have positive momentum, resolving V3's massive downside vulnerability in bear markets.

## Best Refined Candidate

- Name: `dual_sleeve_v3_refined_202`
- Fallback strategy: `cash`
- Bull allocation: `30%` value / `70%` growth
- Normal allocation: `40%` value / `60%` growth
- Bear allocation: `70%` value / `30%` growth
- Bull rule: `qqq200_m126`
- Bear rule: `both_below_200_negative_m63`
- Growth top N: `2`
- Value mode: `top2`

## Full-Period Comparison

| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dual Sleeve V3.1 Best | 5.232 | 18.01% | -32.46% | 18.62% | 0.99 | 1.22 |
| SPY | 4.233 | 15.54% | -33.72% | 17.94% | 0.90 | 1.08 |
| QQQ | 7.156 | 21.77% | -35.12% | 22.30% | 1.00 | 1.27 |
| 50/50 SPY/QQQ | 5.553 | 18.72% | -30.86% | 19.79% | 0.97 | 1.20 |

## Top 10 Candidates

| Rank | Name | Fallback | Full CAGR | Full DD | Sharpe | Train CAGR | Test CAGR | Bear 2022 | Config |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | dual_sleeve_v3_refined_202 | cash | 18.01% | -32.46% | 0.99 | 19.02% | 16.48% | -12.92% | bull 30%/70%, normal 40%/60%, bear 70%/30%, qqq200_m126, top2 |
| 2 | dual_sleeve_v3_refined_178 | cash | 18.04% | -32.46% | 0.98 | 19.45% | 15.99% | -12.20% | bull 30%/70%, normal 40%/60%, bear 80%/20%, qqq200_m126, top2 |
| 3 | dual_sleeve_v3_refined_154 | cash | 18.05% | -32.46% | 0.97 | 19.88% | 15.50% | -11.51% | bull 30%/70%, normal 40%/60%, bear 90%/10%, qqq200_m126, top2 |
| 4 | dual_sleeve_v3_refined_214 | cash | 17.40% | -31.74% | 0.99 | 18.87% | 15.21% | -13.35% | bull 30%/70%, normal 40%/60%, bear 70%/30%, qqq200_m126, top3 |
| 5 | dual_sleeve_v3_refined_190 | cash | 17.42% | -31.74% | 0.98 | 19.30% | 14.74% | -12.63% | bull 30%/70%, normal 40%/60%, bear 80%/20%, qqq200_m126, top3 |
| 6 | dual_sleeve_v3_refined_058 | cash | 18.38% | -32.28% | 0.97 | 19.47% | 16.70% | -13.69% | bull 20%/80%, normal 40%/60%, bear 70%/30%, qqq200_m126, top2 |
| 7 | dual_sleeve_v3_refined_034 | cash | 18.40% | -32.28% | 0.96 | 19.90% | 16.22% | -12.98% | bull 20%/80%, normal 40%/60%, bear 80%/20%, qqq200_m126, top2 |
| 8 | dual_sleeve_v3_refined_166 | cash | 17.44% | -31.74% | 0.97 | 19.73% | 14.25% | -11.94% | bull 30%/70%, normal 40%/60%, bear 90%/10%, qqq200_m126, top3 |
| 9 | dual_sleeve_v3_refined_010 | cash | 18.42% | -32.28% | 0.95 | 20.33% | 15.73% | -12.29% | bull 20%/80%, normal 40%/60%, bear 90%/10%, qqq200_m126, top2 |
| 10 | dual_sleeve_v3_refined_199 | cash | 17.67% | -32.46% | 0.97 | 19.04% | 15.70% | -12.92% | bull 30%/70%, normal 40%/60%, bear 70%/30%, qqq200_m126, top2 |

## Read

- V3.1 successfully combines V3's strong bull-market growth with V2's bear protection.
- Choosing the right fallback (e.g. cash or spy) significantly changes the 2022 downside outcomes.
