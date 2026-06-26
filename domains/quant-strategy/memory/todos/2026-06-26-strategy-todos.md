# 2026-06-26 Strategy Todos

Run time: 2026-06-26 22:00 Asia/Shanghai.

## Open

### 0. 23:17 intraday refresh: post-close audit priority
- Local Node quote workflow is usable; equities/ETFs returned structured Tencent quote objects. Tencent VIX is low quality, so use Yahoo chart fallback or official close sources for volatility.
- GLW traded at `208.17`, below the `210` profit-protection line intraday. Because the rule is completed-close based, do not mark a formal trigger yet; the 04:15 post-close audit must verify the official close and decide reduce/exit review.
- TTMI traded at `194.50`, below the `$200` wind-control line but above the `$188` hard close-stop. Post-close audit must escalate if the completed close remains below `200`.
- DRAM traded at `72.86`, with intraday low `71.33`, still above the `70.50` protective exit. Confirm broker-side `DRAM 4 @ 70.50 stop-market sell` status.
- No new buy/add is valid while `flow_fragility` is elevated/near-acute and the confirmed sleeve is one correlated AI-capex basket.
- Later user-confirmed MXL fill means the confirmed sleeve is now GLW/TTMI/DRAM/MXL, with estimated equity exposure near `29%`. This increases optical/interconnect overlap and should block any further same-theme adds before the post-close audit.

### 1. Reconcile broker cash, NAV and open orders
- Working cash is estimated at `USD 3,368.64` after DRAM, MXL, and MU fills and estimated platform fees.
- Compare with broker statement when convenient.
- Confirm all previous buy orders (WDC at $655, DRAM limit orders) are fully cancelled.

### 2. GLW trailing profit protection review
- Current price `216.34` has pulled back.
- Trailing profit protection line remains **$210.00** (close-based).
- Hold/no add. If it closes below $210, we will review for profit-taking in the post-close audit.

### 3. TTMI wind-control breach review
- Current price `196.03` is trading below the `$200.00` wind-control line and the `$205.00` warning zone.
- Exit trigger remains completed-close below **$188.00**.
- Hold/no add. We do not exit intraday. If it closes below $200, we will alert the user for a potential risk-reduction next week.

### 4. DRAM protective stop order check
- Current price is `72.05`.
- **CRITICAL:** Confirm if the protective `DRAM 4 @ 70.50 stop-market sell` order is active at the broker.
- This is an intraday trigger. If DRAM trades at or below $70.50, all 4 shares must be sold immediately.

### 4a. Data-quality and workflow follow-up
- Issue: Tencent quote workflow returned usable equity/ETF quotes, but VIX was a low-quality zero-OHLC object.
- Impact: do not compute fear score from Tencent VIX; use Yahoo chart / official Cboe / FRED fallbacks.
- Possible cause: Tencent U.S. index-volatility quote fields are incomplete even when the equity quote workflow is available.
- Verification: rerun Node quote smoke test plus Yahoo chart VIX/VIX3M pull during the 04:15 post-close audit.
- Next step: keep reporting source-level quality rather than saying local quote workflow is unavailable.

### 4b. MXL new-position protection check
- User confirmed `MXL 6 @ 90.70`.
- Local Node quote at 23:23 BJT showed MXL `91.14`, intraday low `87.13`, still above the `86.00` risk line.
- Confirm whether the broker has a protective `MXL sell stop-market, 6 shares, trigger 86.00`.
- Do not add more MXL today. If MXL trades below `86.00` or closes with GLW/TTMI/DRAM all weak, escalate to post-close risk review.

### 4c. MU new-position protection check
- User confirmed `MU 1 @ 1155.00`.
- Initial close-based risk line is `1,100.00` (50-day simple moving average).
- Confirm whether the broker has a protective stop-market sell on `1` share at `1,090.00` to avoid intraday whipsaws.
- **Concentration Ban**: Memory theme exposure (MU + DRAM) is at its limit (~23%). Strictly prohibit any further memory/storage additions.

### 5. MRVL re-entry check
- MRVL is trading at `269.22`.
- Re-entry remains blocked. Re-entry requires reclaiming **$285.00** on a completed close and SMH reclaiming its 50-day average. Watch only.

### 6. Next-regime buy queue (NEW — added 2026-06-26 22:16 BJT)
- Broader candidate analysis completed across 27 AI-theme tickers. See `work/2026-06-26-broader-stock-analysis.md`.
- MU has been filled at $1,155.00.
- Priority queue for next Normal fear-gate regime:
  1. **CRDO** — entry $240–$270 on stabilization
  2. **ALAB** — entry $350–$370 (satellite only, valuation risk)
  3. **AMD** — entry $490–$505
  4. **TER** — entry $410–$430 (investigate today's -6.6% drop)
  5. **ANET** — entry $150–$155
- Do NOT add NOW, PLTR, APP — today's green moves are bounces from broken trends.
- Remove LITE and COHR from active queue (theme selling too heavy).

## Completed / verified
- Completed the 2026-06-25 post-close audit.
- Updated 2026-06-25 portfolio summary and daily summaries.
- Appended 2026-06-25 close row to `replay-ledger-template.csv`.
- Checked social/institutional sources (no new articles since yesterday).
- Completed broader 27-ticker AI-theme candidate analysis (2026-06-26 22:16 BJT). RS90d ranking, tier classification, and priority queue updated.

Not investment advice.
