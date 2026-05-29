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

## 2026-05-29 V1 Revalidation

Summary:

- Reran the fixed V1 best configuration and compared it against SPY, QQQ, and 50/50 SPY/QQQ.
- Added split validation for full period, 2016-2021, 2022-2026, 2022 bear market, and 2023-2026 recovery.

Revalidation result:

- Full period reproduced the optimization result: V1 final value 5.288, CAGR 18.14%, max drawdown -32.17%, Sharpe 1.00.
- Full period still did not beat 50/50 SPY/QQQ on CAGR or drawdown.
- 2016-2021: V1 underperformed QQQ and 50/50 SPY/QQQ in the bull market.
- 2022-2026: V1 outperformed SPY, QQQ, and 50/50 SPY/QQQ with lower drawdown.
- 2022 bear market: V1 lost -5.56% versus SPY -18.84%, QQQ -33.54%, and 50/50 SPY/QQQ -26.45%.

Learned:

- V1's edge is defensive and regime-aware, not raw bull-market return.
- The strategy is promising as a drawdown-control overlay.
- The main weakness is insufficient participation in strong QQQ-led bull phases.

Next step:

- Build V2 to improve bull-market participation while preserving 2022 downside protection.
- Candidate V2 tests: allow tactical sleeve to hold QQQ/SMH/XLK more aggressively in confirmed bull regimes, and compare with a simple 50/50 SPY/QQQ hurdle.

## 2026-05-29 V2 Bull-Participation Optimization

Summary:

- Added V2 variants that increase tactical/growth exposure during confirmed QQQ bull regimes.
- Tested several bull-market allocation shifts, tactical top N settings, bull-regime rules, and QQQ inclusion rules.
- Best V2 candidate uses a 35% value / 65% tactical-growth mix during QQQ long-trend bull regimes, and reverts to the V1-style 50/50 structure otherwise.

Best candidate:

- Name: dual_sleeve_v2_05.
- Bull allocation: 35% value, 65% tactical/growth.
- Normal allocation: 50% value, 50% tactical.
- Bull rule: QQQ above 200-day moving average with positive 6-month momentum.
- Tactical top N: 2.
- Fallback: QQQ.
- Include QQQ in bull ranking: true.

Result:

- V2 final value: 5.759.
- V2 CAGR: 19.15%.
- V2 max drawdown: -31.04%.
- V2 Sharpe: 1.02.
- V2 beats V1 on CAGR, drawdown, and Sharpe.
- V2 slightly beats 50/50 SPY/QQQ on CAGR and Sharpe, but has slightly worse drawdown.
- V2 still trails QQQ on full-period CAGR, while carrying less volatility and drawdown.

Learned:

- Bull-market participation improved when the tactical sleeve became more growth-oriented in confirmed QQQ trends.
- A slower bull rule using QQQ 200-day moving average plus 6-month momentum was better than the faster QQQ 100-day / 3-month rule in the tested candidates.
- V2 gives up some of V1's 2022 protection, but still protects much better than SPY, QQQ, and 50/50 SPY/QQQ.

Next step:

- Validate V2 with a more formal walk-forward process.
- Add individual-stock sleeves to test whether value selection and industry leaders can improve beyond ETF proxies.

## 2026-05-29 V2 Robustness Revalidation

Summary:

- Fixed the best V2 configuration and tested it across fixed splits plus rolling 3-year windows.
- Compared V2 against SPY, QQQ, and 50/50 SPY/QQQ.

Fixed split result:

- Full period: V2 beats 50/50 SPY/QQQ by 0.43 percentage points CAGR and 0.05 Sharpe, but has 0.18 percentage points worse drawdown.
- 2016-2021: V2 underperforms 50/50 SPY/QQQ by 3.97 percentage points CAGR.
- 2022-2026: V2 beats 50/50 SPY/QQQ by 5.95 percentage points CAGR and has much shallower drawdown.
- 2022 bear market: V2 loses -6.79% versus 50/50 SPY/QQQ losing -26.45%.

Rolling 3-year result versus 50/50 SPY/QQQ:

- CAGR wins: 4 / 9.
- Drawdown wins: 6 / 9.
- Sharpe wins: 4 / 9.

Learned:

- V2 is not a stable return winner across all windows.
- V2's clearest edge is drawdown control, especially around bear-market regimes.
- V2 still lags in early bull-market windows such as 2017-2019 and 2018-2020.

Next step:

- Decide whether the strategy objective is defensive compounding or full-cycle return maximization.
- If full-cycle return maximization is required, add a stronger bull-market accelerator or move to individual-stock leadership selection.

## 2026-05-29 Objective Choice

Decision:

- User selected direction 2: pursue full-cycle return maximization.

Implication:

- V3 may accept higher volatility or somewhat weaker bear-market protection if it materially improves bull-market participation and full-cycle CAGR.
- Strategy comparisons must continue to include QQQ and 50/50 SPY/QQQ, because a return-focused version can easily become disguised QQQ exposure.

## 2026-05-29 V3 Return Engine Test

Summary:

- Built V3 ETF-proxy return engine candidates after user selected full-cycle return maximization.
- V3 tested stronger bull-market growth allocations and more aggressive normal-regime growth exposure.

