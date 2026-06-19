# 2026-06-19 Trade Plan

Run time: 2026-06-19 18:55 Asia/Shanghai.

Scope: `automation-3` execution checklist (Revised after manual audit & HKD 50k update). Because the U.S. stock market is **CLOSED** on Friday, June 19, 2026, for the **Juneteenth holiday**, all orders are pending execution for the next regular session on **Monday, June 22, 2026**.

## Data Snapshot

Local quote workflow was run post-close on 2026-06-18, and confirmed as current.

| Item | Result |
| --- | --- |
| Node quote workflow | Usable; returned structured quote objects |
| Equity / ETF source | `Tencent (Primary)` |
| Quote reference | 2026-06-18 close |
| Volatility quality | Cboe VIX `16.40` (Normal, Fear Gate open 100%) |
| Account Baseline | HKD 50,000 (Approx. USD 6,410.26 at 7.80 HKD/USD) |

## Executive Action (Revised)

The market fear gate is **NORMAL** (risk multiplier **100%**).
Following a manual audit and account baseline increase to HKD 50,000 (USD 6,410.26):
1. **RDW Exit:** Selling all 5 shares of RDW at market/limit (yesterday's close reference: $14.35) due to breaching the $14.50 stop line.
2. **TTMI Core Buy:** Buying 3 shares of TTMI (yesterday's close reference: $216.44) as our top fundamental/quant AI PCB infrastructure play, now optimized as a standard ~10.1% core position.
3. **MXL Satellite Buy:** Buying 2 shares of MXL (yesterday's close reference: $88.76) as a standard ~2.8% satellite position.

We will execute three actions on **Monday, June 22**:
- Sell RDW (5 shares)
- Buy TTMI (3 shares)
- Buy MXL (2 shares)

## Execution Checklist

| Priority | Ticker | Direction | Quantity | Target amount | Approx account weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason | Risk point | Status |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | RDW | Sell (Exit) | 5 shares | USD 71.75 gross | ~1.1% | $14.35 | Market open sell to cut loss | Stop triggered below $14.50 | None; mandatory stop | EPS miss and trend breakdown | Realized loss | Executing |
| 2 | TTMI | Buy | 3 shares | USD 649.32 gross | ~10.1% | $216.44 | Pullback to $210-213 or breakout above $220. Do not chase above $225. | Daily close below $188.00 | Daily close below $188.00 | AI Data Center PCB demand surge, V7 Top 3 | High beta | Executing |
| 3 | MXL | Buy | 2 shares | USD 177.52 gross | ~2.8% | $88.76 | Pullback to $85-87 or breakout above $90. Do not chase above $92. | Daily close below $80.00 | Daily close below $80.00 | V6/V7 Top 1; strong PAM4 DSP growth | Volatility | Executing |
| 4 | MRVL | Hold | 1 share | USD 310.58 | ~4.8% | $310.58 | Hold above $315; trailing stop | Review below $285; stop below $280 | Loss of theme support | AI interconnect leader | Fading momentum | Holding |
| 5 | GLW | Hold | 2 shares | USD 389.84 | ~6.1% | $194.92 | Hold; target zone reached (192-198) | Stop review below $186 | Loss of theme support | Optical/fiber starter; working | Profit protection | Holding |

## Real Account Target Positions (Revised)

| Ticker | Shares | Expected Role |
| --- | ---: | --- |
| MRVL | 1 | AI Interconnect Core (Hold) |
| GLW | 2 | Optical/Fiber Core (Hold) |
| TTMI | 3 | AI Infrastructure PCB Core (New Buy) |
| MXL | 2 | AI Silicon/Interconnect Satellite (New Buy) |

Not investment advice.
