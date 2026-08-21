# Forward validation power and duration audit — preregistration

Frozen on 2026-08-20 before calculating this audit's outputs. This is a
read-only interpretation layer. It does not change the original 126-session /
20-closed-trade promotion gate, the forward ledgers, formal V9, RSR1, RSR2, or
live permissions.

## Frozen retrospective calibration inputs

Use the existing scorecard values through the frozen 2026-08-18 cache:

- matched baseline: 19 wins / 44 closed trades, win rate 43.1818%;
- RSR1: 15 / 23, win rate 65.2174%, break-even win rate 27.0389%;
- RSR2: 16 / 23, win rate 69.5652%, break-even win rate 26.7623%;
- RSR1 historical arrival calibration: 23 closed trades over 659 completed
  sessions from 2024-01-02 through 2026-08-18.

These inputs are survivorship- and selection-contaminated calibrations, not
priors and not forward evidence.

## Exact one-sample power calculations

For RSR1 and RSR2 separately, assume the retrospective candidate win rate only
as a planning effect size. For each null below, enumerate binomial outcomes and
use a one-sided 5% test:

1. candidate-specific break-even win rate;
2. 50% win rate; and
3. retrospective matched-baseline win rate, 19/44.

For each null report:

- power at 20 candidate trades;
- the minimum sample from 5 through 500 with at least 80% power; and
- the critical number of wins at that minimum sample.

For every sample size, the rejection boundary is the smallest integer wins
`k` such that `P_null(X >= k) <= 0.05`. No normal approximation may replace
this one-sample enumeration.

## Relative two-sample comparison

Estimate the equal-sample size required to distinguish the candidate planning
rate from 19/44 with 80% power at one-sided 5%. Enumerate the joint binomial
outcome distribution and apply the pooled two-proportion z rejection rule.
Search equal sample sizes from 5 through 500. This is a planning approximation:
forward baseline and candidate trade paths are not guaranteed independent or
equal-sized.

## Confidence and precision calculations

Using a two-sided Wilson 95% interval, report for each candidate:

- at 20 trades, the probability that the Wilson lower bound exceeds the
  candidate break-even rate, 19/44, and 50%;
- the minimum sample from 5 through 500 at which that probability is at least
  80% under the candidate planning rate; and
- the minimum sample at which the probability of Wilson half-width no greater
  than 10 percentage points is at least 80%.

The probability integrates over all possible observed win counts. It does not
plug in a fractional expected number of wins.

## Duration calibration

Treat the historical RSR1 count only as a homogeneous Poisson planning rate:
`23 / 659` trades per completed session. For every material target sample size,
report:

- expected sessions (`target / rate`);
- median sessions and 80%-completion sessions found from the Poisson count CDF;
- expected years at 252 sessions per year; and
- probability of reaching the target within the original 126-session minimum.

The arrival estimate is descriptive and regime-dependent. It cannot justify
expanding the universe, weakening rules, or backfilling missed signals.

## Interpretation

- Twenty trades remain the immutable first-stage economic/falsification gate.
- If twenty trades have high power only against break-even but low power to
  establish a majority win rate or the historical headline, label that
  distinction explicitly; do not silently redefine the promotion gate.
- Any larger sample shown by this audit is a second-stage confidence benchmark,
  not an automatic new formal gate.
- No result authorizes a trade.
