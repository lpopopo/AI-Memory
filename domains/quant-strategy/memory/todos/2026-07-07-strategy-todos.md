# 2026-07-07 Strategy Todos

Run time: 2026-07-07 23:17 Asia/Shanghai. Scope: intraday execution prep and full watchlist scan.

## Priority 0 - broker facts and stop execution

1. Confirm whether GLW `2`, DRAM `4`, MXL `6`, and MRVL `4` are still held. If still held, all remain mandatory risk-handling items and real new-buy capacity stays `0%`.
2. If any were sold, record ticker, quantity, fill price, time, fees, FX and settlement from user/broker report only.
3. Confirm XLI old order state: `never placed / cancelled / open / filled`. If open, it conflicts with the zero-new-buy gate and should be cancelled by user/broker action.

## Priority 1 - portfolio reconciliation

4. Reconcile broker cash after MU sale and any additional stop executions. Working intraday NAV estimate is `USD 5,905.73` only if GLW/DRAM/MXL/MRVL remain open.
5. Verify platform fees, FX spread, tax and settlement effects.

## Priority 2 - next analysis

6. At 04:15 post-close, rerun completed-close audit with official VIX/VIX3M and completed daily bars.
7. If AI-capex bounces, explicitly label it as rebound risk-reduction window unless all stops are closed and V9/promoted rules authorize a new entry.
8. Independently verify the 20:30 monitor gaps: CNBC/SemiAnalysis Kyber source, NVIDIA roadmap, COHR/LITE order or margin evidence, and institutional official pages.
