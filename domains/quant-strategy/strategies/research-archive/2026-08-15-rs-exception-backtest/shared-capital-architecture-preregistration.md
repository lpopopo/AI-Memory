# Shared-capital architecture preregistration

Registered before running the integrated comparison on 2026-08-15.

## Question

The core-allocation frontier identified an 80% index-core / 20% stock ceiling
as a research challenger to formal V9's 70% / 30% architecture. That result did
not share cash with RSR, enforce whole-share SPY/QQQ execution, or measure the
stock opportunities lost when the available stock sleeve shrinks. This audit
tests whether the challenger survives those operational constraints.

## Frozen architectures

- `formal_70_25`: 70% V9 SPY/QQQ core ceiling and the frozen RSR internal stock
  ceiling of 25%. Formal V9 permits up to 30% stocks, but RSR itself has never
  been tested above 25%; the remaining 5% is not silently reassigned.
- `challenger_80_20`: 80% V9 SPY/QQQ core ceiling and a 20% RSR stock ceiling.
- Both use the frozen RSR2 8% target, maximum three names, ATR/close-location
  filter, 20-session maximum and +15%/+5% profit lock. No RSR signal or exit
  parameter changes.

## Frozen account and execution assumptions

- Initial NAV scenarios: USD 6,000 research baseline and USD 5,751.77 latest
  working account NAV.
- One shared cash balance for the index core and RSR stocks.
- Whole shares for SPY, QQQ and all stocks; no fractional shares and no leverage.
- USD 1 commission for every buy or sell order and 10 bps slippage per side.
- RSR exits and entries execute using the frozen next-open/resting-stop path;
  core target changes execute at the frozen next-session close.
- Core sells execute before core buys. Core buys may not consume money already
  committed to an open stock position. Existing stock positions are not forced
  out merely to fill a core rounding shortfall.
- Core target shares round down so a whole-share implementation never exceeds
  its intended ETF target merely because of rounding.

## Frozen samples and metrics

- Training: 2024-01-02 through 2025-12-31.
- Held-out monitor: 2026-01-02 through the latest completed formal local row.
- Full context: 2024-01-02 through that same latest row.

Report combined return, max drawdown, Sharpe, monthly win rate, final value,
average/max core, stock and gross exposure, minimum cash, total costs, core
target shortfalls, RSR planned/filled/skipped entries, closed stock trades,
stock win rate and stock realized PnL.

## Shared-capital challenger screen

The 80/20 architecture remains a research challenger only if all of the
following hold for both NAV scenarios:

1. Combined total return is strictly higher in training, held-out 2026 and the
   full period.
2. Maximum drawdown is no more than 2 percentage points worse in each sample.
3. Sharpe is no more than 0.05 lower and monthly win rate is no more than 1
   percentage point lower in each sample.
4. Realized average core exposure is strictly higher in training and 2026; a
   theoretical ceiling that whole-share rounding cannot deploy is not useful.
5. Closed RSR trade count remains at least 80% of formal 70/25 and RSR win rate
   is not lower in training or 2026.
6. Maximum gross exposure does not exceed 100%, cash never becomes negative,
   and every filled order can be reconciled to the shared ledger.

Passing cannot promote 80/20 because RSR1/RSR2 lack genuine forward evidence.
It only determines whether 80/20 remains worth forward tracking. Failing removes
the challenger without reopening the core-ceiling grid on the same history.

## Governance

Research-only. No formal V9 file, live account, forward ledger or order may be
changed by this audit.
