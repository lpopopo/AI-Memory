# Hypotheses

## 2026-05-29

### H1: US-stock-first universe improves strategy reliability

The strategy should focus on US equities first because market data availability, liquidity, disclosure quality, and backtest tooling are generally stronger than for mixed-market experiments.

Validation needed:

- Confirm stable daily OHLCV source.
- Confirm survivorship-bias-aware universe source or define an acceptable starting universe.
- Backtest against SPY and QQQ benchmarks.

### H2: Multi-factor confirmation is safer than single-signal chasing

Initial strategy should require at least trend, relative strength, and risk filter confirmation before entry.

Validation needed:

- Compare single-factor momentum against combined trend plus relative strength.
- Measure drawdown, turnover, win rate, and benchmark-relative return.

### H3: Alternative or external signals should be secondary at first

The first usable version should not depend on hard-to-verify alternative data. Price, volume, liquidity, fundamentals, and event calendars should come before sentiment or news-derived signals.

Validation needed:

- Build a price-volume baseline.
- Add fundamentals/events only after baseline backtest is stable.

### H4: Dual-sleeve allocation can balance compounding and opportunity capture

A 50% value sleeve plus 50% hot-industry momentum sleeve may produce better behavioral and risk balance than a pure momentum or pure value strategy.

Validation needed:

- Backtest value sleeve, tactical sleeve, and combined portfolio separately.
- Compare against SPY, QQQ, and a 50/50 SPY/QQQ benchmark.
- Measure whether combined drawdown is lower than the tactical sleeve alone.
- Check whether both sleeves are accidentally concentrated in the same sectors or factors.

Initial V0 result:

- ETF-proxy V0 did reduce drawdown versus SPY and QQQ.
- ETF-proxy V0 did not outperform SPY, QQQ, or 50/50 SPY/QQQ on CAGR or Sharpe.
- Hypothesis remains open; needs V1 with true scoring models before acceptance or rejection.

V1 optimization result:

- V1 improved strongly over V0: CAGR 18.14% and Sharpe 1.00.
- V1 still did not clearly beat 50/50 SPY/QQQ on CAGR or drawdown.
- V1's best result depended on QQQ fallback, so the dual-sleeve thesis remains unproven.
- Hypothesis remains open and needs walk-forward validation plus individual-stock sleeves.

Revalidation result:

- V1 showed stronger performance in 2022-2026 and much better 2022 drawdown control.
- V1 underperformed in 2016-2021 bull-market conditions.
- Hypothesis should be reframed: dual-sleeve ETF V1 may be useful as a regime-aware drawdown-control strategy, but not yet as a full-cycle return-maximizing strategy.

V2 result:

- V2 improved bull-market participation by shifting to 35% value / 65% tactical-growth during confirmed QQQ bull regimes.
- V2 slightly beat 50/50 SPY/QQQ on full-period CAGR and Sharpe, while drawdown remained slightly worse.
- V2 still did not beat QQQ on full-period CAGR.
- Hypothesis remains promising but not proven; next evidence should come from walk-forward validation and individual-stock implementation.

V2 robustness revalidation:

- Rolling 3-year windows show V2 beats 50/50 SPY/QQQ on CAGR in 4 of 9 windows, drawdown in 6 of 9 windows, and Sharpe in 4 of 9 windows.
- Evidence supports V2 as a defensive/regime-aware ETF strategy more than as a consistently superior return engine.
- Hypothesis remains open; individual-stock sleeves or a bull accelerator are needed before treating the strategy as superior.

V3 result:

- A stronger ETF-level bull accelerator did not improve on V2.
- V3 matched V2's full-period CAGR but had worse drawdown and lower Sharpe.
- Evidence now points toward individual-stock leadership selection as the next required improvement path.

### H5: AI infrastructure bottleneck tracking can improve candidate-universe selection

Qualitative public research sources focused on AI compute, interconnect, optical modules, and storage may help identify which subthemes deserve a temporary candidate-universe tilt before pure price momentum fully reflects the shift.

Initial source:

- Xiaohongshu account "美研芒格君" repeatedly focuses on AI infrastructure bottlenecks including optical modules/interconnect, memory/storage, AI inference, cloud capex, and earnings-driven dislocations.
- On 2026-06-19, user-authorized logged-in Chrome reading exposed the 16-image carousel for `分享我压箱底的，AI下一阶段“瓶颈”玩家`. The image-level framework added testing / validation and interconnect delivery networks as more explicit bottleneck layers, with `TER` and `CRDO` as source-only new candidate lines requiring independent validation.
- X account `@Kay2289123` appears to be the same public-source identity and, through user-authorized logged-in Chrome reading on 2026-06-19, exposed recent timeline posts and long-form Articles around `MRVL`, `NVDA`, `ORCL`, `AVGO`, `TTMI`, `AXTI`, token inference, AI cloud factories, optical/InP, equipment, and moving AI bottlenecks.
- See `references/xiaohongshu-mungerjun-content-framework.md`.

Validation needed:

