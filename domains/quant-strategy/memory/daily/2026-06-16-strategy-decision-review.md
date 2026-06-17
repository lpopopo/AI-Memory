# 2026-06-16 Strategy Decision Review

Scope: intraday process review prompted by user feedback. This is not a broker execution record.

## What Went Wrong

Recent live guidance had three process errors:

- The strategy overcorrected between fear of missing a rebound and fear of being trapped. This produced inconsistent order logic, first suggesting a breakout stop-limit and then switching to a pullback limit without making the invalidated premise explicit.
- The market confirmation gate was not enforced cleanly enough. A participation trade should not be recommended when QQQ is only marginally reclaiming its trigger and SMH remains weak.
- Existing-position risk was underweighted. MRVL was fading from its intraday high and RDW was below its review line, so the next decision should have prioritized current position management before adding a third holding.

## Stable Corrections

- Treat `anti-FOMO` as a small participation sleeve, not as permission to chase. It requires explicit market confirmation.
- If market confirmation fails, new entries must default to support-based limit orders or no trade.
- Every actionable order must name one primary plan, a cancellation rule, and an exit/failure rule.
- Current holdings breaching review lines must be handled before opening an additional position unless the new trade has strong independent confirmation and account risk remains controlled.

## Account Baseline Update

User stated that total deployable real-account capital can increase to HKD 40,000. This changes sizing:

- USD 250-class shares are about 5% of the account and can fit starter orders.
- USD 500-class shares are about 10% and require higher conviction.
- USD 1,000-class shares are about 20% and are generally too large for fresh entries.
- Satellite trades should remain small, usually 2%-4%, because percentage risk can expand quickly.
- User fee drag is material: platform fee is about USD 1 per order, so a buy-and-sell round trip costs about USD 2 before FX/tax/slippage. Future orders must show fee-adjusted breakeven or minimum target, and uneconomic tiny orders should be avoided.
- Under this fee rule, new core trades should generally use at least about USD 200-250 notional. Very small low-priced satellite trades need either enough shares to make the fee drag reasonable or no trade at all.

These rules were added to `decisions.md`.

Not investment advice.
