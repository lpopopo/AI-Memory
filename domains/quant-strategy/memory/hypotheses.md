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
- See `references/xiaohongshu-mungerjun-content-framework.md`.

Validation needed:

- Build an AI infrastructure watchlist grouped by bottleneck subtheme.
- Compare strategy results with and without a qualitative-theme candidate-universe tilt.
- Require normal technical filters: relative strength, 63/126-day momentum, 50/200-day trend, benchmark comparison, and drawdown control.
- Test crowding flags when content repeatedly signals sector overheating.

### H6: AI application-layer monitoring may become a separate investable theme

AI application evidence should be tracked separately from GPU, data center, optical, and storage infrastructure. Strong consumer adoption or enterprise AI workflow evidence does not automatically mean more infrastructure buying; it can benefit application software, cloud platforms, inference compute, storage, cybersecurity, or endpoints depending on monetization and cost structure.

Initial 2026-06-03 evidence:

- Reuters/Sensor Tower reported that ChatGPT crossed 1B global monthly active app users, supporting consumer AI adoption but not directly proving public-stock monetization.
- Nvidia/Huang comments helped repair the "AI kills software" narrative, but this is still narrative evidence unless CRM/NOW/ADBE/SNOW/DDOG/CRWD show AI revenue, ARR, retention, pricing power, and gross-margin stability.
- Initial watch pool: SNOW, CRWD, DDOG, NOW, CRM, ADBE, MSFT, GOOGL, AMZN, META, APP, PLTR.

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

## 2026-06-08

### H7: Institutional flow-fragility overlay can reduce crowded AI drawdown risk

Public market-structure research from Citadel Securities suggests that the current AI/semiconductor rally may be supported by earnings revisions and buybacks, but also by narrow breadth, passive flows, retail/options demand, levered ETF exposure, CTA positioning, and volatility-control rebuilding. This can turn a strong trend into a fragile one if momentum stalls.

Proposed use:

- Add a daily `flow_fragility` note when AI/semiconductor leadership is narrow and upside-option or systematic-flow pressure appears elevated.
- Use it as a sizing/profit-protection overlay, not as a short signal.
- Combine it with the existing market fear gate and portfolio concentration rules.

Validation needed:

- Identify practical proxies available in daily workflow: breadth versus SPY/QQQ, SMH concentration, option implied-vol behavior, put/call/skew data if available, buyback window calendar, levered ETF theme exposure, and CTA/vol-control proxy data.
- Test whether adding this overlay reduces drawdown after crowded semiconductor rallies without forcing premature exits during healthy trends.

### H8: AI quality and capex-cycle classification improves candidate ranking

GMO and Man Group research point to a key split inside AI exposure: diversified platform/hyperscaler and quality suppliers may be more resilient than cyclical suppliers tied mainly to hyperscaler growth capex, while optical/interconnect bottlenecks may offer real upside but can become crowded or cyclically exposed.

Proposed use:

- Classify AI names into platform/hyperscaler, diversified supplier, cyclical supplier, application/data owner, and speculative bottleneck beneficiary.
- Use the class to set maximum weight, core/satellite status, and trim discipline.
- Require actual revenue, margins, customer diversification, balance sheet strength, and relative strength before promoting a bottleneck name to core.

Validation needed:

- Build a simple scoring sheet for current AI candidates: MRVL, AMD, WDC, STX, MU, AVGO, NVDA, MSFT, GOOGL, AMZN, META, SNOW, CRWD, DDOG, NOW, CRM, ADBE, plus optical/interconnect watch names.
- Backtest whether quality/capex-cycle labels improve post-signal holding returns and reduce gap-down risk after AI capex scares.

### H9: Trend-aligned support buys outperform plain dip-buying in the current strategy

AQR's trend-following research argues against automatic buy-the-dip timing because it often fights momentum. This directly affects current AI infrastructure pullback rules.

Proposed use:

- Replace any plain "buy lower" logic with "hold/reclaim support plus improving relative strength" logic.
- Treat cheaper prices as watchlist improvement only until price action confirms.

Validation needed:

- Compare support-buy variants across V4/V5/V6: plain pullback limit, reclaim-after-pullback, relative-strength reclaim, and fear-gated reclaim.
- Measure CAGR, max drawdown, false-entry rate, and missed-rebound cost.
