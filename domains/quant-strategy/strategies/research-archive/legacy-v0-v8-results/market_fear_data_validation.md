# Market Fear Data Validation

- Data range: `2025-01-02` to `2026-05-29`
- Rows: `353`
- Columns returned: `HYG, IWM, LQD, QQQ, RSP, SMH, SPY, TLT, ^VIX, ^VIX3M`
- Latest regime: `normal`
- Latest score: `0`
- Risk multiplier: `100%`
- Cash floor: `5%`

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| non_empty_dataset | PASS | 353 rows, 10 columns |
| core_column_SPY | PASS | exists=True, non_na_rows=352 |
| core_column_QQQ | PASS | exists=True, non_na_rows=352 |
| core_column_SMH | PASS | exists=True, non_na_rows=352 |
| core_column_^VIX | PASS | exists=True, non_na_rows=353 |
| core_column_^VIX3M | PASS | exists=True, non_na_rows=352 |
| optional_column_IWM | PASS | exists=True, non_na_rows=352 |
| optional_column_RSP | PASS | exists=True, non_na_rows=352 |
| optional_column_HYG | PASS | exists=True, non_na_rows=352 |
| optional_column_LQD | PASS | exists=True, non_na_rows=352 |
| optional_column_TLT | PASS | exists=True, non_na_rows=352 |
| latest_value_sanity_SPY | PASS | 757.1000 in [50, 2000] |
| latest_value_sanity_QQQ | PASS | 738.3000 in [50, 2000] |
| latest_value_sanity_SMH | PASS | 600.9600 in [10, 2000] |
| latest_value_sanity_^VIX | PASS | 15.4600 in [5, 100] |
| latest_value_sanity_^VIX3M | PASS | 18.8800 in [5, 100] |

## Latest Fear Signals

| Signal | Value | Points | Note |
| --- | ---: | ---: | --- |
| vix_level | 15.46 | 0 | calm volatility |
| vix_5d_change | -7.43% | 0 | no major VIX spike |
| vix_vix3m_ratio | 0.82 | 0 | VIX term structure normal |
| spy_drawdown_63d | 0.00% | 0 | SPY near short-term high |
| spy_trend_break | 0.00 | 0 | SPY trend intact |
| qqq_drawdown_63d | 0.00% | 0 | QQQ near short-term high |
| qqq_trend_break | 0.00 | 0 | QQQ trend intact |
| smh_drawdown_63d | -0.20% | 0 | SMH near short-term high |
| smh_trend_break | 0.00 | 0 | SMH trend intact |
| smallcap_vs_spy_21d | 0.20% | 0 | smallcap_vs_spy_21d stable |
| equal_weight_vs_spy_21d | -1.87% | 0 | equal_weight_vs_spy_21d stable |
| credit_risk_21d | -0.34% | 0 | credit_risk_21d stable |

## Warnings

- None.
