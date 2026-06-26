# 2026-06-24 Strategy Todos

Run time: 2026-06-25 09:00 Asia/Shanghai.

## Open

### 1. Reconcile broker cash, NAV and open orders

- Working cash is `USD 5,376.56`; exact cash, FX, fees, taxes, settlement and open orders remain unverified.
- Compare the broker statement with `memory/portfolio/2026-06-24-portfolio-summary.md`.
- Cancel stale buy orders if any; do not infer cancellation without user/broker confirmation.

### 2. GLW profit-protection near-stop review

- Formal close `205.83` is only 0.40% above the `205` protection line.
- Hold/no add. A completed close below `205` moves to reduce-review; `200/195` are serious-risk bands and `180-181` remains the hard stop-review zone.

### 3. TTMI near-stop review

- Formal close `209.74` triggered the `210` warning and is below the `213` gross cost.
- Hold/no add. Loss of `205` moves to reduce-review; completed close below `188` moves to exit-review.

### 4. Portfolio correlation gate

- GLW and TTMI are one effective AI infrastructure/interconnect theme.
- Keep new MRVL/CRDO/ALAB/MXL/WDC/STX/DRAM and other correlated-theme exposure at `0%` until flow fragility and trend alignment improve.

### 5. Daily strategy artifact naming gap

- No separate dated `2026-06-24-us-stock-*strategy*.md` artifact was found.
- Keep the next open-prep output consistently named so formal audit can trace recommendation -> checklist -> intraday review -> close result.

## Completed / verified

- MRVL stop-loss execution confirmed: sold 1 share at USD 272.30.
- Node quote workflow returned structured Tencent objects; Yahoo daily bars and Cboe official VIX/VIX3M closes completed the audit.
- Formal fear gate computed at `normal 3/14`.
- 2026-06-24 replay close row added.

Not investment advice.
