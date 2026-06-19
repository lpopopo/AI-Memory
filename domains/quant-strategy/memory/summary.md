# Domain Summary: Quant Strategy

**Primary Goal:**
To develop and backtest a robust, full-cycle quantitative trading strategy focused on US equities (S&P 500 and Nasdaq 100), maximizing long-term CAGR while strictly controlling maximum drawdowns during systemic bear markets.

**Current State:**
We have successfully developed and backtested the **V4.0 Hybrid Individual-Stock & ETF Dual-Sleeve Strategy** over a 26-year period (2000-2025). It uses dynamic sector rotation and individual stock selection with macro-micro trend filters, achieving a 16.70% long-term CAGR with significantly lower drawdown than major indices. We have also built a 516-ticker US stock universe database for upcoming optimizations.

Recent qualitative overlay added: a public-content framework from Xiaohongshu account "美研芒格君" and X account `@Kay2289123` has been captured as an AI infrastructure bottleneck watchlist source. Treat it as idea generation for optical/interconnect, memory/storage, AI inference, AI factory / cloud, server infrastructure, and semiconductor equipment subthemes, not as a standalone trading signal.

Latest institutional research overlay: a 2026-06-08 first-stage synthesis from AQR, Citadel Securities, GMO, and Man Group has been added as `references/institutional-market-research-framework.md`. It proposes trend-aligned entry discipline, flow-fragility monitoring, AI quality/capex-cycle classification, factor-macro exposure audits, and optical/interconnect watchlist expansion. These are hypotheses and monitoring upgrades for now, not stable trading decisions.

**Next Major Milestone:**
Leverage the newly scraped 500-stock database to run dynamic, constituent-level multi-factor optimizations (e.g., cross-sectional relative strength and GICS sector leader momentum).

**Risk Gate:**
Daily stock recommendations now require a market fear gate before position sizing. The framework classifies market state as `normal`, `elevated`, `stress`, or `panic` using VIX, VIX term structure, index drawdowns/trends, breadth, and credit proxies. See `references/market-fear-technical-framework.md`.

**Portfolio Construction:**
Current preference is concentrated: target 4 to 6 active stocks, hard maximum 8, across 2 to 3 themes. Daily recommendations should choose the strongest core names and avoid holding many overlapping stocks from the same subtheme. See `references/portfolio-concentration-rules.md`.

**Aggressive Satellite Module:**
Per 2026-06-11 strategy update, the portfolio framework now includes a Double-Radar satellite module for 6-12 month potential double or multi-bagger candidates. V5 Optimal remains the core engine; default research mix is `75%` V5 core plus `25%` Double-Radar Top5 gated. The radar requires strong 50/200-day trend, 63/126-day momentum, high volatility, limited short-term extension, and a bullish QQQ regime gate. A 10-year current-S&P-500 approximation test showed the combined approach at CAGR `28.09%`, max drawdown `-30.70%`, Sharpe `1.24`, versus V5-only CAGR `25.95%` and SPY CAGR `14.82%`. See `references/double-radar-satellite-strategy.md`.

**Daily Monitoring:**
Daily work must include a broad market-monitoring and strategy self-review layer: index/risk state, sector/theme leadership, top winners/losers, recommended stock behavior, market emotion distribution, and whether the strategy needs repair. See `references/daily-market-monitoring-framework.md`.

Daily monitoring also includes real-time hot news analysis. News must be mapped to macro, sector, theme, and ticker-level catalysts, then checked against price action and risk controls before affecting recommendations.

**Latest Operational Status (2026-06-12):**
The 2026-06-11 U.S. close produced a broad rebound: AP reported S&P 500 +1.8%, Dow +1.9%, Nasdaq +2.5%, and Russell 2000 +3.0%; Cboe VIX spot improved to about `19.89`. Current confirmed real-account equity holdings remain none after the `MRVL` sale at `USD 267.020`; gross realized P/L on that closed trade remains about `USD +15.020` / `+5.96%` before fees and FX. MRVL closed around `280.71` after the sale, but this should not trigger automatic chase-buying. Fear improves from `stress` toward `elevated / repair`, yet new buys still require pullback/reclaim or second-day confirmation. MRVL and the expanded watchlist remain observation-only until trend and account-level entry discipline confirm. No stable strategy decision was promoted.

