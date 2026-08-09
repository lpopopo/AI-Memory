# Institutional Market Research Framework

## 2026-08-09 Update: Retail Risk Transfer And Complex-Credit Complacency

Verified source pages:

- Citadel Securities, `Traders on Defense`, published 2026-08-05: https://www.citadelsecurities.com/news-and-insights/retail-detail/traders-on-defense/
- Man Group, `The Yield Trap Hiding in Junior Bank Bonds`, published 2026-07-28: https://www.man.com/insights/views-from-the-floor-2026-28-July

Reusable framework:

- Add `retail_risk_transfer` under `flow_fragility`.  Keep outright retail participation separate from its direction: broad-index/ETF put demand, an index-or-ETF-to-single-stock option-activity shift, and monetisation after a rebound can indicate hedging or de-risking rather than fresh directional risk appetite.  Record `defensive`, `neutral`, `risk_seeking`, or `unavailable`, plus the source, first-visible time and whether the measure is proprietary.  It is not a contrarian buy or sell signal.
- Add `complex_credit_complacency` under `factor_macro_exposure`.  A high-yield instrument can quietly become more rate-sensitive, long-duration or negatively convex while its spread compensation compresses.  Record the risk object, spread/compensation percentile, duration or extension risk, documentation/structure risk, source and as-of date; do not substitute a generic high-yield ETF for a complex-credit observation without marking it a proxy.

Strategy mapping:

- `market fear gate`: unchanged.  These fields can request a risk review but cannot alter the gate without the existing completed-close volatility, breadth, credit and trend inputs.
- `flow_fragility` / `portfolio concentration`: defensive retail flow in semiconductors, memory or broad ETFs is a cross-sectional-risk input; review the common AI-capex sleeve and keep missing direct flow measures `unavailable`.
- `trend_aligned_entry`: a rebound after retail monetisation still requires the existing support/reclaim, relative-strength and earnings/guidance checks.
- `replay protocol`: freeze 2026-08-05 and 2026-07-28 as source-event dates; compare 1/5/20/60-day QQQ/SPY, SMH/QQQ, RSP/SPY, HYG/LQD, VIX/VIX3M and yield changes.  Test direct data only where point-in-time public access exists; do not backfill Citadel platform flow or AT1 structure from later information.

Evidence notes:

- High evidence for the pages' stable titles, dates and stated observations through official-domain Reader details.  Citadel's retail-flow figures are proprietary platform observations, and Man's AT1 analysis is an institutional interpretation of a specialised credit market; transmission to US equities is therefore medium evidence and remains experimental.
- This update is a monitoring and replay framework, not a stable rule, market forecast or trade recommendation.

## 2026-08-04 Update: Flow Reset, Market-Guidance Reflexivity, And AI Diffusion Friction

Verified source pages:

- Citadel Securities, `August - After The Reset`, published 2026-08-03: https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/august-after-the-reset/
- Citadel Securities, `From Forward Guidance to Market Guidance`, published 2026-08-03: https://www.citadelsecurities.com/news-and-insights/macro-thoughts/from-forward-guidance-to-market-guidance/

Reusable framework:

- Extend `flow_to_fundamentals_handoff` with retail net flow, leveraged-product AUM, equity-financing spreads, index concentration, single-stock/index volatility dispersion, earnings revisions and buyback eligibility. A source-level claim that positioning has normalized remains provisional until point-in-time public proxies and subsequent completed-close price action agree.
- Add `market_guidance_reflexivity` under `factor_macro_exposure` and `flow_fragility`: long-end yield and term-premium shocks can pressure duration equities while weakening the bond hedge, which can create correlated losses, deleveraging and further financial-condition tightening.
- Add `AI_diffusion_cost_policy` under `AI_quality/capex_cycle`: for agentic applications with repeated model calls, model access and unit inference cost are application-ROI inputs. Separate frontier-capability controls from broad restrictions that raise ordinary application-layer diffusion costs.
- Add `social_license_permitting_bottleneck` under `AI bottleneck watch`: local permitting, community acceptance, construction moratoria and grid queues are separate from chips, power generation, cooling and interconnect supply.
- Add `product_complex_inflation_pass_through` under `factor_macro_exposure`: track diesel, gasoline, LPG, refining margins and product cracks alongside crude oil when assessing an energy shock's inflation path.

Strategy mapping:

- `market fear gate`: unchanged. Flow normalization and market-guidance feedback are context only until VIX term structure, breadth, credit and completed-close trend inputs confirm a regime change.
- `flow_fragility` and `portfolio concentration`: a calm index can mask semiconductor/memory liquidation, high single-name volatility and low implied correlation. Review correlated AI-capex exposure without automatically changing position state.
- `trend_aligned_entry`: a technical reset, valuation compression or reopening buyback window does not authorize entry; require the existing support/reclaim, relative-strength and earnings/guidance confirmation.
- `AI infrastructure/application watchlists`: add permitting/social-license evidence to infrastructure and low-cost model access/call intensity to applications. Company-level promotion still needs orders, deployments, revenue, margin or cash-flow evidence.
- `replay protocol`: freeze both 2026-08-03 timestamps and compare 1/5/20/60-day QQQ/SPY, SMH/QQQ, RSP/SPY, VIX/VIX3M, HYG/LQD, 10Y/30Y yields, breakevens, bond-equity correlation, semiconductor implied/realized volatility and energy-product cracks. Record unavailable proprietary flow fields as `unavailable`, not inferred values.

Evidence notes:

- High evidence for article existence, titles, timestamps and stated observations because both official-domain detail bodies were readable through the Reader channel.
- Medium evidence for strategy transmission: Citadel platform flow, financing and volatility figures require independent point-in-time replication, and the macro/AI-policy conclusions remain institutional interpretation.
- AQR and GMO had no post-2026-07-31 official-detail research item verified in this run. No framework was inferred from search summaries or undated candidates.
- This update is an experimental monitoring and replay framework, not a stable rule, market forecast or trade recommendation.

## 2026-07-26 Update: Complacency Divergence And Power-Delivery Evidence Ladder

Verified source pages:

- GMO, `The Electricity Tipping Point & the Next Energy Boom`, displayed 2026-07-23: https://www.gmo.com/americas/research-library/the-electricity-tipping-point--the-next-energy-boom_insights/
- GMO, `Mid-Year Update: Equity Dislocation Strategy`, displayed 2026-07-23: https://www.gmo.com/americas/research-library/mid-year-update-equity-dislocation-strategy_marketcommentary/
- Man Group, `The VIX Isn't Worried, But Maybe It Should Be`, displayed 2026-07-21: https://www.man.com/insights/views-from-the-floor-2026-21-July

Reusable framework:

- Add `complacency_divergence` under `flow_fragility`: a dated diagnostic for the combination of subdued index volatility, compressed cross-sectional correlation or credit compensation, concentrated AI/large-cap leadership, and a near-term macro or earnings-event cluster. It is `present`, `absent`, or `unavailable`; never infer `present` from a low VIX alone. The Man article is a high-evidence source event, but its market interpretation is not a stand-alone risk signal.
- Keep `systemic_market_stress` separate from `complacency_divergence`. The former remains the Fear Gate's domain and needs completed-close VIX, breadth, credit and trend inputs. The latter is a cross-sectional/crowding review that can only reinforce existing no-chase and concentration controls.
- Add `power_delivery_evidence` to `AI_quality/capex_cycle` and `bottleneck_watch`. Track `source_only`, `independently_confirmed`, or `unavailable`: generation availability, grid-interconnection queue or delivery date, transmission/distribution equipment, storage, cooling and site-power procurement are distinct stages. A thematic article, product claim, or announced project is `source_only`; only independently verifiable planning, procurement, operating or financial evidence is `independently_confirmed`.
- GMO's Equity Dislocation update reinforces `expectation_gap_repricing`: an expensive company can disappoint despite strong reported growth when the embedded outcome is exceptional, while a cheaper company can reprice on an upside surprise. Apply this only with point-in-time valuation, earnings/guidance and completed-close reaction data; it is not a generic value or short signal.

Strategy mapping:

- `market fear gate`: unchanged. Do not upgrade a low-VIX or power-demand narrative into a risk-regime change without the existing completed-close inputs.
- `flow_fragility` and `portfolio concentration`: if `complacency_divergence = present` and the normal flow-fragility evidence is also elevated, require the existing support/reclaim discipline and review correlated AI-capex exposure. Missing implied-correlation, spread or options data stays `unavailable`.
- `AI_quality/capex_cycle` and `bottleneck_watch`: use the power-delivery ladder to distinguish a long-duration infrastructure narrative from evidence that a specific supplier or operator is converting it into orders, revenue or margins. It does not change a ticker class or weight by itself.
- `replay protocol`: freeze first-visible dates for 2026-07-21 and 2026-07-23; compare QQQ/SPY, SMH/QQQ, RSP/SPY, HYG/LQD, VIX/VIX3M, implied correlation where available, energy/power, semiconductor equipment, memory/storage, optical/interconnect and software/application baskets over 1/5/20/60 days. Record earnings/Fed/macro confounders and baseline-authorized entries separately.

Evidence notes:

- High evidence for the three official-domain pages' stable titles, dates and bodies through the Reader channel.
- Medium evidence for transmission to public US-equity overlays: the articles use institutional interpretation and, for power, macro/industry data. Public point-in-time replication is required before any rule promotion.
- This is a monitoring and backtest framework, not a prediction, power trade, or buy/sell rule.

## 2026-07-19 Update: Flow-to-Fundamentals Handoff And Risk Localisation

Verified source page:

- Citadel Securities, `After the Reset: Time to Focus on Fundamentals`, displayed 2026-07-13: https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/after-the-reset/

Reusable framework:

- Separate `systemic_market_stress` from `cross_sectional_risk_localisation`. Broad index/ETF skew and credit/breadth deterioration belong to the former; an extreme semiconductor/Nasdaq implied-vol premium, low implied correlation, or single-name/factor hedging belongs to the latter. The latter can coexist with a calm headline index and should raise concentration review, not automatically change the Fear Gate.
- Record `flow_to_fundamentals_handoff` only as a dated diagnostic: retail demand, positioning reset, leveraged-product AUM, financing conditions, breadth/rotation, valuation, and the next earnings window. A handoff is provisional until realised earnings/guidance and completed-close price action agree; it is never a buy signal.
- When the inputs are unavailable, write `unavailable` rather than infer them from an index rise. Citadel's retail-platform, option-skew, implied-correlation and financing-spread figures are source-specific and are not silently substituted by price-only proxies.

Strategy mapping:

- `market fear gate`: remains governed by its existing VIX, breadth, credit and completed-close inputs. Cross-sectional stress alone cannot upgrade or downgrade the gate.
- `flow_fragility`: distinguish broad deleveraging from semiconductor/momentum-specific hedging. The latter triggers an AI-capex common-factor review and blocks chase entries, while existing stops and trend signals retain priority.
- `trend_aligned_entry`: after a flow reset, wait for earnings/guidance evidence and relative-strength confirmation; do not interpret a single rebound as a confirmed fundamentals handoff.
- `replay protocol`: freeze the first-visible date and compare the risk-localisation fields with QQQ/SPY, SMH/QQQ, RSP/SPY, VIX, sector/factor implied volatility where available, HYG/LQD and subsequent 1/5/20/60-day returns.

Evidence notes:

- High evidence for the Citadel article's title, displayed date and stated observations because the official-domain detail page was readable through the Reader channel.
- Medium evidence for transmission to this strategy: its proprietary retail, financing and options data need public/proxy replication and point-in-time replay.
- This is a monitoring and backtest framework, not a trading rule or a prediction of earnings.

Date captured: 2026-06-08

Purpose: convert public institutional research from AQR, Citadel Securities, GMO, and Man Group into reusable strategy-improvement inputs for the US equity quant strategy.

This file is a reference framework, not a trade signal. The ideas below should feed hypotheses, daily monitoring, and backtest design before being promoted to stable decisions.

## Source Index

## 2026-07-10 Update: AI Stack Selectivity, Private-AI Concentration, And IPO Lock-Up Pressure

Source page:

- https://www.man.com/insights/h2-2026-technology-outlook

Verified public item:

- Man Group published `H2 Technology Outlook - Still Dancing, But Moving Closer to the Door?` on 2026-07-10. The official-domain detail page exposed a stable title, date and body. It argues that the AI trade is maturing from broad thematic exposure into sharper winner/loser discrimination across semiconductors, infrastructure, cybersecurity, software, private AI entities, China cost-efficient AI, and the IPO pipeline.

Reusable framework:

- Add `AI_stack_selectivity_rotation` under `AI_quality/capex_cycle`: track whether capital is rotating from GPU-only winners toward memory, optics, wafer capacity, infrastructure, cybersecurity, software efficiency, model companies, and applications.
- Add `semiconductor_peak_margin_trap`: low multiples on peak earnings can be misleading when margins depend on supply discipline and downstream AI ROI remains unproven.
- Add `private_AI_customer_concentration`: cloud/provider backlog quality can depend heavily on a small number of private AI entities and their spending commitments.
- Add `China_AI_efficiency_competition`: Chinese semiconductors and open-source models may compete through cost-to-output and availability even under export-control constraints.
- Add `AI_IPO_lockup_pressure`: IPOs can extend risk appetite, but later lock-up expiries and venture-capital recycling may become a delayed liquidity pressure point.

Strategy mapping:

- `market fear gate`: context only; no regime change without VIX, breadth, credit, and completed-close trend evidence.
- `trend_aligned_entry`: broad AI theme heat is insufficient; require sub-sector leadership, price confirmation, and stop closure before any action.
- `flow_fragility`: combine AI crowding with private-AI concentration, IPO supply, and capital-recycling timing rather than treating semiconductor strength as self-validating.
- `AI_quality/capex_cycle`: prefer validated monetization, customer diversification, margin durability and cash-flow evidence over bottleneck narrative alone.
- `AI bottleneck watch`: keep GPU, memory, optics, wafer capacity and software-efficiency bottlenecks separate; do not map one bottleneck automatically to all AI tickers.
- `replay protocol`: freeze the 2026-07-10 event and compare 1/5/20/60-day QQQ/SMH/XSD/HYG/LQD plus semiconductor equipment, memory/storage, optical/interconnect, infrastructure/cybersecurity, SaaS, cloud and IPO/new-listing baskets.

Evidence notes:

- High evidence for official article existence, title, date and body.
- Medium evidence for strategy transmission because the article's backlog, spending-commitment, cost-efficiency and IPO claims require filings, primary data and market replay.
- This is an experimental monitoring and backtest framework, not a buy/sell signal or stable decision.

## 2026-07-05 Weekly Update: Structural Flow Concentration And Short-Duration Leverage

Source page:

- https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/1h-2026-market-structure-flows/

Verified public item:

- Citadel Securities published `1H 2026 Market Structure & Flows` on 2026-06-30. The Reader official-domain channel and direct official detail page exposed a stable title, date, body, and the article's 20 market-structure observations. It links index concentration, passive ownership, retail participation, short-dated options, leveraged ETFs, financing costs, implied correlation, and upside-volatility demand rather than treating them as independent indicators.

Reusable framework:

- Add `structural_flow_concentration` under `flow_fragility`: narrow benchmark leadership is more fragile when passive inflows, retail calls, leveraged products, and systematic positioning converge on the same technology/semiconductor names.
- Add `short_duration_leverage_density`: track 0DTE share, average option tenor, call-premium concentration, and leveraged-ETF theme exposure. High activity is not bearish by itself; it indicates that price moves may be amplified and intraday liquidity can differ from apparent headline depth.
- Add `spot_vol_correlation_shift`: `spot up / vol up`, inverted call skew, low implied single-stock correlation, and unusually high semiconductor implied volatility can coexist. Treat this as upside-chase/cross-sectional-dispersion evidence, not as a simple risk-on or panic label.
- Add `financing_capacity_pressure`: rising equity-financing spreads can make an apparently liquid rally more vulnerable when leverage demand is concentrated and dealer/balance-sheet capacity is constrained.

Strategy mapping:

- `market fear gate`: these fields are context only; they do not change the fear regime without VIX term structure, breadth, credit, and completed-close trend evidence.
- `trend_aligned_entry`: require support/reclaim and relative-strength confirmation when structural flows are crowded; do not equate retail dip buying with durable support.
- `flow_fragility`: monitor breadth concentration, 0DTE/call demand, leveraged technology/semiconductor exposure, financing spreads, implied correlation, and spot-vol co-movement.
- `portfolio concentration`: ticker diversification does not reduce risk when holdings share the same passive, retail-option, leverage, and semiconductor-flow channel.
- `replay protocol`: test whether the expanded fields improve warnings before AI/semiconductor reversals without blocking too many continued-trend winners.

Evidence notes:

- High evidence for article existence, date, and reported Citadel platform/market observations on the official-domain detail page.
- Medium evidence for broad-market transmission because several observations use Citadel's own platform data and the proposed strategy mapping still requires independent, point-in-time proxies and replay.
- This is an experimental monitoring and backtest framework, not a short signal, trade recommendation, or stable decision.

## 2026-07-01 Update: AI Credit Funding Fragility

Source page:

- https://www.man.com/insights/views-from-the-floor-2026-1-july

Verified public item:

- Man Institute published `The Hard Questions for AI Bonds Investors` on 2026-07-01. The official-domain detail page exposed a stable title, date and body. The article separates AI equity upside from bondholders' fixed-coupon exposure to construction delays, cost overruns, competition and long-duration demand uncertainty. It also distinguishes issuers with a cash-generating business backstop from pure-play data-centre, neocloud and leveraged-software issuers.

Reusable framework:

- Add `AI_credit_funding_fragility` under `flow_fragility`: very large AI bond supply can create a substitution effect, forcing wider compensation across lower-quality credit even when equity appetite remains strong.
- Add `cashflow_backstop_separation` under `AI_quality/capex_cycle`: consolidated market capitalization is not enough; identify which segment actually supplies EBITDA/FCF and whether the AI segment is self-funding.
- Add `credit_duration_mismatch` under `factor_macro_exposure`: short-dated lenders may accept near-term visibility while long-dated bonds price execution, technology and demand uncertainty more aggressively.
- Separate `equity_optionality` from `credit_asymmetry`: equity captures upside if the boom succeeds; debt has capped upside and full exposure to delays/failure.

Strategy mapping:

- `market fear gate`: context only; require live HYG/LQD, credit spreads, VIX, breadth and index trend before changing exposure.
- `flow_fragility`: monitor AI issuance calendar, new-deal concessions, long-end underperformance and spread widening.
- `AI_quality/capex_cycle`: prefer proven segment cash flow, financing headroom and billable utilization over headline valuation or contracted capacity.
- `portfolio concentration`: multiple equity holdings can share the same external-financing and AI-capex risk even when they sit in different subthemes.
- `replay protocol`: compare AI bond issuance events with 1/5/20/60-day HYG/LQD, equity-theme returns, issuer spreads, maximum adverse excursion and financing revisions.

Evidence notes:

- High evidence for official article existence, title, date and body.
- Medium evidence for strategy transmission because the article's cited issuance forecasts and credit interpretation require primary-market, spread and company-level cash-flow validation.
- This is an experimental overlay, not a buy/sell signal or stable `decisions.md` rule.

## 2026-06-17 Update: Policy Hysteresis And AI Listing Fragility

Source pages:

- https://www.citadelsecurities.com/news-and-insights/global-macro-strategy/hysteresis-may-set-up-a-september-hike/
- https://www.man.com/insights/views-from-the-floor-2026-17-June

Verified public items:

- Citadel Securities published `Hysteresis May Set Up a September Hike` with official-domain title, timestamp `2026-06-16T20:54:12Z`, and readable body through the Reader official-domain channel. The article argues that temporary energy and supply-chain shocks can become persistent if they hit an economy with easy financial conditions, positive output gap, AI capex support, and reaccelerating labor demand; it frames the risk as a more hawkish Fed path and possible 2026-2027 rate hikes.
- Man Group published `SpaceX - To Infinity and Beyond?` on 2026-06-17 with official-domain title/date/body. The article treats the hypothetical SpaceX listing as evidence that the AI listing window remains open, but warns that SpaceX valuation is more a Musk-specific belief story than a clean read-through for AI sector health. It also highlights a split between strong semiconductor leadership and weak software/free-cash-flow dynamics, with hyperscaler AI capex consuming a very large share of operating cash flow.

Reusable framework:

- Add `policy_hysteresis_risk` under `factor_macro_exposure`: if energy/supply shocks, wage acceleration, easy financial conditions, AI capex stimulus, and inflation breadth rise together, the rate backdrop can tighten even while equity leadership looks strong.
- Add `AI_listing_window_liquidity` under `flow_fragility`: a large successful AI-adjacent IPO can extend risk appetite and funding windows, but may also mark late-cycle liquidity confidence if valuations depend on aggressive TAM assumptions.
- Add `AI_capex_cashflow_pressure` under `AI_quality/capex_cycle`: monitor whether hyperscaler AI capex is consuming operating cash flow faster than AI revenue converts into free cash flow. This raises the bar for treating semiconductor strength as a durable core signal.
- Separate `semiconductor_momentum` from `software_monetization`: semiconductor leadership can coexist with software weakness, SaaS multiple compression, and delayed AI application-layer payback.

