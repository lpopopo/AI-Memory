# 2026-07-03 正式休市组合摘要

Formal audit run time: 2026-07-04 05:57 Asia/Shanghai. NYSE and Nasdaq were closed on 2026-07-03; values formally carry the latest completed 2026-07-02 close. This is an estimated ledger, not broker truth. See `memory/daily/2026-07-03-post-close-audit.md`.

Assumptions: GLW `2`, DRAM `4`, MXL `6`, MU `1`, and the user-confirmed MRVL `4 @ 263.80` remain open because no later broker fills were supplied. Working cash is `USD 2,875.69` (`3,930.89 - 1,055.20`), excluding fees/FX. XLI is excluded because its order state is unknown.

| Holding | Price | Market value | NAV weight | Classification |
| --- | ---: | ---: | ---: | --- |
| GLW 2 | 196.79 | 393.58 | 6.53% | `exit-review`; prior stop unresolved |
| DRAM 4 | 60.63 | 242.52 | 4.02% | `exit-review`; hard protection unresolved |
| MXL 6 | 93.12 | 558.72 | 9.27% | `exit-review`; trailing stop unresolved |
| MU 1 | 975.56 | 975.56 | 16.19% | `exit-review`; risk line unresolved |
| MRVL 4 | 245.29 | 981.16 | 16.28% | `exit-review`; latest close below 260 failure rule |

- Estimated equity value: `USD 3,151.54`.
- Estimated NAV: `USD 6,027.23`.
- Working cash: `USD 2,875.69 / 47.71%`.
- Equity exposure: `USD 3,151.54 / 52.29%`.
- Holdings: `5`; effective broad themes: `1` (AI capex).
- Largest position: MRVL `16.28%`, followed by MU `16.19%`.
- Entire equity sleeve is correlated and all five holdings are exit/reduce items under existing or newly reached completed-close lines.

If all five pending exits are confirmed, equity exposure becomes approximately `0%` before fees/slippage and cash becomes the full account balance; this is a scenario, not a recorded transaction. Exact cash, NAV, fees, FX, settlement and XLI state must come from the user/broker.
