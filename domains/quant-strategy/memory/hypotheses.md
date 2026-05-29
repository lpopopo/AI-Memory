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
