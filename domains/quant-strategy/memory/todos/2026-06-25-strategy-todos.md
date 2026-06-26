# 2026-06-25 Strategy Todos

Run time: 2026-06-26 21:54 Asia/Shanghai.

## Open

### 1. Reconcile broker cash, NAV and open orders
- Local working cash estimate after DRAM purchase and assumed USD 1 fee is `USD 5,069.84`; exact cash, FX, fees, taxes, settlement and open orders remain unverified.
- Compare the broker statement with `memory/portfolio/2026-06-25-portfolio-summary.md` and subsequent trades.
- Confirm every residual `DRAM` buy order and the `WDC 1 @ 655` buy order are cancelled.

### 2. Confirm DRAM protection
- DRAM 2026-06-25 close was `76.89`, above the `70.50` protective exit line.
- Confirm whether the protective `DRAM 4 @ 70.50 stop-market sell` is active. This automation did not place it.
- No further DRAM or WDC buy is authorized after the 4-share DRAM fill.

### 3. GLW profit-protection trailing stop review
- GLW 2026-06-25 close was `228.01`, above the completed-close protection line `210`.
- Hold/no add. If a later completed close breaks `<210`, run reduce/exit review.

### 4. TTMI warning zone review
- TTMI 2026-06-25 close was `210.57`, above the `<200` reduce-review line and `<188` hard exit-review line.
- Hold/no add. Continue watching Russell rebalance pressure and AI-infrastructure correlation.

### 5. MRVL re-entry check
- MRVL is closed in the real account. 2026-06-25 close was `281.26`, below the `285` re-entry condition.
- Watch only. Do not rebuy because of event rebound unless a fresh completed-close trend/RS setup appears.

## Completed / verified

- MRVL stop-loss execution remains recorded: sold 1 share at USD 272.30.
- DRAM real-account buy remains recorded: 4 shares at USD 76.430.
- Formal 2026-06-25 completed-close audit created.
- Formal 2026-06-25 portfolio summary updated.
- Replay ledger appended for the completed 2026-06-25 close.
- Local Node quote workflow verified working; structured quote objects returned. 2026-06-26 intraday bars were excluded from the 2026-06-25 formal audit.

## Theme-crowding overlay replay

- Problem: MU/WDC/STX/DRAM produced a large opening gap followed by material intraday fade.
- Impact: a normal fear score alone may overstate entry quality in a crowded high-capex theme.
- Suggested validation: in later completed-close replay rows, record `opening_gap_rejection`, post-gap 5/20-day performance, and whether overlay rules avoided duplicate WDC/DRAM exposure.
- Verification: 2026-06-25 completed close row was appended; do not prefill a future row.

## Live quote workflow

- Status: verified working.
- Node equities/ETFs returned structured `Tencent (Primary)` objects; completed-close audit used Yahoo chart daily bars after excluding 2026-06-26 intraday bars.
- No Python or Google browser fallback was required.
- Next validation: retain source-level logging and reject low-quality zero-OHLC VIX arrays before using explicit Yahoo/FRED fallback.

Not investment advice.
