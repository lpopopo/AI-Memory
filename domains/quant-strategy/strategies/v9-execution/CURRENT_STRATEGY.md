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
- Review monthly; next-session execution, transaction costs and no leverage
  apply.
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
..\..\.venv\Scripts\python.exe scripts\run_v9_daily_execution.py
..\..\.venv\Scripts\python.exe scripts\run_v9_shadow.py --as-of YYYY-MM-DD
```

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

## Evidence boundary

The V9 promotion is user-directed strategy governance, not a claim that its
short historical sample has proved information alpha. The archive currently
has only 18 reliable point-in-time events, so V9 performance, source quality
and V9.1 upgrades continue to be measured prospectively and reported without
claiming a statistically established return premium.
