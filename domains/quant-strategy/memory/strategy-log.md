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

## 2026-05-29 Dual-Sleeve V0 Backtest

Summary:

- Built and ran the first 10-year US ETF proxy backtest for the 50% value plus 50% hot-industry strategy.
- Period tested: 2016-05-31 to 2026-05-28.
- Data source: yfinance auto-adjusted daily close data.
- Value sleeve proxy: equal-weight `VTV`, `IWD`, `SCHD`.
- Tactical sleeve proxy: monthly rotation among sector/theme ETFs.

Result:

- Dual Sleeve V0 final value: 2.463.
- Dual Sleeve V0 CAGR: 9.44%.
- Dual Sleeve V0 max drawdown: -24.48%.
- Dual Sleeve V0 Sharpe: 0.74.
- SPY CAGR: 15.54%, max drawdown: -33.72%, Sharpe: 0.90.
- QQQ CAGR: 21.77%, max drawdown: -35.12%, Sharpe: 1.00.
- 50/50 SPY/QQQ CAGR: 18.72%, max drawdown: -30.86%, Sharpe: 0.97.

Learned:

- The V0 ETF-proxy version reduces drawdown versus SPY and QQQ, but underperforms on CAGR and Sharpe.
- The current tactical regime filter may be too conservative.
- ETF-based value exposure may be too broad and defensive to represent the intended value-investing sleeve.
- The 50/50 idea remains testable, but V0 rules are not strong enough.

Next step:

- Improve V1 by building explicit value and industry scoring models instead of using broad ETF proxies only.
- Test tactical sleeve with top 2 vs top 3 industries, SPY/QQQ dual regime filters, and different cash rules.

## 2026-05-29 Dual-Sleeve V1 Optimization

Summary:

- Added a V1 parameter-scan optimizer for the dual-sleeve ETF-proxy strategy.
- Tested dynamic value sleeve selection, tactical top N selection, regime filters, trend filters, and fallback rules.
- Used a representative 48-configuration grid after the full grid proved too slow for the first pass.

Best candidate:

- Value mode: top 2 value ETFs by momentum score.
- Tactical top N: 2.
- Regime filter: SPY above 200-day moving average or QQQ above 100-day moving average.
- Tactical filter: positive 3-month momentum.
- Score mode: 3-month plus 6-month momentum.
- Fallback: QQQ.

Result:

- Dual Sleeve V1 Best final value: 5.288.
- Dual Sleeve V1 Best CAGR: 18.14%.
- Dual Sleeve V1 Best max drawdown: -32.17%.
- Dual Sleeve V1 Best Sharpe: 1.00.
- Compared with V0: materially better CAGR and Sharpe.
- Compared with 50/50 SPY/QQQ: slightly lower CAGR and deeper drawdown, but slightly higher Sharpe.

Learned:

- Cash fallback was too conservative in V0.
- Top 2 tactical industry/theme selection worked better than top 3 in the tested grid.
- QQQ fallback drives much of the improvement; this must be treated as a growth-index fallback, not pure industry rotation.
- Dynamic value ETF selection had only a small impact compared with tactical/fallback rules.

Next step:

- Build V2 walk-forward validation to reduce in-sample overfitting risk.
- Add a stricter comparison against 50/50 SPY/QQQ because V1 still does not clearly beat it.
- Consider individual-stock value and industry leader selection, because ETF proxies may be too blunt.
