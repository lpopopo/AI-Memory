# Dual-Sleeve 10-Year Backtest

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
```

## Data Notes

- V0 uses yfinance daily data.
- Prices use auto-adjusted close values.
- Raw downloaded data should not be committed unless explicitly needed.

## Known Limitations

- ETF proxy does not fully represent individual-stock value investing.
- Sector ETF history may not capture narrower current themes.
- No tax model.
- No individual-stock survivorship-bias handling yet.
- V0 uses end-of-month signal and next available trading day portfolio return approximation.