- Build an AI infrastructure watchlist grouped by bottleneck subtheme.
- Compare strategy results with and without a qualitative-theme candidate-universe tilt.
- Require normal technical filters: relative strength, 63/126-day momentum, 50/200-day trend, benchmark comparison, and drawdown control.
- Test crowding flags when content repeatedly signals sector overheating.

2026-06-24 evidence update:

- Logged-in Chrome exposed the new Xiaohongshu note `要看懂MRVL和10 倍万亿光互联，Credo很关键` (ID `6a3b5e5c0000000015027e00`) with readable body, author comments, relative edit time, and all `24/24` carousel images.
- The source thesis splits CRDO into two evidence chains: `current_AEC_cashflow` from SerDes/AEC/retimer scale-out connectivity, and `optical_optionality` from optical DSP, silicon-photonics PIC, ZeroFlap modules, and acquired optical assets.
- This is source-driven research structure, not a confirmed company fact or trade signal.

Additional validation needed:

- Verify CRDO employee count, revenue growth, customer concentration, AEC contribution, optical revenue guidance, acquisition terms, CPO exposure, product distances/speeds, optical gross margin, and hyperscaler adoption from 10-K/10-Q, earnings calls, and official product material.
- Add `scale_up`, `scale_out`, and `scale_across` labels to the AI interconnect watchlist.
- Replay whether the two-chain classification improves candidate ranking after AI/semiconductor drawdowns without increasing theme overlap or false entries.

2026-06-25 evidence update:

- Logged-in Chrome exposed Xiaohongshu note `MU先别眼红, 5+4逻辑全面梳理搞懂存储产业` (ID `6a3caa1a000000001700a95a`) with readable body, author comments, relative time and all `21/21` carousel images.
- The source framework separates memory demand into `SRAM`, `HBM`, `DDR`, `NAND/SSD`, `HDD`, and application-specific `edge_memory`; this is a candidate research taxonomy, not a confirmed demand forecast.
- X Article `2069958412872638784` adds a separate inference-accelerator test: low single-user latency can coexist with weaker high-concurrency unit economics, customer concentration, data-center capex burden and margin volatility.
- X post `2069864998801961428` adds a CXL-memory-efficiency path: cheaper memory, compression and pooling may reduce capacity cost, but latency, software adoption, hot/cold-data fit and realized TCO must be measured.

Additional validation needed:

- Build `memory_hierarchy_demand_map` fields for HBM/DDR/NAND-SSD/HDD/CXL/edge memory and record revenue exposure, inventory, pricing, capex, gross margin and relative strength.
- Add `latency_vs_throughput_cost` fields for inference accelerators: single-user latency, total throughput, concurrency, energy, unit token cost, software ecosystem and customer concentration.
- Replay memory-theme gaps and earnings surprises over 5/20/60 trading days to separate structural demand from supply-shortage crowding.
- Treat `CBRS` as source-driven speculative inference watch only until SEC filings, customer contracts, margins, OCF-CapEx and price trend are independently verified.

2026-06-26 evidence update:

- Logged-in Chrome showed no strict-window new Xiaohongshu note; the latest non-pinned note remained the already captured MU/storage note, so no new carousel evidence was added.
- X `@Kay2289123` added an ALAB Article (`2070338459932529140`) and related MRVL/ALAB/CRDO posts that strengthen the need to split AI interconnect into `MRVL_custom_optical_CXL`, `ALAB_interconnect_router`, and `CRDO_scale_out_AEC_optical_optionality` rather than treating them as interchangeable optical/interconnect exposure.
- X `@Kay2289123` added a Samsung/SK Hynix capex thread (`2070399554625982852` and replies) that supports an `HBM_upstream_bottleneck_map`: WFE tools, wafer thinning, TSV etch, TCB / hybrid bonding, ABF substrate materials, EUV mask blanks, and photoresists.
- X `@Kay2289123` added a Micron / hyperscaler-cost-pushback post (`2070403183680045076`): memory pricing power may trigger customer and supplier responses through capacity expansion, CXL/compression, procurement pushback, and architecture changes.

Additional validation needed:

- For ALAB, verify CXL/PCIe/retimer revenue, customer concentration, inventory, gross margin, product roadmap, hyperscaler adoption, and relative strength versus QQQ/SMH/CRDO/MRVL.
- For HBM upstream, verify Samsung/SK Hynix official capex, actual orders to ASML/AMAT/LRCX/KLAC/DISCO/ASMPT/Hanmi/material suppliers, delivery timing, revenue exposure, valuation, liquidity and post-announcement 5/20/60-day returns.
- For memory-cost pushback, track DDR/HBM/NAND contract pricing, hyperscaler capex commentary, CXL/compression deployment, realized TCO, and whether memory supplier margin strength leads to downstream demand destruction or architecture substitution.

2026-06-29 evidence update:

