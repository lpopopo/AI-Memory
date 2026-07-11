# V9 Phase 4 Shadow Portfolio Engineering Audit

Date: 2026-07-05 Asia/Shanghai.

## Outcome

The shadow architecture is now suitable for engineering dry-runs, but formal forward tracking is intentionally blocked until the working tree is committed and a clean freeze is generated.

## Material corrections

- Shadow stepping now evaluates exactly one requested completed session instead of traversing the full history on every daily run.
- Previous sleeve valuations, turnover, position stops, trim state and event identities are serialized and restored across sessions.
- Unsafe `eval` state-key decoding was replaced by JSON decoding with `ast.literal_eval` only for backward-compatible dry-run files.
- Rule-E information orders no longer require an impossible 1.5-share minimum in a normalized-NAV account; the minimum is now 0.5% NAV.
- Event IDs now flow through pending orders, positions and the execution ledger.
- Code/config/market/event/execution/decision hashes feed an append-only state-hash chain.
- Forward events use an append-only JSONL hash chain. New IDs are permitted; duplicate or modified baseline IDs trigger a tamper alarm.
- Dry-runs are namespaced by frozen code hash, preventing a new engineering freeze from overwriting an older dry-run.
- Open executions and close decisions are frozen separately per account and session.
- A lifecycle exporter reports only metrics completed by the requested `as_of` date.

## Verification

- 23 V9/shadow tests pass.
- Continuous execution equals daily serialize/reload execution across the fixed historical fixture.
- Same-day reruns are idempotent.
- Duplicate historical event IDs and changed frozen artifacts trigger alarms.
- Formal forward mode correctly refuses to start from a dirty engineering freeze.
- Historical dry-run `826f23bb2d07` advanced session by session from 2026-06-18 through 2026-07-02 across four isolated accounts.

## Dry-run diagnostic

As of 2026-07-02, V9-A and V9-E both had NAV `0.98336635`, zero information PnL and no information executions. The V9-E lifecycle contained 35 rejected event-symbol records. This is an engineering diagnostic only and is excluded from forward evidence.

## Forward launch gate

1. Review and commit the intended Rule-E and shadow-engine files.
2. Confirm the worktree is clean.
3. Generate a new freeze without `--replace`.
4. Initialize forward accounts on the first completed session after that freeze.
5. Append new events to `forward/shared/event_append_log.jsonl`; never edit the baseline snapshot.
6. Evaluate only after at least three months and ten completed independent information trades.
