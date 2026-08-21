# Forward opportunity-cost diagnostics registration

Frozen on 2026-08-15 before the first eligible completed session. Research-only; no order authorization and no change to V9, RSR1 or RSR2.

## Start and data contract

- First eligible completed U.S. session: 2026-08-17.
- Use the same completed-session cutoff, 32-name `ai_capex_broad` universe and source-completeness checks as the RSR1/RSR2 forward runner.
- If the latest required OHLCV or VIX/VIX3M data are incomplete, append nothing.
- Existing dated rows are immutable. A recomputed mismatch raises a conflict and preserves the ledger.
- Rows before the start date are forbidden.

## Daily diagnostic fields

1. `rsr1_signal_symbols`: frozen RSR1 signals on the completed close.
2. `high_vol_central_symbols`: the already-registered `hv_central` signal. This branch failed its portfolio gate and remains diagnostic-only.
3. `realized_5d_leaders`: stocks whose completed close is at least 10% above the close five sessions earlier.
4. `high_vol_missed_leaders`: realized five-session leaders with no frozen RSR1 signal during those five completed sessions and whose current ATR exceeds 4% or MA20 extension exceeds 12%.
5. `core_month_end`: whether the date is a visibly completed month-end.
6. At month-end, record SPY/QQQ V8 base targets, Fear-Gate-adjusted effective targets and the core risk regime.
7. `core_one_month_reversal`: label `down_then_up` or `up_then_down` only when the latest effective month-end target change reverses the immediately preceding month's change for either SPY or QQQ.

The five-session missed-leader label is an outcome diagnostic, never an entry signal. The core reversal label is known only at the later completed month-end and cannot rewrite the earlier decision.

## Review thresholds

- Report after 126 completed sessions even if there are no events.
- High-volatility diagnostics require at least 20 central signals and 20 missed-leader observations before any new research design.
- Core confirmation research requires at least five independent one-month reversals.
- These thresholds permit a new preregistered study only; they cannot promote a live rule.
