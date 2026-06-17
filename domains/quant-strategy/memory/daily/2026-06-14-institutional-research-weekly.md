# 2026-06-14 Institutional Research Weekly Study

Run time: 2026-06-14 18:08 Asia/Shanghai

Window used: `2026-06-08T14:21:03.357Z` to checker run time `2026-06-14T10:08:33.531Z`.

This note is a weekly deep-study update for AQR Research, Citadel Securities Market Insights, GMO Research Library, and Man Institute Market Views. It records public research learning only. It is not a trade recommendation and does not override the market fear gate, trend confirmation, concentration rules, stops, or user/broker-confirmed account state.

## Local Checker Output

Required checker command completed after a longer timeout:

```powershell
node D:\code\AI-Memory\domains\quant-strategy\tools\institutional-research-checker.js --since 2026-06-08T14:21:03.357Z --max-items 8 --out D:\code\AI-Memory\domains\quant-strategy\work\institutional-research-latest.md
```

Outputs read:

- `work/institutional-research-latest.md`
- `work/institutional-research-latest.json`

Checker summary:

| Source | Window result | Evidence status |
| --- | --- | --- |
| AQR Research | 0 post-window items, 8 candidates checked | Official list and detail pages readable through Reader; window after baseline had no new AQR item. |
| Citadel Securities Market Insights | 0 post-window items, 0 candidates extracted in this run | Reader official-domain list channel returned readable response but no article candidates; manual Reader checks for `Tokenomics` and `Too Much of a Good Thing?` returned security-verification pages in this run. Do not call the whole source unavailable; classify this run as list-channel readable / detail blocked or not extracted. |
| GMO Research Library | 5 post-window list candidates, 8 candidates checked | Official list page readable. Checker marked five 2026-06-12 candidates as list-only; manual Reader detail succeeded for `GMO 7-Year Asset Class Forecast: May 2026` and `Diversifying Beyond 60/40 with a More Dynamic Allocation`. |
| Man Institute Market Views | 1 post-window verified item, 8 candidates checked | Official list and details readable through Reader; `When the AI Bubble Bursts, Don't Count on the US Consumer` verified with title, date, and body. |

## New Research Index

| Source | Date | Title | Link | Topic | Evidence |
| --- | --- | --- | --- | --- | --- |
| AQR | 2026-05-19 | `Total Portfolio Approach` | https://www.aqr.com/Insights/Research/Alternative-Thinking/Total-Portfolio-Approach | Portfolio construction, guardrails, flexible allocation | High for existence/content; pre-window / existing. |
| AQR | 2025-12-01 | `Hold the Dip` | https://www.aqr.com/Insights/Research/Alternative-Thinking/Hold-the-Dip | Trend-aligned entry vs plain dip buying | High for existence/content; pre-window / existing. |
| AQR | 2025-11-24 | `Active Extension` | https://www.aqr.com/Insights/Research/White-Papers/Active-Extension | Active risk efficiency, index concentration, long-short alpha capacity | High for existence/content; pre-window / existing. |
| Citadel Securities | 2026-06-10 catch-up in prior memory | `Tokenomics` | https://www.citadelsecurities.com/news-and-insights/global-macro-strategy/tokenomics/ | Token-cost elasticity, AI deployment cost, inference economics | Prior memory records official-domain body verification; current run hit security verification, so no new framework is extracted today. |
| Citadel Securities | 2026-06-07 / pre-window vs this run | `Too Much of a Good Thing?` | https://www.citadelsecurities.com/news-and-insights/macro-thoughts/too-much-of-a-good-thing/ | AI capex, inflation bottlenecks, compute economics | Prior checker snapshots read detail; current run detail blocked. Treat as existing context, not new today. |
| GMO | 2026-06-12 | `Diversifying Beyond 60/40 with a More Dynamic Allocation` | https://www.gmo.com/americas/research-library/diversifying-beyond-6040-with-a-more-dynamic-allocation_insights/ | Expensive U.S. growth, tight credit spreads, valuation-sensitive dynamic allocation | High for title/date/body via official-domain Reader manual check. |
| GMO | 2026-06-12 | `GMO 7-Year Asset Class Forecast: May 2026` | https://www.gmo.com/americas/research-library/gmo-7-year-asset-class-forecast-may-2026_gmo7yearassetclassforecast/ | Long-horizon asset-class expected return context | Medium-high for title/date and download page; limited article body, use as valuation context only. |
| GMO | 2026-06-12 list candidates | `Japan Equities`, `Japan's Next Phase...`, `Part 1: What Barbarians Like to Take Private` | See checker JSON | Japan governance / private-equity topics | List-only in checker for this run; record as candidates, do not extract new U.S. quant framework without detail body. |
| Man Institute | 2026-06-09 | `When the AI Bubble Bursts, Don't Count on the US Consumer` | https://www.man.com/insights/views-from-the-floor-2026-9-june | AI concentration, K-shaped consumption, consumer backstop fragility | High for official article title/date/body; already added as framework on 2026-06-09, reinforced this week. |

