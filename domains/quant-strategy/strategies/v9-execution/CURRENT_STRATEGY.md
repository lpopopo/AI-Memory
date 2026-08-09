# Current Strategy

## Unified portfolio manager — V9

**V9 Rule E** is the promoted long-term portfolio framework. It manages one
portfolio through an embedded V8 index-core module, a V9 individual-stock
module and a unified cash reserve.

| Component | Portfolio ceiling | Rule |
| --- | ---: | --- |
| SPY/QQQ index core | 70% | V8 MA150/MA200 long-term trend allocation |
| Individual stocks | 30% | V9 Rule E information, technical and risk process |
| Cash | residual | retained whenever either module lacks authorization |

### Embedded V8 index core

- The index core is not a separate strategy or account.
- Within its 70% ceiling, SPY and QQQ each receive half of the core budget
  above MA150 and another half above MA200.
- Unallocated index-core weight stays as V9 cash.
- Review monthly; execute core target changes at the next session close, pay
  transaction costs and never use leverage. Between reviews, weights drift.
- Daily/post-close market context for this module follows
  `references/v9-index-core-momentum-monitor.md`: MA150/MA200 remain the only
  formal index weights; QQQ stress amplification (~1.3x) is a risk caution;
  absolute/relative mom63 continuation is monitor-only and not trade
  authorization.

The index-core allocation is generated inside the V9 completed-bar output; it
has no standalone execution command.

### V9 individual-stock sleeve

- The stock sleeve has a 30% portfolio ceiling and does not force investment.
- Every stock action must pass V9 information, technical, sizing,
  common-factor and stop checks.
- A recommendation must state evidence, technical trigger, entry zone,
  invalidation/stop, size, theme exposure and next review condition.
- V9.1, V9.1.1 and dynamic-stop variants remain separately labelled research
  upgrades until their own forward evidence supports adoption.

Run the next completed U.S. trading session only after closing data is final:

```powershell
..\..\.venv\Scripts\python.exe scripts\preflight_formal_forward.py YYYY-MM-DD
..\..\.venv\Scripts\python.exe scripts\download_v9_data.py --completed-through YYYY-MM-DD
..\..\.venv\Scripts\python.exe scripts\run_v9_daily_execution.py
..\..\.venv\Scripts\python.exe scripts\run_v9_shadow.py --as-of YYYY-MM-DD
```

The refresh is fail-closed: all required market proxies must reach the declared
completed session before any cache is replaced. VIX and VIX3M OHLC history is
overridden by Cboe's official daily index files, with the prior quote-source
status retained in metadata for audit.

For a manual real-account reconciliation, copy
`validation/account-state-template.json`, fill it from the broker snapshot and
run:

```powershell
..\..\.venv\Scripts\python.exe scripts\run_v9_daily_execution.py --account-state PATH_TO_ACCOUNT_JSON
```

The frozen model decision and broker observations use two separate append-only
chains. Re-running after an order changes from `open` to `filled` appends a new
account audit; it does not rewrite the market decision. The runner only emits
proposals and audit classifications. Broker submission is always disabled.

For the first formal forward day checklist, event-append template and PIT gap
rules, see `validation/formal-forward-monday-runbook.md`,
`validation/event-append-template.json` and `validation/pit-event-gap-analysis.md`.
Append newly observed events with `scripts/append_shadow_event.py --forward`
(never edit the frozen baseline snapshot).

Rules:

- Never backfill or overwrite an official forward state.
- Never edit a historical event; append newly observed events with real timestamps.
- Never skip a completed trading session in the state chain.
- Do not refreeze after forward tracking starts. A code change requires a new version and genesis.
- V9 orders are next-session orders; a signal cannot execute on its discovery close.

## Recommendation and real-account boundary

V9 owns every portfolio decision. A real-account action is never automatic: it
requires a completed-bar V9 authorization, human review and reconciled broker
state. Existing broker positions, cash, stops and pending orders must be
reconciled before any new exposure is considered.

## Fear Gate allocation priority

The portfolio uses `core_priority` when the Market Fear Gate requires cash.
Execution and research diagnostics call the same canonical completed-close
Fear Gate implementation. A regression test requires identical scores,
regimes, cash floors and per-signal points; research diagnostics remain
read-only and cannot authorize a trade.
The index core keeps priority because its MA150/MA200 evidence is stronger;
the unproven stock sleeve yields risk budget first. The effective ceilings are:

| Fear regime | Index core | New/target stock sleeve | Cash floor |
| --- | ---: | ---: | ---: |
| normal | 70% | 25% | 5% |
| elevated | 70% | 5% | 25% |
| stress | 55% | 0% | 45% |
| panic | 35% | 0% | 65% |

Core Fear Gate resizing occurs at month-end. A `VIX >= 35` panic may cut the
core immediately and the lower budget stays latched until the next month-end.
Daily stock entries still use the current Fear Gate and its size multiplier.
Existing real-account sleeve overages are not automatic sell orders: they must
be identified by broker reconciliation and resolved by an explicit human plan.

## Action accountability

Every account audit classifies actions as `executed_required_action`,
`required_action_open`, `required_action_pending`, `missed_required_action`,
`blocked_signal`, `correct_skip`, or `unmapped_broker_order_review`. A required
action is called missed only after its execution date is due and no confirmed
fill or still-open matching order exists. Price appreciation without a prior
required action is never retroactively labelled a miss.

## Evidence boundary

The V9 promotion is user-directed strategy governance, not a claim that its
short historical sample has proved information alpha. The archive currently
has only 18 reliable point-in-time events, so V9 performance, source quality
and V9.1 upgrades continue to be measured prospectively and reported without
claiming a statistically established return premium.

`source_health=partial` remains fail-closed for new information-driven entries.
Price-data availability cannot restore information-source health. Recovery must
follow `validation/source-health-recovery-contract.md`, preserve the historical
partial interval and provide current timestamped coverage evidence.
