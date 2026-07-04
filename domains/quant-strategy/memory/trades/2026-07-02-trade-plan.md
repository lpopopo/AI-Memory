# 2026-07-02 Intraday Trade Plan

Run time: 2026-07-02 01:55 Asia/Shanghai / 2026-07-01 13:55 ET, U.S. regular session intraday. Prices are not formal closes. No brokerage login or order submission occurred.

Account basis: confirmed holdings are GLW `2`, DRAM `4`, MXL `6`, MU `1`; TTMI `3` was user-confirmed sold at `187.75`. XLI order/fill state is unknown.

| Priority | Ticker | Direction | Qty | Target amount / NAV | Reference / trigger | Stop / reduction | Invalidation | Reason / risk | State |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 0 | XLI | Cancel or verify | 2 | USD 366 / ~5.7% | Prior limit `183.00`; current `183.86`, low `182.72` | If genuinely filled, completed close `<178` -> exit review | QQQ `-1.15%`, SMH `-5.06%`; market-confirmation gate closed | The old order may have traded through; only broker report can establish a fill | `user/broker confirmation` |
| 0 | GLW | Hold pending close audit | 2 | USD 439.90 / 6.89% | Intraday `219.95`; below raised completed-close protection `227` | 04:15 audit decides formal trigger | A recovery/close at or above the applicable protection line | `-13.89%` event-like fall; do not convert intraday print into formal close exit | `reduce-review intraday` |
| 0 | DRAM | Hold pending broker/close check | 4 | USD 265.52 / 4.16% | Intraday `66.38`; below `70.50` protection | Confirm whether broker stop existed/filled; otherwise 04:15 audit | Broker-confirmed prior exit or completed-close rule review | Second unresolved breach; no averaging down | `exit-review / confirmation needed` |
| 0 | MU | Hold pending broker/close check | 1 | USD 1,042.80 / 16.34% | Intraday `1042.80`; below `1090` hard reference and `1100` close-risk line | Confirm stop state; formal close audit has priority | Broker-confirmed prior exit or close recovery under governing rule | Oversized, high capex-cycle sensitivity, `-9.66%` intraday | `exit-review / confirmation needed` |
| 1 | MXL | Hold, no add | 6 | USD 704.64 / 11.04% | Intraday `117.44`; above `104.30` protection | Completed close `<104.30` -> reduce/exit review | Material recovery does not authorize chasing | Still above stop but correlated sleeve is breaking | `defensive hold` |
| 2 | TTMI | No action | 0 | USD 0 / 0% | Confirmed sold `3 @ 187.75` | Fresh setup required for re-entry | Any stale buy/sell plan | Real stop execution is already complete | `closed` |
| 3 | AMD | No buy | 0 | — | Intraday `549.69`; historical stop breach remains replay context | No real holding | Fresh trend-aligned setup and portfolio capacity | Current AI selloff invalidates chase | `watch only / historical reduce-review` |
| 3 | WDC | No buy | 0 | — | Intraday `596.08` | Historical near-stop line `500` | Trend and storage breadth repair | Storage theme down sharply | `watch only / defensive near-stop review` |
| 3 | STX | No buy | 0 | — | Intraday `917.00` | Historical near-stop line `835` | Trend and storage breadth repair | Storage theme down sharply | `watch only / defensive near-stop review` |
| 3 | MRVL | No buy | 0 | — | Intraday `274.76` | Historical protection context `260` | Confirmed trend repair after event move | Event move has not produced durable trend confirmation; no chase | `watch only` |

No model-portfolio simulated fill was added. Real fills are limited to previously user-confirmed records. All pending actions require user/broker confirmation or the 04:15 completed-close audit.
