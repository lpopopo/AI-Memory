# Domain Summary: Quant Strategy

**Primary Goal:**
To develop and backtest a robust, full-cycle quantitative trading strategy focused on US equities (S&P 500 and Nasdaq 100), maximizing long-term CAGR while strictly controlling maximum drawdowns during systemic bear markets.

**Current State:**
We have successfully developed and backtested the **V4.0 Hybrid Individual-Stock & ETF Dual-Sleeve Strategy** over a 26-year period (2000-2025). It uses dynamic sector rotation and individual stock selection with macro-micro trend filters, achieving a 16.70% long-term CAGR with significantly lower drawdown than major indices. We have also built a 516-ticker US stock universe database for upcoming optimizations.

Recent qualitative overlay added: a public-content framework from Xiaohongshu account "美研芒格君" has been captured as an AI infrastructure bottleneck watchlist source. Treat it as idea generation for optical/interconnect, memory/storage, AI inference, and cloud/AI-factory subthemes, not as a standalone trading signal.

Latest institutional research overlay: a 2026-06-08 first-stage synthesis from AQR, Citadel Securities, GMO, and Man Group has been added as `references/institutional-market-research-framework.md`. It proposes trend-aligned entry discipline, flow-fragility monitoring, AI quality/capex-cycle classification, factor-macro exposure audits, and optical/interconnect watchlist expansion. These are hypotheses and monitoring upgrades for now, not stable trading decisions.

**Next Major Milestone:**
Leverage the newly scraped 500-stock database to run dynamic, constituent-level multi-factor optimizations (e.g., cross-sectional relative strength and GICS sector leader momentum).

**Risk Gate:**
Daily stock recommendations now require a market fear gate before position sizing. The framework classifies market state as `normal`, `elevated`, `stress`, or `panic` using VIX, VIX term structure, index drawdowns/trends, breadth, and credit proxies. See `references/market-fear-technical-framework.md`.

**Portfolio Construction:**
Current preference is concentrated: target 4 to 6 active stocks, hard maximum 8, across 2 to 3 themes. Daily recommendations should choose the strongest core names and avoid holding many overlapping stocks from the same subtheme. See `references/portfolio-concentration-rules.md`.

**Daily Monitoring:**
Daily work must include a broad market-monitoring and strategy self-review layer: index/risk state, sector/theme leadership, top winners/losers, recommended stock behavior, market emotion distribution, and whether the strategy needs repair. See `references/daily-market-monitoring-framework.md`.

Daily monitoring also includes real-time hot news analysis. News must be mapped to macro, sector, theme, and ticker-level catalysts, then checked against price action and risk controls before affecting recommendations.

**Latest Operational Status (2026-06-11):**
The 2026-06-11 layered review found no same-day 20:30 realtime/institutional monitor product; the same-day premarket strategy report classified market risk as `stress`. Local Tencent/Sina quote refresh failed again, but public StockAnalysis pages provided the latest stable 2026-06-10 U.S. regular-session close and after-hours snapshots. Current real holdings remain real-account only: `MRVL` 1 share bought at `USD 252.00`; using the 2026-06-10 close `252.59`, unrealized P/L is about `USD +0.59` / `+0.23%` before fees and FX. MRVL after-hours was `244.55`, below the `245` review line, but this is not a formal close trigger. No broker action, new real trade, or new simulated fill was recorded. New buys remain blocked because market state is `stress`, `flow_fragility_state` is `acute` or `elevated / acute watch`, and `trend_aligned_entry_state` is `trend_broken`. Legacy model-only AMD remains `reduce-review`; WDC and STX should be treated as historical model/replay reduce-review after their 2026-06-10 closes fell below old 500/835 risk lines, not as current real holdings. No stable decision was promoted.

Current portfolio scope update: per user instruction on 2026-06-11, stop routine tracking of the retired USD 20,000 model/paper ledger. Daily execution, post-close audits, NAV, stop-trigger tables, and risk reviews should focus only on real-account holdings confirmed by the user or broker. Historical model/replay records should be used only when the user explicitly asks for replay/backtest analysis.

Watchlist update: per user request on 2026-06-11, add `TSLA`, `NOK`, `QCOM`, `RKLB`, `RDW`, `INTC`, and `ORCL` to monitoring. `TSLA` remains physical AI/autonomous systems watch-only; `QCOM` is edge inference/device AI watch-only; `NOK` is telecom/network infrastructure and private-network edge-AI watch-only; `RKLB` and `RDW` are space / satellite / space-infrastructure watch/satellite only; `INTC` is AI compute / AI PC / foundry-turnaround watch/satellite only; `ORCL` is cloud / AI factory / database infrastructure watch-only. This is a universe update, not a buy recommendation.

**Prior Operational Status (2026-06-10):**
Per user instruction on 2026-06-10, the prior USD 20,000 strategy-tracking model portfolio is retired from current holdings tracking and should no longer be treated as an active current portfolio. Current holdings should be read from real-account confirmations only. The only confirmed real-account position is `1` share of `MRVL` bought at `USD 252.00` using a real HKD 20,000 account baseline. The latest formal reference close for that position is `MRVL 266.88` from the 2026-06-09 U.S. regular-session close, implying about `USD +14.88` / `+5.90%` unrealized P/L before fees and FX. The real-account state remains `starter defensive hold`; no automatic add is authorized. Risk review lines remain: MRVL official close `<245` triggers cut-or-wait review; MRVL near `<235` with weak QQQ/SMH indicates starter thesis failure. Any old MRVL `315` real-account limit order still needs user-side/broker confirmation before it is recorded. The proposed institutional/theme-crowding overlays remain experimental and are not yet stable decisions.

## Key Links
- [Decisions](decisions.md)
- [Daily Summaries](daily-summaries.md)