- Xiaohongshu note `6a41e1fd00000000170095e6` adds `decoder_latency_specialist`: Cerebras/WSE-style wafer-scale SRAM may excel at low-latency decoder and long Agent chains, but this does not establish superior business quality without concurrency, capacity, cluster scaling, yield, ecosystem, customer concentration, margins and OCF-CapEx evidence.
- X posts `2071359522791473185` and `2071423413944734166` add `memory_substitution_stack`: HBF, CXL, predictive tiering, SRAM inference and Optical HBM should be compared as complementary paths using end-to-end latency, capacity, power, software migration, reliability and realized TCO.
- X post `2071479718315168032` adds `compute_rationing`: visible model-access quotas may support alternative compute providers, but could also expose dependence, utilization, financing and margin fragility.
- X post `2071488648776958136` adds `capex_supply_response`: Samsung/SK Hynix expansion can support upstream tools/materials while reducing medium-term scarcity rents; both directions require official capex and 5/20/60-day price/revenue validation.
- Xiaohongshu note `6a2b982f0000000017029b43` adds `capacity_to_revenue_lag`: for AI factories, depreciation and operating cost can start at power-on while GPU deployment, testing, customer acceptance, billing and utilization ramp later. Track RPO, powered/installed/accepted/billable capacity, utilization, gross margin, FCF, financing and dilution separately; do not treat contracted capacity as cash or live utilization.

2026-06-30 evidence update:

- X Article `2071640439934074904` adds `capacity_relief_vs_bandwidth_relief`: HBF, CXL/tiering, compression and SRAM-oriented designs should be evaluated for capacity relief separately from PIM/PNM and optical-interconnect bandwidth/power relief.
- NVIDIA posts `2071654937335926864` and `2071715347581837357` add `secure_sovereign_ai`: Azure-hosted GB300 agent workloads and air-gapped government/critical-infrastructure deployments may represent distinct demand pools, but require contract size, utilization, certification and revenue evidence.
- NVIDIA post `2071979909199577560` adds `software_efficiency_demand_elasticity`: lower token cost can reduce hardware per unit of inference while expanding total inference demand. Replay must test both effects rather than assume a one-way capex implication.
- Kay follow-up posts on CBRS/MRVL/ALAB/GLW add a source-attention crowding flag. Author-stated holdings and gains are not verified trades and should enter `theme_crowding / flow_fragility`, not candidate scores.

2026-07-02 evidence update:

- Kay META posts `2072359344705085763` and `2072364009341464877` add `localized_capacity_mismatch_vs_structural_demand`: a company can resell capacity in a region/GPU generation/time bucket while broader demand remains tight. Validate with utilization, rental prices, GPU generation, geography, contract terms and official capex rather than treating either “oversupply” or “shortage” as a universal label.
- Kay equipment post `2072022672603848988` adds `equipment_capex_lead_lag`: hiring requirements, fab expansion and management Q&A may precede equipment orders and revenue recognition. Validate official capex, orders, backlog, delivery, acceptance, revenue and margins for AMAT/KLAC/LRCX/ASML before ranking.
- Interconnect/equipment posts repeatedly display self-reported 40%-170% gains, heavy positioning and concentration language. These are `source_attention_crowding` evidence only and must not enter company quality scores or real-account trade memory.
- Replay the META compute-resale rumor and equipment-capex posts over 1/5/20/60 days versus QQQ/SMH/XSD, recording volume and maximum adverse excursion.
- Xiaohongshu note `6a45e9690000000016027e78`, verified with `32/32` images, adds `memory_standard_power_shift`: when hyperscalers specify long contracts, interfaces and system architecture, value may migrate from commodity bit production toward standards, controllers, predictive tiering, packaging/foundry and software. Validate JEDEC/OCP/CXL standards, procurement contracts, HBM4 base-die/foundry claims, product qualification, volume and revenue before ranking.
- The same note reinforces that capacity relief (HBF, CXL, predictive tiering, SRAM) and bandwidth/data-movement relief (PIM/PNM, optical interconnect, 3D integration) are complementary, not interchangeable. Replay and scoring must keep capacity, bandwidth, latency, power, standard maturity and realized TCO separate.

Additional validation needed:

- Build separate score fields for capacity added/saved, bandwidth, latency, power, software migration, reliability, standard maturity and realized TCO.
- For secure/sovereign AI, track disclosed contract value, GPU count, deployment timing, utilization, software attach and recurring revenue.
- Replay official performance claims and influencer follow-up posts over 5/20/60 trading days versus QQQ/SMH, including maximum adverse excursion and post-event volume.

2026-07-06 evidence update:

