# Forward shadow review — 2026-08-20

- Completed forward sessions: 4 (`2026-08-17` through `2026-08-20`).
- Source completeness: passed for all 47 downloaded symbols; VIX/VIX3M use
  official Cboe histories.
- RSR1 / RSR2 / matched-baseline signals: 0 / 0 / 0.
- Closed RSR1 / RSR2 / matched-baseline trades: 0 / 0 / 0.
- New opportunity diagnostic: one raw high-volatility missed-leader
  observation, MRVL. Cumulative raw observations are 24 and overlap-controlled
  primary episodes remain 16, so this is not a new independent episode.
- Mature five-session / twenty-session opportunity outcomes: 0 / 0.
- Forward economic-edge attribution remains `awaiting_sample`.

The broad gate passed all four sessions, but SMH remained below MA50 for Aug
18-20. On Aug 20, SMH closed `562.65` versus MA50 `589.51`; zero stock-level
matched-baseline candidates existed even before the market gates. MRVL was the
only realized five-session leader. It was already a real-account holding, so
this diagnostic is not a real-account missed buy. It also remained outside
RSR1: `20.52%` above MA20, `6.91%` ATR, event cooldown blocked, and the SMH
gate was closed.

The risk-action counterfactual provides the clearest new lesson. The fixed
one-session result is unchanged: paper full reduction helps only one of three
retrospective seeds and adds net `$10.16`. The descriptive as-of result moved
from `+$39.90` on Aug 19 to `-$6.14` on Aug 20 because MRVL extended. This
one-day sign reversal is direct evidence that an arbitrary as-of mark cannot
select an exit policy. Five- and twenty-session action outcomes remain
unavailable, and genuine-forward risk-action events remain zero.

Formal V9, frozen RSR1/RSR2, long-term classifications, and the real account
remain unchanged. No order is authorized.
