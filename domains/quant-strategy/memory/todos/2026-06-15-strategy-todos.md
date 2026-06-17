# 2026-06-15 Strategy Todos

Created during the 2026-06-15 formal U.S. post-close audit.

## Broker / Account Reconciliation

- Confirm real account cash after MRVL and RDW fills.
- Confirm exact buy-side fees, FX spread, tax, and settlement treatment for MRVL and RDW.
- Check whether any stale MRVL, RDW, RKLB, ORCL, AMD, WDC, or STX broker-side orders remain open.

## Position Monitoring

- RDW: next completed close below `14.50` should trigger exit / stop-review; no averaging down before that review.
- MRVL: hold starter while above downside review lines, but review profit protection if it reaches or sustains `315+`.
- AMD/WDC/STX: keep as replay/watch context only; no real-account chase after the 2026-06-15 vertical repair.

## Data / Process

- Keep using local Node quote workflow first for equities/ETFs.
- Continue treating local Tencent VIX with zero OHLC/volume as low quality; use external Cboe/MarketWatch/Google visible volatility snapshots when needed.
- Do not promote single-day replay or crowding warnings into `decisions.md`.
