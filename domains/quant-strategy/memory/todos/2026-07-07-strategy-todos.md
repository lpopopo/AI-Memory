# 2026-07-07 Strategy Todos

Run time: 2026-07-08 09:36 Asia/Shanghai. Scope: formal post-close audit.

## Priority 0 - broker facts and stop execution

1. Confirm whether GLW `2`, DRAM `4`, MXL `6`, and MRVL `4` are still held. If still held, all remain mandatory risk-handling items and real new-buy capacity stays `0%`.
2. If any were sold, record ticker, quantity, fill price, time, fees, FX and settlement from user/broker report only.
3. Confirm XLI old order state: `never placed / cancelled / open / filled`. If open, it conflicts with the zero-new-buy gate and should be cancelled by user/broker action.

## Priority 1 - portfolio reconciliation

4. Reconcile broker cash after MU sale and any additional stop executions. Working formal NAV estimate is `USD 5,935.53` only if GLW/DRAM/MXL/MRVL remain open.
5. Verify platform fees, FX spread, tax and settlement effects.

## Priority 2 - next analysis

6. Treat AI-capex rebounds as risk-reduction windows unless all stops are closed and a promoted/frozen rule set explicitly authorizes a new entry.
7. Recheck AMD `492`, WDC `500`, and STX `835` replay risk lines on the next completed close; STX is currently below `835` and should remain `reduce-review` in replay context.
8. Independently verify the 20:30 monitor gaps: CNBC/SemiAnalysis Kyber source, NVIDIA roadmap, COHR/LITE order or margin evidence, and institutional official pages.