- Chrome-visible Xiaohongshu复核显示 `6a45e9690000000016027e78` 仍是最新可见非置顶笔记，正文继续支持把“绕开内存税”拆成容量缓解、带宽/搬运缓解、CXL/标准、软件调度、封装/代工和 SRAM 等分支；本轮图片级新增核验失败，当前-run 为 `0/32`，不得覆盖 2026-07-02 的历史 `32/32` 证据。
- Kay X 新增 `AI_FDE_token_demand_signal`：微软/亚马逊 forward-deployed engineers 可能代表企业 AI 落地和 token 消耗需求，但需招聘数据、客户付费、云收入和 token 用量验证。
- Kay X 新增 `AI_token_budget_control`：Tesla 员工 AI token 配额传闻说明成本控制可能与需求不足并存，不能把预算上限单向解释为 AI ROI 失败。
- Kay X 新增 `custom_AI_chip_memory_pull`：Anthropic/Samsung 自研 AI 芯片传闻与存储瓶颈相关，但必须回到 The Information 原文、Samsung/Anthropic 官方、工艺、订单和存储接口验证。
- NVIDIA 官方帖新增 `AI_domestic_supply_chain_localization` 观察：美国 AI 供应链、本土制造和伙伴生态可能成为政策/产业叙事字段，但没有订单、收入、产能或毛利证据前，不影响 AI 质量分或持仓角色。
- Replay 需要把 2026-07-02 至 2026-07-06 的 Kay/NVIDIA/Elon/Trump 事件按 first-visible time 冻结，比较 1/5/20/60 日 QQQ/SMH/XSD/HYG/LQD、相关 ticker、成交量和最大不利波动。

2026-07-07 evidence update:

- Chrome-visible Xiaohongshu profile still shows `6a45e9690000000016027e78` as the latest non-pinned note, with no strict-window new note. Current-run detail/image review failed (`300017` or explore redirect), so image-level evidence remains `0/32` for this run and historical `32/32` from 2026-07-02 is not overwritten.
- Kay X post `2074172593175957904` adds `rack_architecture_delay_vs_pluggable_lifecycle`: if Kyber/rack-scale or CPO timing is delayed, 800G/1.6T pluggable optics, DSP, and scale-out links may have a longer validation window. This requires CNBC/SemiAnalysis original text, NVIDIA roadmap confirmation, COHR/LITE/AAOI/MRVL order evidence, and hyperscaler capex validation.
- NVIDIA official posts add `open_model_research_ecosystem` and `AI_for_good_compute_access` as ecosystem observations. These support monitoring of AI research and compute-access narratives but do not prove incremental revenue, orders, utilization, or margins.
- Elon Musk's `Grok Imagine update` adds `xAI_generative_video_iteration` under application-layer monitoring. It needs product usage, subscription, token cost, inference margin, and compute procurement evidence before it can be mapped to infrastructure demand.
- Replay should add the Kay Kyber/CPO post, NVIDIA ICML/open-model posts, NVIDIA AI for Good posts, and Elon Grok Imagine update to the 2026-07-06/07 event table, then compare 1/5/20/60-day returns and maximum adverse excursion for QQQ/SMH/XSD plus NVDA/COHR/LITE/AAOI/MRVL.

2026-07-09 evidence update:

- Chrome-visible Xiaohongshu profile still shows no strict-window new note; the latest non-pinned item remains `6a45e9690000000016027e78`. Direct detail access redirected to explore, so current-run image evidence remains `0/32`; do not overwrite the historical `32/32` image read from 2026-07-02.
- Kay X posts `2074755111679877351`, `2074541184098398705`, `2074528471225892956`, and `2074583043361386771` add candidate fields `token_intensity_from_better_models`, `custom_compute_co_design`, `AI_hardware_deleveraging_chain`, and `MRVL_valuation_path_compression`. These require official OpenAI/DeepSeek/MRVL/Reuters/company-source verification before affecting scores or rules.
- NVIDIA official posts `2074872091388903774` and `2074510027897844105` add `agentic_AI_inference_stack` and `CPU_GPU_utilization_bottleneck`: agent workflows may shift bottleneck attention from GPU-only capacity toward CPU orchestration, tool calls, software stack and inference cost, but this needs benchmark, deployment and revenue evidence.
- Kay self-reported returns, cash level, position discipline and buy/sell behavior remain `source_attention_crowding` only. They are not real-account fills, not verified trades, and not company facts.
- Replay should freeze the 2026-07-07/08 Kay/NVIDIA/Elon event rows by first-visible time and compare 1/5/20/60-day returns and maximum adverse excursion for QQQ/SMH/XSD/HYG/LQD plus MRVL/ALAB/CRDO/MU/DRAM/GLW/MXL/NVDA/AMD/INTC/ORCL/CRWV/NBIS.

### H6: AI application-layer monitoring may become a separate investable theme

AI application evidence should be tracked separately from GPU, data center, optical, and storage infrastructure. Strong consumer adoption or enterprise AI workflow evidence does not automatically mean more infrastructure buying; it can benefit application software, cloud platforms, inference compute, storage, cybersecurity, or endpoints depending on monetization and cost structure.

Initial 2026-06-03 evidence:

- Reuters/Sensor Tower reported that ChatGPT crossed 1B global monthly active app users, supporting consumer AI adoption but not directly proving public-stock monetization.
- Nvidia/Huang comments helped repair the "AI kills software" narrative, but this is still narrative evidence unless CRM/NOW/ADBE/SNOW/DDOG/CRWD show AI revenue, ARR, retention, pricing power, and gross-margin stability.
- Initial watch pool: SNOW, CRWD, DDOG, NOW, CRM, ADBE, MSFT, GOOGL, AMZN, META, APP, PLTR.

