# Risk-action counterfactual preregistration

## Purpose

Measure what happens after a documented long-term position enters
`reduce-review`, `profit-protection`, or another risk-review state. The study
compares a paper full reduction and a paper half reduction with continued
holding. It does not infer a broker order, change the user's long-term
classification, or turn a price review into an automatic sale.

## Sample boundary

- The three already-observed GLW/MRVL/MXL events are labeled
  `retrospective_seed`; they may validate calculations and illustrate the
  action gap, but they are not genuine forward evidence.
- A genuine-forward event must be appended before its next-session open and
  labeled `genuine_forward`.
- Events are keyed by `trigger_date + symbol`; duplicates are invalid.
- Prices after the completed-session `as_of` date are excluded even if the
  provider file contains a live or later row.

## Frozen policies

1. `full_exit`: paper sale of all documented shares at the first valid open
   after the completed-close trigger.
2. `half_exit`: paper sale of `floor(shares / 2)` at the same open.
3. `hold`: comparison baseline with zero action benefit.

The sell price receives 10 basis points of adverse slippage and each paper sale
pays USD 1 commission. Gross values before costs are also retained. No tax,
spread beyond the fixed slippage, FX, or replacement investment is assumed.

## Frozen horizons

- `1`, `5`, and `20` valid closing sessions, counted from and including the
  execution session.
- `as_of`, a descriptive current mark that must never be pooled with a fixed
  horizon.
- An immature horizon is `unavailable`, not zero.

For each event/policy/horizon, net benefit versus holding is:

```text
action_shares * (next_open * (1 - 0.001) - horizon_close) - USD 1 commission
```

Positive benefit means the paper reduction preserved value relative to holding;
negative benefit means it missed subsequent appreciation.

## Decision rule

This measurement has no promotion threshold yet. The three retrospective seeds
cannot select a policy, action fraction, trigger, or stock-class exception.
Report retrospective and genuine-forward samples separately. Any future policy
proposal requires a new preregistration and independent forward evidence.

Formal V9, RSR1, RSR2, the real account, and `memory/decisions.md` remain
unchanged. The output authorizes no order.
