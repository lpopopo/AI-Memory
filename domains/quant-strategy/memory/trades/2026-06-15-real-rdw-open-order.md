# 2026-06-15 Real RDW Open Order

Scope: real account ledger, based only on user-confirmed broker action.

## User-Confirmed Open Order

| Date | Account scope | Ticker | Action | Shares | Limit price | Max notional | Source |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| 2026-06-15 Asia/Shanghai | Real account, HKD 20,000 baseline | RDW | Buy limit | 5 | USD 15.00 | USD 75.00 | User confirmation |

Status: filled, per user confirmation. See `2026-06-15-real-rdw-fill.md`.

## Order Classification

This is a satellite pullback limit order.

Technical basis:

- Latest structured quote before order: RDW around USD 15.42.
- Intraday low around USD 15.30.
- Limit USD 15.00 is below the intraday low and near a round-number support zone.

## Fee / Cost Estimate

User fee rule: minimum platform fee is USD 1 per trade.

If fully filled:

- Gross notional: USD 75.00.
- Buy-side platform fee estimate: USD 1.00.
- Entry cash cost: USD 76.00.
- Effective cost per share after buy fee: USD 15.20.
- If sell-side platform fee is also USD 1.00, round-trip breakeven is roughly USD 15.40.

Approximate HKD exposure before FX spread:

- Around HKD 585-595 total entry cash cost.
- About 3% of HKD 20,000 baseline.

## Risk Plan If Filled

- Do not add more RDW today.
- If filled and RDW closes below USD 14.50, exit / stop-review.
- If filled and RDW reclaims USD 16.00+, hold and reassess.
- If RDW spikes to USD 17.00+ quickly, consider profit protection because this is a satellite, not a core holding.
- Keep MRVL as the only core AI-infrastructure real holding; RDW is high-volatility satellite exposure only.

## Current Real Account State

Confirmed active real equity holding:

| Ticker | Shares | Cost |
| --- | ---: | ---: |
| MRVL | 1 | USD 289.50 |

Open real order:

| Ticker | Shares | Limit |
| --- | ---: | ---: |
| RDW | 5 | USD 15.00 |
