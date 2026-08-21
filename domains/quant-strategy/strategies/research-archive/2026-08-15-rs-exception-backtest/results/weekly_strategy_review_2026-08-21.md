# Weekly strategy error and missed-opportunity review — 2026-08-21

## Boundary

This review uses completed U.S. sessions through `2026-08-20`. All 47 local
symbols are source-complete through that close and the volatility indices use
official Cboe histories. No broker access, submitted order or confirmed fill
is available. Real-account execution errors therefore cannot be asserted;
next-open comparisons below are counterfactual process measurements only.

## Bottom line

The week-to-date evidence does **not** show that the entry model missed a broad
set of profitable AI-capex trades. From the Aug 14 close to the Aug 20 close,
only `4/32` names in the frozen RSR universe were positive: MRVL `+13.06%`,
TSLA `+0.84%`, DRAM `+0.45%`, and MU `+0.27%`. The other `28/32` declined.
AAOI fell `14.09%`, MXL fell `23.06%`, and SMH fell `4.28%`.

The main correctable weakness is an action-layer gap: labels such as
`reduce-review` identified risk, but did not map to a deterministic paper
action whose next-open result could be audited. That makes the analysis less
useful even when the risk diagnosis is directionally correct. The repair is an
immutable risk-action counterfactual ledger, not a retrospective change to the
entry thresholds.

## Week-to-date scorecard

| Item | Aug 14 | Aug 20 | Change | Interpretation |
| --- | ---: | ---: | ---: | --- |
| SPY | 776.34 | 762.60 | -1.77% | Broad market lower |
| QQQ | 731.07 | 710.93 | -2.75% | Growth weaker than broad market |
| SMH | 587.82 | 562.65 | -4.28% | Semiconductor trend deterioration |
| AAOI | 150.28 | 129.10 | -14.09% | One-day rebound did not repair the weekly reversal |
| MRVL | 222.02 | 251.01 | +13.06% | Dominant positive real holding; already owned |
| Real-account equity sleeve | 2,060.68 | 2,020.10 | -1.97% | MRVL offset most correlated-sleeve weakness |
| Working real-account NAV | 5,817.17 | 5,776.59 | -0.70% | 65% cash materially buffered the decline |

The real-account mark uses the unchanged working cash of USD `3,756.49` and
GLW `2`, MXL `6`, MRVL `4`, QCOM `2`. Its USD `40.58` week-to-date decline is
attributed to GLW `-29.08`, MXL `-117.36`, MRVL `+115.96`, and QCOM `-10.10`.

## What was actually wrong

| Item | Evidence | Classification | Correction |
| --- | --- | --- | --- |
| Risk-review action gap | GLW and MXL risk states were visible, but `reduce-review` did not create a deterministic next-session paper action | Process weakness; no confirmed live execution error | Record trigger date, hypothetical next-open action, shares, cost and 1/5/20-session saved-or-lost P&L |
| AAOI explanation timing | The later audit numerically showed extreme ATR and extension, but the original user-facing message did not make the exact failed conditions prominent enough | Communication/traceability error | Publish the full failed-condition card at decision time |
| Profit-maximization framing | Historical RSR2 win rate and return can look broadly superior even though only two trades had direct protected-exit effects and the top two deltas supplied 86.93% of its improvement | Analysis-risk correction | Lead with expectancy decomposition and concentration, not headline win rate |
| Cash drag | Zero-yield simulations omit potential sweep income | Model omission, conditional on broker mechanics | Keep zero-yield base and a separate sweep proxy; no operational recommendation without settlement, fee and tax facts |

## What was not wrong

### AAOI no-buy

AAOI had no exact RSR1 signal on Aug 10-14. On Aug 14 it was `30.24%` above
MA20 with `11.37%` ATR, versus frozen limits of `12%` and `4%`. On Aug 17 it
still had `31.29%` extension, `10.91%` ATR and only `1.06x` volume. It then
closed Aug 20 at `129.10`, down `14.09%` from Aug 14 and down `16.65%` from
Aug 17 despite a `5.66%` one-day rebound.

