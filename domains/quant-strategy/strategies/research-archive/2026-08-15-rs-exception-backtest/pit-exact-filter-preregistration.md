# Point-in-time exact OHLCV filter audit — preregistration

Frozen on 2026-08-20 before downloading the new OHLCV panel or inspecting any
result from this experiment.

## Question

Does the frozen RSR1 quality pair — `ATR14 / close <= 4%` and signal-day close
location `>= 50%` — improve an otherwise identical breakout system outside the
fixed current watchlist when membership is point-in-time?

This is a transferability audit, not a new live strategy. The historical
S&P 500 plus Nasdaq-100 universe contains many non-semiconductor companies, so
even a pass cannot promote RSR1, change formal V9, or authorize an order.

## Frozen data boundary

- Point-in-time membership: the existing S&P 500 plus Nasdaq-100 membership
  history, deduplicated by symbol on each completed session.
- Candidate symbols: only symbols already present in the existing point-in-time
  adjusted-close panel and active at least once from 2015-01-01 through
  2025-12-31. This list is fixed before the OHLCV download.
- OHLCV warm-up begins 2014-01-01. Evaluation ends 2025-12-31; no 2026 data may
  enter this audit.
- OHLCV is adjusted consistently for splits and distributions. Volume is not
  price-adjusted.
- Download failures, coverage, and symbol mappings must be reported. Missing
  delisting returns remain a limitation.
- The audit is descriptive-only if median active-membership close coverage is
  below 70% in any evaluation period.

## Frozen comparison

Both variants use the same completed-close signal and next-session execution:

- market gate: SPY above MA200, QQQ above MA100, SMH at or above MA50, VIX below
  25, and VIX/VIX3M below 1;
- stock close above MA20 and MA50 and above the prior 20-session high;
- 20-session relative return versus SMH at least 3%;
- volume at least 1.2 times its prior 20-session average;
- extension above MA20 from 0% through 12%;
- no 10% positive-gap event block under the frozen two-session cooldown rule;
- ranking is the frozen `RS20 * 100 + min(volume ratio, 5)` score.

`matched_baseline` sets no effective ATR or close-location veto.
`combined_4pct_50pct` adds only:

- `ATR14 / close <= 4%`; and
- `(close - low) / (high - low) >= 50%` on the signal session.

## Frozen execution model

- USD 6,000 initial NAV for each independently restarted period.
- Whole shares, USD 1 commission per order, 10 bps slippage per side.
- Target 8% NAV per entry, maximum 15% per name when one whole share is needed.
- Maximum three open names and 25% aggregate stock-sleeve exposure.
- Entry is skipped when the next open gaps more than 5% above signal close.
- Resting 8% stop; ordinary exit at the next open after close below MA20,
  RS20 below zero, or 20-session maximum hold.
- Three-calendar-day same-symbol re-entry cooldown.
- No profit lock, partial sale, winner extension, cash yield, or parameter search.

## Frozen periods and scorecard

- development: 2015-01-01 through 2019-12-31;
- validation: 2020-01-01 through 2022-12-31;
- final: 2023-01-01 through 2025-12-31.

Report period return, maximum drawdown, Sharpe, win rate, trade count, mean net
trade return, profit factor, payoff ratio, break-even win rate, and exposure.
Also report the candidate's excluded baseline trades and their outcomes.

The quality pair is called transferable only if, in both validation and final:

1. coverage is at least 70%;
2. the candidate has at least 20 closed trades;
3. return and Sharpe are higher than the matched baseline;
4. maximum drawdown is no worse;
5. win rate is no lower; and
6. mean net trade return is positive.

Development results are diagnostic and cannot rescue a failed validation or
final period. No threshold neighbors will be tested in this branch. A pass
would justify only stronger confidence in the existing forward falsification
test; a failure stops the exact-filter transferability claim.

## Governance

Formal V9, RSR1, RSR2, the real-account holdings, and all live permissions remain
unchanged. This experiment cannot submit or recommend an order.
