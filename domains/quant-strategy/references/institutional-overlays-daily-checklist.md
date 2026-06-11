# Institutional Overlays Daily Checklist

Date created: 2026-06-08

Purpose: turn the AQR, Citadel Securities, GMO, and Man Group research synthesis into a practical daily checklist for the US equity strategy.

Status: experimental monitoring overlay. Use it for risk review, position sizing, and hypothesis tracking. Do not treat it as a standalone buy/sell model until validated.

## 1. Trend-Aligned Entry Check

Source inspiration: AQR trend-following and anti-plain-dip-buying research.

Before any new buy or add:

- Market fear gate is `normal` or explicitly permits reduced exposure.
- Stock is above or reclaiming 20/50-day trend support.
- Stock relative strength versus QQQ and theme peers is stable or improving.
- Pullback is orderly, not a high-volume break of leadership.
- News/catalyst supports the thesis but price confirms it.

Daily wording:

- `trend_aligned`: buy/add can be considered.
- `cheap_but_unconfirmed`: watch only; no order.
- `trend_broken`: no buy; review stop/reduce.

## 2. Flow-Fragility Check

Source inspiration: Citadel Securities market-structure research.

Flag `flow_fragility = elevated` when three or more are true:

- Market leadership is narrow: a small group of mega-cap AI/semiconductor names drives most index gains.
- SMH/SOXX outperformance is strong but breadth inside semiconductors is weak.
- Nasdaq or semiconductor names show `spot up, vol up` behavior.
- Retail/options activity appears concentrated in the same AI/semiconductor leaders.
- Levered ETF or thematic ETF flows appear crowded in technology/semiconductors.
- Buyback open-window support is fading or entering blackout.
- CTA/vol-control exposure is likely high after a sharp rally and volatility compression.
- Downside hedging appears unusually cheap or under-owned.

Daily action guide:

| State | Meaning | Strategy response |
| --- | --- | --- |
| low | Trend is supported by breadth or healthy rotation | Normal rules apply |
| medium | Leadership is strong but crowded | Avoid chasing; prefer support/reclaim entries |
| elevated | Trend is narrow and mechanically supported | No new chase buys; consider trims into strength |
| acute | Crowded leaders begin breaking with VIX or breadth stress | Apply portfolio-level risk review before single-stock optimism |

## 3. AI Quality and Capex-Cycle Check

Source inspiration: GMO AI quality framework and Man Group AI bottleneck work.

Classify each AI candidate before sizing:

| Class | Description | Core eligibility |
| --- | --- | --- |
| platform_hyperscaler | Diversified cash flow and direct AI capex control | Core candidate if trend and valuation are acceptable |
| diversified_supplier | Supplier upside with multi-customer or non-AI resilience | Core or satellite depending on cycle risk |
| cyclical_supplier | High upside but sensitive to hyperscaler growth-capex pause | Usually satellite unless evidence is exceptional |
| application_data_owner | AI monetization through workflow, data, retention, or pricing | Watch/core only after revenue evidence and RS confirm |
| speculative_bottleneck | Strong bottleneck narrative but unproven durable revenue | Watchlist or small satellite only |

Daily review fields:

- AI class.
- Capex-cycle sensitivity: `low`, `medium`, or `high`.
- Customer concentration: `low`, `medium`, or `high`.
- Evidence type: `earnings`, `guidance`, `backlog`, `capex`, `product`, `partnership`, `narrative`.
- Price confirmation: `confirmed`, `mixed`, or `rejected`.

## 4. Factor-Macro Exposure Check

Source inspiration: Man Group factor-macro risk work.

Weekly or during regime transitions, record:

- Growth/duration exposure: high growth stocks can be rate-sensitive.
- Inflation/value exposure: value may implicitly benefit from rising inflation/rates.
- Momentum reversal risk: high after panic-to-normal recovery and volatility collapse.
- Quality exposure: can protect in some regimes but may lag speculative catch-up rallies.
- Theme overlap: multiple stocks can express the same AI capex bet.
- Sleeve drawdown overlap: value sleeve and momentum sleeve may fail together if both are exposed to the same macro shock.

Daily action guide:

- If `momentum_reversal_risk = high`, avoid adding lagging defensive winners just as risk appetite returns.
- If `growth_duration_risk = high`, reduce aggressive AI adds before CPI/Fed/rate shocks.
- If `theme_overlap = high`, prefer trimming the weakest duplicate rather than adding a new related name.

## 5. AI Bottleneck Watch Check

Source inspiration: Man Group optical-interconnect research plus existing AI infrastructure memory.

Track these subthemes:

- Optical modules and coherent optics.
- Optical circuit switching.
- Co-packaged optics.
- InP lasers and compound semiconductors.
- Data-center power and cooling.
- Network equipment and custom silicon.
- Memory/storage throughput.

Watchlist rule:

- Supply-chain evidence can promote a subtheme to `watch`.
- Price-volume leadership can promote a ticker to `candidate`.
- Only market fear, trend, relative strength, and portfolio concentration rules can promote a ticker to `actionable`.

## 6. Daily Report Snippet

Use this compact block in daily reports:

```text
Institutional overlays:
- trend_aligned_entry:
- flow_fragility:
- AI_quality/capex_cycle:
- factor_macro_exposure:
- bottleneck_watch:
- action impact:
```

## 7. Memory Promotion Rules

- One-day observations stay in `memory/daily/`.
- Repeated but unproven patterns update `memory/hypotheses.md`.
- Validated process improvements update `memory/decisions.md`.
- Source frameworks and reusable checklists stay in `references/`.
