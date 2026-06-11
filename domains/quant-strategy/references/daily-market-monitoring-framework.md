# Daily Market Monitoring Framework

Purpose: define the daily market-monitoring layer that runs alongside stock recommendation tracking.

Daily work should not only review recommended holdings. It must also observe the full market: which sectors are leading, where money is rotating, how market emotion is distributed, and whether the strategy is missing or misreading the active theme.

## Daily Monitoring Questions

1. What did the market reward today?
2. Which sectors, themes, and industries led or lagged?
3. Was leadership broad or narrow?
4. Did speculative appetite expand or contract?
5. Did recommended stocks behave better or worse than their themes?
6. Did the strategy miss an obvious leading theme?
7. Did the strategy overconcentrate in a fading theme?
8. Did market fear indicators confirm, warn, or contradict stock-level signals?
9. Which real-time news items explain today's price action?
10. Does the strategy need a parameter, universe, risk, or execution adjustment?

## Required Daily Sections

### 1. Index and Risk State

Track:

- SPY
- QQQ
- IWM
- DIA
- SMH
- VIX
- VIX/VIX3M if available
- HYG/LQD if available

Summarize:

- Risk-on or risk-off.
- Growth versus value.
- Large-cap versus small-cap.
- Semiconductor leadership versus broad Nasdaq.
- Credit appetite.

### 2. Sector and Theme Leadership

Track sector ETFs:

- XLK technology
- XLC communication services
- XLY consumer discretionary
- XLI industrials
- XLF financials
- XLV healthcare
- XLE energy
- XLB materials
- XLU utilities
- XLRE real estate
- XLP consumer staples
- SMH or SOXX semiconductors

Track current AI infrastructure themes:

- AI compute: NVDA, AMD, AVGO, ARM, INTC
- AI compute / edge inference: NVDA, AMD, AVGO, ARM, QCOM, INTC
- AI interconnect / optical / networking: MRVL, ALAB, LITE, COHR, CIEN, NOK, GLW
- AI memory / storage: MU, WDC, STX, SNDK
- Cloud / AI factory: AMZN, MSFT, META, GOOGL, ORCL, CRWV, NBIS
- Space / satellite / edge-AI infrastructure: RKLB, RDW
- Physical AI / autonomous systems: TSLA, TER, ROK, DE, ISRG

### 3. Best and Worst Movers

Daily report should identify:

- Top 5 to 10 notable winners from the active universe.
- Top 5 to 10 notable losers from the active universe.
- Whether moves came from earnings, guidance, news, sector rotation, or pure momentum.
- Whether winners belong to our selected themes or reveal a new theme.

### 4. Real-Time Hot News Analysis

Daily monitoring must include a real-time hot-news layer.

Sources can include public market news, earnings releases, guidance headlines, sector news, analyst actions, macro data, rates, Fed comments, geopolitics, and company-specific announcements.

For each meaningful news item, record:

- Time or recency if available.
- Source or outlet if available.
- Related ticker(s).
- Related sector/theme.
- Whether it is bullish, bearish, or mixed.
- Whether price action confirms or rejects the news.
- Whether the news is a one-day catalyst or changes the medium-term thesis.

Required news categories:

- Macro: CPI/PCE/jobs/Fed/rates/dollar/oil/geopolitics.
- Market structure: VIX, liquidity, credit stress, broad risk-on/risk-off.
- Earnings/guidance: company results, capex, margins, backlog, demand signals.
- AI infrastructure: compute, optical/interconnect, memory/storage, cloud capex, power.
- Analyst/positioning: upgrades/downgrades, target changes, crowded trade warnings.

News should not override price and risk controls by itself. Use news to explain moves, identify new watchlist candidates, and decide whether a thesis is strengthened or weakened.

### 5. Recommended Stock Review

For every active recommendation:

- Today return.
- Relative performance versus QQQ and relevant theme ETF.
- Whether entry conditions still hold.
- Whether stop, reduce, hold, or add rules triggered.
- Whether position size remains appropriate under market fear gate.

### 6. Strategy Self-Review

Daily reflection must include:

- What did the strategy get right?
- What did it miss?
- Was concentration helpful or harmful?
- Did cash level help or hurt?
- Did market fear gate over-protect or under-protect?
- Did any stop-loss or limit-order logic need adjustment?
- Should any theme be promoted, demoted, or removed from watchlist?
- Did real-time news reveal a catalyst that our purely technical scan missed?

### 7. Experimental Institutional Overlays

When time and data allow, include the experimental institutional overlay block from `institutional-overlays-daily-checklist.md`. Use `institutional-overlay-scorecard.md` for consistent scoring and `us-stock-daily-strategy-report-template.md` when producing a full daily report.

Track:

- `trend_aligned_entry`: whether any buy/add idea is confirmed by trend and relative strength rather than merely cheaper.
- `flow_fragility`: whether leadership is narrow, crowded, options-driven, or vulnerable to systematic-flow reversal.
- `AI_quality/capex_cycle`: whether AI candidates are platform/hyperscaler, diversified supplier, cyclical supplier, application/data owner, or speculative bottleneck beneficiary.
- `factor_macro_exposure`: whether the portfolio is implicitly long duration/growth, inflation/value, momentum, quality, or a concentrated theme.
- `bottleneck_watch`: whether optical/interconnect, power/cooling, memory/storage, network, or custom-silicon bottleneck evidence changed.

These overlays are not stable trading decisions yet. Use them to improve monitoring, sizing caution, and hypothesis tracking.

### 8. Memory Update Rules

- Daily observations go to `memory/daily/YYYY-MM-DD-*.md`.
- One short line goes to `memory/daily-summaries.md`.
- Repeated evidence across days can update `hypotheses.md`.
- Stable validated process changes can update `decisions.md`.
- External source or universe definitions go to `references/`.

## Output Style

Daily market monitoring should be concise but complete:

- Start with market regime and dominant themes.
- Then list sector/theme leaders.
- Then summarize real-time hot news and map it to themes.
- Then evaluate recommended stocks.
- Then produce action changes.
- End with strategy reflection and memory updates.
