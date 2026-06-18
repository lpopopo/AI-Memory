# 2026-06-18 Trade Plan

Run time: 2026-06-18 23:18 Asia/Shanghai.

Scope: `automation-3` intraday execution checklist. This is not broker login, not order submission, not a real execution record, and not the formal 04:15 post-close audit.

## Data Snapshot

Local quote workflow was run first per `tools/README.md`.

| Item | Result |
| --- | --- |
| Node quote workflow | Usable; returned structured quote objects |
| Equity / ETF source | `Tencent (Primary)` |
| Quote time | 2026-06-18 23:16 Asia/Shanghai |
| Daily K-line source | Yahoo chart daily, 125 bars for most tickers; `DRAM` 54 bars |
| Volatility quality | Local Tencent `VIX` remains low quality with zero OHLC; Yahoo chart showed intraday `^VIX` about `17.06` and `^VIX3M` about `19.86` |
| Session context | U.S. intraday; do not treat prices as official close triggers |

## Executive Action

Market remains `elevated / repair risk-on`: QQQ and SMH are strong intraday, but flow fragility is still elevated because AI / semiconductor / memory leadership is crowded and RDW remains below its stop-review line. The real account already added GLW today, so new buys are blocked for this run unless the user explicitly overrides after broker cash and open orders are synchronized.

## Execution Checklist

| Priority | Ticker | Direction | Quantity | Target amount | Approx account weight | Reference price | Trigger condition | Stop / reduce line | Invalid condition | Strategy reason | Risk point | Status |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | RDW | Sell / reduce review | up to 5 shares | about USD 69 gross at `13.81` | about `2.7%` of old HKD 20k baseline; `1.3%` of HKD 40k | `13.81` intraday | User confirms exit/reduce after continued failure below `14.50`; do not average down | Stop-review remains below `14.50`; reclaim `16.00` improves hold | If user explicitly chooses manual defensive hold until 04:15 formal close audit | Stop discipline and weak daily trend: below 5/10/20D and still under review line | High-vol satellite; sell-side fee may be material vs small notional | Waiting user confirmation; no broker order submitted |
| 2 | MRVL | Hold / profit-protection review | 1 share | about USD 325 market value | about `12.7%` old baseline; `6.3%` forward HKD 40k | `324.66` intraday | Hold while above `315` and SMH/QQQ stay strong; review profit protection if it rejects `324-326` | Review below `285`; reduce/exit review below `280` close | If it loses `315` intraday with SMH fading, move to profit-protection discussion | Event/AI interconnect strength repaired the prior risk line and reached the old profit-protection zone | Sharp intraday event rally; no chase/add allowed | Core hold / profit-protection review |
| 3 | GLW | Hold | 2 shares | about USD 369 market value | about `14.4%` old baseline; `7.2%` forward HKD 40k | `184.62` intraday | Hold while support-test entry stays above `181-182.50` breakeven area | Caution below `181`; stop/exit review below `180` without quick reclaim | If it loses `180` or QQQ/SMH/optical theme reverses sharply | New support-test starter in optical / fiber / AI infrastructure; now above round-trip breakeven | Same-day fill; do not add again | Core hold / support-test starter |
| 4 | WDC | Observe; conditional participation only if user overrides | 0 | one share would be about USD 772 | about `30%` old baseline; `15%` forward HKD 40k | `771.74` intraday | Only if user confirms cash and accepts concentration: breakout above `800` or pullback/reclaim near `763-780` with SMH/QQQ confirmation | No chase if below opening range; stop would need user-defined max loss | Invalid if SMH fades or WDC loses `763` support zone | Memory/storage leader and trend participation candidate | Too extended vs 20D `566`; high single-share concentration | Watch only; no order |
| 5 | AMD | Hold no position / observe | 0 | none | none | `537.34` intraday | Recheck only after clean support or breakout setup; old `492` close stop is repaired | If future completed close below `492`, return to reduce-review in replay context | Invalid as real buy while existing real risk is unresolved | AI compute strength, but not current real holding | High-beta AI capex exposure overlaps MRVL/GLW | Watch only |
| 6 | STX | Observe | 0 | none | none | `1085.80` intraday | Recheck after base or pullback; no USD 1,000-class single-share entry without explicit approval | Old replay risk `835` is far below, but not a real holding | Invalid due to size and extension | Storage leader | Too large per share and extended vs 20D `910` | Watch only |
| 7 | DRAM | Observe | 0 | none | none | `77.32` intraday | Use as memory/storage ETF read-through only; no same-day buy | Needs ETF liquidity/spread/holdings review | Invalid if used as substitute for due diligence | Basket proxy for memory/storage theme | New ETF, limited history | Watch only |
| 8 | SMCI / INTC / QCOM / RKLB / ORCL / NOK / TSLA | Observe | 0 | none | none | see daily detail | Require separate trend-aligned entry and account fit | Ticker-specific risk lines not active as real holdings | Invalid if based only on headline/theme strength | Watchlist expansion and theme temperature | Crowding, governance, turnaround, or high volatility risks | Watch only |

## Real vs Pending vs Model

| Category | Items |
| --- | --- |
| Confirmed real fills | MRVL `1 @ 289.50`; RDW `5 @ 15.00`; GLW `2 @ 181.50` |
| Waiting user confirmation | RDW sell/reduce vs manual defensive hold; MRVL profit-protection if the event rally rejects; broker cash / fees / FX / stale orders |
| Model / replay trades | None added in this run |
| Broker actions | None; no login and no submitted order |

## Six-Dimensional Read

| Dimension | Current read | Impact |
| --- | --- | --- |
| Market sentiment | SPY +0.96%, QQQ +2.17%, SMH +5.48%; Yahoo `^VIX` about `17.06` | Repair/risk-on, but still `elevated` rather than normal |
| Theme strength | Semiconductors, memory/storage, AI infrastructure and GLW optical/fiber are strong; space is mixed | Helps MRVL/GLW; does not repair RDW |
| Stock relative strength | MRVL +12.13%, GLW +5.25%, WDC +8.37%, RDW -3.83% | RDW is the weak real holding; MRVL/GLW working intraday |
| Technical entry quality | GLW fill near day-low support worked; WDC/MRVL are extended; RDW below 5/10/20D | Hold winners, avoid fresh chase, review RDW |
| Account constraints | Broker cash / FX / open orders still unverified; old HKD 20k exposure now about 30% | No new buy until sync |
| Exit / risk plan | RDW below `14.50` review; MRVL profit-protection near `324`; GLW stop review below `180` | Risk actions before watchlist expansion |

Not investment advice.
