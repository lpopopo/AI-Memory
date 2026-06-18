# 2026-06-18 US Stock Order Prep

Run time: 2026-06-18 21:36 Asia/Shanghai.

Scope: `automation-2` daily U.S. stock open-prep. This is candidate preparation only, not broker login, not order submission, and not a record of real execution.

## Inputs Checked

- Required memory and rules: root README, memory architecture, quant summary / decisions / hypotheses / daily summaries, latest daily / todos / portfolio / trades, market fear framework, concentration rules, daily monitoring framework, institutional overlay checklist / scorecard, AI quality / capex-cycle classification, replay protocol, strategy blueprint, and quote workflow instructions.
- Public-source checker since `2026-06-17T12:45:40.258Z`: wrote and read `work/realtime-public-source-latest.md/json`.
- Institutional checker since `2026-06-17T12:45:40.258Z`: first run timed out, rerun with longer timeout succeeded; wrote and read `work/institutional-research-latest.md/json`.
- Quote workflow: Node `stock_service.js` returned structured Tencent Primary quote objects. Yahoo chart returned about 125 daily bars for the candidate set. Browser / Google fallback was not required.

## Realtime Public / Institutional Evidence

- X accounts `@nvidia`, `@elonmusk`, and `@realDonaldTrump`: no post-window verified account post. Jina profile diagnostics returned status 200 but zero-length content for each account.
- Xiaohongshu account `美研芝格君`: raw public HTML / SSR returned visible title candidates and `raw_profile_html` length about `935041`, but no stable note URL, publish time, or body. Evidence is low-to-medium for theme temperature only, not a body-level fact.
- AQR / GMO / Man: official list and detail channels were readable, but no post-window new framework was verified.
- Citadel Securities: one official-domain post-window verified item, `July`, dated `2026-06-18`, mapped to `flow_fragility` / market-structure monitoring. It supports attention to options expiry, month-end / quarter-end rebalancing, positioning reset, and possible July seasonal flow support. It is not a standalone trade signal.

## Market / Risk Gate

- Market gate remains `elevated / repair`, not stress or panic.
- VIX Yahoo chart snapshot showed about `16.99` intraday on 2026-06-18; latest reliable VIX3M from Yahoo chart was stale at 2026-06-12, so term-structure confidence is limited.
- SPY / QQQ / SMH were above key 50-day trends, with SMH and storage/memory leaders showing strong but crowded risk-on behavior.
- Institutional overlay remains `flow_fragility=elevated`: strong AI / semiconductor / storage leadership, high theme crowding, and existing RDW risk item block fresh chase buys.

## Candidate Conclusions

| Ticker | Status | Daily K-line basis | Prep action |
| --- | --- | --- | --- |
| RDW | real holding, exit / stop-review still active | Latest intraday `13.82-13.94`, below 5/10/20D and below `14.50` review line; 50D near `13.75`; ATR about `2.34` | User-confirmed sell/reduce review remains first priority; no averaging down |
| MRVL | real holding, manual risk hold / no add | Latest `308.99-309.35`, above 5/10/20/50D but far extended vs 20D near `257.54`; prior 20D high `324.20`; ATR about `37.76` | Hold review / no add; profit-protection review if it approaches `315-324` |
| AMD | watch / replay only | Latest about `533`, above 5/10/20/50D, near 20D high `558.37`; ATR about `36.63` | No real action; watch only, no chase |
| WDC | watch / replay only, extended leader | Latest about `788-792`, far above 20D near `567.24` and 50D near `480.90`; fresh gap-up | No chase; participation only after pullback/base and account risk sync |
| STX | watch / replay only, extended leader | Latest about `1131-1136`, far above 20D near `912.62` and 50D near `762.10`; fresh gap-up | No chase; watch only |
| ORCL | watch only | Latest about `178`, below 5/10/20/50D and near prior `176` review line | Watch only; no buy until reclaim `185-190` or hold support with relative strength |
| RKLB | watch only | Latest about `105`, above 50D near `103.86` but below 10/20D; RDW risk unresolved | No second space exposure while RDW remains triggered |

## Action Conclusion

Today does not authorize new real-account orders. The preparation list is: resolve RDW risk first, keep MRVL as manual risk hold / no add, and leave AMD / WDC / STX / ORCL / RKLB as watch-only until user synchronizes broker cash, open orders, fees, FX, and confirms whether RDW should be sold/reduced or held defensively.

