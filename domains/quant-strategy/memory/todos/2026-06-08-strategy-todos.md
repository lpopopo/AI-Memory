# 2026-06-08 Strategy Todos

Run time: 2026-06-08 22:25 Asia/Shanghai.

## Open

### 1. Add a mandatory U.S. post-close audit

- Problem: the 2026-06-04 review ran during the U.S. session and no 2026-06-05 post-close audit was recorded.
- Impact: AMD's close below the `492` stop line and the portfolio's roughly `-4.99%` model drawdown were only detected on 2026-06-08.
- Possible cause: automation timing is aligned to China evening rather than U.S. post-close.
- Repair suggestion: add a second post-close audit after about `04:15` Asia/Shanghai during U.S. daylight-saving time, or move the formal daily review to post-close.
- Validation method: each formal daily detail should include official close prices, stop-trigger table, market fear state, and model portfolio value.
- Next step: decide whether to split the automation into intraday review plus post-close audit.

2026-06-08 23:33 addendum:

- Same-day intraday snapshots showed a rebound, but they do not resolve the audit gap.
- Add an explicit rule to the audit workflow: intraday data may update watch priority only; it must not downgrade fear state, mark stop rules repaired, or authorize new buys without official close data.

### 2. Handle AMD close-stop trigger

- Problem: AMD closed at `466.38` on 2026-06-05, below the existing daily close stop of `492`.
- Impact: AMD should no longer be treated as ordinary hold-only without a rule review or model reduction.
- Possible cause: 6 月 5 日盘后审计缺失，导致触发延迟记录。
- Repair suggestion: before the next regular-session plan, mark AMD as stop-triggered and decide whether the model should reduce at next executable window or require a close back above `492`.
- Validation method: check the next regular-session close; if AMD cannot reclaim `492`, model rules should record a reduction or an explicit rule override.
- Next step: include AMD in the next execution checklist as first-priority risk item.

2026-06-08 23:33 addendum:

- AMD was observed around `493.50` intraday, temporarily above the `492` line.
- This does not close the todo. Next formal check must classify the 2026-06-08 official close as either: still stop-triggered (`<492`) or delayed-trigger override (`>=492`, with documented reason).

### 3. Reclassify WDC/STX from strong hold to defensive hold

- Problem: WDC closed at `511.72` versus stop `500`; STX closed at `847.47` versus stop `835`.
- Impact: both storage holdings are close to hard risk lines after a synchronized theme selloff.
- Possible cause: original rules lacked a near-stop warning state.
- Repair suggestion: add a temporary watch state: within roughly `3%-5%` of stop after same-theme selloff, no adds, no complacent hold label, and require next-close confirmation.
- Validation method: track whether WDC holds `500`, STX holds `835`, and whether storage relative strength recovers versus SMH over 1-3 sessions.
- Next step: do not promote this to `decisions.md` until validated.

2026-06-08 23:33 addendum:

- WDC `529.13` and STX `886.84` intraday prices were above their risk lines, so immediate near-stop pressure eased.
- Keep both as defensive hold until at least 1-3 official closes confirm storage relative strength versus SMH; do not restore strong-hold language from one intraday rebound.

### 4. Validate a theme-crowding risk overlay

- Problem: VIX jumped to `21.51`, QQQ fell sharply, and AI/semiconductor names sold off together after strong-news/weak-price behavior.
- Impact: the model protected MRVL partly but did not reduce correlated AI/storage exposure quickly enough.
- Possible cause: current fear gate handles broad panic and single-stock stops, but not same-theme crowded unwinds.
- Repair suggestion: test a rule where VIX `>20` plus QQQ/SMH sharp drop blocks all new buys and forces review of every correlated holding against stop/near-stop thresholds.
- Validation method: compare 2026-06-05 through the next 5 trading days under current rules versus the proposed overlay. Use `references/institutional-overlay-replay-protocol.md` and `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv`.
- Next step: append completed close rows to the replay ledger as data becomes available; keep as todo/hypothesis and do not add to stable decisions yet.

### 5. Repair live quote refresh workflow

- Problem: prior local quote refresh failed; today's review relied on public web snapshots and search results rather than a repeatable local quote path.
- Impact: daily audit remains slower and less reproducible.
- Possible cause: local network restrictions or source availability.
- Repair suggestion: implement a fallback hierarchy: local quote script, then browser/public snapshot, then manually supplied close table with timestamp and source.
- Validation method: next audit should cite one repeatable source path for every active ticker and index proxy.
- Next step: test fallback quote workflow before the next formal review.

2026-06-08 23:33 addendum:

- Browser/public pages worked as a fallback for `MRVL`, `AMD`, `WDC`, `STX`, `SPY`, `QQQ`, and `SMH`, but VIX/VIX3M, HYG/LQD, and breadth proxies remain incomplete.
- Next validation should separate three labels: official close, intraday public snapshot, and unavailable proxy.
