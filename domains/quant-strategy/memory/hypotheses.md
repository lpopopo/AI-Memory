# Hypotheses

## 2026-05-29

### H1: US-stock-first universe improves strategy reliability

The strategy should focus on US equities first because market data availability, liquidity, disclosure quality, and backtest tooling are generally stronger than for mixed-market experiments.

Validation needed:

- Confirm stable daily OHLCV source.
- Confirm survivorship-bias-aware universe source or define an acceptable starting universe.
- Backtest against SPY and QQQ benchmarks.

### H2: Multi-factor confirmation is safer than single-signal chasing

Initial strategy should require at least trend, relative strength, and risk filter confirmation before entry.

Validation needed:

- Compare single-factor momentum against combined trend plus relative strength.
- Measure drawdown, turnover, win rate, and benchmark-relative return.

### H3: Alternative or external signals should be secondary at first

The first usable version should not depend on hard-to-verify alternative data. Price, volume, liquidity, fundamentals, and event calendars should come before sentiment or news-derived signals.

Validation needed:

- Build a price-volume baseline.
- Add fundamentals/events only after baseline backtest is stable.

### H4: Dual-sleeve allocation can balance compounding and opportunity capture

A 50% value sleeve plus 50% hot-industry momentum sleeve may produce better behavioral and risk balance than a pure momentum or pure value strategy.

Validation needed:

- Backtest value sleeve, tactical sleeve, and combined portfolio separately.
- Compare against SPY, QQQ, and a 50/50 SPY/QQQ benchmark.
- Measure whether combined drawdown is lower than the tactical sleeve alone.
- Check whether both sleeves are accidentally concentrated in the same sectors or factors.

Initial V0 result:

- ETF-proxy V0 did reduce drawdown versus SPY and QQQ.
- ETF-proxy V0 did not outperform SPY, QQQ, or 50/50 SPY/QQQ on CAGR or Sharpe.
- Hypothesis remains open; needs V1 with true scoring models before acceptance or rejection.

V1 optimization result:

- V1 improved strongly over V0: CAGR 18.14% and Sharpe 1.00.
- V1 still did not clearly beat 50/50 SPY/QQQ on CAGR or drawdown.
- V1's best result depended on QQQ fallback, so the dual-sleeve thesis remains unproven.
- Hypothesis remains open and needs walk-forward validation plus individual-stock sleeves.

Revalidation result:

- V1 showed stronger performance in 2022-2026 and much better 2022 drawdown control.
- V1 underperformed in 2016-2021 bull-market conditions.
- Hypothesis should be reframed: dual-sleeve ETF V1 may be useful as a regime-aware drawdown-control strategy, but not yet as a full-cycle return-maximizing strategy.

V2 result:

- V2 improved bull-market participation by shifting to 35% value / 65% tactical-growth during confirmed QQQ bull regimes.
- V2 slightly beat 50/50 SPY/QQQ on full-period CAGR and Sharpe, while drawdown remained slightly worse.
- V2 still did not beat QQQ on full-period CAGR.
- Hypothesis remains promising but not proven; next evidence should come from walk-forward validation and individual-stock implementation.

V2 robustness revalidation:

- Rolling 3-year windows show V2 beats 50/50 SPY/QQQ on CAGR in 4 of 9 windows, drawdown in 6 of 9 windows, and Sharpe in 4 of 9 windows.
- Evidence supports V2 as a defensive/regime-aware ETF strategy more than as a consistently superior return engine.
- Hypothesis remains open; individual-stock sleeves or a bull accelerator are needed before treating the strategy as superior.

V3 result:

- A stronger ETF-level bull accelerator did not improve on V2.
- V3 matched V2's full-period CAGR but had worse drawdown and lower Sharpe.
- Evidence now points toward individual-stock leadership selection as the next required improvement path.
