# RSR2 partial-profit scale-out preregistration

## Status and purpose

- Frozen before reading any result from this branch.
- Research only; no formal V9, live order, holding, RSR1/RSR2 rule or existing
  forward-ledger change.
- Objective: test whether realizing part of a confirmed winner reduces profit
  giveback without eliminating the remaining right tail or letting extra
  commissions overwhelm a small whole-share account.

The earlier three-day failed-breakout exit was already rejected by a separate
ablation study and is not reopened here.

## Baseline

Use the frozen 32-name `ai_capex_broad` RSR2 path:

- all RSR1 broad, theme, breakout, relative-strength, volume, extension, ATR,
  close-location and event-gap rules;
- current RS20-plus-volume ranking;
- next-session open execution, whole shares, USD 200 minimum entry, 8% target,
  15% single-name maximum, 25% stock-sleeve maximum and three names;
- 8% initial stop, MA20/negative-RS exit and 20-session maximum;
- after a completed close reaches +15% from entry, raise the next-session stop
  on the entire position to +5% from entry.

## Single frozen challenger

`partial_half_at_15` keeps every baseline rule and adds only this action:

1. On the first completed close at or above +15%, schedule one partial sale for
   the next session open.
2. Sell `floor(current_shares / 2)` whole shares. Never sell the entire position
   through this action; a one-share holding is ineligible.
3. Execute only when the partial-sale gross notional is at least USD 200. If it
   is not executable at that next open, mark the trade ineligible and do not
   retry later.
4. Charge the same one-way slippage and an additional USD 1 commission.
5. Allocate original cost basis pro rata to the sold shares. Aggregate partial
   and final realized P&L back to one trade so win rate cannot be inflated by
   counting two exits as two trades.
6. The remaining shares retain the RSR2 +5% stop and every ordinary exit rule.
   The partial exit creates no new buying capacity exception and no re-entry.
7. If a full RSR2 exit is already due at the same next open, execute the full
   exit only; do not manufacture a partial sale immediately before it.

No alternate trigger, fraction, notional threshold or stop is tested.

## Periods and stresses

- Development: 2024-01-02 through 2025-12-31.
- Held-out consistency monitor: 2026-01-02 through the latest locally completed
  OHLCV session.
- Full descriptive period: 2024-01-02 through that same boundary.
- Initial NAV: USD 6,000 and USD 5,751.77.
- Slippage: 10 bps and 20 bps per side, both as full portfolio reruns.
- Cash earns zero.

The current-list history and 2026 observations have been seen in other studies;
they are not genuine forward evidence.

## Advancement gate

The challenger may become a separate future forward shadow only if all hold:

- At least five partial exits execute in development and two in the 2026
  monitor at each NAV under 10 bps. Otherwise label `insufficient`.
- Net total return exceeds baseline RSR2 in both periods and at both NAVs under
  10 bps.
- Sharpe and closed-trade win rate are not below baseline in any 10 bps
  period/NAV cell.
- Maximum drawdown is not worse by more than one percentage point.
- The return advantage remains positive in both periods and at both NAVs under
  20 bps.
- At least three symbols contribute gross profit and no symbol contributes more
  than 35% of full-period gross profit at either NAV under 10 bps.

Passing only creates a newly versioned shadow after this study. It cannot amend
or backfill the already-frozen Aug 17 RSR1/RSR2 chains. Failure or insufficient
whole-share feasibility closes the branch until a materially larger NAV or new
independent forward evidence changes the mechanism's economics.
