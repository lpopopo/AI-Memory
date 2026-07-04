# 2026-07-03 Strategy Todos

Run time: 2026-07-03 23:15 Asia/Shanghai. U.S. market holiday; next tradable regular session is expected 2026-07-06.

## Priority 0 — broker facts and stop execution

1. Confirm whether GLW `2`, DRAM `4`, MXL `6`, and MU `1` were sold after their existing completed-close triggers. Impact: estimated NAV/exposure can be materially wrong and delayed exits increase gap risk. Likely cause: repeated `awaiting confirmation` loop. Fix: user/broker supplies order status or fills; verify quantity, price, time and fees without storing credentials. Next step: if still held, apply the stable next-session-open execution rule.
2. MRVL `4 @ 263.80`: latest structured snapshot is `245.29`, below the explicit completed-close failure line `260`. Impact: about `USD 74.04` gross mark-to-market loss from cost before fees, with gap risk. Fix: run the missing formal-close catch-up and, if still held, execute the governing next-open exit; verify only from broker/user report.
3. XLI `2 @ 183` old order: confirm `never placed / cancelled / open / filled`. Impact: cash and exposure could differ by about `USD 368`; an open stale buy conflicts with the `0%` new-buy gate. Fix: cancel if still open; verify broker status.

## Priority 1 — missing control artifacts

4. The delayed 2026-07-02 formal post-close audit now exists, and the 2026-07-03 holiday was formally audited on 2026-07-04. No 2026-07-03 replay row is permitted because there was no trading session. Remaining control gap: reconcile all broker facts before changing holdings, cash or execution status.
5. No 2026-07-03 daily strategy recommendation or 20:30 monitor artifact exists. Impact: no same-day catalyst/news layer can be attributed. Likely cause: holiday scheduling or upstream automation absence. Fix: explicitly skip on holidays or write a holiday marker. Verification: upstream automation memory/output shows a deliberate holiday branch.
6. Cboe official history confirms VIX3M `19.04` for 2026-07-02; term-structure quality is now high. Keep excluding the stale Tencent VIX object and use official Cboe history for completed-close volatility.

## Priority 2 — replay and strategy review

7. The 2026-07-02 completed-close replay row already exists. Do not duplicate it and do not add 2026-07-03 or later before a completed trading session exists.
8. Audit the MRVL entry sequence: support was tested, but the theme/market relative-strength filter remained broken. Test whether `trend_aligned_entry=trend_broken` should have blocked the real-account recommendation; do not promote a new rule from this single case.
9. Continue AMD close-stop replay (`517.82 > 492`, repair watch), WDC near-stop review (`539 > 500`), and STX historical stop review (`820.16 < 835`). These are watch/replay items, not real holdings.
10. Freeze all new buys and remove/cancel stale buy orders until stop execution, cash/NAV and XLI are confirmed. Reopening requires `trend_aligned_entry`, no unresolved hard stops and concentration compliance.
