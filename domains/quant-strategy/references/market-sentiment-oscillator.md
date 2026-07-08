# Market Sentiment Oscillator

## Purpose

This is a separate 0-100 market-behavior thermometer. Zero represents extreme fear and 100 extreme greed. It identifies possible contrarian windows but never overrides the Market Fear Gate, individual stops, the unresolved-stop account veto, or V9 qualification rules.

## Components

Seven reconstructable daily components are converted to causal rolling empirical percentiles over the prior 756 sessions, with at least 252 observations:

1. SPY versus MA125.
2. Inverse VIX versus its MA50.
3. Inverse VIX/VIX3M term structure.
4. 20-day RSP/SPY equal-weight breadth.
5. 20-day IWM/SPY small-cap breadth.
6. 20-day HYG/LQD credit-risk appetite.
7. SPY 20-day return minus TLT 20-day return.

The total score is the mean of available component percentiles. At least six components must be available; missing data is not assigned a neutral score. Volatility-only holiday rows are removed before rolling equity indicators are calculated.

An optional five-day Put/Call input is supported. It is excluded from the long-history baseline until a complete point-in-time source is available. CNN Fear & Greed is an external validation series only and is not used to fit the local score.

## Regimes

| Score | Regime |
| ---: | --- |
| 0-20 | extreme_fear |
| 20-40 | fear |
| 40-60 | neutral |
| 60-80 | greed |
| 80-100 | extreme_greed |

## Contrarian Research Rule

- Arm when the score reaches 20 or below within the past 10 sessions.
- Confirm only when sentiment is rising, SPY closes above MA5, and five-day RSP/SPY breadth is positive.
- Use only unallocated V8 cash, with a maximum 10% overlay split equally between SPY and QQQ.
- Exit when sentiment reaches 55, SPY closes below MA20, or 20 sessions elapse.
- Signal at completed close and execute at the next completed close in adjusted-close research.

The rule remains shadow-only because its frozen-test improvement is small and cost-sensitive.

## Artifacts

- Implementation: `scripts/market_sentiment.py`
- Backtest: `scripts/backtest_market_sentiment_overlay.py`
- Latest output: `results/market_sentiment_latest.json` and `.md`
- Backtest output: `results/market_sentiment_overlay_metrics.json` and `_report.md`
