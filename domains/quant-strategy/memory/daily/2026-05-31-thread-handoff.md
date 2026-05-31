# Thread Handoff: Restart US Stock Journey

Date: 2026-05-31

## Purpose

Use this file to restore working context when continuing the US stock strategy workflow in a new Codex thread.

## Portfolio Objective

- Hypothetical portfolio size: USD 20,000.
- Focus on US equities, especially Nasdaq 100 and S&P 500 constituents.
- Prefer concentrated holdings: 4 to 6 active stocks, hard maximum 8.
- Keep exposure within 2 to 3 themes. Select the strongest 1 to 2 names per theme.
- Distinguish executable limit orders from watchlist-only candidates.

## Current Strategy State

The current strategy combines:

1. The existing V5 dual-sleeve strategy.
2. A market fear risk governor.
3. Concentrated portfolio construction rules.
4. Daily broad-market monitoring.
5. Real-time hot-news analysis.
6. Daily reflection on whether the strategy requires repair.

The market fear gate is a risk governor, not an alpha selector. It uses VIX, VIX term structure, index trend/drawdown, breadth, credit proxies, and risk appetite ratios to classify the market as `normal`, `elevated`, `stress`, or `panic`.

## 2026 Validation Results

Using 2026 YTD data:

| Strategy | Return | Max Drawdown | Volatility | Sharpe | Sortino |
|---|---:|---:|---:|---:|---:|
| V5 original | +54.47% | -11.86% | 38.06% | 3.05 | 4.14 |
| V5 + market fear gate | +40.93% | -8.55% | 31.68% | 2.86 | 4.23 |

Conclusion:

- Keep the fear gate because it reduces drawdown and improves downside-adjusted quality.
- Do not use the fear gate to select stocks.
- Use it to control gross exposure and minimum cash.

## Latest Concentrated Recommendation

Core candidates:

| Ticker | Target Weight | Target Amount | Staged Limit Orders |
|---|---:|---:|---|
| MRVL | 13% | USD 2,600 | 202 / 199 / 195 |
| AMD | 12% | USD 2,400 | 511 / 505 / 492 |
| WDC | 10% | USD 2,000 | 528 / 520 / 508 |
| STX | 10% | USD 2,000 | 878 / 860 / 840 |

Conditional satellite:

- INTC: 3% to 5% only if the core names do not fill and the thesis remains valid.

Watchlist only:

- SNDK
- MU
- ARM
- ALAB
- CIEN

Before executing any recommendation, refresh real-time prices, latest news, the market fear state, and stop-loss conditions. The prices above are historical planning references, not standing instructions.

## Required Daily Workflow

Every weekday before 21:00 Asia/Shanghai:

1. Refresh real-time market data.
2. Evaluate the fear gate and minimum cash level.
3. Track existing recommendations against entry, add, reduce, and stop-loss conditions.
4. Rank major indices and sector ETFs.
5. Review AI infrastructure theme strength.
6. Review market emotion distribution and the strongest daily movers.
7. Analyze real-time hot news:
   - macro, rates, USD, oil, and geopolitics;
   - liquidity and risk appetite;
   - earnings and guidance;
   - AI infrastructure supply chain;
   - analyst ratings and institutional positioning.
8. For each important news item, record source, time, related tickers or sectors, bullish/bearish/mixed impact, price confirmation, and whether it is a one-day catalyst or a medium-term thesis change.
9. Produce explicit `buy`, `sell`, `hold`, and `watch only` actions with position size, staged limit prices, stop-loss level, and invalidation conditions.
10. Reflect on strategy errors and update AI-Memory.

## Automation State

Codex automation:

- Name: `每日美股策略建议`
- ID: `automation-2`
- Schedule: weekdays at 20:45 Asia/Shanghai
- Status: active
- Workspace: `D:\code\AI-Memory`

The automation prompt already includes real-time hot-news analysis as its first required module.

## Xiaohongshu Content Tracking

A public Xiaohongshu profile was reviewed as an idea-generation source. Public access exposed only a limited subset of post titles, not the full recent 50 posts or complete article text.

Use the captured framework as a watchlist input for:

- optical and interconnect bottlenecks;
- memory and storage;
- AI inference infrastructure;
- cloud and AI-factory supply-chain themes.

Do not treat Xiaohongshu content as a standalone trading signal.

## AI-Memory Plugin State

The local Codex plugin `ai-memory@personal` has been installed and enabled.

Included skill:

- `quant-stock-data`

Capabilities:

- Tencent real-time quote fetching;
- Sina quote fallback;
- historical market data guidance;
- symbol normalization;
- CN/HK/US resilient quote fetching.

Start a new Codex thread after plugin installation so the skill is loaded.

## Key Files

- `references/market-fear-technical-framework.md`
- `references/portfolio-concentration-rules.md`
- `references/daily-market-monitoring-framework.md`
- `references/xiaohongshu-mungerjun-content-framework.md`
- `experiments/2026-05-29-dual-sleeve-backtest/results/strategy_2026_ytd_validation.md`
- `experiments/2026-05-29-dual-sleeve-backtest/results/strategy_2026_ytd_fear_integrated_validation.md`
- `memory/daily/2026-05-29-concentrated-recommendation-restart.md`
- `memory/daily/2026-05-29-realtime-validation-order-plan.md`

## Pending Repository Changes

- `skills/quant-stock-data/SKILL.md`: corrected the wording from `量外策略` to `量化策略`.
- This handoff file must also be committed and pushed.

## New Thread Pickup Instruction

In the `重启美股之旅` thread, ask Codex:

`请读取 D:\code\AI-Memory\domains\quant-strategy\memory\daily\2026-05-31-thread-handoff.md，并基于最新实时行情、热点新闻和市场恐慌门控继续今天的美股策略分析。`
