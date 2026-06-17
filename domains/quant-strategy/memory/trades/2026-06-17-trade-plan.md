# 2026-06-17 Trade Plan

Run time: 2026-06-17 23:03 Asia/Shanghai.

Scope: daily U.S. stock execution preparation and real-account ledger sync. This is intraday / pre-close preparation only, not the formal 04:15 post-close audit, not broker login, and not real order submission.

## 1. Data Snapshot

Primary quote source: local Node `StockService.fetchQuotes`, Tencent Primary, refreshed around 2026-06-17 23:00 Asia/Shanghai. Daily K-line source: Yahoo chart API, 3-month daily bars, refreshed during this run. External volatility cross-check: public Cboe / Yahoo / MarketWatch / Investing.com visible snippets around 2026-06-17 show VIX around `16.5-16.6`.

Data quality:

- Equity / ETF intraday quotes: usable structured local quote objects, delayed public data, not broker executable data.
- Daily OHLC / moving averages: usable public daily bars; 2026-06-17 row is still intraday and not a completed close.
- VIX: local quote workflow remains low-quality for VIX; external public pages are used for sanity check only.
- Broker facts: cash, FX, taxes, settlement, margin status, and open orders remain unverified.

| Ticker | Latest | Change | Day high / low | Daily MA5 / MA10 / MA20 / MA50 | 20D high / low | Strategy read |
| --- | ---: | ---: | --- | --- | --- | --- |
| MRVL | 291.19 | +4.49% | 295.43 / 283.32 | 287.95 / 282.80 / 251.52 / 194.06 | 324.20 / 182.28 | intraday reclaim above 285/289.50, but prior close already triggered reduce-review; wait for completed close |
| RDW | 14.18 | +5.00% | 14.56 / 13.55 | 15.22 / 16.89 / 18.41 / 13.59 | 26.64 / 12.86 | still below 14.50 stop-review and below 5/10/20D MAs; no averaging down |
| AMD | 521.07 | +2.72% | 529.85 / 507.30 | 515.16 / 498.36 / 497.80 / 405.11 | 558.37 / 426.05 | above 492 replay line; repair watch only, not a real holding |
| WDC | 723.93 | +6.29% | 729.48 / 694.55 | 630.26 / 577.33 / 551.23 / 472.08 | 729.92 / 456.18 | storage leadership extended near 20D high; no chase |
| STX | 1073.45 | +4.08% | 1087.76 / 1043.90 | 985.69 / 924.07 / 894.02 / 749.57 | 1097.00 / 741.00 | storage leadership extended near 20D high; no chase |
| SPY | 749.43 | -0.12% | 752.15 / 747.85 | 746.82 / 743.04 / 747.23 / 728.41 | 760.40 / 722.59 | broad market flat, above key daily MAs |
| QQQ | 732.07 | +0.30% | 735.68 / 729.56 | 728.89 / 720.77 / 725.98 / 690.69 | 748.65 / 686.37 | growth stabilized but not clean risk-on breakout |
| SMH | 633.78 | +2.89% | 637.30 / 626.88 | 625.29 / 608.38 / 603.35 / 543.05 | 649.24 / 551.65 | semiconductor rebound, but after sharp 6/16 unwind |
| ORCL | 187.32 | -0.54% | 190.19 / 184.70 | 187.30 / 200.54 / 205.60 / 187.65 | 250.25 / 175.28 | around 5/50D but below 10/20D; watch only |
| RKLB | 107.74 | +2.97% | 110.40 / 104.04 | 107.81 / 110.57 / 122.96 / 102.37 | 151.00 / 99.61 | still below 10/20D; no second space satellite while RDW is impaired |

## 2. Real Trades / Pending / Model Trades

Confirmed real-account fills already recorded:

| Date | Ticker | Action | Shares | Fill | Gross notional | Classification | Source |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 2026-06-15 | MRVL | Buy | 1 | 289.50 | 289.50 | pullback starter, AI interconnect / custom silicon | user confirmation |
| 2026-06-15 | RDW | Buy | 5 | 15.00 | 75.00 | high-volatility space satellite | user confirmation |

Waiting user confirmation:

- Whether RDW should be sold / reduced after the completed 2026-06-16 close below `14.50`, or held only for a manual post-close review.
- Whether MRVL should remain manual hold after the 2026-06-16 close below `280`, or be reduced if it fails to close back above `285-289.50`.
- Broker cash, USD/HKD conversion, fees, taxes, settlement, margin status, and any stale open orders.

Model / simulated trades: none added. The retired historical model ledger remains replay context only.

## 3. Institutional Overlay Summary

```text
flow_fragility_state: elevated, about 8-9/14
trend_aligned_entry_state: MRVL held position = partial intraday repair but still post-stop reduce-review; RDW = trend_broken; fresh AI/space/storage adds = cheap_but_unconfirmed or chase-invalid
AI_quality/capex_cycle: MRVL cyclical_supplier / bottleneck high sensitivity; RDW speculative_space high sensitivity; AMD/WDC/STX cyclical high sensitivity; ORCL platform_cloud watch; RKLB speculative_space watch
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high; sleeve_correlation_high for historical replay basket; policy_hysteresis_risk; AI_capex_cashflow_pressure; AI_listing_window_liquidity; semiconductor_momentum_vs_software_monetization divergence
action impact: prioritize RDW and MRVL risk decisions; block fresh buys until triggered positions and broker facts are synchronized; allow only observation triggers, not executable new entries
```

