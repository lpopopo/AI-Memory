# 2026-06-17 Strong Trend Participation Review

Scope: strategy process correction prompted by the WDC missed-rally review. This is not a broker instruction.

## Problem

The strategy correctly identified the AI storage theme, but repeatedly treated WDC as watch-only because it was expensive per share and extended above daily moving averages. This was incomplete: WDC was a clear relative-strength leader in a strong theme, and the HKD 40,000 account could theoretically support a one-share trend participation order with predefined risk.

## What Was Wrong

- Too much emphasis on pullback-only entry for a trend leader.
- Too much emphasis on single-share notional as a hard rejection.
- Daily K-line extension was used as a veto instead of a sizing and stop-control input.
- The report did not give a concrete trigger, such as breakout participation, pullback participation, or explicit no-trade reason.

## Stable Correction

Add a strong-trend participation module:

- If a watchlist stock is a clear theme leader and repeatedly outperforming, classify it as `trend participation candidate`.
- If one share fits account risk, provide a controlled one-share plan: breakout stop-limit, pullback limit, or no-trade with precise invalidation.
- If the stock is extended, reduce size and tighten risk rather than defaulting to watch-only.
- For HKD 40,000, USD 600-750 stocks can be considered for one-share participation if stop risk is controlled. USD 1,000-class names remain generally too large unless user explicitly approves concentration.

## Current Example

- WDC should have been presented earlier as a one-share trend participation candidate, not only as watch-only.
- STX/MU/SNDK remain more difficult because single-share exposure is around or above 20% of the account.
- ALAB/AVGO can be reviewed as smaller strong-trend participation candidates when theme confirmation is present.

Updated `decisions.md`.

Not investment advice.