## Source Learning

### AQR

AQR had no post-window new research after the weekly baseline. List and detail pages were still verified rather than treated as unavailable.

Reusable learning remains:

- `Hold the Dip`: do not treat cheaper price as an entry signal when it fights momentum. For the current strategy, dip-buying must be replaced by support hold / reclaim / relative-strength confirmation.
- `Total Portfolio Approach`: flexible capital movement can improve portfolio construction only when guardrails prevent hidden concentration. This maps directly to theme overlap, sleeve correlation, and market fear constraints.
- `Active Extension`: relaxing long-only constraints can improve active risk efficiency in theory, but current live strategy remains long-only; for this repo it is only a diagnostic idea: benchmark-relative active risk and index-concentration exposure should be measured, not traded as a short book.

### Citadel Securities

This run should not be recorded as Citadel unavailable. The checker reached the official-domain Reader list channel but did not extract article candidates; manual Reader detail checks hit security verification for `Tokenomics` and `Too Much of a Good Thing?`.

Reusable learning therefore stays with already captured items:

- `Tokenomics`: AI adoption should be tested against all-in token cost, inference budgets, compute availability, power/cooling, memory bandwidth, and substitution toward cheaper models.
- `Too Much of a Good Thing?`: AI capex and compute economics can support infrastructure demand but can also create inflation, power, and adoption bottleneck risk.
- Strategy implication: `flow_fragility` should combine narrow leadership with cost/energy/inflation pressure, not only options or ETF flow.

### GMO

GMO produced the most useful new weekly input. The official list showed multiple 2026-06-12 items, and manual Reader detail verified at least two official-domain pages.

Key takeaways:

- `Diversifying Beyond 60/40` argues that strong recent market gains can turn a default allocation into a concentrated bundle of expensive U.S. growth equities plus tight-spread credit exposure.
- The article's practical point is not "avoid growth"; it is that high valuation and extrapolated growth assumptions reduce the margin for error when the market is concentrated in U.S. growth and AI-adjacent winners.
- For quant-strategy, this adds a valuation-concentration dimension to `portfolio concentration` and `factor_macro_exposure`: a portfolio can look diversified by ticker count but still be one expensive U.S. growth / AI / credit-liquidity bet.
- `GMO 7-Year Asset Class Forecast` is useful as a long-horizon valuation context source, but the page exposed mainly the title/date/download surface in this run. Use it as a monitoring input, not as a new rule.

### Man Institute

Man's 2026-06-09 article was verified again and remains the most important new post-window institutional item.

Key takeaways:

- AI leadership concentration can mask weakness in mass-market consumer demand.
- Aggregate spending and equity-market strength can be held up by affluent households and a narrow large-cap cohort.
- If AI enthusiasm reverses, the lower and middle income consumer may not cushion the equity-market shock.
- For quant-strategy this strengthens `consumer_backstop_fragility`, `K_shaped_consumption_risk`, and the need to record whether AI drawdowns coincide with consumer, credit, energy, or inflation stress.

## Mapping To Quant Strategy

Immediate daily-monitoring observations:

- Add `valuation_concentration_pressure` to the daily institutional overlay note when U.S. growth / AI leadership is narrow, valuations are extended, and credit spreads are tight.
- Keep `trend_aligned_entry = cheap_but_unconfirmed` until support/reclaim plus relative strength confirm; lower price alone is not enough.
- Keep `flow_fragility` on medium/elevated watch when AI winners are narrow and token-cost / energy / inflation constraints are rising.
- In `AI_quality/capex_cycle`, separate platform/hyperscaler cash-flow resilience from cyclical suppliers and speculative bottleneck beneficiaries.
- In `factor_macro_exposure`, explicitly note whether the current book is one concentrated U.S. growth / AI capex / wealth-effect bet.

Unverified hypotheses added:

- H10: Valuation-concentration overlay may reduce false adds in expensive U.S. growth / AI regimes by blocking fresh exposure when the strategy is already long the same valuation, duration, and growth-extrapolation risk.

Stable framework/reference updates:

- Updated `references/institutional-market-research-framework.md` with `valuation_concentration_pressure` and `dynamic_allocation_drift`.
- Updated `references/institutional-overlays-backtest-plan.md` with Overlay E: valuation concentration and dynamic allocation pressure.

Backtest/replay tasks:

- Add a diagnostic-only series first: record `valuation_concentration_pressure` during daily reports without changing trades.
- Replay 2021-2022 growth-duration drawdown, 2024-2026 AI concentration episodes, and the 2026-06-05 AI/semiconductor/storage drawdown.
- Compare baseline V5/Double-Radar behavior against a variant that reduces new AI/growth adds when valuation concentration, flow fragility, and trend weakness are all present.

## AI Theme Implications

AI infrastructure:

- Still a valid watch theme, but institutional inputs increasingly warn against extrapolating capex demand without checking token economics, power/cooling, and customer-funded cash flows.

AI applications:

- Application names need revenue, retention, margin, and price confirmation. GMO and Citadel both push against treating product narrative as equal to durable monetization.

Storage and memory:

- WDC/STX/MU style cyclical suppliers remain high capex-cycle sensitivity. Their role should stay tactical/satellite unless earnings, pricing, and relative strength confirm.

Optical/interconnect:

- The bottleneck thesis remains important, but Man/GMO/Citadel together argue for crowding and valuation checks before increasing exposure. Optical winners need both bottleneck evidence and durable revenue/margin capture.

Market risk:

- The largest shared warning is concentration: AI market leadership, affluent-consumer spending, tight credit, and U.S. growth valuation can all fail together. Daily reports should make this overlap visible before any new add.

## Memory Updates Made

- Added this weekly note: `memory/daily/2026-06-14-institutional-research-weekly.md`.
- Added H10 to `memory/hypotheses.md`.
- Added a 2026-06-14 weekly update to `references/institutional-market-research-framework.md`.
- Added Overlay E to `references/institutional-overlays-backtest-plan.md`.
- Appended a summary line to `memory/daily-summaries.md`.
- Left `memory/decisions.md` unchanged.

## Next Validation Items

1. Add `valuation_concentration_pressure` to the next daily institutional overlay block.
2. Build a simple daily proxy: QQQ/SPY, RSP/SPY, SMH/QQQ, IGV/QQQ, HYG/LQD, VIX, and top-10 contribution share if available.
3. Replay 2026-06-05 and 2026-06-10 to 2026-06-12 with baseline vs overlay annotations.
4. Test whether the overlay blocks more false adds than true winners before any promotion to `decisions.md`.
