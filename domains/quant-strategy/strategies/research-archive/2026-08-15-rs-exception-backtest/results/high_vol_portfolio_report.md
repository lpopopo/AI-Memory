# High-volatility trend portfolio simulation

## Scope

Only the preregistered `hv_central` signal is used. The simulation applies whole shares, next-open entry, gap rejection, volatility-linked stops, a 0.75% NAV risk budget, a 15% sleeve cap, commissions and slippage. It remains current-list and post-2026-definition research.

## Results

| Period | Cost/side | Return | Max DD | Sharpe | Trades | Win rate | Profit factor | Avg exposure | Max exposure |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| development_2024_2025 | 10 bps | 2.12% | -4.36% | 0.32 | 17 | 17.65% | 1.25 | 1.57% | 14.63% |
| development_2024_2025 | 20 bps | 1.92% | -4.48% | 0.29 | 17 | 17.65% | 1.23 | 1.57% | 14.65% |
| retrospective_2026 | 10 bps | 3.93% | -1.75% | 1.12 | 12 | 58.33% | 2.23 | 4.80% | 15.33% |
| retrospective_2026 | 20 bps | 3.80% | -1.76% | 1.09 | 12 | 58.33% | 2.17 | 4.80% | 15.34% |

## Continuation gate

- `minimum_trade_count`: `True`
- `positive_return_both`: `True`
- `sharpe_ge_0_50_both`: `False`
- `win_rate_ge_50_both`: `False`
- `profit_factor_ge_1_20_both`: `True`
- `max_drawdown_no_worse_10pct_both`: `True`
- `positive_at_20bps_both`: `True`
- `entry_path_stable_10_to_20bps`: `True`
- `gross_profit_concentration`: `33.77%`
- `gross_profit_concentration_le_35`: `True`
- `passes_portfolio_gate`: `False`

## Decision

Stop the sleeve branch. Retain only the non-trading high-volatility missed-opportunity diagnostic; do not optimize position or exit parameters on this history.
