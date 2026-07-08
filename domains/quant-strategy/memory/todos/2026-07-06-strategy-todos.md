# 2026-07-06 Strategy Todos

Run time: 2026-07-07 08:02 Asia/Shanghai. Scope: follow-ups from the 2026-07-06 formal post-close audit.

## Priority 0 - broker facts and stop execution

1. Confirm whether GLW `2`, DRAM `4`, MXL `6`, and MRVL `4` are still held. All four remain below existing completed-close risk lines after the 2026-07-06 close, so unresolved-stop veto keeps real new-buy capacity at `0%`.
2. If GLW/DRAM/MXL/MRVL were sold, record ticker, quantity, fill price, time, fees, FX and settlement from user/broker report only. Do not infer fills from market prices.
3. MRVL closed `249.27 < 260`; the intraday high above 260 does not cancel the completed-close failure. If still held, it stays `mandatory exit/reduce-review`; no event-rebound chase or averaging down.
4. Confirm XLI old order state: `never placed / cancelled / open / filled`. If open, it conflicts with the `0%` new-buy gate and should be cancelled by user/broker action.

## Priority 1 - portfolio reconciliation

5. Reconcile broker cash after MU `1 @ 1010` sale. Working estimate uses `USD 3,884.69` cash and `USD 6,104.49` NAV after a `USD 1` sell fee, but exact values require broker confirmation.
6. Verify whether platform fees, FX spread or taxes make the working NAV materially different from the estimate.
7. Keep AMD, WDC and STX in replay/watch scope only, not real holdings, unless the user supplies broker evidence.

## Priority 2 - strategy review

8. Continue portfolio-level AI-capex correlation review while `flow_fragility=acute` and `theme_overlap_high`.
9. Do not add new AI/semiconductor/storage exposure until all unresolved stops are closed or explicitly superseded by rule-consistent broker facts.
10. Recheck Cboe VIX official history on the next run because the VIX CSV had not yet updated to 2026-07-06 while VIX3M had.
