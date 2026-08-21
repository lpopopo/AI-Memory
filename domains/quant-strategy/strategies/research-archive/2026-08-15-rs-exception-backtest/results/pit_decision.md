# PIT low-volatility proxy decision

## Decision

Do not promote `ATR14 / close <= 4%` or its adjusted-close volatility proxy as a
hard entry filter. Keep the frozen `RSR1-shadow` only as a forward falsification
test. For now, volatility may be displayed as a risk flag, but it must not veto
an otherwise valid V9 entry or authorize a larger position.

## Why

- In the independent 2020-2025 period, the dual low-volatility proxy improved
  max drawdown from -35.04% to -27.64%, but CAGR fell from 5.41% to 3.01% and
  Sharpe fell from 0.34 to 0.26 after 10 bps one-way costs.
- The 20-session positive-event rate improved only from 54.55% to 54.82%.
- The close-stop rate fell from 19.63% to 15.90%, but the +10% winner rate also
  fell from 13.79% to 10.10%. Rejected high-volatility events contained both
  more failures and substantially more convex winners.
- The result was not driven by hiding in cash: both variants averaged 72.00%
  exposure in 2020-2025.
- Absolute volatility thresholds were unstable. In 2020-2025, caps at 35% and
  40% produced negative CAGR, while 30%, 45%, and 50% were positive.
- Weekly ranking turnover was roughly 47 times NAV per year. At 20 bps, the
  2020-2025 CAGR was 0.60% for baseline and -1.77% for the proxy, so neither
  weekly implementation is deployable as tested.
- Across sixteen rolling three-year windows, the proxy improved drawdown in
  81.2% and monthly win rate in 68.8%, but improved Sharpe in only 62.5%; the
  aggregate return sacrifice remained material.

## What remains useful

The evidence supports using relative volatility as a position-sizing or entry-
quality diagnostic. It does not support a binary fixed threshold. A future test
may compare unchanged entry eligibility with smaller initial sizing for the
highest-volatility bucket, provided the sizing rule is preregistered and tested
with lower turnover, exact OHLCV/ATR, and complete delisting returns.

The exact OHLCV filter on the fixed current list (36 listed symbols, 35
research-tradable after excluding duplicate index vehicle QQQM) does outperform
a corrected matched baseline whose RS20 threshold and all other rules are identical. This
confirms that a forward falsification test is worthwhile, but does not reverse
the no-promotion decision because the point-in-time universe cannot reproduce
ATR/close location and the fixed watchlist remains survivorship-biased.

## Data limitation

The point-in-time membership panel covers 698 of 945 historical symbols with a
median month-end price coverage of 78.6%. It lacks OHLCV, permanent identifiers,
and complete delisting returns. All results remain research-only.
