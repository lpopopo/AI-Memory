# Double-Radar Satellite Strategy

Purpose: define the aggressive satellite module for finding 6-12 month potential double or multi-bagger stocks.

This module supplements the main V5 Optimal strategy. It does not replace V5 as the portfolio core.

## Role In Portfolio

- Core engine: V5 Optimal remains the main compounding and risk-control strategy.
- Satellite engine: Double-Radar targets high-elasticity stocks with potential to double or more in a strong theme cycle.
- Default allocation for research/backtest: `75%` V5 core plus `25%` Double-Radar satellite.
- Practical real-account use: start smaller when account size is limited or market state is not clearly bullish.

## Quantitative Price Rules

Use a monthly scan. A stock is eligible when:

- Price is above 50-day moving average.
- Price is above 200-day moving average.
- 63-trading-day momentum is above `15%`.
- 126-trading-day momentum is above `25%`.
- 126-day annualized volatility is above `40%`.
- Extension from 50-day moving average is below `35%`.
- Price is above `USD 5`.

Rank eligible stocks with:

- `30%` 126-day momentum z-score.
- `25%` 63-day momentum z-score.
- `20%` 252-day momentum z-score.
- `15%` 126-day volatility z-score.
- `-10%` positive 21-day momentum z-score penalty.
- `-10%` positive 50-day extension z-score penalty.

Select the top `5` names by score.

## Risk Gate

Use the market regime gate:

- If QQQ is above its 200-day moving average and 126-day QQQ momentum is positive, radar buying is allowed.
- If the gate is not bullish, hold cash for the radar sleeve.
- This is stricter than using the radar as a standalone high-volatility strategy.

## Position And Exit Rules

For the radar sleeve:

- Equal-weight selected names inside the sleeve.
- Rebalance monthly.
- Use `0.1%` transaction cost assumption in research.
- Use a `25%` trailing stop from position high-water mark for radar positions.
- Cash earns `0%` in current backtests.

For real-account use:

- Treat radar positions as satellite only.
- Initial single-name exposure should usually be small, especially in small accounts.
- Do not use margin by default.
- If a name doubles, review partial profit, thesis strength, and trend quality.

## Fundamental And Theme Confirmation

The quant scan is only the first filter. Before real recommendations, require at least one of:

- Revenue acceleration.
- Guidance raise.
- Margin improvement.
- Loss narrowing or path to profitability.
- Large order or backlog evidence.
- Industry supply-demand bottleneck.
- Theme-level capital flow or institutional confirmation.

Common historical themes:

- AI infrastructure and storage.
- AI software/platform repricing.
- EV/autonomy.
- Space and defense technology.
- Crypto-cycle proxies.
- Biotech breakthrough or healthcare re-rating.
- Cyclical recovery after deep drawdowns.

## Validation Snapshot

2026 YTD validation from `2026-01-02` to `2026-05-29`:

- Radar Top5 strict: `+99.49%`, max drawdown `-15.01%`.
- Radar Top3 strict: `+117.40%`, max drawdown `-20.02%`.
- Radar Top5 gated: `+64.40%`, max drawdown `-15.01%`.
- QQQ: `+19.76%`, max drawdown `-11.72%`.

10-year current-S&P-500 approximation validation from `2016-01-04` to `2025-12-30`:

- Combined `75%` V5 plus `25%` Radar: CAGR `28.09%`, max drawdown `-30.70%`, Sharpe `1.24`.
- V5 S&P500 approximation: CAGR `25.95%`, max drawdown `-30.88%`, Sharpe `1.19`.
- Radar Top5 gated standalone: CAGR `33.02%`, max drawdown `-35.77%`, Sharpe `1.15`.
- SPY: CAGR `14.82%`, max drawdown `-33.72%`, Sharpe `0.87`.
- QQQ: CAGR `19.56%`, max drawdown `-35.12%`, Sharpe `0.92`.

Backtest artifact:

- `experiments/2026-05-29-dual-sleeve-backtest/results/double_radar_10yr_sp500_approx_summary.md`

Important limitation:

- The 10-year test uses current S&P 500 membership with cached adjusted closes and therefore has survivorship bias. Treat it as a structural validation, not a final production-grade point-in-time constituent backtest.