This does not prove that every future AAOI exclusion will be correct. It does
show that the prior no-buy was risk-consistent and that chasing the observed
Aug 14 breakout would have created substantial immediate adverse excursion.
The error was explaining the decision too generically, not refusing the trade.

### Zero RSR1/RSR2 signals

The broad gate was open on all four completed sessions. On Aug 18-20, SMH was
below MA50 and correctly closed the theme gate. On Aug 17, AXTI was the only
name to survive through the volume step, but it was `48.55%` above MA20 with
`12.59%` ATR. Across the full stock funnel there were zero matched-baseline
candidates even before the RSR1 quality pair. Relaxing SMH, extension or ATR
after seeing individual moves would manufacture trades rather than repair a
demonstrated bottleneck.

### High cash

The equity sleeve lost `1.97%`, while working NAV lost only `0.70%`. Cash did
create opportunity cost in long rising periods, but during this week's
semiconductor reversal it served its intended drawdown-buffer role. It should
not be labeled idle-loss without accounting for the risk reduction it bought.

## Counterfactual risk actions

These comparisons do not assert that the user should or did sell. They measure
whether a clearly defined next-open response would have improved the mark.

| Trigger | Paper action price | Fixed 1-session net benefit | Aug 20 as-of net benefit |
| --- | ---: | ---: | ---: |
| GLW completed-week review at Aug 14 close | Aug 17 open 169.74 | USD -8.28 | USD +35.24 |
| MXL completed-close below 78 on Aug 18 | Aug 19 open 74.45 | USD +46.67 | USD +53.57 |
| MRVL completed-week review at Aug 14 close | Aug 17 open 227.75 | USD -28.23 | USD -94.95 |

A blanket automatic exit for every review is therefore not supported. Full
reduction wins only `1/3` fixed one-session cases and totals `+$10.16`; the
arbitrary as-of total changed from `+$39.90` on Aug 19 to `-$6.14` on Aug 20.
That sign reversal is evidence against selecting a rule from an observation
date. Because there is only one short episode, no new fraction, stock-class
exception, or stop parameter is selected here.

## Historical backtest lessons that remain valid

- RSR1 improved the fixed current-list history mainly by avoiding losses: it
  excluded 16 losers and USD `554.79` of loss, but also seven winners and USD
  `159.37` of profit.
- RSR1/RSR2 historical win rates were `65.22%/69.57%`, but this is
  current-list retrospective evidence, not a forward hit-rate claim.
- RSR2 added USD `145.34` versus RSR1; only USD `77.95` was a direct exit
  effect, and USD `67.39` came from later capital-path/whole-share sizing.
- Through Aug 20, forward RSR1, RSR2 and matched baseline have zero signals and
  zero closed trades. No win-rate or expectancy conclusion is available.
- The historical research tree is saturated: 13 branches are closed, two
  remain frozen forward shadows, and nearby parameter rescue is not authorized.

## Corrective operating plan

1. Keep formal V9, RSR1 and RSR2 unchanged.
2. Add no AI-capex exposure while the completed-close portfolio audit keeps the
   correlated-add cap at `0%`.
3. Continue the now-active immutable paper risk-action ledger for every future
   `reduce-review`, recording next-open full/half reductions and subsequent
   1/5/20-session saved-or-lost P&L without assuming a real order.
4. Continue the frozen high-volatility missed-leader ledger. Wait for matured
   5/20-session outcomes; do not reopen the rejected high-volatility sleeve from
   AAOI, AXTI or SNDK anecdotes.
5. Judge improvement by net expectancy, drawdown and concentration together.
   A higher win rate alone is not profit maximization.

## Decision

This week produced a useful distinction: the entry restraint was broadly
correct, while the risk-review-to-action workflow was underspecified. The next
research gain should come from measuring that action layer, not from adding
more entry parameters. This report authorizes no order and makes no change to
the real account or formal strategy.
