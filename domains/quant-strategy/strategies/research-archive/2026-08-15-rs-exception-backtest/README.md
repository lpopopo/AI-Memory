# Relative-Strength Exception Backtest

This research experiment tests whether the daily `SMH < MA50` blanket veto can
be replaced by a tightly sized relative-strength exception without changing the
formal V9 strategy.

## Research boundary

- Current user list contains 36 symbols; QQQM is excluded as a duplicate index
  vehicle, leaving 35 research-tradable stocks. The retrospective universe is
  subject to survivorship/selection bias.
- The preregistered SMH-gated forward shadow uses the 32-name `ai_capex_broad`
  scope. KO, RKLB and RDW remain in full-watchlist analysis but are excluded
  from this shadow because their existing themes do not share the intended
  semiconductor/AI-capex factor.
- Signal uses completed close data; entry and ordinary exits execute at the next
  session open.
- Intraday stops are assumed to be resting orders and use adjusted OHLC data.
- Whole shares, USD 1 commission per order, 10 bps slippage per side, USD 6,000
  initial NAV, fee-economics floor, single-name caps and a 25% stock-sleeve cap.
- 2024-2025 is the training interval. 2026 through the latest cached completed
  session is held out for testing.
- The experiment is research-only and cannot authorize a live trade or modify
  the frozen V9 chain.

## Compared variants

- `strict_veto`: no new stock entry while SMH is below its MA50.
- `rs_exception`: same baseline, but permits at most one 3%-5% target satellite
  (up to 8% when one whole share cannot fit the target) when the broad market is
  healthy and the stock passes breakout, MA20/MA50, volume, relative-strength,
  extension and event-gap cooldown checks.
- `unrestricted`: ignores the SMH MA50 entry veto. It is an upper-bound diagnostic,
  not a promotion candidate.

Run:

```powershell
..\..\..\.venv\Scripts\python.exe run_backtest.py
```

Outputs are written below `results/`.

The exact filter's fair matched-baseline comparison is generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_matched_baseline.py
```

ATR/close-location ablation, parameter neighbors, exit neighbors,
leave-one-symbol-out checks and descriptive block resampling are generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_risk_filter_ablation.py
```

Whole-share position-size and execution-cliff diagnostics are generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_position_sizing.py
```

Signal-delay and next-open gap robustness are generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_execution_robustness.py
```

Predefined universe-scope sensitivity is generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_universe_scope.py
```

All four predefined scopes improved paired-baseline return, drawdown and Sharpe
in both training and 2026. The 32-name forward scope is chosen from strategy
meaning before the first observation, not from the highest historical return.

Signal-date crowding, calendar attribution and signal-day regime dependence are
generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_temporal_concentration.py
```

Trade MFE/MAE, close-confirmed profit-stop neighbors and cost robustness are
generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_profit_protection.py
```

Zero-yield cash, an SGOV total-return proxy and passive opportunity-cost
benchmarks are evaluated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_cash_efficiency.py
```

Current SGOV/BIL yield, whole-share deployment, friction/tax break-even and the
cash reserve required for one to three future RSR entries are evaluated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_operational_cash_sweep.py
```

This operational audit remains research-only. It cannot authorize an ETF order
until broker interest, USD settlement, proceeds availability, fees and tax are
confirmed.

The 2026 held-out V9 70% index core plus RSR1/RSR2 stock-sleeve contribution is
evaluated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_combined_v9_portfolio.py
```

The preregistered 50%-100% V9 index-core allocation frontier, split-period
metrics and rolling three-year robustness are generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_core_allocation_frontier.py
```

Only the 80% ceiling passes the isolated core-only screen. Its required
shared-capital and whole-share follow-up is generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_shared_capital_architecture.py
```

The integrated audit rejects 80/20 at both tested account sizes because it
reduces training/full return and Sharpe after accounting for lost RSR capacity.
Formal V9 stays at 70% core / 30% stock ceiling; no allocation challenger remains.