No stable rule was promoted to `decisions.md`.

Not investment advice.

## User Feedback / Process Error

User correctly challenged that WDC was missed. The run had usable WDC quote and daily K-line data, and existing decisions.md already requires strong trend leaders to be labeled as trend participation candidates with a concrete controlled plan rather than left as generic watch-only. The output was too conservative/mechanical because it over-weighted RDW risk and theme crowding without still presenting a conditional one-share WDC participation plan for user confirmation. Future open-prep outputs must show the controlled participation path and cancellation/stop levels even when final action remains subject to account sync.

## Correction Run After User Feedback

Run time: 2026-06-18 21:42 Asia/Shanghai.

Fresh Tencent Primary quote and Yahoo daily K-line refresh:

- WDC: quote about `794.11`, day high about `799.87`, day low `763.00`, previous close `712.13`, 5D MA about `680.91`, 20D MA about `567.38`, 50D MA about `480.95`, ATR14 about `51.93`. Corrected classification: `trend participation candidate`, not generic watch-only.
- RDW: quote about `13.47`, still below `14.50` stop-review and below 5/10/20D; remains the first real-account risk item.
- MRVL: quote about `310.33`, repaired but extended; hold / profit-protection review rather than add.

Corrected WDC plan: if user confirms available HKD 40,000 cash and accepts one share above the normal 15% single-stock threshold, a controlled one-share WDC participation plan can be prepared with a breakout trigger above `800`, a pullback alternative near `780-785` / `763-765`, and cancellation if WDC loses the opening range or SMH / QQQ confirmation fades. No broker action was taken.

## Real GLW Fill

User later confirmed that the GLW support-test order filled:

- Ticker: `GLW`
- Action: buy
- Shares: `2`
- Fill: `USD 181.50`
- Gross notional: `USD 363.00`
- Estimated buy-side platform fee: about `USD 1.00`
- Buy-fee-adjusted cost: about `USD 182.00/share`
- Estimated round-trip breakeven: about `USD 182.50/share`

Recorded files:

- `memory/trades/2026-06-18-real-glw-buy.md`
- `memory/portfolio/2026-06-18-portfolio-summary.md`

Risk line: below `181` is caution; below `180` without quick reclaim triggers stop / exit review. Initial target / profit-protection zone remains `192-198`.

## DRAM Watchlist Add

User asked whether `DRAM` was visible and then requested adding it to the local watchlist.

Verification:

- Local quote workflow returned `USDRAM` / `usdram.am`, price about `76.28`, previous close `69.95`, change about `+9.05%`, high about `76.29`, low about `75.02`, volume about `15.1M`.
- Yahoo chart cross-check for `DRAM` showed meta price about `76.36`, previous close `69.95`, day high about `76.36`, day low about `75.00`.
- Web check identified `DRAM` as the Roundhill Memory ETF, a memory-stock thematic ETF launched on 2026-04-02, not a single operating company.

Memory updates:

- Added `DRAM` to `memory/summary.md` as a memory/storage thematic ETF proxy.
- Added `DRAM` to `memory/hypotheses.md` watchlist context.
- Added `DRAM` to `references/ai-quality-capex-cycle-classification.md` as `thematic_etf / memory_storage_basket`.

Strategy note: `DRAM` is a theme read-through / basket proxy for AI memory-storage exposure, not a standalone buy signal and not a same-day +50% candidate without separate catalyst evidence.

## SMCI Watchlist Add

User requested adding `SMCI` to the local watchlist.

Classification:

- Theme: AI server / rack-scale infrastructure / hardware integration.
- Role: high-volatility watch / satellite only.
- Strategy use: monitor AI server demand, rack-scale deployment, liquid cooling, supply-chain integration, customer concentration, margin quality, and competitive pressure.

Memory updates:

- Added `SMCI` to `memory/summary.md` as an AI server / rack-scale infrastructure watch name.
- Added `SMCI` to `memory/hypotheses.md` watchlist context.
- Added `SMCI` to `references/ai-quality-capex-cycle-classification.md` as `AI_server_integrator / rack_scale_infrastructure`.

Strategy note: `SMCI` is not a buy signal. It requires stronger accounting / governance risk review, margin and cash-flow evidence, trend confirmation, and portfolio concentration checks before any trade role.