Current portfolio scope update: per user instruction on 2026-06-11, stop routine tracking of the retired USD 20,000 model/paper ledger. Daily execution, post-close audits, NAV, stop-trigger tables, and risk reviews should focus only on real-account holdings confirmed by the user or broker. Historical model/replay records should be used only when the user explicitly asks for replay/backtest analysis.

Watchlist update: per user request on 2026-06-11 and 2026-06-17, add `TSLA`, `NOK`, `QCOM`, `RKLB`, `RDW`, `INTC`, `ORCL`, and `SPCX` / SpaceX to monitoring. `TSLA` remains physical AI/autonomous systems watch-only; `QCOM` is edge inference/device AI watch-only; `NOK` is telecom/network infrastructure and private-network edge-AI watch-only; `RKLB` and `RDW` are space / satellite / space-infrastructure watch/satellite only; `SPCX` / SpaceX is space-launch / Starlink / IPO-liquidity sentiment watch only and should be treated as a high-volatility theme anchor, not an automatic buy signal; `INTC` is AI compute / AI PC / foundry-turnaround watch/satellite only; `ORCL` is cloud / AI factory / database infrastructure watch-only. This is a universe update, not a buy recommendation.

Watchlist update: per user request on 2026-06-18, add `DRAM` to monitoring as the Roundhill Memory ETF / memory-storage thematic basket proxy. Treat it as an ETF-level read-through for the AI memory/storage bottleneck theme and a possible lower-single-name-risk alternative to chasing individual storage/memory names such as WDC, STX, MU, or SNDK. This is a universe update, not a buy recommendation; use price action, market fear gate, ETF holdings/structure, liquidity, spread, and account concentration checks before any trade role.

Watchlist update: per user request on 2026-06-18, add `SMCI` to monitoring under AI server / rack-scale infrastructure / hardware integration. Treat it as a high-volatility AI infrastructure execution and margin-risk watch name, useful for tracking AI server demand, rack-scale deployment, supply-chain integration, liquid cooling, and competitive pressure. This is a universe update, not a buy recommendation; require trend confirmation, accounting / governance risk review, margin evidence, liquidity, and concentration checks before any trade role.

Watchlist update: per user request on 2026-06-19 after logged-in Chrome reading of `美研芒格君` / `Kay2289123` Xiaohongshu carousel and X articles, add `CRDO`, `TER`, `MXL`, `AXTI`, and `TTMI` to monitoring as AI bottleneck subtheme candidates. `CRDO` is an AEC / high-speed connectivity transmission watch name; `TER` is an HBM / insertion / system-level-test validation watch name; `MXL` and `AXTI` are optical / InP / interconnect component watch names; `TTMI` is an AI infrastructure / PCB / interconnect "shovel seller" watch name. These are source-driven candidate additions only, not buy recommendations; require independent business validation, liquidity, spread, valuation, daily K-line structure, and theme-crowding checks before any trade role.

**Prior Operational Status (2026-06-10):**
Per user instruction on 2026-06-10, the prior USD 20,000 strategy-tracking model portfolio is retired from current holdings tracking and should no longer be treated as an active current portfolio. Current holdings should be read from real-account confirmations only. The only confirmed real-account position is `1` share of `MRVL` bought at `USD 252.00` using a real HKD 20,000 account baseline. The latest formal reference close for that position is `MRVL 266.88` from the 2026-06-09 U.S. regular-session close, implying about `USD +14.88` / `+5.90%` unrealized P/L before fees and FX. The real-account state remains `starter defensive hold`; no automatic add is authorized. Risk review lines remain: MRVL official close `<245` triggers cut-or-wait review; MRVL near `<235` with weak QQQ/SMH indicates starter thesis failure. Any old MRVL `315` real-account limit order still needs user-side/broker confirmation before it is recorded. The proposed institutional/theme-crowding overlays remain experimental and are not yet stable decisions.

## Key Links
- [Decisions](decisions.md)
- [Daily Summaries](daily-summaries.md)