The V9 core's March-exit/April-recovery whipsaw and predefined confirmation
alternatives are audited, without changing formal V9, with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_v9_core_whipsaw.py
```

The completed 2026-08-10 through 2026-08-14 watchlist moves and exact rejected
RSR1 conditions, including AAOI, are explained with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_latest_week_opportunities.py
```

The separately registered high-volatility trend event study and its conditional
whole-share portfolio simulation are generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_high_vol_trend.py
..\..\..\.venv\Scripts\python.exe evaluate_high_vol_portfolio.py
```

The event layer passed, but the portfolio layer failed its cross-period win-rate
and Sharpe gates. The branch is stopped and cannot be combined with V9/RSR on
this history.

Conditional extension of qualifying RSR2 winners beyond the frozen 20-session
maximum is tested with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_winner_extension.py
```

All three registered extension variants failed the cross-period screen; frozen
RSR2 remains unchanged.

Forward observations are regenerated deterministically with:

```powershell
..\..\..\.venv\Scripts\python.exe run_forward_shadow.py
```

Separate append-only, non-trading opportunity diagnostics are maintained with:

```powershell
..\..\..\.venv\Scripts\python.exe run_forward_opportunity_diagnostics.py
```

The immutable opportunity events receive read-only 5/20-session outcome
tracking with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_forward_opportunity_outcomes.py
```

It reports raw observations and overlap-controlled primary episodes, exact
horizon return, MFE and MAE. Incomplete horizons remain `n/a`; no one-day metric
is introduced after observing a reversal.

After the forward runner and opportunity diagnostics, the read-only economic
evidence scorecard is regenerated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_forward_expectancy_scorecard.py
```

It reports win-rate uncertainty, payoff, break-even win rate, expectancy,
profit factor, loss streaks, profit concentration and clustered-bootstrap
uncertainty for the matched baseline, RSR1 and RSR2. It never writes a forward
ledger and does not change the original promotion gates.

The preregistered audit of ordering among already-qualified RSR2 entries is run
with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_capital_constrained_ranking.py
```

It compares the current RS-plus-volume ordering with RS-only, low-ATR-first and
an equal-rank quality composite at two NAVs and two slippage levels. No
challenger passed; the current ordering remains unchanged and no additional
forward ledger was created.

The single preregistered whole-share partial-profit overlay is tested with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_partial_profit_scaleout.py
```

It sells half the executable whole shares at the next open after the existing
RSR2 +15% close trigger, while retaining the +5% stop on the remainder. The
overlay improved drawdown/Sharpe but reduced development and full-period return
and did not preserve win rate, so RSR2 remains unchanged.

This second ledger starts on 2026-08-17, refuses pre-start rows and incomplete
data, and records frozen RSR1 signals, failed high-volatility trend signals,
realized five-session leaders outside RSR1, and completed-month V9 core target
reversals. Existing dated rows cannot be changed by recomputation.

The forward runner does not write a ledger before the first completed session
on or after 2026-08-17, refuses to record incomplete-source sessions, never
liquidates an open shadow position merely because a report cutoff was reached,
and never authorizes a live order. It also records the separately preregistered
`RSR2-profit-lock-shadow` in its own ledger without changing RSR1.

The current evidence hierarchy and unresolved conflict are summarized in
`results/evidence_synthesis.md`.

The two below-MA50 exception variants failed the retrospective gate and are not
forward trade candidates.

The follow-up point-in-time test is run with:

```powershell
..\..\..\.venv\Scripts\python.exe pit_low_vol_backtest.py
```

It uses historical S&P 500/Nasdaq-100 membership and adjusted closes from
2006-2025. Because that panel lacks OHLCV and complete delisting returns, it can
test only a realized-volatility proxy, not the exact ATR/close rule. The proxy
reduced failed breakouts and drawdown but also removed large winners, lowered
final-period return/Sharpe, and was unstable across absolute thresholds. The
volatility filter is therefore research-only and cannot be promoted as a hard
entry veto. See `results/pit_decision.md`.

