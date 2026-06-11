# Institutional Overlay Replay Protocol

Date created: 2026-06-08

Purpose: define a repeatable replay method for comparing the existing strategy workflow against the experimental institutional overlays.

Status: experimental protocol. Use for historical diagnostics and paper-model comparison only.

## Replay Question

When AI/semiconductor/storage themes experience a crowded unwind, does the institutional overlay framework improve portfolio behavior versus the existing workflow?

Primary comparison:

- `baseline_rules`: existing market fear gate, single-stock stop rules, concentration rules, and daily monitoring.
- `overlay_rules`: baseline rules plus flow-fragility score, trend-aligned entry score, AI quality/capex-cycle classification, and factor-macro flags.

## First Replay Window

Initial event:

- Event date: 2026-06-05 close.
- Trigger: AI/semiconductor/storage synchronized drawdown with VIX about `21.51`.
- Model holdings: MRVL, AMD, WDC, STX.
- Event-day diagnostic: `memory/daily/2026-06-08-institutional-overlay-replay-2026-06-05.md`.

Replay window:

- `T0`: 2026-06-05 close.
- `T1`: 2026-06-08 close or best verified regular-session snapshot.
- `T2-T5`: next four completed trading days after `T1`.

Do not fill future rows before the data exists.

## Baseline Rules For Replay

Use only rules already present before the institutional overlay:

- Market fear gate controls new exposure and cash floors.
- Existing single-stock stops and reduce lines remain active.
- Portfolio concentration rules remain active.
- News does not override price or risk rules.

Baseline action logic:

- If a stop line is breached by daily close, mark the position reduce-review.
- If a near-stop warning is not already formalized, do not assume a forced trim.
- If market fear is elevated, no new aggressive buys.
- If no post-close audit exists, record the delay as process risk but do not invent same-day execution.

## Overlay Rules For Replay

Apply these additions:

### Flow Fragility

If `flow_fragility = elevated`:

- Block new AI/semiconductor/storage chase buys.
- Require trend-aligned reclaim before any add.
- Review every correlated holding against stop and near-stop levels.
- Prefer defensive-hold or profit-protection language over normal hold when theme weakness is synchronized.

If `flow_fragility = acute`:

- Block all new correlated-theme adds.
- Run portfolio-level correlated-risk review before single-stock optimism.
- Consider model trims only when price action also breaches stop, near-stop, or profit-protection rules.

### Trend-Aligned Entry

If `trend_aligned_entry = trend_broken`:

- No new buy/add.
- Existing holdings move to stop/reduce/defensive review depending on price.

If `trend_aligned_entry = cheap_but_unconfirmed`:

- Watch only.
- No order until reclaim or support confirmation.

If `trend_aligned_entry = trend_aligned`:

- Candidate can enter ranking, subject to fear gate and concentration.

### AI Quality / Capex-Cycle

Use `ai-quality-capex-cycle-classification.md`.

High capex-cycle sensitivity names:

- Lower max role during elevated flow fragility.
- Need stronger trend confirmation.
- Cannot be called diversified AI exposure if several holdings express the same capex chain.

### Factor-Macro Flags

If `theme_overlap_high` or `sleeve_correlation_high`:

- Treat the portfolio as one effective theme basket for risk review.
- Trim/add decisions must evaluate total theme exposure, not only single-ticker weight.

If `consumer_backstop_fragility` or `K_shaped_consumption_risk`:

- Do not assume broad consumer demand will cushion an AI/growth de-rating shock.
- Record whether consumer stress, energy prices, credit stress, or wealth-effect concentration coincided with the equity drawdown.
- Use the flags as macro context, not as standalone sell signals.

## Replay Ledger Fields

Use `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv`.

Minimum required fields:

- Date.
- Data timestamp and quality.
- Ticker prices and portfolio value.
- Market fear state.
- Flow-fragility score and state.
- Trend-aligned entry state.
- Factor-macro flags.
- Baseline action.
- Overlay action.
- Baseline portfolio value.
- Overlay portfolio value.
- Difference and explanation.

## Initial Overlay Action Assumption

For the first 2026-06-05 event replay only:

- AMD: overlay marks `reduce-review` immediately because the stop was breached.
- MRVL: overlay marks `profit-protection review`, but no automatic extra sale unless close `<260` or later weakness confirms.
- WDC: overlay marks `defensive hold / near-stop review`, no automatic sale unless close `<500` or later weakness confirms.
- STX: overlay marks `defensive hold / near-stop review`, no automatic sale unless close `<835` or later weakness confirms.
- All new AI/semiconductor/storage buys: blocked until trend-aligned entry improves.

This keeps the overlay from becoming a retroactive "sell everything" model.

## Metrics

Compare baseline versus overlay:

- Portfolio value by day.
- Max drawdown from 2026-06-04 model snapshot.
- Cash percentage.
- Stock exposure percentage.
- Number of unnecessary sells.
- Number of avoided false adds.
- Missed rebound cost.
- Whether stop/reduce decisions were recorded on time.

## Interpretation Rules

Promising:

- Overlay reduces drawdown or forces earlier risk review without materially missing a confirmed recovery.

Too defensive:

- Overlay blocks recovery buys after trend confirmation returns, or raises cash drag without reducing risk.

Too noisy:

- Overlay frequently flags elevated risk but no correlated drawdown follows.

Insufficient data:

- Options, CTA, and ETF-flow components remain low-quality; keep score as diagnostic rather than decision.

## Promotion Boundary

Do not update `memory/decisions.md` from one replay. Promotion requires broader historical replay or repeated live usefulness.
