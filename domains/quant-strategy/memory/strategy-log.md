# Strategy Log

## 2026-05-29

Initial memory repository created. Data-source problem handled first; strategy analysis will be added after the source layer is stable.

Open topics:

- Define the exact meaning and scope of “量外策略”.
- Signal universe decided for initial work: US stocks and ETFs first.
- Decide required data granularity: real-time quote, daily K, minute, or all.
- Add backtest data format after strategy rules are clarified.

## 2026-05-29 US Stock Strategy Start

Summary:

- User clarified that the strategy should mainly target US stocks.
- Created initial US-stock-first strategy blueprint.
- Added hypotheses for universe selection, multi-factor confirmation, and delaying external signals until the price-volume baseline is stable.

Learned:

- The first strategy should not be a mixed-market strategy.
- US equities should become the default research universe.
- Strategy work should begin with daily OHLCV and explainable signal rules.

Open questions:

- Initial universe: S&P 500, Nasdaq 100, or top N US stocks by dollar volume.
- Benchmark: SPY, QQQ, or both.
- Risk target: maximum drawdown and maximum single-position size.
- Data source: choose a stable daily OHLCV provider for US equities.

Next step:

- Decide the first universe and benchmark, then create the backtest data contract.

## 2026-05-29 Dual-Sleeve Portfolio Design

Summary:

- User proposed splitting capital into 50% value investing and 50% hot-industry investing.
- Formalized the structure as a dual-sleeve US equity strategy.
- Added separate rules for value selection, hot-industry selection, risk control, and rebalancing.

Learned:

- The strategy should combine a stable long-term base with a tactical industry-rotation component.
- The two sleeves need different review cadences: value monthly/quarterly, tactical weekly/monthly.
- Portfolio-level sector and factor concentration must be monitored across both sleeves.

Open questions:

- Should the value sleeve use only individual stocks, or allow value ETFs?
- Should the hot-industry sleeve begin with ETFs, then move to individual stocks after confirmation?
- What maximum portfolio drawdown should trigger risk reduction?
- Should tactical sleeve be allowed to hold cash when no industry qualifies?

Next step:

- Define exact scoring models for value stocks and hot industries, then create a backtest data contract.
