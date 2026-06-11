# 2026-06-03 Strategy Todos

Run time: 2026-06-03 23:33 Asia/Shanghai / 11:33 ET.

## Open

### 1. Validate a two-day vertical-extension profit-protection rule

- Problem: MRVL moved from a first headline gap into a second strong continuation day, but the strategy only has an informal second-tranche profit-protection plan.
- Impact: retained gains can be exposed to a sharp crowding reversal, while overly aggressive selling can reduce upside capture.
- Possible cause: current market fear and stop-loss rules are stronger on downside protection than on upside event-crowding management.
- Repair suggestion: when an existing holding rises sharply for two consecutive catalyst sessions and reaches a predefined profit-protection zone, block new buys, allow small staged trims, and convert remaining shares to close-based trailing protection.
- Validation method: track MRVL over the next 1-5 trading days, including close, next-day gap, intraday drawdown, and retained-position return. Compare with future event-gap cases before promotion to `decisions.md`.
- Next step: continue observation; do not promote to stable rule yet.

### 2. Add or schedule a post-close daily audit

- Problem: the 2026-06-03 review ran at 23:33 Asia/Shanghai / 11:33 ET, before the U.S. close.
- Impact: official closes, close-based stops, final market breadth, and final model-account value are still unverified.
- Possible cause: automation timing is aligned to China evening rather than after the U.S. session.
- Repair suggestion: add a post-close audit or move the formal final review to after `04:15` Asia/Shanghai during U.S. daylight-saving time.
- Validation method: confirm the next final daily detail file includes official closes for MRVL, AMD, WDC, STX, index/fear checks, stop checks, and final model portfolio value.
- Next step: ask user to choose whether to split the automation or move the final review time.

### 3. Confirm MRVL real-account execution status

- Problem: the strategy plan authorizes a `2.50` share MRVL limit sell at `>=315`, but no broker/user fill confirmation exists.
- Impact: memory can only maintain a model plan, not an actual execution ledger.
- Possible cause: real brokerage data is intentionally unavailable and should not be written into memory unless the user reports non-sensitive execution facts.
- Repair suggestion: keep real-account action separate from model tracking; only mark a real trade when the user confirms ticker, direction, quantity, and price without credentials or sensitive account details.
- Validation method: compare future portfolio records against explicitly confirmed fills only.
- Next step: user should confirm whether MRVL was submitted or filled, if they want memory to track it.
