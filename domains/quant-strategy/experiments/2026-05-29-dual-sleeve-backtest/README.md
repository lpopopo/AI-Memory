# Dual-Sleeve 10-Year Backtest

## V9 information-driven research strategy

V9 is an independent, non-promoted full-account research model. Timestamped public-content events generate candidates; two-day price confirmation, scoring, concentration limits, stops, and portfolio drawdown breakers control execution. Formal V8 remains unchanged.

Operational outputs include `results/v9_execution_playbook.md`, `results/v9_information_funnel_report.md`, and the point-in-time event study CSV. The live signal now distinguishes qualified trades from watchlist names and reports each candidate's remaining score gap without lowering the 70-point entry threshold.

`scripts/run_v9_daily_execution.py` produces a human-review daily target and an append-only frozen forward ledger. It is deliberately not connected to a broker.

Point-in-time primary-evidence upgrades live in `datasets/v9_evidence_updates.json`. Only filings, earnings releases, company investor-relations material, and regulator filings are accepted; repeated commentary cannot stack validation points.

```bash
python scripts/download_v9_data.py
python scripts/validate_v9_information_strategy.py
python scripts/v9_signal.py --json
```

The tracked event store is `datasets/v9_information_events.json`. Missing publication timestamps use `first_seen_at`; fewer than 50 reliable events disables optimization and promotion. A non-healthy source state blocks new information entries but never disables price stops on existing positions.

> **V8 audit status (2026-07-03):** Legacy V5/V6/V7 performance reports are not
> decision-grade because the stock universe is not point-in-time. The authoritative
> current result is `results/v8_model_optimization_report.md`; the robust engine is
> `scripts/robust_portfolio_engine.py` with tests in
> `scripts/test_robust_portfolio_engine.py`.

Reproduce the V8 audit and print the latest completed-bar target:

```bash
source .venv/bin/activate
python -m unittest -v scripts/test_robust_portfolio_engine.py
python scripts/optimize_v8_robust.py
python scripts/optimize_v8_etf.py
python scripts/optimize_v8_core.py
python scripts/write_v8_report.py
python scripts/v8_signal.py
```

Re-run V5 with point-in-time S&P 500/Nasdaq-100 membership:

```bash
pip install index-constitution==0.6.1
python scripts/build_point_in_time_data.py
python -m unittest -v scripts/test_v5_point_in_time.py
python scripts/backtest_v5_point_in_time.py
python scripts/write_v5_point_in_time_report.py
```

The authoritative result is `results/v5_point_in_time_report.md`. Free Yahoo
prices still omit 212 of 940 historical symbols, so this materially reduces but
does not claim to eliminate survivorship bias.

Research the non-promoted V8.1 dynamic QQQ/VT enhancement sleeve:

```bash
python -m unittest -v scripts/test_v81_dynamic_enhancer.py
python scripts/optimize_v81_dynamic.py
python scripts/write_v81_report.py
python scripts/v8_signal.py --version v8.1 --json
```

V8.1 is promoted only when every hard gate in
`results/v81_dynamic_optimization_report.md` passes. Otherwise the live/default
signal remains `python scripts/v8_signal.py --version v8`.

This experiment validates the current US-stock strategy with approximately 10 years of daily data.

## Purpose

Test whether a 50% value sleeve plus 50% hot-industry momentum sleeve improves risk-adjusted behavior versus simple benchmarks.

## V0 Scope

V0 uses ETF proxies instead of individual stocks:

- Value sleeve: value/dividend ETF proxies.
- Hot-industry sleeve: US sector and theme ETF rotation.
- Benchmarks: SPY, QQQ, and 50/50 SPY/QQQ.

This is not the final strategy. It is a first validation of the allocation structure.

## Period

Target period:

- Start: 2016-05-29
- End: 2026-05-29

The script uses available trading days around those dates.

## Execution Plan

1. Download daily OHLCV data for value ETFs, sector/theme ETFs, SPY, and QQQ.
2. Align all symbols on common trading dates.
3. Compute daily returns, moving averages, and trailing momentum.
4. Rebalance monthly.
5. Allocate 50% to the value sleeve.
6. Allocate 50% to the hot-industry sleeve when market regime is positive.
7. Move tactical sleeve to cash when market regime is negative or no ETF qualifies.
8. Compare strategy against SPY, QQQ, and 50/50 SPY/QQQ.
9. Record CAGR, max drawdown, volatility, Sharpe ratio, Sortino ratio, turnover proxy, and final value.

## V0 Rules

### Value Sleeve

- Equal-weight `VTV`, `IWD`, and `SCHD` when data is available.
- Rebalance monthly.

### Hot-Industry Sleeve

Candidate ETFs:

- `XLK`, `XLC`, `XLY`, `XLI`, `XLF`, `XLV`, `XLE`, `XLB`, `XLU`, `XLRE`, `XLP`, `SMH`, `IBB`, `ITA`.

Eligibility:

- SPY close is above its 200-day moving average.
- ETF has positive 3-month momentum.
- ETF close is above its 50-day moving average.

Selection:

- Rank eligible ETFs by 3-month plus 6-month momentum.
- Hold top 3 equal-weight.
- If fewer than 3 qualify, hold the qualifying ETFs and keep the remainder in cash.

## Run

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/backtest_dual_sleeve.py
.venv/bin/python scripts/optimize_dual_sleeve.py
.venv/bin/python scripts/validate_dual_sleeve.py
.venv/bin/python scripts/test_v2_variants.py
.venv/bin/python scripts/validate_v2_robustness.py
.venv/bin/python scripts/test_v3_return_engine.py
```

## Data Notes

- V0 uses yfinance daily data.
- Prices use auto-adjusted close values.
- Raw downloaded data should not be committed unless explicitly needed.

## V1 Optimization

The optimizer scans:

- Static versus dynamic value ETF selection.
- Tactical top 1, 2, 3, or 4 ETF rotation.
- Different market regime filters.
- Different tactical trend filters.
- Cash, SPY, QQQ, or SPY/QQQ fallback when tactical conditions fail.

The best in-sample configuration is only a candidate. It needs walk-forward validation before being treated as a durable strategy rule.

## Revalidation

`validate_dual_sleeve.py` reruns the best V1 configuration and compares it against SPY, QQQ, and 50/50 SPY/QQQ across:

- Full period.
- 2016-2021 training-like period.
- 2022-2026 test-like period.
- 2022 bear-market segment.
- 2023-2026 post-bear recovery segment.

## V2 Variants

`test_v2_variants.py` tests bull-market participation upgrades. In strong QQQ regimes, selected variants temporarily shift from 50/50 to a more aggressive value/tactical mix such as 35/65, while reverting to the V1-style defensive structure outside those regimes.

`validate_v2_robustness.py` fixes the best V2 candidate and tests it across fixed splits plus rolling 3-year windows against SPY, QQQ, and 50/50 SPY/QQQ.

## V3 Return Engine

`test_v3_return_engine.py` follows the selected direction of full-cycle return maximization. It tests stronger bull-market growth allocations while keeping a basic bear-market risk reduction rule.

## Known Limitations

- ETF proxy does not fully represent individual-stock value investing.
- Sector ETF history may not capture narrower current themes.
- No tax model.
- No individual-stock survivorship-bias handling yet.
- V0 uses end-of-month signal and next available trading day portfolio return approximation.
