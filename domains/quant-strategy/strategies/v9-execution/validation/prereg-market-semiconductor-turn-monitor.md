# Pre-registration: Market / Semiconductor Turn Monitor

Status: research-only, frozen before reading event-study results.

## Question

Does a completed-close transition package add forward information beyond the
existing Fear Gate and a simple QQQ trend repair after a meaningful drawdown?

## Causal inputs

Only data available at the completed close are allowed. A signal requires a
recent stress base: during the latest 21 sessions, QQQ or SMH must have reached
an 8% or deeper 63-session drawdown.

The state ladder is fixed as follows:

1. `risk_off`: recent stress exists but stabilization is absent.
2. `stabilizing`: SMH has avoided a new rolling 10-session low for three
   consecutive completed closes.
3. `repair_attempt`: stabilization plus positive SMH five-session return and
   SMH above its 10-session average.
4. `confirmed_turn`: repair attempt plus all of:
   - SMH above its 20-session average for two consecutive closes;
   - SMH five-session return exceeds QQQ five-session return;
   - QQQ is above its 20-session average;
   - RSP/SPY and HYG/LQD five-session changes are non-negative;
   - Fear Gate is `normal` or `elevated` and its score has not worsened versus
     five sessions earlier.

Missing breadth, credit, volatility or required price data prevents
`confirmed_turn`; missing evidence is not treated as a pass.

## Evaluation

- Candidate events are rising edges into `confirmed_turn`.
- Baseline dates have the same recent stress base, Fear Gate no worse than
  `elevated`, and QQQ above MA20, without requiring semiconductor relative
  strength, breadth or credit confirmation.
- Report 5/10/21/63-session forward returns for SPY, QQQ and SMH, plus SMH
  excess return over QQQ.
- Report event counts and medians; do not optimize thresholds from this sample.

## Promotion / rejection

This monitor never authorizes trades or changes V9 weights. Fewer than 20
independent confirmed events is insufficient for promotion. Even with adequate
count, promotion requires candidate median drawdown/return behavior to improve
over the baseline without excessive missed-repair frequency, followed by a
genuinely new forward sample.
