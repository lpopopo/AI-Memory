# 2026-06-15 US Stock Order Prep Rerun 2

Run time: 2026-06-15 20:59 Asia/Shanghai.

Scope: `automation-2` retry 2 for Chinese U.S.-stock candidate order-prep only. This is not broker activity, not a real order, and not a final trade instruction.

## Required Context Read

- Core memory: `summary.md`, `decisions.md`, `daily-summaries.md`.
- Recent daily records: 2026-06-14 details, 2026-06-14 institutional weekly, 2026-06-12 order-prep rerun, and 2026-06-12 realtime public/institutional monitor.
- Required references: `market-fear-technical-framework.md`, `portfolio-concentration-rules.md`, `daily-market-monitoring-framework.md`, `institutional-overlays-daily-checklist.md`, `institutional-overlay-scorecard.md`, and `ai-quality-capex-cycle-classification.md`.
- Quote workflow instructions: `domains/quant-strategy/tools/README.md` Quote Workflow Smoke Test.
- Same-day realtime public-source product: `work/realtime-public-source-latest.md/json`, run at 2026-06-15 20:57 Beijing.

## Market Data and Quality

Local quote workflow status: available.

- Node path `stock_service.js` returned structured `Tencent (Primary)` quote objects for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, HYG, LQD, IWM, RSP, VIX, ORCL, RKLB, NVDA, AVGO, MU, and ALAB.
- Bundled Python path returned matching structured `Tencent` quote objects for the same list.
- Equity and ETF quotes are usable as latest structured snapshots.
- Local VIX remains low quality because it returned `21.67` with zero OHLC and zero volume; VIX/VIX3M term structure remains a data gap.

Selected quotes:

| Ticker | Price | Change | Source | Quality |
| --- | ---: | ---: | --- | --- |
| MRVL | 279.70 | -0.36% | Tencent / Tencent Primary | usable |
| AMD | 511.57 | +4.73% | Tencent / Tencent Primary | usable |
| WDC | 562.93 | +6.35% | Tencent / Tencent Primary | usable |
| STX | 931.04 | +7.25% | Tencent / Tencent Primary | usable |
| SPY | 741.75 | +0.54% | Tencent / Tencent Primary | usable |
| QQQ | 721.34 | +0.59% | Tencent / Tencent Primary | usable |
| SMH | 619.96 | +1.72% | Tencent / Tencent Primary | usable |
| ORCL | 184.13 | +0.02% | Tencent / Tencent Primary | usable |
| RKLB | 102.39 | -10.79% | Tencent / Tencent Primary | usable but high-volatility |
| VIX | 21.67 | 0.00% | Tencent | low quality; OHLC/volume zero |

## Same-Day Realtime Input

The 2026-06-15 20:57 realtime public-source product verified no reliable new X content from `@nvidia`, `@elonmusk`, or `@realDonaldTrump`. Xiaohongshu raw public HTML exposed visible title candidates around MRVL, ORCL, AVGO, MU, ALAB, optical modules, token inference, NBIS, and CRWV, but without stable note URL, publish time, or body. Treat this as theme heat / crowding context only, not as a trade signal.

## Order-Prep Conclusion

Market gate: `elevated / repair watch`, not unrestricted `normal`. Broad ETFs and semiconductors repaired, but AI infrastructure/storage remains crowded, VIX quality is weak, and institutional overlays still flag valuation concentration and flow-fragility risk.

New real-account order permission: do not treat any row as directly executable. Only prepare watch-only / conditional limit levels. Real-account cash, settlement, FX, fees, tax, and open orders still require user sync before any real order size can be confirmed.

High-priority order-prep candidates:

| Ticker | Prep status | Reference level | Size note | Risk line |
| --- | --- | ---: | --- | ---: |
| MRVL | watch only / no chase | 270.00-267.50 pullback zone | 0 now; possible 1-share recalculation only after user sync | 263.00 / 260.00 |
| AMD | watch only / repair watch | 500.00-494.00 reclaim/pullback zone | 0 now; possible 1-share recalculation only after user sync | 492.00 close-loss review |
| ORCL | watch only | 179.50-180.00 support/reclaim zone | 0 now; possible 1-share recalculation only after user sync | 176.00 |
| RKLB | watch only / high-volatility review | 100.00-99.50 stabilization zone only | 0 now; speculative satellite only after user sync | 95.00 |

WDC and STX remain historical replay / observation context only after sharp extensions; no fresh real-account buy prep was promoted. No stable decision was promoted.
