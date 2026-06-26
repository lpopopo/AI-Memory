# 2026-06-22 Open Prep Automation 2

Run time: 2026-06-22 21:55 Asia/Shanghai.

Scope: automation-2 open-prep review for U.S. individual-stock operations. Live regular session is open. No broker login, order submission, cancellation, or fill assumption is made.

## Data And Source Checks

- Required memory, portfolio, trade-plan, candidate-pool, institutional-overlay, public-source, and quote-workflow files were read.
- Public source status: No new verified items since the 2026-06-19 check. The latest Xiaohongshu/X candidates remain the bottleneck thematic players (TER, CRDO, MXL, AXTI, TTMI) as of June 19.
- Institutional research checker was run with `--since 2026-06-19T10:00:00Z`. AQR, GMO, and Man Group had readable lists/details but no new post-window framework items. Citadel had no new insights.
- Live quote check: Node stock service and Yahoo Finance chart API returned live quotes:
  - SPY: $748.60 (+0.25%)
  - QQQ: $742.31 (+0.34%)
  - SMH: $666.86 (+1.06%)
  - MRVL: $301.72 (-2.85%)
  - RDW: $13.33 (-7.14%)
  - GLW: $198.65 (+1.91%)
  - TTMI: $216.28 (-0.07%) (High $222.93, Low $213.86)
  - MXL: $95.91 (+8.06%) (Open $92.50, High $96.04)
  - ALAB: $436.91 (+4.76%)
  - DRAM: $80.05 (+4.35%)
  - VIX: 16.78
  - VIX3M: 19.60

## Operating Conclusion

- Market gate: VIX is 16.78 (elevated: 1 point). VIX/VIX3M is 0.856 (normal: 0 points). Overall fear score is carried forward as `5 / 14` (elevated) for risk controls. Risk multiplier is 70%, cash floor is 25%.
- Real-account confirmed holdings remain MRVL 1, RDW 5, and GLW 2.
- Priority order:
  1. **RDW Exit:** Immediate exit of RDW is required. It closed below the $14.50 stop line on June 18 and is currently trading at $13.33 (down -7.14%). Per decision rule, this must be executed in the first 15 minutes of the next session (currently 25 minutes in, action is urgent).
  2. **Protect GLW/MRVL:** Keep profit-protection review active. MRVL is at $301.72 (stop below $280 close, profit-protection near $295-298). GLW is at $198.65 (trailing stop $188-190).
  3. **TTMI Conditional Buy:** Wait. TTMI is trading at $216.28, which is inside the neutral range. Pulback condition ($210-213) or breakout reclaim ($220) is not met.
  4. **MXL Conditional Buy:** Cancel/Invalidated. MXL opened at $92.50, which triggered the "Opens above 92 without reset" invalidation rule. It is currently at $95.91, which is above the no-chase limit of $92. Do not buy.
  5. **ALAB, AMD, WDC, STX:** Watch-only.

Not investment advice.