Strategy mapping:

- `market fear gate`: policy hysteresis is not a panic signal by itself, but it raises sensitivity to VIX, rates, credit, breadth, and QQQ/SMH trend breaks.
- `trend_aligned_entry`: require reclaim/relative-strength confirmation before buying AI pullbacks when rate-hike odds or front-end policy pricing are moving against growth duration.
- `flow_fragility`: treat large AI IPO demand and high semiconductor valuation as liquidity/crowding context, not automatic confirmation.
- `AI_quality/capex_cycle`: prefer companies with self-funded capex, proven AI revenue, and resilient free cash flow; mark suppliers and application names separately.
- `AI bottleneck watch`: keep space/satellite/edge-AI themes in the observation pool, but do not infer SpaceX read-through to RKLB/RDW/TSLA/xAI without direct revenue, order, and price-action evidence.
- `replay protocol`: add policy-hysteresis and AI-listing-window fields to future AI drawdown, rate-shock, and IPO/liquidity-window replays.

Evidence notes:

- High evidence for official article existence, title/date/body for Citadel and Man via official-domain Reader/detail checks.
- Medium evidence for strategy transmission because both articles are forward-looking interpretations and require market-data confirmation before affecting position sizing.
- Do not convert either item into a buy/sell signal or a stable `decisions.md` rule without replay evidence.

## 2026-06-14 Weekly Update: GMO Valuation Concentration And Dynamic Allocation

Source pages:

- https://www.gmo.com/americas/research-library/diversifying-beyond-6040-with-a-more-dynamic-allocation_insights/
- https://www.gmo.com/americas/research-library/gmo-7-year-asset-class-forecast-may-2026_gmo7yearassetclassforecast/

Verified public items:

- GMO published `Diversifying Beyond 60/40 with a More Dynamic Allocation` on 2026-06-12. The official-domain Reader detail page exposed title, body, and the core argument that the traditional 60/40 profile has become highly dependent on expensive U.S. growth equities and tight credit spreads after strong recent gains.
- GMO published `GMO 7-Year Asset Class Forecast: May 2026` on 2026-06-12. The official-domain Reader page exposed title/date and a download surface; use it as valuation-context evidence rather than a full article framework unless the PDF is separately reviewed.

Reusable framework:

- Add `valuation_concentration_pressure` as a sub-flag under `factor_macro_exposure`.
- Treat a portfolio as concentrated when it has common exposure to expensive U.S. growth, AI capex expectations, long-duration valuation, tight credit/liquidity, or wealth-effect consumption, even if ticker count looks diversified.
- Add `dynamic_allocation_drift`: after a long bull run, passive or default allocations may drift into a narrow risk bundle. Current strategy reviews should ask whether cash, sleeves, and watchlists are merely rebuilding the same AI/growth exposure after a pullback.
- A high `valuation_concentration_pressure` flag does not force selling by itself; it raises the confirmation threshold for fresh adds and makes support/reclaim evidence more important.

Strategy mapping:

- `market fear gate`: context only; valuation pressure is not a panic signal without current VIX, breadth, credit, and trend evidence.
- `trend_aligned_entry`: reinforces waiting for reclaim and relative strength when expensive growth sells off.
- `flow_fragility`: combine valuation pressure with narrow breadth, options/crowding, tight credit, and systematic-flow risk.
- `AI_quality/capex_cycle`: prefer names with durable cash flows and proven AI monetization when valuation concentration is elevated.
- `portfolio concentration`: review whether multiple holdings express one U.S. growth / AI capex / wealth-effect bet.
- `replay protocol`: add valuation-concentration notes to 2021-2022, 2024-2026 AI concentration, and 2026-06-05 AI/semiconductor/storage replays.

Evidence notes:

- High evidence for the `Diversifying Beyond 60/40` article existence and body via official-domain Reader.
- Medium evidence for strategy transmission because it is an asset-allocation view and must be validated against the strategy's actual universe, timing rules, and drawdown behavior.
- Do not treat GMO's asset-allocation preference as a direct U.S. equity buy/sell signal.

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