The preregistered exact-OHLCV transferability audit is generated with:

```powershell
..\..\..\.venv\Scripts\python.exe download_pit_exact_ohlcv.py
..\..\..\.venv\Scripts\python.exe evaluate_pit_exact_filter.py
```

It freezes the historical-membership symbol list before downloading adjusted
OHLCV, then applies the same 4% ATR / 50% close-location pair to an otherwise
matched breakout portfolio across development, validation and final periods.
Coverage was 99.3%-100.0%, but the pair failed the registered cross-period
screen: 2020-2022 Sharpe was marginally worse and mean trade return remained
negative. The 2023-2025 segment passed, which cannot rescue the failed
validation period. RSR1 therefore remains a forward-only falsification test,
not a hard formal veto.

The preregistered parameter-selection-bias audit is run with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_selection_bias_audit.py
```

It evaluates the already-inspected 20-cell ATR/close-location family with all
252 symmetric five-of-ten time-block splits and a 10,000-sample family-wise
20-session block bootstrap. The result is suggestive but not sufficient: PBO
is 13.1% and the family-wise p-value is 0.063, yet the frozen 4%/50% cell
improves return and Sharpe in only 6/10 registered blocks. Three early blocks
had no activity; the rule improved 6/7 active blocks, but those empty blocks
cannot be removed after observation. The selection-bias concern therefore
remains formally uncontained and no parameter rescue is allowed.

Forward evidence power and duration are calibrated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_forward_power_duration.py
```

At 20 closed trades, the frozen historical effect sizes imply 94.9%/98.1%
power for RSR1/RSR2 to beat their historical payoff-derived break-even hit
rates, but only 25.2%/40.0% power to establish a win rate above 50%. Equal-sized
candidate/baseline samples require about 59/43 trades per arm for 80% relative
power. At the historical RSR1 arrival rate of 23 trades per 659 sessions, the
20-trade gate takes about 573 sessions/2.3 years in expectation; reaching it by
126 sessions has probability below 0.01%. These are planning calibrations, not
new gates. Forward payoff and expectancy must still be measured because the
historical break-even rate may not persist.

The final registered-branch inventory and forward-only roadmap are generated
with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_research_saturation.py
```

All 27 decision-register branches are classified: 13 historical branches are
closed/rejected, two variants remain frozen forward shadows, eleven items are
retained measurement/control layers, and one cash-yield item remains conditional
on external account facts. This inventory freezes additional parameter searches
on the same history; it does not declare forward validation complete. Through
2026-08-20 there are four completed forward sessions, zero closed RSR1/RSR2
trades and zero mature opportunity outcomes. See
`results/research_saturation_roadmap.md`.

Backtest mechanics are independently audited with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_backtest_integrity_audit.py
```

The audit perturbs all future rows, reconstructs fills and cash, checks adjusted
OHLC geometry, compares RSR1/RSR2 common paths, and reruns the point-in-time
screen without artificial period-end liquidation. All causal/accounting checks
passed. Nine terminal exits changed return by at most 0.0715 percentage points
and the transfer screen still failed; six malformed provider bars touched no
held trade. A guard now preserves a pending exit when a session lacks an open.

Historical profit sources and opportunity cost are decomposed with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_economic_edge_decomposition.py
```

The fixed 32-name path shows that RSR1 directly excludes 16 losers/$554.79 of
loss and seven winners/$159.37 of profit. Its top-three winners account for
50.15% of net P&L, although the remaining P&L is still positive. Of RSR2's
$145.34 incremental P&L, only $77.95 is a direct changed-exit effect; $67.39 is
later capital-path and whole-share sizing. These are attribution diagnostics,
not permission to tune or trade.

The same attribution is carried into immutable forward evidence with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_forward_edge_attribution.py
```

It reads but never changes the signal, baseline, RSR1, RSR2 and status ledgers.
With four sessions and zero trades it correctly returns `awaiting_sample` and
null economic fields, not a fabricated zero effect.