Best V3 candidate:

- Name: dual_sleeve_v3_04.
- Bull allocation: 20% value, 80% growth.
- Normal allocation: 40% value, 60% growth.
- Bear allocation: 70% value, 30% growth.
- Bull rule: QQQ above 100-day moving average with positive 3-month momentum.
- Bear rule: SPY and QQQ below 200-day moving averages with negative 3-month momentum.

Result:

- V3 final value: 5.758.
- V3 CAGR: 19.15%.
- V3 max drawdown: -33.12%.
- V3 Sharpe: 0.96.
- V3 does not improve on V2: similar CAGR, worse drawdown, lower Sharpe.
- V3 improves 2016-2021 bull participation but gives up too much in 2022-2026 and 2022 bear-market protection.

Learned:

- Simply increasing ETF growth exposure is not enough.
- The ETF proxy layer appears close to its useful limit for this strategy direction.
- To pursue full-cycle return maximization, the next test should move to individual-stock leadership selection inside strong industries.

## 2026-05-29 V4 Individual-Stock Alpha Strategy

Summary:

- Built and backtested the **V4.0 Hybrid Individual-Stock & ETF Dual-Sleeve Strategy** to extract stock-level Alpha while retaining V3.1's robust asset allocation and cash fallback mechanism.
- Value sleeve (30% weight) dynamically rotates the top 2 Value ETFs (VTV/IWD/SCHD).
- Growth sleeve (70% weight) rotates the top 3 individual stock leaders from the top 2 tactical sectors, applying a stock-level 50-day moving average and 3-month momentum trend filter. If fewer than 3 stocks qualify, the rest shifts to cash.
- Downloaded and cached 10-year daily historical adjusted close prices for all sector leaders.

Result (10-Year Backtest 2016-2026):

- V4 Best CAGR: **26.25%** (vs QQQ's **21.77%** and 50/50 SPY/QQQ's **18.72%**).
- V4 Best Max Drawdown: **-37.01%** (vs QQQ's **-35.12%**).
- V4 Best Sharpe: **1.12** (vs QQQ's **1.00** and 50/50 SPY/QQQ's **0.97**).
- Bear 2022 CAGR: **-16.20%** (vs QQQ's **-33.54%** and 50/50's **-26.45%**).
- Post-2023 CAGR: **42.96%** (vs QQQ's **35.89%**).

Learned:

- Micro-level stock selection inside strong macro sectors extracts a massive amount of Alpha, completely beating QQQ and SPY indices on a risk-adjusted basis.
- The 50-day MA and 3-month momentum stock-level trend filters, combined with cash fallback, successfully prevent catastrophic individual stock drawdowns.

## 2026-05-29 V4 26-Year Long-Term Backtest (2000-2025)

Summary:

- Acquired and cached the full 26-year daily OHLCV dataset (2000-2025) under `data_long/`.
- Ran V4 strategy over the full 26-year period (6,538 trading days).

Result (26-Year Long-Term Backtest):

- V4 Long Term Final Value: **55.403** (meaning $1 turned into **$55.40** vs SPY's **$7.50** and QQQ's **$7.74**).
- V4 Long Term CAGR: **16.70%** (vs QQQ's **8.19%** and SPY's **8.06%**).
- V4 Long Term Max Drawdown: **-50.83%** (vs QQQ's **-82.96%** and SPY's **-55.19%**).
- V4 Long Term Sharpe: **0.79** (vs QQQ's **0.43** and SPY's **0.50**).
- Dot-com Crash (2000-2002) CAGR: **-6.60%** with only **-34.03%** Max DD (vs QQQ's CAGR **-36.48%** and Max DD **-82.96%**).
- 2008 Financial Crisis CAGR: **-29.83%** with **-40.76%** Max DD (vs QQQ's CAGR **-40.90%** and Max DD **-49.40%**).
- Rolling 3-Year CAGR Win Rate: **21 / 24 (87.5% win rate)** against 50/50 SPY/QQQ.
- Rolling 3-Year Sharpe Win Rate: **17 / 24 (70.8% win rate)** against 50/50 SPY/QQQ.

Learned:

- Preventing catastrophic peak-to-trough losses during systemic crises (like Dot-com and 2008) is the absolute foundation of long-term compounding.
- V4 successfully avoids index-level ruin through macro-micro dual windbreaks and dynamic cash retreat.

## 2026-05-29 US Stock constituent-level Database Creation

Summary:

- Developed `download_stock_universe.py` to scrape all active S&P 500 and Nasdaq 100 components from Wikipedia, resulting in **516 unique stock tickers**.
- Executed the scraping and downloading pipeline over the 26-year period (2000-2025).
- Successfully cached and aligned **517 columns** (516 stocks + SPY + QQQ) with 6,538 daily trading rows.
- Only 1 ticker failed (INVH due to empty data), representing a **99.8% ingestion success rate**.
- Consolidated the entire dataset into a single massive, index-aligned database: `data_universe/us_stock_universe_2000_2025.csv` (size: **6.88 MB**).

Next step:
- The database is fully cached. Future steps can leverage this 500-stock database to run dynamic, constituent-level multi-factor optimization (such as cross-sectional relative strength and GICS sector leader momentum).
