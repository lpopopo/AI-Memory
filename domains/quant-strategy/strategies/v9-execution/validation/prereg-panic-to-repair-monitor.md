# Pre-registration: Panic-to-Repair Monitor

Frozen date: 2026-07-11  
Status: research-only; does not authorize trades.

## Hypothesis

A lagged panic-to-repair package (prior deep drawdown + elevated volatility +
sharp rebound) adds tail-risk warning value beyond Fear Gate and MA150/MA200.

## Label definition

On day `t`:

1. SPY min 63-day drawdown over `[t-252, t-21]` <= -15%.
2. Peak VIX over `[t-21, t]` >= 25, or VIX unavailable.
3. SPY rebound over last 21 sessions >= +8%.

If all true: `panic_to_repair`; else if only (1): `post_drawdown_watch`; else
`normal`.

## Comparator

- Baseline: existing Fear Gate advisory + MA150/MA200 regime.
- Candidate: baseline + panic-to-repair warning that only reduces new buys /
  theme adds in shadow reports.

## Metrics and gates

Primary: max drawdown and 5% expected shortfall during labeled windows.  
Secondary: false reductions, missed winners, cash drag.  
Promotion requires incremental tail improvement after 0.1%/0.2%/0.5% costs and
stability outside 1932/2009-like episodes.

## Explicit non-claim

This label does not authorize shorts, MA overrides, or Rule E score changes.
