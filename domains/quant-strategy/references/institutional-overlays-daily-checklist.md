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

When available, record these direct diagnostics separately rather than forcing missing data into the score:

- 0DTE share or average option tenor.
- Semiconductor call-premium concentration and inverted call-skew breadth.
- Leveraged technology/semiconductor ETF AUM or flow acceleration.
- Single-stock implied correlation and semiconductor implied volatility.
- Frequency of Nasdaq/semiconductor `spot up / vol up` sessions.
- Equity-financing spread or another balance-sheet-capacity proxy.
- Risk localisation: `broad/systemic`, `cross-sectional`, `mixed`, or `unavailable`. Compare index/ETF hedging and breadth/credit with semiconductor, momentum and single-name hedging; do not infer this state from the index level alone.
- Flow-to-fundamentals handoff: `not_observed`, `provisional`, `confirmed`, or `unavailable`. `Confirmed` requires realised earnings/guidance plus completed-close/relative-strength confirmation; it is context, not an entry trigger.
- Complacency divergence: `present`, `absent`, or `unavailable`. `Present` needs more than a low VIX: record the dated combination of subdued index volatility, concentrated leadership, credit/implied-correlation or options evidence where available, and a known macro/earnings event cluster. It prompts a concentration/no-chase review only and cannot override the Fear Gate.
- Retail risk transfer: `defensive`, `neutral`, `risk_seeking`, or `unavailable`. Record the index/ETF-versus-single-stock option mix, put/call or monetisation observation, source and first-visible time. Treat a platform-specific statistic as source-only, not as a price-derived fact.

These diagnostics describe amplification risk. High values do not create a standalone bearish signal.

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
- Power-delivery evidence: `source_only`, `independently_confirmed`, or `unavailable`; record whether the evidence concerns generation, grid interconnection/delivery, transmission/distribution, storage, cooling, procurement, utilisation, revenue or margin. Do not promote a ticker or subtheme on an announcement alone.

## 4. Factor-Macro Exposure Check

Source inspiration: Man Group factor-macro risk work.

Weekly or during regime transitions, record:

- Growth/duration exposure: high growth stocks can be rate-sensitive.
- Inflation/value exposure: value may implicitly benefit from rising inflation/rates.
- Momentum reversal risk: high after panic-to-normal recovery and volatility collapse.
- Quality exposure: can protect in some regimes but may lag speculative catch-up rallies.
- Theme overlap: multiple stocks can express the same AI capex bet.
- Sleeve drawdown overlap: value sleeve and momentum sleeve may fail together if both are exposed to the same macro shock.
- Climate-resource input stress: use the shared classification contract in `institutional-market-research-framework.md`. Retain constraint category, affected geography/supply chain, direct AI-capex linkage, severity, independent-source count, `first_visible`, `source`, `as_of`, and `expires_at`; record `unavailable` if the two-independent-source threshold is not met.
- Complex-credit complacency: `present`, `absent`, or `unavailable`. Only flag when dated evidence identifies compressed compensation alongside duration/extension, negative-convexity or structural/documentation risk. It requests a macro/common-factor review; it is not a credit or equity signal.

Daily action guide:

- If `momentum_reversal_risk = high`, avoid adding lagging defensive winners just as risk appetite returns.
- If `growth_duration_risk = high`, reduce aggressive AI adds before CPI/Fed/rate shocks.
- If `theme_overlap = high`, prefer trimming the weakest duplicate rather than adding a new related name.
- If climate-resource input stress is `elevated` or `high`, review AI infrastructure, storage and optical/interconnect as one common-input cluster; it is an explanation/review flag, not an automatic risk-state or trade trigger.

## 5. AI Bottleneck Watch Check

Source inspiration: Man Group optical-interconnect research plus existing AI infrastructure memory.

Track these subthemes:

- Optical modules and coherent optics.
- Optical circuit switching.
- Co-packaged optics.
- InP lasers and compound semiconductors.
- Data-center power and cooling.
- Power generation, grid interconnection/delivery, transmission/distribution and storage; keep the evidence stage separate from a thematic demand narrative.
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
