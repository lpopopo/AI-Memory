# 2026-06-12 US Stock Order Prep Rerun

Run time: 2026-06-12 21:28 Asia/Shanghai.

Scope: automation-2 rerun for Chinese premarket candidate order-prep only. This is not broker activity, not a real order, and not a final trade instruction.

## Required Context Read

- `summary.md`, `decisions.md`, `daily-summaries.md`.
- Recent daily records: `2026-06-12-us-stock-premarket-strategy.md`, `2026-06-12-realtime-public-institutional-monitor.md`, `2026-06-12-details.md`, and related 2026-06-11/2026-06-12 real-account state records.
- Required references: `market-fear-technical-framework.md`, `portfolio-concentration-rules.md`, `daily-market-monitoring-framework.md`, `institutional-overlays-daily-checklist.md`, `institutional-overlay-scorecard.md`, `ai-quality-capex-cycle-classification.md`.
- Quote workflow instructions: `domains/quant-strategy/tools/README.md` Quote Workflow Smoke Test plus `quant-stock-data` skill reference.

## Market Data Check

Local quote workflow status: available.

- Node path: `stock_service.js` returned structured quote objects for `MRVL`, `AMD`, `WDC`, `STX`, `SPY`, `QQQ`, `SMH`, and `VIX`.
- Python path: Codex bundled Python returned structured quote objects for the same list.
- Selected source: `Tencent` / `Tencent (Primary)`.
- Data-quality note: quotes appear to be 2026-06-11 regular-session close snapshots with premarket fields mostly zero; use them as latest local structured quotes, not as full intraday tape.

Key quotes:

| Ticker | Local quote | Source | Strategy status |
| --- | ---: | --- | --- |
| MRVL | 280.71 | Tencent | watch only / no chase |
| AMD | 488.45 | Tencent | reduce-review below 492 |
| WDC | 529.29 | Tencent | defensive hold / repair review |
| STX | 868.09 | Tencent | defensive hold / repair review |
| SPY | 737.76 | Tencent | broad repair |
| QQQ | 717.12 | Tencent | growth repair |
| SMH | 609.45 | Tencent | semiconductor repair, high beta |
| VIX | 21.67 | Tencent | still elevated by local close snapshot |

Public news cross-check on 2026-06-12 still supports a repair-watch regime, not a normal-risk regime: Barron's reported VIX near 18.5 in early trading; Investing.com described the prior Wall Street rebound and oil decline on U.S.-Iran deal hopes; Adobe results/news remained a reminder that AI application/software evidence can be rejected by price; Marvell's CFO hire from Adobe is a catalyst/watch item, not a chase-buy signal.

## Order-Prep Conclusion

Market gate: `elevated / repair watch`.

New order permission: no immediate new buy order is allowed from this rerun; only watch-only levels or conditional prep are valid until the user syncs real account cash/holdings and the market confirms trend-aligned entries.

Cash target: keep model cash target around `60%-70%`; real account equity exposure remains unconfirmed and should be treated as cash/no confirmed stock holdings after the user-confirmed MRVL exit unless the user later syncs brokerage data.

No stable decision was promoted.

