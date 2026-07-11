# 2026-07-09 Intraday Trade Plan

Run time: 2026-07-09 23:20 Asia/Shanghai. This is an intraday execution checklist, not a post-close audit. No brokerage login was used and no order was submitted by this process.

## Real fills already confirmed

| Symbol | Side | Qty | Fill price | Cost / proceeds | Source | Status |
| --- | --- | ---: | ---: | ---: | --- | --- |
| QCOM | Buy | 2 | 187.50 | gross cost 375.00; estimated entry cost 376.00 with USD 1 platform fee | user confirmation | real holding recorded |

QCOM role: small edge-inference / diversified semiconductor position. It is not a V9-authorized information trade and it does not reopen new-buy capacity while GLW/DRAM/MXL/MRVL stop items remain unresolved. Round-trip breakeven is about `188.50` before FX/tax/slippage. Review below `185`; a completed regular-session close below `182` is a failed-entry exit/reduce-review.

## Pending real-account execution checklist

| Action | Symbol | Direction / qty | Reference price | Trigger condition | Stop / reduce line | Invalid if | Strategy reason | Risk point | Status |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| Sell/reduce | GLW | sell/reduce 2 if still held | 197.26 | broker confirms position remains open | completed-close trailing stop 227 already breached | broker/user confirms already sold | completed-close stop discipline | rebound may be mistaken as new signal | waiting user confirmation |
| Sell/exit | DRAM | sell 4 if still held | 65.11 | broker confirms position remains open | hard protection 70.50 already breached | broker/user confirms already sold | hard protection failed | memory rebound can reverse | waiting user confirmation |
| Sell/reduce | MXL | reduce/exit 6 if still held | 95.88 | broker confirms position remains open | 113.38 trailing line breached; 91-92 core context | broker/user confirms already sold or provides rule-consistent override | stop discipline and concentration control | high beta rebound / liquidity risk | waiting user confirmation |
| Sell/reduce | MRVL | reduce/exit 4 if still held | 247.84 | broker confirms position remains open | close-failure line 260 already breached | broker/user confirms already sold or provides rule-consistent override | failed entry and correlated AI-capex risk | catalyst optimism without price repair | waiting user confirmation |
| Hold/watch | QCOM | hold 2, no add | 195.09 | already held after user-confirmed fill | review below 185; completed close below 182 | user reports sale | small diversified semiconductor exposure | still correlated with AI/semis | active real holding |
| Cancel/verify | XLI | cancel if any old order remains open | n/a | broker shows order open | n/a | broker confirms never placed/cancelled/expired | prevent accidental buy under zero-new-buy veto | unknown order state | waiting user confirmation |

## Not authorized today

- No additional buys in AI-capex, semiconductor, memory/storage, optical/interconnect, equipment, or edge-inference names.
- No averaging down in stopped positions.
- No model or shadow fill is recorded as real.
- V9 shadow status: not authorized. Candidates fail account veto, theme cap, chase filter, and/or completed two-session confirmation.
