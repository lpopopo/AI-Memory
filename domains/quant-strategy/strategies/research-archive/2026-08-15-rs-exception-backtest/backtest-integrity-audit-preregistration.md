# Backtest integrity audit preregistration

Status: frozen before line-by-line inspection of the backtest engines on
2026-08-20. Research-only; no formal/live rule or order authorization.

## Objective

Test whether implementation details can mechanically inflate the reported RSR
win rate, expectancy or portfolio return. This is an integrity audit, not a new
parameter search. No entry, exit, ranking, universe or sizing threshold may be
changed to improve a result.

## Authoritative scope

- Current-list RSR baseline, RSR1 and RSR2 engines and their shared-capital
  overlays.
- Point-in-time exact-OHLCV transfer engine.
- Frozen data and result files already present in this research directory.
- Intended contracts in the existing preregistrations and decision register.

## Frozen checks

1. **Causal features:** every signal-day feature uses only observations dated on
   or before the signal close. Modifying rows strictly after a cutoff must not
   change signals, entries, exits or equity through that cutoff.
2. **Execution chronology:** an end-of-day signal cannot execute on that same
   day's open or close. Entry and close-confirmed exit execution must occur on a
   later valid session under the registered convention.
3. **Price feasibility:** recorded fills must be reproducible from the stated
   session OHLC and slippage/fee convention; no fill may use a future day's
   price or an impossible price outside the applicable bar after accounting for
   the explicit cost model.
4. **Corporate-action consistency:** open/high/low/close used together must share
   one adjustment basis. Split handling may not create artificial ATR, gaps,
   returns or share counts.
5. **Portfolio accounting:** cash, market value, realized P&L, costs and total
   equity must reconcile; cash cannot become negative; whole-share, maximum
   position, sleeve-cap and duplicate-symbol constraints must hold.
6. **Exit-path integrity:** stop, profit lock and maximum-hold logic must inspect
   only information available when the decision is made. End-of-sample open
   positions may be marked for reporting but may not be converted into a closed
   trade or win.
7. **Data invariants:** dates must be strictly increasing and unique per symbol;
   required OHLCV fields must be finite and economically valid; missing symbols
   or sessions must be explicit rather than silently forward-filled into a
   signal.
8. **Cross-engine consistency:** when two variants have identical rules over a
   trade path, signal date, entry date, entry price and costs must match. RSR2
   may differ from RSR1 only after its registered profit-lock condition becomes
   available.

## Severity and decision rules

- `critical`: future information, same-bar execution, impossible fills, or an
  accounting error that changes headline return/win rate. Recompute all affected
  evidence and withdraw any invalid conclusion.
- `major`: a reproducible bias that can change trade selection, payoff or risk
  but does not affect every headline. Discount the affected evidence and repair
  before further forward comparison.
- `minor`: documentation, schema or guardrail weakness with no observed metric
  impact. Repair and add a regression test.
- `pass`: code inspection plus an executable adversarial/regression test supports
  the contract. Absence of an obvious bug alone is not a pass.

The audit passes only if all eight checks are either `pass` or `minor` with no
metric-changing effect. Tests and findings must be reported even if the outcome
weakens the strategy.
