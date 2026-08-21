# RSR filter selection-bias audit — preregistration

Frozen on 2026-08-20 before generating any result from this audit. This audit
does not search for a successor rule. It measures how much confidence should be
discounted because twenty ATR/close-location cells were inspected on the same
fixed-current-watchlist history.

## Frozen trial family

The family contains exactly the existing 20 cells:

- ATR14/close cap: 3%, 4%, 5%, 6%, or no effective cap (`100%`);
- signal-day close-location floor: 0%, 25%, 50%, or 75%.

Every cell keeps RS20 3%, volume ratio 1.2, extension 12%, the strict SMH MA50
gate, broad/fear gates, event-gap cooldown, frozen RS-plus-volume ranking, 8%
whole-share sizing, 25% sleeve, three-name capacity, 8% stop, 20-session hold,
USD 1 orders and 10 bps slippage. The unfiltered `100% ATR / 0% location` cell
is the matched baseline. The already-frozen RSR1 cell is `4% / 50%`.

Data begin 2024-01-02 and end at the latest completed cached session available
when the audit first runs, expected 2026-08-18. Later sessions cannot be added
to this audit. The universe remains the fixed current watchlist, so this test
cannot cure survivorship bias or replace genuine forward evidence.

## Combinatorially symmetric cross-validation

1. Run each cell once over the full frozen interval and retain its net daily
   equity returns.
2. Divide completed equity sessions into ten contiguous, near-equal blocks by
   session count. No date-based block may be moved after results are seen.
3. Evaluate all `C(10, 5) = 252` choices of five in-sample blocks; the other
   five blocks are out of sample.
4. Within each split, select the finite cell with the highest in-sample daily
   Sharpe. Ties use higher in-sample compounded return, then lexical cell ID.
5. Rank the selected cell's out-of-sample Sharpe among all twenty cells. PBO is
   the fraction of splits where its out-of-sample rank is at or below the
   median. Report selection frequency, median out-of-sample rank, median
   selected-minus-baseline return, and median regret versus the best OOS cell.

This is a selection-bias diagnostic, not an independent market test. Holding
state comes from each cell's single chronological full-path simulation; the
block recombination is used only to compare return observations.

## Family-wise block-bootstrap test

- For each of the nineteen challengers, form paired daily return differences
  versus the matched baseline.
- Observed statistic: the largest mean daily difference among challengers.
- Null bootstrap: center each difference series, then resample the same
  circular 20-session blocks across every challenger.
- Use 10,000 deterministic samples with seed `20260820`.
- Family-wise p-value is the proportion of bootstrap maximum means at least as
  large as the observed maximum, with the plus-one correction.
- Also report the fixed 4%/50% cell's unadjusted paired p-value, but it cannot
  override the family-wise result because the cell was identified after
  inspecting the family.

## Frozen 4%/50% stability check

For each of the ten chronological blocks, report fixed-cell minus baseline
compounded return and Sharpe. Count positive return and positive Sharpe blocks.
No block may be excluded for an unfavorable market regime.

## Interpretation gate

Call the retrospective selection-bias concern `contained` only if all hold:

1. PBO is below 50%;
2. family-wise p-value is below 10%;
3. the fixed 4%/50% cell has positive return delta in at least 7/10 blocks; and
4. it has positive Sharpe delta in at least 7/10 blocks.

Failure does not prove the filter has no edge; it means the current-list
historical headline must be treated as selection-contaminated and genuine
forward evidence must carry the decision. Passing would still not authorize a
trade or modify formal V9, RSR1, or RSR2.