2026-07-09 evidence update:

- Elon/X-visible Grok 4.5 posts and reposts add `xAI_agent_model_cost_efficiency`: coding/agent models are being marketed around speed, token efficiency, lower cost and Cursor/Vercel distribution. Treat this as application-layer and inference-demand monitoring, not infrastructure demand proof.
- Kay/OpenAI-visible GPT 5.6 discussion adds a parallel `longer_reasoning_more_tool_use` watch field. Validate with official OpenAI release material, enterprise usage, token consumption, cloud deployment, pricing and margin evidence before mapping to public equities.

Validation needed:

- Track AI-related revenue, ARR/ACV, paid users, retention, gross margin, inference cost, and capex burden.
- Separate proven revenue from product launches, customer anecdotes, and market narrative.
- Require price relative strength versus QQQ/IGV and no violation of market fear/concentration rules before any application-layer buy recommendation.

2026-06-08 evidence update:

- Physical AI / robotics and industrial digital twins should be added to the AI application observation pool after NVIDIA/SK hynix referenced personal AI and physical AI in its memory roadmap and Reuters/Investing.com reported an expanded NVIDIA/Hyundai physical-AI and robotics partnership.
- Initial U.S.-listed watch dimensions: NVDA platform exposure, TSLA/autonomous systems, TER/ROK/DE/ISRG industrial or robotics proxies, and software/platform links through Omniverse, simulation, edge AI, and digital twins.
- Evidence strength is high for partnership/product-roadmap facts but still medium-to-low for public-equity monetization. Validation must require customer deployments, robotics revenue, Jetson/Omniverse adoption, unit economics, and price relative strength before any trade trigger.

2026-06-11 watchlist update:

- User requested adding Tesla, Nokia, and Qualcomm to the observation list.
- `TSLA` is reaffirmed under physical AI / autonomous systems as watch/satellite only.
- `QCOM` is added under edge inference / mobile, automotive, PC, and device-side AI as watch-only.
- `NOK` is added under telecom/network infrastructure and private-network edge-AI optionality as watch-only.
- This update expands the monitoring universe only. It does not authorize buys while market fear is `stress`, flow fragility is elevated/acute, or trend-aligned entry remains broken.

2026-06-11 additional watchlist update:

- User asked about `RKLB`.
- Add `RKLB` under space / satellite / edge-AI infrastructure as watch/satellite only.
- Treat RKLB as a high-volatility optionality name tied to launch cadence, satellite systems revenue, defense/government demand, financing risk, and execution quality. It requires stronger confirmation than core AI names before any trade role.

2026-06-11 additional watchlist update:

- User asked about `RDW`.
- Add `RDW` under space / satellite / space-infrastructure optionality as watch/satellite only.
- Treat RDW as a high-volatility space-infrastructure name tied to backlog quality, satellite/component revenue, government/national-security demand, margins, debt/financing risk, and price relative strength.

2026-06-11 additional watchlist update:

- User requested adding Intel and Oracle to the observation list.
- Add `INTC` under AI compute / AI PC / foundry-turnaround as watch/satellite only.
- Add `ORCL` under cloud / AI factory / database infrastructure as watch-only.
- Neither name is a buy signal. INTC requires roadmap, margin, foundry/customer, and relative-strength confirmation; ORCL requires AI backlog conversion, capex/margin/debt discipline, and price confirmation.

2026-06-18 additional watchlist update:

- User requested adding `DRAM`.
- Add `DRAM` under memory / storage bottleneck monitoring as the Roundhill Memory ETF, a thematic ETF proxy for global memory-stock exposure rather than a single operating company.
- Treat `DRAM` as a basket-level read-through for memory/storage leadership, useful when WDC/STX/MU/SNDK single-stock concentration or price-per-share risk is too high.
- This is not a buy signal. It requires ETF holdings/structure review, liquidity/spread checks, trend confirmation, market fear gate permission, and comparison versus existing single-name candidates before any trade role.

2026-06-18 additional watchlist update:

- User requested adding `SMCI`.
- Add `SMCI` under AI server / rack-scale infrastructure / hardware integration as a high-volatility watch name.
- Use it to monitor AI server demand, rack-scale deployment, liquid cooling, supply-chain integration, customer concentration, margin quality, and competitive pressure.
- This is not a buy signal. SMCI requires stronger accounting / governance risk review, margin and cash-flow evidence, trend confirmation, and portfolio concentration checks before any trade role.

2026-06-19 additional watchlist update:

- User requested that the newly learned `美研芒格君` / `Kay2289123` X and Xiaohongshu carousel content be added into the local strategy and watchlist.
- Add `CRDO` under AI interconnect / AEC / high-speed connectivity transmission as a source-driven watch name. Validate AEC revenue durability, hyperscaler mix, gross margin, copper-vs-optical distance economics, valuation, liquidity, and daily K-line before any trade role.
- Add or reclassify `TER` under AI testing / validation: HBM insertion, system-level test, and AI package validation. This supplements the older physical-AI/robotics watch angle. Validate semi-test cycle, AI/HBM exposure, order growth, margins, and relative strength.
- Add `MXL` and `AXTI` under optical / InP / interconnect component monitoring. Treat them as highly speculative component-layer candidates requiring revenue capture, customer concentration, dilution/liquidity, and volatility checks.
- Add `TTMI` under AI infrastructure / PCB / interconnect "shovel seller" monitoring. Validate AI data-center exposure, customer concentration, margin durability, backlog, valuation, liquidity, and trend confirmation.
- All five are `新增候选/待验证`; none is a buy signal.

2026-07-01 additional watchlist update:

- User formally requested adding `AMAT` to the self-selected monitoring universe.
- Classify AMAT under semiconductor equipment / wafer-fab equipment / AI capacity expansion, with high semiconductor-capex-cycle sensitivity.
- Monitor foundry/logic and DRAM/HBM equipment demand, advanced-packaging exposure, customer capex, order/backlog conversion, China/export-control exposure, gross margin, valuation, liquidity, daily trend and relative strength.
- AMAT was already present in the scanner's technical universe; this update makes it an explicit user-selected watch name. This is not a buy signal.

2026-07-01 canonical watchlist unification:

- User requested that every symbol already present in the codebase manual watchlist become a formal self-selected name and enter routine analysis.
- Canonical scope is the 31-symbol manual watchlist in `references/user-selected-watchlist.json`, not the separate 516-stock constituent research universe.
- Full-watchlist analysis must retain weak, repairing and data-unavailable names instead of showing only top-ranked candidates; ranking remains a selection layer, not an inclusion layer.
- `SPCX` remains context-only because it is not a public tradable ticker.

## 2026-06-08

### H7: Institutional flow-fragility overlay can reduce crowded AI drawdown risk

Public market-structure research from Citadel Securities suggests that the current AI/semiconductor rally may be supported by earnings revisions and buybacks, but also by narrow breadth, passive flows, retail/options demand, levered ETF exposure, CTA positioning, and volatility-control rebuilding. This can turn a strong trend into a fragile one if momentum stalls.

Proposed use:

- Add a daily `flow_fragility` note when AI/semiconductor leadership is narrow and upside-option or systematic-flow pressure appears elevated.
- Use it as a sizing/profit-protection overlay, not as a short signal.
- Combine it with the existing market fear gate and portfolio concentration rules.

Validation needed:

- Identify practical proxies available in daily workflow: breadth versus SPY/QQQ, SMH concentration, option implied-vol behavior, put/call/skew data if available, buyback window calendar, levered ETF theme exposure, and CTA/vol-control proxy data.

2026-07-05 institutional evidence update:

- Citadel Securities' official `1H 2026 Market Structure & Flows` article links historically high index/semiconductor concentration with accelerating passive flows, record retail participation, short-dated options, leveraged technology/semiconductor products, tighter financing capacity, low implied correlation, and `spot up / vol up` behavior.
- Add `short_duration_leverage_density`, `spot_vol_correlation_shift`, and `financing_capacity_pressure` to H7 validation. These remain amplification-risk diagnostics, not standalone bearish signals.
- Replay each field incrementally against the existing 14-point score and measure warning lead time, blocked winners, blocked losers, cash drag, and 1/5/20-day maximum adverse excursion.
- Test whether adding this overlay reduces drawdown after crowded semiconductor rallies without forcing premature exits during healthy trends.

2026-07-10 institutional evidence update:

- Man Group's official `H2 Technology Outlook - Still Dancing, But Moving Closer to the Door?` article adds `AI_stack_selectivity_rotation`, `private_AI_customer_concentration`, and `AI_IPO_lockup_pressure` to flow-fragility validation. The article's core point is that AI exposure is becoming more selective across stack layers while private-AI commitments and IPO/lock-up supply can create delayed pressure points.
- Replay the 2026-07-10 event over 1/5/20/60 days versus QQQ/SMH/XSD/HYG/LQD, semiconductor equipment, memory/storage, optical/interconnect, cloud infrastructure, cybersecurity/software-efficiency, SaaS and IPO/new-listing baskets.
- Treat these fields as monitoring inputs only; they do not override the market fear gate, stop rules, or unresolved-stop veto.

### H8: AI quality and capex-cycle classification improves candidate ranking

GMO and Man Group research point to a key split inside AI exposure: diversified platform/hyperscaler and quality suppliers may be more resilient than cyclical suppliers tied mainly to hyperscaler growth capex, while optical/interconnect bottlenecks may offer real upside but can become crowded or cyclically exposed.

Proposed use:

- Classify AI names into platform/hyperscaler, diversified supplier, cyclical supplier, application/data owner, and speculative bottleneck beneficiary.
- Use the class to set maximum weight, core/satellite status, and trim discipline.
- Require actual revenue, margins, customer diversification, balance sheet strength, and relative strength before promoting a bottleneck name to core.

