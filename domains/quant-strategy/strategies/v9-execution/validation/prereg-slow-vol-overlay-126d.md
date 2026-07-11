# Pre-registration: 126-Day Slow Volatility Overlay

Frozen date: 2026-07-11  
Status: research-only; no leverage; does not change formal V9 weights.

## Hypothesis

Scaling the SPY/QQQ core by `target_vol / realized_vol_126`, clipped to
`[0.25, 1.00]`, improves net drawdown control versus unscaled V8-equivalent
core exposure.

## Implementation

- Realized vol: annualized std of daily returns over 126 sessions.
- Target vol: 12%.
- No leverage: ceiling = 1.0.
- Floor = 0.25.
- Apply only to index-core weights; cash absorbs residual.

## Costs

Evaluate at one-way costs of 0.1%, 0.2%, and 0.5%.

## Metrics and gates

Primary: max drawdown and Sharpe after costs.  
Reject if turnover or cash drag erases the drawdown benefit, or if improvement
vanishes outside crisis windows.

## Separation rule

This experiment is independent from the panic-to-repair monitor. Do not combine
until both pass alone.
