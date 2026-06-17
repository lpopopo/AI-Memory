# 2026-06-16 US Stock Order Prep

Run time: 2026-06-16 20:49 Asia/Shanghai.

Task: `automation-2` daily U.S. stock premarket candidate order-prep. This is not a broker instruction and records no order placement.

## Inputs

- Read required core memory: `summary.md`, `decisions.md`, `daily-summaries.md`.
- Read recent daily records including 2026-06-16 realtime public/institutional monitor, 2026-06-16 layered review, and 2026-06-15 formal post-close portfolio summary.
- Read required references: market fear framework, portfolio concentration rules, daily monitoring framework, institutional overlay checklist/scorecard, and AI quality/capex-cycle classification.
- Read `tools/README.md` Quote Workflow Smoke Test.
- Read current 20:32 realtime public-source and 20:36 institutional checker outputs.

## Quote Workflow

Node quote workflow was run first using `stock_service.js` and returned structured `Tencent (Primary)` quote objects for MRVL, RDW, AMD, WDC, STX, ORCL, RKLB, SPY, QQQ, SMH, HYG, LQD, IWM, RSP, and VIX. Python and Google browser fallback were not required.

Data quality:

- Equity/ETF quotes: usable structured local quote objects.
- VIX: low quality locally because OHLC/volume were zero; keep prior formal external VIX/VIX3M context for market gate.

## Strategy State

- Market gate remains `elevated / repair risk-on`, not full normal.
- Cash target: keep at least 25% cash by framework; operationally no fresh real-account order is final without user/broker cash, fee, FX, settlement, and open-order sync.
- Flow fragility remains elevated because QQQ/SMH and AI infrastructure leadership are strong while IWM/RSP lag.
- Confirmed current real-account holdings remain MRVL 1 share and RDW 5 shares; AMD/WDC/STX are historical replay/watch only, not real holdings.

## Candidate Prep Summary

- MRVL: conditional profit-protection review only; no add.
- RDW: defensive near-stop review; no averaging down.
- ORCL: watch-only pullback/reclaim candidate; no chase after extension.
- RKLB: watch-only only because RDW already occupies the speculative space/satellite sleeve.
- AMD/WDC/STX: not listed as real-account order candidates; historical replay/observation only.

No stable rule was promoted to `decisions.md`.

Not investment advice.
