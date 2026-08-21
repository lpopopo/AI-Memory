# Forward zero-signal bottleneck preregistration

Status: frozen on 2026-08-21 after three completed sessions produced no signals
and before computing condition-level counts. Research-only; no rule relaxation.

## Objective

Attribute zero RSR1 signals to public market gates, the SMH regime veto,
stock-level breakout requirements, or the ATR/close-location quality pair. This
diagnostic prevents a zero-trade period from being blamed on whichever threshold
is most salient after the fact.

## Frozen sample

- Completed sessions from the forward start 2026-08-17 through the current
  `forward_shadow_status.json` as-of date.
- Frozen 32-name `ai_capex_broad` universe and local validated adjusted OHLCV.
- Same feature definitions and thresholds as frozen RSR1.

## Fixed sequential funnel

The order is immutable:

1. usable stock OHLCV;
2. broad gate: SPY above MA200, QQQ above MA100, VIX below 25 and
   VIX/VIX3M below 1;
3. SMH at or above MA50;
4. stock above MA20;
5. stock above MA50;
6. close above prior 20-session high;
7. RS20 versus SMH at least 3%;
8. volume at least 1.2 times the prior 20-session average;
9. extension from MA20 between 0% and 12%;
10. not in the frozen positive-gap event cooldown;
11. ATR14/close no more than 4%;
12. signal-day close location at least 50%.

Report both sequential survivors and marginal pass/fail counts. Marginal counts
evaluate each condition independently; they cannot be added because failures
overlap.

## Counterfactual diagnostics

For each date also report:

- stock-level matched-baseline candidates before the broad/SMH gates;
- matched-baseline candidates with broad gate but without the SMH veto;
- candidates after the strict SMH veto but before the quality pair;
- final RSR1 candidates.

These are causal same-close diagnostics, not executable trades. No counterfactual
may authorize a buy, remove the SMH veto, change 4%/50%, or expand the universe.
