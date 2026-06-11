# Institutional Overlays Backtest Plan

Date created: 2026-06-08

Purpose: define how to validate the institutional research overlays before promoting them to stable strategy decisions.

## Candidate Overlays

### Overlay A: Trend-Aligned Support Buy

Question:

- Does waiting for reclaim/relative-strength confirmation beat plain pullback limit buying?

Variants:

- `plain_pullback`: buy when price falls to support/limit zone.
- `support_hold`: buy only if price holds support by close.
- `reclaim`: buy only after price reclaims 20-day or 50-day trend level.
- `reclaim_rs`: buy only after reclaim plus relative strength versus QQQ/theme peers improves.
- `fear_gated_reclaim_rs`: add market fear gate sizing to `reclaim_rs`.

Metrics:

- CAGR.
- Max drawdown.
- False-entry rate.
- Average 5/10/20-day post-entry return.
- Missed-rebound cost.
- Turnover and slippage sensitivity.

### Overlay B: Flow-Fragility Filter

Question:

- Can a crowding/market-structure overlay reduce drawdown after crowded AI/semiconductor rallies without exiting too early?

Proxy inputs:

- Breadth: RSP/SPY, equal-weight tech versus cap-weight tech if available.
- Theme concentration: SMH or SOXX versus QQQ and number of AI/semiconductor winners.
- Volatility: VIX level/change and Nasdaq/semiconductor implied-vol behavior if available.
- Options/crowding: put/call, skew, options volume, or substitute public proxies when direct data is unavailable.
- Flows: buyback calendar, ETF flow proxies, levered ETF AUM if available.
- Trend crowding: very high 20/63-day return with narrowing breadth.

Backtest behavior:

- If `flow_fragility = elevated`, reduce new position size by 25%-50%.
- If `flow_fragility = acute`, block new chase buys and allow only reclaim-after-pullback entries.
- Existing positions can be trimmed only if price action also weakens or profit-protection rules trigger.

Metrics:

- Max drawdown during AI/semiconductor reversals.
- Return captured during continued rallies.
- Number of blocked winners versus blocked losers.
- Impact on cash drag.

### Overlay C: AI Quality / Capex-Cycle Score

Question:

- Does ranking AI candidates by business resilience improve returns and reduce gap risk?

Score components:

- Business class: platform, diversified supplier, cyclical supplier, application/data owner, speculative bottleneck.
- Balance sheet strength.
- Customer concentration.
- Gross margin stability.
- Non-AI revenue base.
- Evidence type: earnings/guidance/backlog is stronger than product/partnership/narrative.
- Relative strength confirmation.

Backtest behavior:

- Use quality score as a tie-breaker inside theme selection.
- Lower max weight for high capex-cycle sensitivity names.
- Require stricter trend confirmation for speculative bottleneck names.

Metrics:

- Post-signal returns by class.
- Drawdown by class.
- Gap-down frequency after capex scares or earnings misses.
- Whether the score improves selection among MRVL/AMD/WDC/STX/MU/NVDA/AVGO-style candidates.

### Overlay D: Factor-Macro Exposure Audit

Question:

- Does tracking hidden macro exposure prevent both sleeves from failing together?

Inputs:

- Growth/duration exposure.
- Value/inflation exposure.
- Momentum exposure.
- Quality exposure.
- Sector/theme concentration.
- Sleeve-level return correlation and drawdown overlap.

Backtest behavior:

- Record diagnostics first without changing trades.
- Later test exposure caps if diagnostics predict drawdown clusters.

Metrics:

- Sleeve-level drawdown overlap.
- Conditional correlations during VIX spikes, volatility collapses, inflation shocks, and rate shocks.
- Frequency of "diversified on paper, same risk in practice" episodes.

## Validation Phases

### Phase 1: Diagnostic Only

- Add overlay fields to daily reports.
- Do not change historical trades.
- Collect at least 10-20 trading days of observations if doing live monitoring.
- Use `institutional-overlay-data-proxies.md` when direct options, CTA, buyback, or levered-ETF data is unavailable.

### Phase 2: Historical Replay

- Replay 2020, 2022, 2024, and 2026 YTD if data is available.
- Focus on crisis rebounds, AI rallies, semiconductor reversals, and rate/inflation shocks.
- First replay target: 2026-06-05 AI/semiconductor/storage synchronized drawdown. See `memory/daily/2026-06-08-institutional-overlay-replay-2026-06-05.md`.
- Use `institutional-overlay-replay-protocol.md` for baseline-versus-overlay comparison rules and `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` for the replay ledger.

### Phase 3: Rule Integration

- Promote only overlays that improve either drawdown or risk-adjusted return without excessive cash drag.
- Add stable rule text to `memory/decisions.md` only after validation.

## Promotion Threshold

An overlay can become a stable decision if it satisfies at least two of:

- Reduces max drawdown by 10% or more without reducing CAGR by more than 5% relative.
- Improves Sharpe or Sortino in at least two major regimes.
- Blocks more false entries than true winners in historical replay.
- Produces repeated useful daily warnings that match later price action.
