# Decisions

## 2026-05-29

- Data source baseline: Tencent Smartbox for fuzzy search, Tencent quotes as primary, Sina quotes as fallback.
- All quote text responses should be decoded as GBK.
- Strategy analysis should consume normalized quote objects rather than raw endpoint payloads.
- Quote outputs should preserve `source` for debugging and data-quality review.
- Runtime caveat: old Node can fetch Tencent data but may not decode GBK Chinese names correctly without a decoder.
- Repository memory model: use layered storage with root-level `docs/`, `domains/`, `skills/`, `templates/`, and `archive/`. Stable conclusions live in `memory/decisions.md`; running notes live in `memory/strategy-log.md`; factual contracts live in `references/`; reusable workflows live in `skills/`.
- Strategy market focus: prioritize US-listed stocks and ETFs first. Treat A/H/other markets as later extensions, not the initial strategy target.
- Initial strategy direction: build a daily, long-only, medium-frequency US equity strategy before adding complex alternative data or intraday execution.
- Portfolio design: use a dual-sleeve structure with 50% value-investing allocation and 50% hot-industry momentum allocation. Each sleeve should have independent selection, exit, and review rules.
- Market panic framework: daily strategy analysis must include a market fear gate before stock-level recommendations. Use VIX level/spike/term structure, SPY/QQQ/SMH drawdown and trend, breadth proxies, and credit-risk proxies to classify `normal`, `elevated`, `stress`, or `panic`; then scale new buy exposure and cash floor accordingly.
- Market fear gate validation: 2026 YTD test supports keeping the gate as a risk governor. It lowered V5 return but improved max drawdown and volatility while maintaining benchmark outperformance. Do not use it as a stock selector; use it for exposure scaling, cash floor, and no-new-buy decisions.
- Portfolio concentration preference: daily recommendations should target 4 to 6 active stocks, hard maximum 8, across 2 to 3 themes. Avoid broad baskets of many similar names; pick the strongest core names and keep overlapping names on watchlist.
- Daily market monitoring requirement: each trading day must review not only recommended stocks, but also broad market regime, sector/theme leadership, best/worst movers, emotion distribution, and whether the strategy missed, overconcentrated, or needs repair.
- Real-time hot news requirement: daily market monitoring must include current news catalysts and map them to macro, sector, theme, and ticker-level implications. News explains and validates price action but does not override technical filters, market fear gate, or stop rules by itself.

## 2026-06-11

- Real-account order-price discipline: every new buy limit recommendation must state its technical price basis. Acceptable bases include 5/10/20/50-day moving averages, intraday VWAP, prior low/support, gap level, ATR-derived pullback range, or explicit risk-line offset. A buy price that is only an intuition/discount from the current quote must be labeled as a starter-test price, not a technical support price.
- For the real HKD 20,000 account, single-share sizing makes entry quality more important. New buys should prefer technically justified levels over high-probability fills, and should avoid using margin/financing. If a recommended buy would consume more than roughly 10%-15% of account capital or lacks a clear technical basis, it should default to watch-only.
