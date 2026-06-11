# 2026-06-02 Strategy Todos

Run time: 2026-06-02 23:32 Asia/Shanghai / 11:32 ET.

## Open

### 1. Validate the MRVL event-gap execution overlay

- Problem: stale pullback buy limits are not automatically invalidated after a large headline-driven upward gap.
- Impact: the model can add exposure after accumulation conditions have changed into profit-protection conditions.
- Possible cause: the fear gate is market-wide and existing stock-level rules focus more on downside stops than upward event gaps.
- Repair suggestion: when an existing holding gaps more than `15%` on a fresh headline, cancel stale buys, block same-day additions, and review partial profit-taking or tighter trailing protection.
- Validation method: track MRVL's official 2026-06-02 close, next-session behavior, and retained-position risk; then test the same logic against several future event gaps.
- Next step: keep this as an observation until repeated evidence supports promotion to `decisions.md`.

### 2. Add a post-close daily audit

- Problem: the current night review runs while the U.S. market is still open.
- Impact: close-based stops, final portfolio marks, and end-of-day breadth checks remain unverified.
- Possible cause: the schedule is aligned to Asia/Shanghai evening rather than the U.S. close.
- Repair suggestion: add a post-close audit or move the final review to after `04:15` Asia/Shanghai during U.S. daylight-saving time.
- Validation method: verify that a future final daily record includes official closes, stop checks, final model-account value, and final market-regime notes.
- Next step: discuss the preferred automation schedule.

### 3. Complete close-based checks for AMD, WDC, and STX

- Problem: 2026-06-02 official closes are not available at this run time.
- Impact: daily-close invalidation rules cannot yet be confirmed.
- Possible cause: normal session timing.
- Repair suggestion: perform the checks in the post-close audit.
- Validation method: compare official closes with `AMD <492`, `WDC <500`, and `STX <835`.
- Next step: retain hold-only status until the close audit.

