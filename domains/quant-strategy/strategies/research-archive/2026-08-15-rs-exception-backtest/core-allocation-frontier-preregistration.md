# V9 core-allocation frontier preregistration

Registered before running the allocation comparison on 2026-08-15.

## Question

The formal unified V9 architecture caps the SPY/QQQ index core at 70% and the
individual-stock sleeve at 30%. Long-history evidence shows that an unfilled
30% stock sleeve creates material cash drag, but it does not establish which
index-core ceiling offers the best return/drawdown trade-off. This audit changes
only the index-core ceiling. It does not change MA150/MA200 signals, the Fear
Gate, execution timing, transaction cost, or any stock rule.

## Frozen candidates and samples

- Core ceilings: 50%, 60%, 70%, 80%, 90%, and 100%.
- Development: 2006-01-03 through 2014-12-31.
- Validation: 2015-01-02 through 2019-12-31.
- Final historical test: 2020-01-02 through 2025-12-31.
- Current held-out monitor: 2026-01-02 through the latest completed local row.
- Full historical context: 2006-01-03 through 2025-12-31.
- Rolling robustness: 756-session windows on the continuous 2006-2025 path,
  sampled every 21 sessions.

Each period is run from a fresh unit NAV after an adequate warm-up. The V9
engine's existing 10 bps one-way proportional transaction cost remains active.
No SGOV yield, leverage, stock alpha, tax, FX, or broker-specific commission is
added.

## Frozen metrics

For every ceiling and period report total return, CAGR, maximum drawdown,
annualized volatility, Sharpe, Sortino, Calmar, monthly win rate, positive-year
rate, daily 95% expected shortfall, average/max gross exposure, turnover and
transaction count. Rolling windows report median/minimum CAGR, median/minimum
Sharpe, worst drawdown and positive-return frequency.

## Balanced-challenger screen

The formal 70% ceiling is the reference. A higher ceiling enters research-only
challenger status only if all of the following hold:

1. Total return is strictly higher in validation, final historical test, and
   the 2026 held-out monitor.
2. Maximum drawdown is no more than 3 percentage points worse than 70% in each
   of those three samples.
3. Sharpe is no more than 0.05 below 70% in each sample.
4. Monthly win rate is no more than 1 percentage point below 70% in each sample.
5. Full-2006-2025 maximum drawdown is not worse than -20%.
6. The fraction of positive rolling three-year windows is not below 70%.

If more than one ceiling passes, the lowest passing ceiling is retained as the
only challenger because it achieves the objective with less risk. Passing this
screen does not promote the challenger: any ceiling above 70% necessarily
reduces the maximum stock sleeve so combined gross exposure cannot exceed 100%,
and that shared-capital interaction requires a separate audit.

## Governance

The output is research-only, authorizes no order, cannot change formal V9, and
cannot be used to re-search the thresholds above on the same history. A failed
candidate may be reopened only with a distinct mechanism or genuinely new data.
