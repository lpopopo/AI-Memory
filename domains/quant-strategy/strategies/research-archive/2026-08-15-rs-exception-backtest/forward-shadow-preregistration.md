# RSR1 Forward-Shadow Preregistration

## Status

- Version: `RSR1-shadow`
- Start: first completed U.S. session on or after `2026-08-17`
- Formal V9 change: `false`
- Live-order authorization: `false`
- Frozen after the 2026-08-15 retrospective review.
- Classification after the point-in-time proxy test: falsification shadow only;
  not a promotion-leading candidate.
- Shadow universe: `ai_capex_broad`, 32 symbols. The complete 36-name watchlist
  remains in daily analysis; QQQM is excluded from stock simulation as the index
  duplicate, and KO/RKLB/RDW are excluded only from this SMH-gated shadow.

## Universe scope correction before observation

The first forward session has not occurred, so the scope is corrected before
any forward outcome can be observed. The earlier current-list simulator applied
the SMH gate to all 35 non-index names, including a defensive beverage and two
space names that do not share the intended semiconductor/AI-capex factor.

The frozen shadow therefore uses the 32-name `ai_capex_broad` scope derived from
the existing watchlist theme labels. It excludes KO (`consumer_defensive_beverages`)
and RKLB/RDW (`space_satellite`) while retaining TSLA, TTMI and CEG as AI-capex
adjacent names. All 36 user-selected symbols remain covered by full-watchlist
analysis; this change affects only the SMH-gated shadow ledger.

This scope was selected from strategy meaning, not the best historical result.
The candidate improved return, drawdown and Sharpe versus its paired baseline in
both training and 2026 across all four predefined scopes (`all_35`,
`ai_capex_broad`, `direct_semiconductor_chain`, and `legacy_supergroup_mapped`).
See `results/universe_scope_report.md`.

## Hypothesis retained

Keep the SMH MA50 veto for new semiconductor/common-factor stock entries. Test
whether filtering technically qualified entries for moderate realized
volatility and a constructive signal-day close improves trade quality without
destroying net return.

Frozen candidate rules:

- Broad gate: SPY above MA200, QQQ above MA100, VIX below 25 and VIX/VIX3M below 1.
- Theme gate: SMH at or above MA50.
- Stock: close above MA20 and MA50 and above the prior 20-session high.
- Relative strength: 20-session return exceeds SMH by at least 3 percentage points.
- Volume: signal-day volume at least 1.2 times the prior 20-session average.
- Extension: no more than 12% above MA20.
- ATR14/close: no more than 4%.
- Close location in the daily range: at least 50%.
- Positive opening gap of at least 10%: enforce the existing T+0/T+1 cooldown
  and T+2 stabilization test.
- Execute at the next session open; 10 bps slippage and USD 1 per order.
- Record the realized next-open gap versus the signal close. No retrospective
  gap cap is added to RSR1; the fixed-watchlist sample had no entry above 4.57%.
- Whole shares, minimum USD 200 notional, 8% stop, 20-session maximum hold.
- Normal target 8%, single-name maximum 15%, stock sleeve maximum 25%, maximum
  three simultaneous names.

Frozen matched baseline:

- Use the same broad/theme gates, stock breakout, RS20 minimum 3%, volume 1.2x,
  extension 12%, gap cooldown, next-open execution, sizing, 8% stop and 20-day
  maximum hold.
- Disable only the two tested risk filters by setting ATR/close cap to 100% and
  close-location floor to 0%.
- This pairing isolates the incremental effect of ATR and close location. The
  earlier provisional comparison against the default 5% RS20 threshold was
  confounded and is superseded by `results/matched_baseline_report.md`.

## Hypotheses rejected for now

- A single-stock relative-strength exception while SMH is below MA50.
- A subtheme-breadth repair exception while SMH is below MA50.

Both reduced the default historical/test metrics and remain monitor-only.

## Promotion gate

Do not promote before all are true:

- At least 126 completed sessions and 20 closed candidate trades.
- At least three distinct subthemes and no one symbol contributes more than 35%
  of gross profits. Repeated winning trades are aggregated by symbol before this
  concentration check; losses do not reduce gross-profit concentration.
- Candidate net return is not below the contemporaneous strict baseline.
- Candidate win rate is at least five percentage points above baseline.
- Candidate profit factor is at least 1.30.
- Candidate Sharpe is not below baseline.
- Candidate max drawdown is not worse than baseline by more than one percentage point.
- Results survive the recorded USD 1 commission and 10/20 bps slippage checks,
  both as a full strategy rerun and as a fixed-trade-path repricing. The latter
  prevents whole-share/capacity changes from turning a different trade list into
  an apparent cost benefit.

Failure of any gate keeps the filter in research. No parameter is changed during
the forward interval; a change requires a new version and a new ledger.

## Point-in-time evidence added on 2026-08-15

The 2006-2025 historical-membership test could not reproduce ATR or close
location because its panel contains adjusted closes only. Its closest frozen
proxy (`RV20 <= 40%` plus cross-sectional volatility percentile <= 60%) reduced
20-session close-stop events but also removed a disproportionate share of +10%
winners. In 2020-2025 it returned 3.01% CAGR versus 5.41% for the unfiltered
weekly breakout baseline at 10 bps, with Sharpe 0.26 versus 0.34; max drawdown
improved to -27.64% from -35.04%.

This does not cancel the already-frozen RSR1 shadow, because ATR and signal-day
close location contain information absent from the proxy. It does raise the
burden of proof: RSR1 remains diagnostic, cannot guide live orders, and must
clear every original promotion gate without changing parameters.

The corrected current-watchlist comparison, holding RS20 and every other rule
constant, remains favorable to the exact filter in 2024, 2025 and 2026 YTD.
That evidence is still survivorship-biased and therefore supports observation,
not promotion.

Exact-filter ablation also leaves the frozen combined rule intact. ATR-only and
close-location-only each improved the matched baseline, but the combination was
best in 2025 and 2026 YTD. The combined filter beat its paired baseline across
all 35 leave-one-symbol-out runs and all nine tested stop/maximum-hold neighbors.
These are repeated views of the same post-hoc fixed-watchlist history, not new
forward samples; no threshold or promotion gate changes.

The target weight remains 8%. A 12% retrospective run produced more dollars but
reduced peak diversification from three names to two and changed its trade set
between 10 and 20 bps because one ASML share crossed the 15% cap. No alternative
weight both beat 8% in training and 2026, stayed within the drawdown screen, and
preserved its execution path. No sizing challenger is added.

Signal-to-execution stress does not overturn the filter comparison: the combined
filter improved paired-baseline return, Sharpe and drawdown in both training and
2026 for 11 of 12 delay/gap cells (9 of 12 after a lenient trade-count screen).
Delaying entry to the second or third following open reduced full-sample return
from 17.81% to 11.34%/11.61% but left it positive. No gap or delay parameter is
changed; the shadow must record actual next-open execution.

A pre-start timing audit on the corrected 32-name scope found 23 candidate
trades across 21 signal dates, with no more than two on one date. Candidate PnL
was positive in all three descriptive SMH/MA50-buffer buckets and all three
observed VIX buckets, while baseline-only trades lost money in every SMH bucket.
These small cells add no timing or regime rule; the original promotion gates and
forward start remain unchanged.

The separate `RSR2-profit-lock-shadow` begins on the same date under its own
preregistration and ledger. It changes exits only and is benchmarked against
RSR1. Its existence does not amend this RSR1 specification or promotion gate.
