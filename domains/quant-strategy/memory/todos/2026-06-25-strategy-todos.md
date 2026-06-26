# 2026-06-25 Strategy Todos

Run time: 2026-06-25 22:15 Asia/Shanghai.

## Open

### 1. Reconcile broker cash, NAV and open orders
- Working cash is `USD 5,376.56`; exact cash, FX, fees, taxes, settlement and open orders remain unverified.
- Compare the broker statement with `memory/portfolio/2026-06-24-portfolio-summary.md` and subsequent trades.
- Verify if the limit buy orders for WDC ($655.00) and DRAM ($73.00) are placed at the broker.

### 2. GLW profit-protection trailing stop review
- Current price `221.95` is very strong. Trailing profit protection line is raised to **$210.00** (on completed close).
- Hold/no add. If it closes below $210, we will review for profit-taking in the next post-close audit.

### 3. TTMI warning zone review
- Current price `204.73` is trading slightly below the `205` warning line, with an intraday low of `203.26`.
- Hold/no add. We do not exit intraday. Hard stop remains **$188.00** close-based.
- If it breaks below the $200 wind-control line at the close, we will alert the user for a potential stop-loss/reduction decision.

### 4. WDC & DRAM orders
- WDC ($655.00 limit buy) is cancelled to release core sleeve capital and keep cash high.
- DRAM (4 shares bought at $76.430) is filled. Stop-loss is set at **$70.50** (close-based). No further buying.

- Reconcile the exact buy fee and resulting broker cash.


### 5. MRVL re-entry check
- MRVL is currently trading at `269.585` after a premarket bounce to `281.68` and a regular session high of `292.51`.
- Re-entry requires reclaiming **$285.00** on a completed close and SMH reclaiming its 50-DMA. Watch only.

## Completed / verified
- MRVL stop-loss executed at next session open: sold 1 share at USD 272.30.
- DRAM real-account buy confirmed: 4 shares at USD 76.430.
- Daily K-line check completed for current session ranges.
- Intraday detail log created.

Not investment advice.

## 23:18 BJT Incremental Audit

### Immediate user-side confirmations

1. Confirm every remaining `DRAM` buy order and the `WDC 1 @ 655` buy order are cancelled.
2. Confirm whether the protective `DRAM 4 @ 70.50 stop-market sell` is active. This automation did not place it.
3. Provide broker cash / fee / FX / settlement values when convenient; current cash `USD 5,069.84` and NAV `USD 6,442.11` are estimates.

### Post-close audit todo

- Problem: current prices are intraday and cannot confirm GLW `<210`, TTMI `<200` / `<188`, DRAM `<70.50`, or the formal fear gate.
- Impact: treating the 23:18 snapshot as a close could create false stop actions or an incorrect replay row.
- Likely cause: automation-3 intentionally runs before the U.S. close.
- Fix: automation-5 must use completed regular-session bars, reconcile official close timestamps, and update the stop table/NAV.
- Verification: compare completed daily bars with the 23:18 snapshot and record only close-confirmed triggers.
- Next step: run the 04:15 post-close audit.

### Theme-crowding overlay replay

- Problem: MU/WDC/STX/DRAM produced a large opening gap followed by material intraday fade.
- Impact: a normal fear score alone may overstate entry quality in a crowded high-capex theme.
- Suggested validation: in the next completed-close replay row, record `opening_gap_rejection`, post-gap 5/20-day performance, and whether overlay rules avoided duplicate WDC/DRAM exposure.
- Verification: update the replay ledger only after the 2026-06-25 completed close exists; do not prefill a future row.

### Live quote workflow

- Status: verified working.
- Node equities/ETFs returned structured `Tencent (Primary)` objects; VIX/VIX3M returned structured `Yahoo Chart (Fallback)` objects through the Node workflow.
- No Python or Google browser fallback was required.
- Next validation: retain source-level logging and reject empty VIX arrays before using the explicit Yahoo chart fallback.