New buy impact: no new buy passes `trend_aligned_entry` today because existing real positions still need risk decisions, RDW remains below its stop-review level, and the current market data is intraday rather than confirmed close.

## 4. Execution Checklist

| Priority | Ticker | Direction | Quantity | Target amount | Approx account weight | Reference price | Trigger condition | Stop / review price | Invalid condition | Strategy reason | Main risk | Status |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | RDW | Sell / exit-review, or defensive hold only if user rejects sell | 5 held; any sell requires user confirmation | about USD 70.90 at 14.18 | about 2.8% NAV | 14.18 latest; 15.00 gross cost; 15.20 buy-fee-adjusted cost; 15.40 round-trip breakeven | User confirms exit after prior completed close below 14.50, or next completed close remains below 14.50 | 14.50 close review; no averaging down; below 13.55/12.86 increases gap risk | Reclaim and completed close above 14.50 reduces urgency; reclaim above 16.00 can move back to defensive hold | high-volatility satellite is below 5/10/20D MAs and below stop-review | selling locks loss; holding risks deeper drawdown / financing and theme reversal | waiting user confirmation; no broker order placed |
| 2 | MRVL | Reduce-review / risk hold | 1 held; possible sell requires user confirmation | about USD 291.19 | about 11.4% NAV | 291.19 latest; 289.50 gross cost; 290.50 buy-fee-adjusted; 291.50 round-trip breakeven | If it fails to hold/reclose above 285-289.50 after prior close below 280, confirm reduce or exit; if completed close is back above 289.50 with SMH stable, defer to post-close hold review | review below 285; reduce/exit review below 280 close; priority exit below 275 close | Fresh add invalid while event rally is unconfirmed and prior stop breach has not been cleared by completed close | AI interconnect starter has intraday repair, but 6/16 close breached the risk plan | capex-cycle crowding; whipsaw after event rally; fee-adjusted breakeven is only marginally cleared | reduce-review, not upgraded yet; no add |
| 3 | AMD | Watch only / replay repair watch | 0 real shares | 0 | 0 | 521.07 latest | Reconsider only after completed-close strength plus QQQ/SMH confirmation and account risk sync | replay risk reference 492 close | Any close below 492 returns AMD to reduce-review in replay context | above 5/10/20D and above prior risk line, but volatile after semiconductor unwind | chase risk and capex-cycle beta | watch only; no real action |
| 4 | WDC | Watch only / replay defensive hold, extended | 0 real shares | 0 | 0 | 723.93 latest | Only reassess after pullback toward daily support or base formation | replay risk reference 500 close | Fresh buy invalid near 20D high after vertical extension | storage remains strong, but entry quality is poor | reversal / theme crowding | watch only |
| 5 | STX | Watch only / replay defensive hold, extended | 0 real shares | 0 | 0 | 1073.45 latest | Only reassess after pullback toward daily support or base formation | replay risk reference 835 close | Fresh buy invalid near 20D high after vertical extension | storage remains strong, but entry quality is poor | reversal / theme crowding | watch only |
| 6 | ORCL | Watch only | 0 | 0 | 0 | 187.32 latest | Recheck only if it reclaims 190-195 with QQQ support, or holds 175-185 support with relative strength | 176 review line | No entry while below 10/20D and real-position risk is unresolved | cloud / AI factory watch candidate | capex burden, debt, margin risk | watch only |
| 7 | RKLB | Watch only | 0 | 0 | 0 | 107.74 latest | Recheck only after RDW risk is resolved and RKLB reclaims 110.5/20D with theme confirmation | 95 review line | No second space satellite while RDW is below stop-review | space infrastructure watch candidate | high volatility and sleeve overlap | watch only |
| 8 | Stale broker orders | Check / cancel if unwanted | n/a | n/a | n/a | n/a | User checks broker open-order screen | n/a | Any stale order remains active | prevent accidental duplicate exposure | unintended real fill | user confirmation required |

## 5. Required User Confirmation

- RDW: confirm sell / reduce after prior completed close below `14.50`, or explicitly keep as manual defensive hold until the 04:15 post-close audit.
- MRVL: confirm whether prior close below `280` should trigger a reduce order if the current session cannot close back above `285-289.50`.
- Confirm no stale real orders remain open in MRVL, RDW, AMD, WDC, STX, ORCL, or RKLB.
- Confirm current broker cash, settled USD, HKD/USD rate, fees, tax, and whether HKD 40,000 capital is actually available.

## 6. Replay Protocol

Replay protocol is applicable as a framework, but no replay ledger row was added in this run because 2026-06-17 is still an intraday row. Do not prefill future dates. The next eligible update is the completed 2026-06-17 close row during the formal post-close audit.

Not investment advice.
