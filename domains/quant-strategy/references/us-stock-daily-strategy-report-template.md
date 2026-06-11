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

| Rank | Ticker | Theme | AI class | Entry condition | Risk line | Max size | Reason |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |

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

| Priority | Action | Ticker | Trigger | Size | Notes |
| ---: | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |

Rules:

- Stop-triggered positions come before new buys.
- Near-stop defensive holds come before watchlist expansion.
- No buy order is valid if it violates fear gate cash floor or concentration rules.

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
