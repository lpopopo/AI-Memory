# Institutional Overlay Scorecard

Date created: 2026-06-08

Purpose: provide simple scoring rules for the experimental institutional overlays. The scorecard is designed for daily use before more formal backtests exist.

Status: experimental. Scores are advisory and should not override market fear gate, stops, or portfolio concentration rules.

Use `institutional-overlay-data-proxies.md` when direct market-structure data is unavailable.

## 1. Flow-Fragility Score

Score each component from 0 to 2.

| Component | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Narrow leadership | Broad participation | Mixed breadth | Index gains driven by very few AI/mega-cap leaders |
| Semiconductor/AI concentration | SMH/SOXX participation is healthy | AI leads but breadth is uneven | AI/semiconductors dominate gains while most market lags |
| Options/crowding behavior | Normal vol/skew behavior | Some upside call demand | Spot-up-vol-up, heavy call demand, or visibly crowded upside chase |
| Systematic/vol-control exposure | Exposure likely low | Exposure rebuilt moderately | Exposure likely high after sharp rally and vol compression |
| Buyback window support | Open and supportive | Transition risk | Blackout or weakening buyback support |
| Hedging complacency | Hedges normal or expensive | Hedges cheaper | Downside protection appears unusually cheap/under-owned |
| Levered/thematic crowding | Low | Moderate | Levered ETF/thematic flow concentration in owned theme |

Interpretation:

| Total | State | Daily use |
| ---: | --- | --- |
| 0-3 | low | Normal strategy rules apply |
| 4-6 | medium | Avoid chase buys; require clean entries |
| 7-10 | elevated | New buys only on reclaim/support confirmation; consider profit protection |
| 11+ | acute | No chase buys; run portfolio-level correlated-risk review |

Action constraints:

- `medium` does not block buys by itself.
- `elevated` blocks momentum chase entries but can allow reclaim-after-pullback entries if market fear gate allows.
- `acute` blocks new AI/semiconductor adds unless explicitly overridden after post-close review.

## 2. Trend-Aligned Entry Score

Score each component from 0 to 1.

| Component | Score 1 condition |
| --- | --- |
| Market fear gate permits exposure | Regime and cash floor allow a buy |
| Price trend valid | Above or reclaiming key 20/50-day trend level |
| Relative strength valid | Improving versus QQQ and theme peers |
| Pullback quality valid | Pullback is orderly, not a high-volume breakdown |
| Catalyst confirmed | News/earnings/capex evidence is confirmed by price action |

Interpretation:

| Total | State | Use |
| ---: | --- | --- |
| 0-2 | trend_broken | No buy; review stop/reduce if held |
| 3 | cheap_but_unconfirmed | Watch only |
| 4-5 | trend_aligned | Candidate can enter ranking |

## 3. AI Quality / Capex-Cycle Score

Score business resilience from 0 to 10.

| Component | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Business class | Speculative bottleneck | Cyclical supplier / application unproven | Platform or diversified supplier |
| Revenue evidence | Narrative/product only | Guidance/backlog partial | Real revenue/earnings revisions visible |
| Customer concentration | High/unknown | Medium | Low/diversified |
| Balance sheet/financing | Weak or capex-heavy financing risk | Acceptable | Strong cash flow and balance sheet |
| Margin resilience | Volatile/unknown | Moderate | Stable or improving |

Interpretation:

| Total | Role bias |
| ---: | --- |
| 0-3 | Watchlist only |
| 4-5 | Small satellite only |
| 6-7 | Tactical candidate if trend confirms |
| 8-10 | Core candidate if market regime and valuation allow |

Important caveat:

- High quality does not mean buy. It only allows a higher role if trend, fear gate, valuation, and concentration rules agree.

## 4. Factor-Macro Exposure Flags

Use flags rather than a single score.

| Flag | Trigger examples | Response |
| --- | --- | --- |
| growth_duration_high | Portfolio concentrated in AI/growth before CPI/Fed/rate shock | Reduce chase buys; demand stronger confirmation |
| momentum_reversal_high | Strong momentum after panic recovery and falling VIX | Watch for rotation away from prior winners |
| inflation_value_tilt_high | Value/cyclicals dominate sleeve exposure | Check inflation/rate regime and cyclicality |
| consumer_backstop_fragility | AI/large-cap leadership is narrow while mass-market consumer resilience weakens | Do not assume broad consumer spending will cushion an AI de-rating shock |
| K_shaped_consumption_risk | Aggregate consumption depends heavily on higher-income/equity-owning households | Treat equity-wealth reversal as a possible macro feedback loop |
| theme_overlap_high | Multiple holdings express same AI capex or storage bottleneck | Prefer best name; trim weakest duplicate |
| sleeve_correlation_high | Value and momentum sleeves both exposed to same macro shock | Raise cash or diversify only after evidence |

## 5. Suggested Daily Output

```text
Institutional overlay scorecard:
- flow_fragility_score: /14 -> low/medium/elevated/acute
- trend_aligned_entry_score: /5 -> trend_broken/cheap_but_unconfirmed/trend_aligned
- AI_quality_score_notes:
- factor_macro_flags:
- action impact:
```
