# Institutional Market Research Framework

Date captured: 2026-06-08

Purpose: convert public institutional research from AQR, Citadel Securities, GMO, and Man Group into reusable strategy-improvement inputs for the US equity quant strategy.

This file is a reference framework, not a trade signal. The ideas below should feed hypotheses, daily monitoring, and backtest design before being promoted to stable decisions.

## Source Index

## 2026-06-09 Incremental Update: Man Institute Consumer Backstop Fragility

Source pages:

- https://www.man.com/insights
- https://www.man.com/maninstitute/market-views
- https://www.man.com/insights/views-from-the-floor-2026-9-june

Verified public item:

- Man Institute / Man Group published `When the AI Bubble Bursts, Don't Count on the US Consumer` on 2026-06-09. The public article argues that AI-led market concentration can mask a fragile mass-market consumer base; if AI enthusiasm reverses, household spending may not provide the usual broad economic or equity-market backstop.

Reusable framework:

- Add `consumer_backstop_fragility` as a sub-flag under `factor_macro_exposure`.
- When AI/growth leadership is narrow, do not assume broad consumer demand can offset an AI de-rating shock.
- During inflation or energy shocks, record whether the market is also dependent on wealthy-household spending and concentrated equity ownership.
- In `AI_quality/capex_cycle`, prefer companies with self-funded cash-flow resilience over companies requiring uninterrupted external funding or hyperscaler growth capex.

Strategy mapping:

- `market fear gate`: context only; no regime change without current VIX, breadth, credit, and index-trend data.
- `concentrated holdings`: reinforces strict duplicate-theme review when owned names express the same AI capex bet.
- `institutional overlay`: extend `factor_macro_exposure` with consumer/inflation fragility.
- `replay protocol`: future AI drawdown replays should record whether consumer/inflation stress coincided with AI leadership reversal.

Evidence notes:

- High evidence for the existence and content of the Man article.
- Medium evidence for strategy transmission because the article includes forward-looking macro interpretation and linked data that should be refreshed from primary sources before quantitative scoring.
- Do not treat the author's "AI bubble" framing as a confirmed regime label.

### AQR

Source pages:

- https://www.aqr.com/Insights/Research
- https://www.aqr.com/Insights/Research/Alternative-Thinking/Hold-the-Dip
- https://www.aqr.com/Insights/Research/Alternative-Thinking/Total-Portfolio-Approach

Relevant takeaways:

- AQR's "Hold the Dip" argues that buying drawdowns tends to fight momentum; timing rules should align with trend instead of automatically fading weakness.
- AQR's total-portfolio discussion is useful for portfolio construction: removing rigid sleeves can add flexibility, but only if guardrails prevent hidden concentration and unintended risk.
- Practical implication for current strategy: dip buying should remain conditional on reclaim signals, relative strength, and the market fear gate. The strategy should not add to AI infrastructure names merely because they fall.

Strategy mapping:

- Keep the current no-new-buy discipline under elevated/stress/panic regimes.
- Reframe "support buys" as "trend-aligned support buys": price must hold or reclaim support, not simply become cheaper.
- Test whether dual-sleeve allocation should allow dynamic capital migration only when factor/theme crowding and market fear are acceptable.

### Citadel Securities

Source pages:

- https://www.citadelsecurities.com/news-and-insights/category/market-insights/
- https://www.citadelsecurities.com/news-and-insights/global-roadshow-insights/
- https://www.citadelsecurities.com/news-and-insights/flow-fragility/?series=global-market-intelligence

Relevant takeaways:

- Recent US equity strength is supported by earnings revisions, AI capex, buybacks, systematic flows, and retail/options activity, not only narrative.
- Market participation is still narrow. Citadel Securities highlighted that only a small share of S&P 500 constituents recently outperformed the index, while gains were concentrated in a small leadership cohort.
- Flow support can become flow fragility: passive inflows, levered ETFs, CTAs, volatility-control buying, retail call demand, and reduced downside hedging can all reverse or amplify losses if momentum stalls.
- "Spot up, vol up" in Nasdaq/semiconductor leadership is a crowding and upside-option-demand signal, not a simple risk-on signal.

Strategy mapping:

- Add a market-structure overlay to daily monitoring: breadth concentration, retail/options excess, CTA or systematic exposure proxies, buyback window state, and levered ETF/semiconductor crowding.
- Treat strong AI earnings revisions as medium-term thesis support, but treat narrow leadership plus high options demand as a sizing and profit-protection warning.
- Add an explicit "flow fragility" note when the strategy owns the same crowded leaders favored by passive, retail options, and systematic flows.

### GMO

Source pages:

- https://www.gmo.com/americas/research-library/
- https://www.gmo.com/americas/research-library/hype-vs-high-conviction_insights/

Relevant takeaways:

- GMO separates durable AI winners from companies tied to boom-and-bust supplier cycles.
- Quality features matter: proven cash flows, differentiation, barriers to entry, high returns on investment, and strong balance sheets.
- Hyperscalers may have more resilient AI exposure because AI capex is funded from broad cash flows and diversified revenue. Some suppliers have higher beta to the buildout cycle; if growth capex pauses, supplier revenue can reprice quickly.
- GMO favors selective supplier exposure and highlights that established hyperscalers and some diversified suppliers may be more resilient than pure buildout beneficiaries.
- GMO also treats software/services and healthcare as possible AI beneficiaries when they control critical enterprise data or can monetize real use cases.