Zero-signal sessions are explained without threshold changes using:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_forward_zero_signal_bottleneck.py
```

For Aug 17-19 the broad gate was open throughout. SMH below MA50 bound the last
two sessions. On Aug 17, AXTI alone reached the late stock funnel, but its 48.55%
MA20 extension and 12.59% ATR made it a high-volatility chase rather than a near
miss. The audit therefore supplies no basis for relaxing the frozen gates.

The completed-session weekly review through Aug 20 is recorded in
`results/weekly_strategy_review_2026-08-21.md`. MRVL, TSLA, DRAM and MU were the
only positive names among the frozen 32-name universe
from Aug 14 to Aug 20, and the latter three gained less than 1%; AAOI fell
14.09%. The entry restraint is therefore not classified as a broad
miss. The correctable weakness is the underspecified action layer after a
`reduce-review`; future reviews should measure immutable next-open
counterfactuals without treating them as real orders or tuning new thresholds.

That action layer is now measured with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_forward_risk_actions.py
```

The preregistration separates three already-observed retrospective seeds from
all future genuine-forward events, applies 10 bps sell slippage and USD 1 paper
commission, and reports full/half reductions at fixed 1/5/20-session horizons.
At one session, full reduction helps only one of the three seeds; no five- or
twenty-session outcome is mature. The scorecard therefore cannot select a
policy or authorize an automatic sale.

The completed Aug 20 forward checkpoint is summarized in
`results/forward_review_2026-08-20.md`. It records four source-complete sessions,
zero RSR/baseline signals or trades, one non-independent MRVL raw missed-leader
observation, and the reversal of the arbitrary risk-action as-of total from
+$39.90 to -$6.14. Fixed horizons, not observation dates, remain controlling.

The already-completed experiment families are consolidated without a new
parameter search using:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_objective_frontier.py
```

The resulting 27-row matrix computes Pareto status only inside 11 fixed
family/period/NAV/cost groups. RSR2 is the strongest historical stock-sleeve
candidate, but remains a frozen shadow because exact transfer failed,
selection bias is uncontained and genuine-forward trades remain zero. The
deployable architecture stays formal V9 70/30. Local frontier appearances for
partial scale-out, winner extension, balanced ranking, core-only 80% and the
short 2026 80/20 replay do not override their cross-period/evidence failures.
See `results/objective_frontier_report.md`.

Sampling uncertainty in the historical mechanisms is measured without rerunning
or retuning a strategy using:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_historical_uncertainty.py
```

The fixed 20,000-sample signal-date cluster bootstrap finds a 98.43%
probability that the quality filter's directly excluded trades retain both
negative mean return and negative mean P&L; every leave-one-date omission is
also negative. RSR2's total P&L improvement remains positive in 99.59% of
samples, but the pure direct-exit effect is positive in 87.72%, and total,
direct and win-rate deltas are all positive in only 64.31%. Two paired deltas
explain 86.93% of total uplift, the two direct exits explain 100% of direct
uplift, and only one historical loss becomes a win. This prioritizes genuine
forward validation of entry-quality loss avoidance over more exit tuning; it
does not promote either shadow. See
`results/historical_uncertainty_audit_report.md`.

Peek-safe forward mechanism interpretation is generated with:

```powershell
..\..\..\.venv\Scripts\python.exe evaluate_forward_mechanism_clock.py
```

Entry-quality exclusions and paired RSR1/RSR2 exits accumulate continuously,
but their directional labels are frozen only at 5, 10 and 20 closed outcomes.
Actual non-zero changed exits have descriptive checkpoints at 1, 2 and 5.
Rows are ordered by the date when the complete outcome becomes known, so later
appends cannot redraw an earlier checkpoint. Through Aug 20 all three clocks
remain at zero/`unavailable`; the original promotion gates remain unchanged.
See `results/forward_mechanism_evidence_clock_report.md`.
