# Market Fear Technical Framework

Purpose: define a reusable market-panic layer for US equity strategy analysis.

This framework is a portfolio risk gate. It does not select stocks by itself. It decides whether the strategy may add exposure, should reduce position sizes, or must stop new buys.

## Indicator Groups

### Volatility Stress

- `^VIX` level:
  - below 16: calm
  - 16 to 22: elevated
  - 22 to 30: stress
  - 30 to 35: high stress
  - above 35: panic
- 5-day VIX change:
  - above +15%: early stress
  - above +30%: stress spike
  - above +50%: panic spike
- VIX term structure:
  - `^VIX / ^VIX3M` below 1.00: normal
  - 1.00 to 1.05: flat or mildly inverted
  - above 1.05: near-term panic

### Index Drawdown and Trend

Use `SPY`, `QQQ`, and `SMH`.

- 63-day drawdown:
  - 0% to -4%: normal
  - -4% to -8%: mild drawdown
  - -8% to -12%: meaningful stress
  - below -12%: deep drawdown
- Trend:
  - below 50-day moving average: caution
  - below 200-day moving average: major risk-off

### Breadth and Credit Proxies

- `IWM / SPY`: small-cap relative strength.
- `RSP / SPY`: equal-weight market breadth versus cap-weight leadership.
- `HYG / LQD`: credit risk appetite.

If any 21-day relative ratio falls more than 2.5%, count as mild deterioration. If it falls more than 5%, count as sharp deterioration.

## Fear Score

Each signal contributes points. The sum maps to a portfolio regime:

| Score | Regime | Risk Multiplier | Max Gross Exposure | Max New Buy Exposure | Cash Floor |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0-4 | normal | 100% | 95% | 50% | 5% |
| 5-8 | elevated | 70% | 75% | 25% | 25% |
| 9-13 | stress | 40% | 55% | 10% | 45% |
| 14+ | panic | 20% | 35% | 0% | 65% |

## Strategy Integration

Daily stock recommendations must run this layer before producing buy lists.

Rules:

- `normal`: staged buying is allowed when stock-level V5/V6 filters agree.
- `elevated`: buy only near support, reduce each planned new order by 30%, and keep at least 25% cash.
- `stress`: no momentum chasing; only strongest names after reclaim signals; keep at least 45% cash.
- `panic`: stop new buys; focus on capital preservation, forced risk reduction, or later recovery watchlists.

For the current USD 20,000 model portfolio:

- Multiply planned position sizes by the risk multiplier.
- Enforce the cash floor even if individual stock signals are strong.
- Do not override individual stop-loss rules; this layer only tightens risk.

## Implementation

Script:

- `experiments/2026-05-29-dual-sleeve-backtest/scripts/market_fear.py`

Outputs:

- `results/market_fear_latest.json`
- `results/market_fear_latest.md`

The daily recommendation workflow should quote the latest regime, score, cash floor, and action before listing stock orders.
