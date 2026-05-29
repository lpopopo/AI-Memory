# Domain Summary: Quant Strategy

**Primary Goal:**
To develop and backtest a robust, full-cycle quantitative trading strategy focused on US equities (S&P 500 and Nasdaq 100), maximizing long-term CAGR while strictly controlling maximum drawdowns during systemic bear markets.

**Current State:**
We have successfully developed and backtested the **V4.0 Hybrid Individual-Stock & ETF Dual-Sleeve Strategy** over a 26-year period (2000-2025). It uses dynamic sector rotation and individual stock selection with macro-micro trend filters, achieving a 16.70% long-term CAGR with significantly lower drawdown than major indices. We have also built a 516-ticker US stock universe database for upcoming optimizations.

Recent qualitative overlay added: a public-content framework from Xiaohongshu account "美研芒格君" has been captured as an AI infrastructure bottleneck watchlist source. Treat it as idea generation for optical/interconnect, memory/storage, AI inference, and cloud/AI-factory subthemes, not as a standalone trading signal.

**Next Major Milestone:**
Leverage the newly scraped 500-stock database to run dynamic, constituent-level multi-factor optimizations (e.g., cross-sectional relative strength and GICS sector leader momentum).

**Risk Gate:**
Daily stock recommendations now require a market fear gate before position sizing. The framework classifies market state as `normal`, `elevated`, `stress`, or `panic` using VIX, VIX term structure, index drawdowns/trends, breadth, and credit proxies. See `references/market-fear-technical-framework.md`.

**Portfolio Construction:**
Current preference is concentrated: target 4 to 6 active stocks, hard maximum 8, across 2 to 3 themes. Daily recommendations should choose the strongest core names and avoid holding many overlapping stocks from the same subtheme. See `references/portfolio-concentration-rules.md`.

**Daily Monitoring:**
Daily work must include a broad market-monitoring and strategy self-review layer: index/risk state, sector/theme leadership, top winners/losers, recommended stock behavior, market emotion distribution, and whether the strategy needs repair. See `references/daily-market-monitoring-framework.md`.

Daily monitoring also includes real-time hot news analysis. News must be mapped to macro, sector, theme, and ticker-level catalysts, then checked against price action and risk controls before affecting recommendations.

## Key Links
- [Decisions](decisions.md)
- [Daily Summaries](daily-summaries.md)