## 2026-06-12 Catch-up Update: Citadel Securities Token Cost Elasticity

Source page:

- https://www.citadelsecurities.com/news-and-insights/global-macro-strategy/tokenomics/

Verified public item:

- Citadel Securities / Frank Flight published `Tokenomics` on 2026-06-10. The article was first captured in this memory on 2026-06-12 as a catch-up item because it was not in the prior institutional framework, but its publication date is before the 2026-06-12 automation window.

Reusable framework:

- Add `token_cost_elasticity` under `AI_quality/capex_cycle`.
- Treat AI adoption as constrained by all-in token cost, compute availability, power, cooling, memory bandwidth, and inference budgets, not only by model capability.
- Split AI deployment into `frontier_high_cost` and `everyday_cost_efficient` paths. The first should concentrate in firms with balance-sheet depth, research depth, and high-value operating domains; the second may favor cheaper models, targeted copilots, and token-efficient workflows.
- Interpret falling token-price or token-expenditure indexes carefully. They can signal efficiency and broader usage, but may also indicate substitution away from expensive frontier models.
- For AI infrastructure names, separate durable physical bottleneck demand from valuation expectations that assume ubiquitous, frictionless, immediate deployment.

Strategy mapping:

- `market fear gate`: context only; no regime change without current VIX, breadth, credit, and index-trend data.
- `concentrated holdings`: reinforces duplicate-theme and single-narrative review for AI capex names.
- `institutional overlay`: extends `AI_quality/capex_cycle` and `AI bottleneck watch` with a cost-elasticity dimension.
- `replay protocol`: future AI drawdown or software/infrastructure rotation replays should record token-cost, inference-budget, and model-substitution evidence.

Evidence notes:

- High evidence for the official article existence, title, author, date, and body.
- Medium evidence for strategy transmission because the framework is macro/market-structure interpretation and should be validated against actual AI revenue, capex, and price-action data.
- Do not treat this as a buy/sell signal or as a stable decision.

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

### Man Group: Climate-Resource / AI-Input Stress (2026-07-07)

Source page:

- https://www.man.com/insights/views-from-the-floor-2026-7-july

Reusable framework:

- Climate volatility can be a correlated input shock rather than an isolated weather headline: heat and drought can jointly raise cooling load, constrain water-intensive power generation and metals supply, and add food/LNG/fertiliser pressure.
- AI data centres add electricity and cooling-water demand to that system. This is a risk-transmission framework, not evidence that a particular weather event will move a particular stock.
- The useful distinction is between a verified physical constraint (power, water, LNG, logistics or metal disruption) and a narrative-only climate warning. The latter remains `unavailable`/watch-only until independently supported by public data.

Strategy mapping:

- Add `climate_resource_input_stress` as a diagnostic subfield of `factor_macro_exposure`; record `low`, `elevated`, `high`, or `unavailable`, plus source and as-of date. Use the reproducible classification below rather than an analyst's narrative judgement.
- When `elevated` or `high`, review AI infrastructure, memory/storage and optical/interconnect together for common exposure to power, cooling, water, copper/aluminium and financing-cost pressure; do not convert the flag into a directional commodity or equity signal.
- Keep the market fear gate, completed-close trend confirmation, and existing concentration caps primary. Any sizing rule must first pass point-in-time replay.

Classification and evidence contract:

- Each event row must retain: constraint category, affected geography/supply chain, direct AI-capex linkage, severity (`limited`/`material`/`severe`), independently sourced evidence count, `first_visible`, `as_of`, and `expires_at`. Republishes, syndications and quotations of the same underlying source count as one source.
- `unavailable`: no active event has at least two independent, dated public sources. Absence of a headline is not evidence for `low`.
- `low`: one verified, limited constraint category with at least two independent sources and a plausible, but indirect or geographically limited, link to the monitored AI-capex supply chain.
- `elevated`: either one verified material constraint with a direct AI-capex/supply-chain link, or two or more concurrent verified `low` categories affecting that chain.
- `high`: two or more concurrent verified material constraints, or one severe directly linked constraint, with at least two independent sources for every contributing category.
- An event expires on its stated end date; if no end date is stated, a `low` event expires after 10 trading days and an `elevated`/`high` event after 5 trading days unless a newly dated source refreshes it. Conflicting credible evidence resolves to the lower level and is recorded in the event row.

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
