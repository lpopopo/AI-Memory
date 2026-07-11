# Backtest Data Contract

## Symbols

Benchmarks:

- `SPY`
- `QQQ`

Value sleeve proxies:

- `VTV`
- `IWD`
- `SCHD`

Hot-industry sleeve candidates:

- `XLK`
- `XLC`
- `XLY`
- `XLI`
- `XLF`
- `XLV`
- `XLE`
- `XLB`
- `XLU`
- `XLRE`
- `XLP`
- `SMH`
- `IBB`
- `ITA`

## Required Fields

Daily rows:

- `date`: trading date, ISO `YYYY-MM-DD`
- `open`
- `high`
- `low`
- `close`
- `volume`

Optional:

- `adjusted_close`

## Derived Fields

For each symbol:

- Daily return.
- 50-day moving average.
- 200-day moving average.
- 63-trading-day momentum.
- 126-trading-day momentum.
- Max drawdown series.

## Alignment

- Use the union of benchmark trading dates.
- A symbol is tradable only after it has enough history for the required indicator.
- Missing symbols are excluded from that rebalance date.

## Rebalance Calendar

- Rebalance at month-end using data available at that close.
- Apply selected weights to the following trading day's return.

## Output Files

Generated outputs:

- `results/summary.md`
- `results/equity_curve.csv`
- `results/monthly_allocations.csv`

Only concise summary files should be committed by default.