Strategy mapping:

- Add a quality/resilience score for AI candidates: non-AI revenue base, balance sheet strength, customer concentration, gross margin stability, capex cyclicality, and evidence of actual AI revenue.
- Split the AI universe into: hyperscaler/platform, diversified supplier, cyclical supplier, application/software/data owner, and speculative bottleneck beneficiary.
- Current AI infrastructure momentum names should not be treated equally. MRVL/WDC/STX/AMD need separate cycle-risk and customer/capex-dependency labels.

### Man Group

Source pages:

- https://www.man.com/maninstitute/market-views
- https://www.man.com/insights/views-from-the-floor-2026-26-may
- https://www.man.com/insights/road-ahead-reflections
- https://www.man.com/insights/views-from-the-floor-2026-5-may
- https://www.man.com/insights/views-from-the-floor-2026-2-jun

Relevant takeaways:

- Quant factors can carry hidden macro bets. Value may behave like an inflation/short-duration exposure; momentum can suffer when volatility falls after stress and markets rotate sharply.
- Drawdown analysis should consider not only single-asset losses, but also overlap and conditional correlations among equity, value, momentum, quality, trend, fixed income, and gold-like hedges.
- Man Group's AI optical-interconnect piece supports the AI infrastructure bottleneck thesis: copper limits, high chip-to-chip data traffic, idle processors, power use, optical circuit switching, co-packaged optics, and InP lasers.
- Man Group's inflation discussion reinforces that geopolitical and energy shocks can shift the macro regime quickly, which matters because AI/growth exposure is rate-sensitive.

Strategy mapping:

- Add factor-macro exposure checks to the strategy review: inflation sensitivity, duration/growth exposure, volatility-transition risk, and momentum-crash risk after panic-to-normal rebounds.
- Add drawdown-overlap diagnostics to backtests: how often current sleeves lose money together, especially during inflation shocks, volatility collapses, and growth-to-value rotations.
- Maintain AI optical/interconnect as a high-priority bottleneck theme, but require price/volume leadership and crowding controls before adding exposure.

## Proposed Strategy Improvements

### 1. Trend-Aligned Entry Discipline

Do not treat a selloff as a buy signal. A candidate may become actionable only when:

- Market fear gate permits new exposure.
- Price is above or reclaiming key trend levels.
- Relative strength versus QQQ and the relevant theme group is improving.
- News/catalyst evidence supports the thesis but does not override price confirmation.

### 2. Flow Fragility Overlay

Daily monitoring should flag elevated flow fragility when several of the following are true:

- Leadership breadth is narrow.
- AI/semiconductor leaders dominate index gains.
- Upside option demand is unusually high or "spot up, vol up" appears.
- CTA/vol-control exposure is high or rebuilt after a rally.
- Downside hedging demand has collapsed.
- Buyback open-window support is about to weaken.
- Levered ETF assets or retail options activity are concentrated in the owned theme.

Possible action: reduce new buys, prefer trims into strength, and widen the self-review around crowding before adding to winners.

### 3. AI Quality and Capex-Cycle Classification

For every AI-linked ticker, classify exposure:

- Platform/hyperscaler: diversified revenue, high cash flow, direct AI capex control.
- Diversified supplier: supplier upside with non-AI or multi-customer resilience.
- Cyclical supplier: high upside but exposed to hyperscaler growth-capex pause.
- Application/data owner: monetizes AI through workflow, data control, retention, or pricing.
- Speculative bottleneck beneficiary: strong narrative but unproven revenue durability.

This classification should influence max weight, stop discipline, and whether a stock can be core or only satellite.

### 4. Factor-Macro Exposure Audit

The strategy should record, at least weekly or during regime transitions:

- Net growth/duration exposure.
- Value/inflation exposure.
- Momentum exposure and risk of reversal after volatility collapse.
- Quality exposure.
- Sector/theme concentration.
- Sleeve-level drawdown overlap.

### 5. AI Bottleneck Watchlist Expansion

Maintain optical/interconnect as a core AI infrastructure watch theme. Extend the watch dimensions beyond current US tickers:

- Optical modules and coherent optics.
- Optical circuit switching.
- Co-packaged optics.
- InP lasers and compound semiconductors.
- Data-center power and cooling.
- Network equipment and custom silicon used to reduce idle GPU time.

US-listed tickers still need validation before action; non-US leaders can be used as supply-chain evidence, not automatic buys.

## Validation Plan

Stage 1: Monitoring integration.

- Add flow-fragility and factor-macro checks to daily reports.
- Classify current AI names by quality/capex-cycle risk.
- Mark crowded winners where price is strong but flow risk is elevated.

Stage 2: Backtest integration.

- Test "trend-aligned support buy" versus plain buy-the-dip rules.
- Add breadth and flow-proxy filters to the V4/V5 strategy.
- Add sleeve-level drawdown-overlap diagnostics.
- Test quality/resilience score as a tie-breaker among AI candidates.

Stage 3: Decision promotion.

- Promote to `memory/decisions.md` only after repeated daily usefulness or quantitative validation.
- If the overlays reduce false buys without eliminating too much upside, convert them into stable rules.
