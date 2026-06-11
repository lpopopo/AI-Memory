# 2026-06-10 Real Position Start

Purpose: start tracking the user's real portfolio separately from the prior strategy-tracking model portfolio.

Important distinction:

- Prior MRVL / AMD / WDC / STX portfolio records were strategy simulations unless explicitly confirmed by the user.
- This file starts the real-position ledger from the user's confirmed broker fill.
- Currency base: HKD 20,000 real account capital.

## Confirmed Real Fill

User confirmed:

| Date | Ticker | Action | Shares | Fill price | Notional |
| --- | --- | --- | ---: | ---: | ---: |
| 2026-06-10 Asia/Shanghai | MRVL | Buy | 1 | USD 252.00 | USD 252.00 |

Approximate HKD notional:

- Using USD/HKD near the HKD peg area, USD 252 is roughly HKD 1,960-1,970 before fees and FX spread.
- Approximate account weight: about 9.8% of HKD 20,000.

## Latest Reference Quote

Latest refreshed quote during this session:

- MRVL: about USD 261.09.
- QQQ: about -1.83% intraday.
- SMH: about -2.93% intraday.

Approximate position status at USD 261.09:

- Unrealized P/L: about USD +9.09.
- Return on position: about +3.61%.
- Approximate HKD P/L: about HKD +70 before fees and FX spread.

## Risk Controls

This is a starter position, not a full allocation.

- Do not use margin / financing for the position.
- No same-day add unless SMH and QQQ stop making new intraday lows.
- If MRVL closes below USD 245, review whether to cut or wait.
- If MRVL falls toward USD 235 with broad semiconductor weakness, treat the starter thesis as failed and exit/reassess.
- If MRVL reclaims USD 275-280 with SMH recovering, consider holding rather than adding immediately; the account is small and should avoid overconcentration.

## Next Candidate Rules

- WDC remains the next possible candidate only if it holds above roughly USD 500 and the user has enough non-margin USD cash.
- AMD remains watch-only until it regains the USD 492-500 area.
- MU / SNDK / STX remain watch-only for the real HKD 20,000 account because single-share position sizing is difficult and volatility is high.

## Strategy Reflection

The real account has now started with a small MRVL starter position. This aligns with the revised plan after semiconductor weakness: begin with a small, cash-funded test position rather than using the prior USD 20,000 model allocation.