Validation needed:

- Build a simple scoring sheet for current AI candidates: MRVL, AMD, WDC, STX, MU, AVGO, NVDA, MSFT, GOOGL, AMZN, META, SNOW, CRWD, DDOG, NOW, CRM, ADBE, plus optical/interconnect watch names.
- Backtest whether quality/capex-cycle labels improve post-signal holding returns and reduce gap-down risk after AI capex scares.

2026-07-01 institutional evidence update:

- Man Institute's official `The Hard Questions for AI Bonds Investors` article adds `cashflow_backstop_separation`: determine which segment supplies EBITDA/FCF and whether an AI buildout is self-funded rather than inferring credit quality from market capitalization.
- Add `AI_credit_supply_pressure` and `credit_duration_mismatch` to H8 validation. Large AI debt issuance may widen spreads through substitution effects, and long-dated bonds may price construction, technology and demand risk more harshly than short-dated debt.
- Validation needs issuer-level debt maturity, spreads, capex, billable utilization, segment cash flow, financing revisions and 1/5/20/60-day equity/credit replay before any rule promotion.

2026-07-02 NVIDIA evidence update:

- Official NVIDIA post `2072545807505527251` adds `AI_cloud_credit_support`: NVIDIA says it is using revenue-sharing and credit-support arrangements with AI clouds to deploy multi-tenant AI factories. This may broaden token-compute access, but it may also transmit partner credit, utilization, residual-value and financing risk back toward the platform/supplier.
- Validate named partners, contract size, GPU ownership, guarantees/credit recourse, utilization, pricing, depreciation/residual value, revenue recognition, cash conversion and defaults before this affects AI quality scores or position roles.
- Treat the item as a financing/capex-cycle hypothesis linked to `AI_credit_funding_fragility`, not as automatic demand confirmation or a stable decision.

2026-07-10 institutional evidence update:

- Man Group's official `H2 Technology Outlook` adds `semiconductor_peak_margin_trap`, `China_AI_efficiency_competition`, and `AI_stack_selectivity_rotation` to H8 validation. The article argues that value has accrued heavily at the chip layer while downstream software cash-flow monetization remains uneven, and that Chinese cost-to-output model competition may affect global AI economics.
- Validate semiconductor margin durability, downstream enterprise ROI, cloud backlog customer concentration, model cost/performance data, China supply-chain availability, IPO/lock-up calendars and price relative strength before changing any AI quality score or core/satellite role.
- Do not treat a single institutional outlook as a stable trading rule; keep it in replay/backtest context.

### H9: Trend-aligned support buys outperform plain dip-buying in the current strategy

AQR's trend-following research argues against automatic buy-the-dip timing because it often fights momentum. This directly affects current AI infrastructure pullback rules.

Proposed use:

- Replace any plain "buy lower" logic with "hold/reclaim support plus improving relative strength" logic.
- Treat cheaper prices as watchlist improvement only until price action confirms.

Validation needed:

- Compare support-buy variants across V4/V5/V6: plain pullback limit, reclaim-after-pullback, relative-strength reclaim, and fear-gated reclaim.
- Measure CAGR, max drawdown, false-entry rate, and missed-rebound cost.

## 2026-06-14

### H10: Valuation-concentration pressure can improve AI/growth add discipline

GMO's 2026-06-12 dynamic-allocation research suggests that after strong recent returns, default or passive-like portfolios can drift into a narrow bundle of expensive U.S. growth equities and tight-spread credit exposure. For the current US stock quant strategy, this may map to a portfolio that appears diversified by ticker but is effectively one AI/growth/duration/capex-extrapolation bet.

Proposed use:

- Add `valuation_concentration_pressure` to the institutional overlay block when U.S. growth / AI leadership is narrow, valuations are extended, and credit or liquidity conditions offer little cushion.
- Use it as an entry/sizing caution, not as a standalone sell signal.
- When the flag is high, require cleaner trend-aligned support/reclaim evidence before adding AI infrastructure, software, storage, or optical/interconnect exposure.
- Combine it with `flow_fragility`, `theme_overlap_high`, and `consumer_backstop_fragility`.

Validation needed:

- Build daily proxies: QQQ/SPY, RSP/SPY, SMH/QQQ, IGV/QQQ, HYG/LQD, VIX, and top-contribution concentration if available.
- Replay 2021-2022 growth-duration stress, 2024-2026 AI concentration episodes, and the 2026-06-05 AI/semiconductor/storage drawdown.
- Test whether the overlay blocks false adds after crowded rallies without blocking too many durable winners.

## 2026-07-05

### H11: Adaptive policy and physical AI input pressure can alter factor risk before equity trend breaks

Citadel Securities' 2026-06-19, 2026-06-20, 2026-06-27, and 2026-07-01 macro notes propose that a faster, less pre-communicated central-bank reaction function can raise short-end/tail volatility even if long-horizon inflation credibility improves. The same source argues that AI is initially a physical input-price shock through chips, memory, power, cooling, construction, and engineering before productivity gains dominate. Man Institute's 2026-06-23 article adds energy-logistics normalization risk rather than assuming a ceasefire or lower spot oil immediately removes supply-chain pressure.

