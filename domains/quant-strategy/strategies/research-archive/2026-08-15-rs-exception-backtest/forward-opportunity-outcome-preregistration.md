# Forward opportunity-outcome measurement registration

Frozen on 2026-08-20 after two completed forward sessions but before any
registered event has a five-session outcome. Research-only; no order or rule
authorization.

## Event identity

- Read event identities only from the immutable
  `forward_opportunity_diagnostics_ledger.csv`.
- Measure `high_vol_central_symbols` and `high_vol_missed_leaders` separately.
- Never add an event after looking at its later return.
- The outcome evaluator is read-only and must preserve the input-ledger hash.

## Frozen outcomes

For each event-date/symbol pair, using the event completed close as reference:

- close-to-close return after exactly 5 and 20 later completed sessions;
- maximum favorable excursion from future daily highs during sessions 1..H;
- maximum adverse excursion from future daily lows during sessions 1..H;
- horizon date and maturity status.

No one-day outcome is used. No incomplete horizon enters a mean, median or win
rate. Missing OHLC invalidates that event/horizon rather than being filled.

## Overlap control

Raw daily observations remain visible because the original diagnostic threshold
counts them. For statistical summaries, consecutive observations in the same
symbol/event type separated by no more than five trading sessions form one
episode; only the first observation is primary. Reports show both raw events
and primary episodes so repeated five-day leaders cannot masquerade as
independent evidence.

## Interpretation

- Report mean and median horizon return, positive-return rate, mean MFE and mean
  MAE only for matured primary episodes.
- The original requirement of at least 20 central signals and 20 missed-leader
  observations remains unchanged. These outcomes may motivate a separately
  preregistered future study only; they cannot promote a trade rule.
- RSR1/RSR2 win rate and expectancy continue to come only from their actual
  closed forward trades, never from this diagnostic.
