# US Stock Daily Strategy Report Template

Purpose: reusable template for daily US equity strategy reports. This template integrates the existing market fear gate, concentration rules, hot-news review, and experimental institutional overlays.

Status: template. Fill it with current data each day; do not preserve stale values.

## Header

```text
Date:
Run time:
Session context: premarket / intraday / post-close
Data freshness:
Report type: daily strategy / execution refresh / post-close audit
```

## 1. Executive Decision

```text
Market regime:
Fear score:
Cash target:
New buys:
Reduce/exit items:
Primary themes:
Main risk:
```

Write one concise paragraph:

- What the strategy should do today.
- What it must avoid.
- Which existing position needs attention first.

### 1.1 Six-Dimensional Trade Decision

Every real-account trade recommendation must summarize these dimensions before the action:

| Dimension | Current read | Impact |
| --- | --- | --- |
| Market sentiment | SPY / QQQ / SMH / VIX / breadth |  |
| Theme strength | AI compute / interconnect / storage / cloud / application / defensive |  |
| Stock relative strength | Stock vs QQQ / SMH / direct peers |  |
| Technical entry quality | MA / VWAP / support / opening range / ATR / breakout level |  |
| Account constraints | HKD 20,000 capital, share size, cash, FX, fees, no margin |  |
| Exit / risk plan | Stop, no-chase line, failed-trigger rule, profit-taking level |  |

Final action must be one of:

```text
buy / conditional buy / wait / watch only / reduce / exit
```

If live quote data is unreliable or a required dimension is missing, default to `conditional buy`, `wait`, or `watch only`; do not present the trade as directly executable.

## 2. Market Fear Gate

Use `market-fear-technical-framework.md`.

| Indicator | Current state | Signal |
| --- | --- | --- |
| VIX level/change |  |  |
| VIX/VIX3M |  |  |
| SPY trend/drawdown |  |  |
| QQQ trend/drawdown |  |  |
| SMH/SOXX trend/drawdown |  |  |
| Breadth proxy |  |  |
| Credit proxy |  |  |

Decision:

```text
fear_regime:
risk_multiplier:
max_new_buy_exposure:
cash_floor:
```

## 3. Institutional Overlays

Use `institutional-overlays-daily-checklist.md` and `institutional-overlay-scorecard.md`.

```text
trend_aligned_entry:
flow_fragility:
AI_quality/capex_cycle:
factor_macro_exposure:
bottleneck_watch:
action impact:
```

### 3.1 Flow-Fragility Score

| Component | Score | Evidence |
| --- | ---: | --- |
| Narrow leadership |  |  |
| Semiconductor/AI concentration |  |  |
| Spot-up-vol-up or options crowding |  |  |
| Systematic/vol-control rebuild |  |  |
| Buyback window risk |  |  |
| Hedging complacency |  |  |
| Levered/thematic crowding |  |  |
| **Total** |  |  |

Interpretation:

```text
flow_fragility_state:
strategy_response:
```

## 4. Sector and Theme Leadership

| Theme / sector | Evidence | Action |
| --- | --- | --- |
| Broad indices |  |  |
| Technology / XLK |  |  |
| Semiconductors / SMH |  |  |
| AI compute |  |  |
| AI interconnect / optical |  |  |
| AI memory / storage |  |  |
| Cloud / AI factory |  |  |
| AI application / data owners |  |  |
| Physical AI / robotics |  |  |
| Defensive / non-AI leaders |  |  |

## 5. Real-Time Hot News Map

| News item | Source/time | Tickers | Theme | Direction | Price confirms? | Thesis impact |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Rules:

- News can explain or support price action.
- News does not override fear gate, trend, stop, or concentration rules.
- If news is bullish but price rejects it, mark as crowding or thesis-risk evidence.

## 6. Active Position Review

| Ticker | Role | AI class | Current action | Stop/reduce line | Trend/RS | Overlay impact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MRVL |  |  |  |  |  |  |  |
| AMD |  |  |  |  |  |  |  |
| WDC |  |  |  |  |  |  |  |
| STX |  |  |  |  |  |  |  |

Required language:

- State whether each active holding is `core hold`, `defensive hold`, `reduce-review`, `exit-review`, or `watch only`.
- If a stop was breached, do not call the position a normal hold unless an explicit rule override is recorded.

## 7. Candidate Ranking

Only include actionable candidates after the market fear gate and trend-aligned entry check.

| Rank | Ticker | Theme | AI class | Pullback entry | Breakout / confirmation entry | No-chase line | Risk line | Max size | Reason |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |  |  |

Required entry-price basis:

- Every buy candidate must identify the source of its limit price.
- Acceptable sources: 5/10/20/50-day moving averages, intraday VWAP, prior low/support, gap level, ATR-derived pullback range, or explicit risk-line offset.
- If the price is only a starter-test discount from the current quote, label it as `starter-test price`, not `technical support`.
- For the real HKD 20,000 account, prefer fewer technically justified orders over higher-probability fills.
- Every actionable candidate must include both a pullback path and a breakout/confirmation path. If one path is invalid, state why.
- Breakout/confirmation entries require market confirmation such as QQQ and SMH risk-on behavior plus stock-level confirmation such as reclaiming a trigger level, holding above opening range/VWAP, or outperforming SMH for 15-30 minutes.
- If the market is strong enough for a breakout entry but the stock is beyond the no-chase line, mark it watch-only instead of forcing a trade.

Rejected or watch-only names:

| Ticker | Reason rejected | Recheck trigger |
| --- | --- | --- |
|  |  |  |

## 8. Portfolio Construction

Use `portfolio-concentration-rules.md`.

```text
Active holdings count:
Theme count:
Cash:
Largest position:
Theme overlap:
Max new exposure allowed:
```

If holdings exceed the target range, identify weakest duplicate exposure.

## 9. Execution Checklist

| Priority | Action | Ticker | Path | Trigger | Size | Notes |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 |  |  | pullback / breakout / reduce / exit |  |  |  |

Rules:

- Stop-triggered positions come before new buys.
- Near-stop defensive holds come before watchlist expansion.
- No buy order is valid if it violates fear gate cash floor or concentration rules.
- No buy order is valid unless `Notes` or `Trigger` states the technical basis for the limit price.
- If live quote data is unreliable, do not derive a new buy price from a stale or suspect quote; use broker quote plus technical levels or defer.
- For strong repair/risk-on opens, evaluate breakout confirmation separately from pullback orders. Do not let a valid no-chase rule erase the breakout path without explaining the missed-trigger tradeoff.

## 10. Strategy Self-Review

Answer briefly:

- What did the strategy get right?
- What did it miss?
- Did concentration help or hurt?
- Did cash help or hurt?
- Did the fear gate over-protect or under-protect?
- Did institutional overlays add useful warning or noise?
- Which hypothesis was strengthened or weakened?

## 11. Memory Update

```text
Daily detail file:
Trade plan file:
Portfolio file:
Hypotheses updated:
Decisions updated:
References updated:
Open todos:
```

Stable decisions should remain unchanged unless validation supports promotion.