Proposed use:

- Add `adaptive_policy_surprise`, `AI_input_cost_pressure`, and `energy_logistics_lag` as diagnostic fields under `factor_macro_exposure`.
- Use the fields to explain growth-duration, semiconductor, memory/storage, optical/interconnect, industrial, and application-software relative performance; do not use them as a directional rate, commodity, or equity trade signal.
- Keep the market fear gate primary and require completed-close trend/relative-strength confirmation before any action impact.

Validation needed:

- Build point-in-time event rows for policy communications, inflation releases, energy-logistics disruptions, and verified hardware price/capex evidence.
- Compare 1/5/20/60-day moves in 2-year and 10-year yields, curve slope, breakevens, DXY, VIX/VIX3M, HYG/LQD, QQQ/SPY, SMH/QQQ, IGV/QQQ, memory/storage, and optical/interconnect baskets.
- Test whether the fields add warning value beyond the existing fear gate and price trend; reject them if they merely restate moves already visible in market data.
- Measure CAGR, max drawdown, false-add rate, missed-winner rate, and cash drag before any promotion to `decisions.md`.

## 2026-07-11

### H12: Index-core momentum layers — regime keep, continuation reject

From the SPY/QQQ factor induction:

- **Retain:** MA150/MA200 trend regime for V9 embedded index-core weights; QQQ ~1.3x drawdown amplification when SPY 63-day DD &lt; −5%.
- **Reject for trade authorization:** absolute mom63 continuation and QQQ−SPY relative mom63 continuation into the next 21 days (failed on 2024–2026 / 2026YTD).
- **Reject as short signal:** “below MA200 stays weak for the next 63 days” (2026YTD V-recovery counterexample).

Status: incorporated into V9 as monitor-only via `references/v9-index-core-momentum-monitor.md` and `memory/decisions.md` (2026-07-11). Not a promotion of a momentum sleeve.

Validation needed for any future promotion beyond monitor status:

- Rolling sample-out protocol with costs, orthogonal to V8 monthly weights.
- Explicit separation of event-driven V-recoveries from trend regimes.
- No Rule E override unless forward gates are met independently.

### H13: Panic-to-repair monitoring and slow risk scaling may improve V9 tail control

Prospect-theory research supports a behavioral execution audit, while
momentum-crash research suggests that a prior market decline, elevated
volatility and a sharp rebound can create winner-crowding and high-beta reversal
risk. The direct academic mechanism is strongest in cross-sectional
long-winner/short-loser portfolios and does not automatically apply to V9's
long-only MA core or Rule E stock sleeve.

Status: research-only. See
`strategies/v9-execution/BEHAVIORAL_MOMENTUM_SUPPLEMENT.md`,
`strategies/v9-execution/validation/`, and first-pass outputs in
`strategies/v9-execution/results/validation/`. Formal V9 weights remain
unchanged.

Validation needed:

- Build a causal panic-to-repair label and test whether it adds warning value
  beyond the existing Fear Gate and MA150/MA200 regime.
- Test a separate 126-day slow-volatility overlay with no leverage, fixed
  exposure caps and realistic one-way costs.
- Measure long-winner and short-loser legs separately before mapping any WML
  result to V9.
- Report net CAGR, max drawdown, expected shortfall, skew, turnover, cash drag,
  false reductions and missed winners in rolling/expanding sample-out tests.
- Require point-in-time membership, deletions/delisting returns and genuinely
  new forward evidence before promotion.

## 2026-07-12

### H14: Verified climate-resource input stress may add an early AI-capex fragility diagnostic

Man Group's 2026-07-07 discussion of a possible strong El Niño treats heat, drought, power-grid load, cooling water, LNG, fertiliser and water-intensive metals as potentially compounding constraints. For AI data centres this suggests a conditional common-input risk across infrastructure, memory/storage and optical/interconnect rather than a standalone weather trade thesis.

Proposed use:

- Add `climate_resource_input_stress` under `factor_macro_exposure` only from dated, independently verifiable public evidence of active power, water, LNG/logistics or critical-material constraints; otherwise record `unavailable`.
- Use it to request a common-factor and input-cost review before fresh AI-capex adds when it agrees with `flow_fragility`, concentration or weak trend confirmation. The Fear Gate and completed-close price confirmation remain primary.

Validation needed:

- Build point-in-time rows for independently verified constraint events, preserving first-visible time and source; exclude hindsight relabeling of weather outcomes.
- Compare 1/5/20/60-day QQQ/SPY, SMH/QQQ, memory/storage, optical/interconnect, energy/power, industrial-metal, VIX/VIX3M, HYG/LQD and yield responses.
- Test incremental warning value over the Fear Gate, trend-aligned entry, flow fragility, `AI_input_cost_pressure` and `energy_logistics_lag`; reject the hypothesis if it merely restates market prices or produces excessive cash drag.
