# Current Strategy

## Production baseline

The only promoted return engine is **V8 Defensive Core**:

- Base allocation: 50% SPY / 50% QQQ.
- Each ETF receives half of its base weight above MA150 and half above MA200.
- Unallocated weight remains in cash.
- Review monthly; leverage is prohibited.

Generate the current completed-bar V8 signal with:

```powershell
..\..\.venv\Scripts\python.exe scripts\v8_signal.py --version v8 --json
```

## Forward research strategy

**V9 Rule E** is frozen for forward shadow testing. It is not yet a promoted
return engine and must not replace V8. The official runner maintains four
isolated accounts: V8, V9-A, V9-E, and passive SPY/QQQ 50/50.

Run the next completed US trading session only after its closing data is final:

```powershell
..\..\.venv\Scripts\python.exe scripts\run_v9_shadow.py --as-of YYYY-MM-DD
```

Rules:

- Never backfill or overwrite an official forward state.
- Never edit a historical event; append newly observed events with real timestamps.
- Never skip a completed trading session in the state chain.
- Do not refreeze after forward tracking starts. A code change requires a new version and genesis.
- V9 orders are next-session orders; a signal cannot execute on its discovery close.

## Real-account boundary

V8 remains the decision baseline. V9 is observation-only until it has at least
20 forward sessions and 5 independent entries with valid integrity, execution,
and attribution records. Existing broker positions, cash, stops, and pending
orders must be reconciled before any new real-account exposure is considered.
