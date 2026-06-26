# 2026-05-29 Realtime Validation and Order Plan

Purpose: Re-validate the current US stock recommendation with latest available intraday quotes and convert the recommendation into staged limit-order guidance for a hypothetical USD 20,000 account.

Important note: This is a research plan, not guaranteed return or personalized financial advice. Quotes may be delayed. If there are existing holdings, the order plan must be adjusted.

## Market Check

Latest available intraday quote time: around 2026-05-29 15:18 UTC.

- SPY: 757.16, +0.34% intraday.
- QQQ: 738.52, +0.40% intraday.
- SMH: 601.59, +0.29% intraday.

Market regime remains risk-on. Semiconductor leadership is intact, but SMH pulled back from its intraday high, so use limit orders instead of market orders.

Market fear gate:

- Latest computed regime: `normal`.
- Fear score: `0`.
- VIX: about `15.53`.
- Risk multiplier: `100%`.
- Cash floor: `5%`.
- Interpretation: the market panic layer does not block staged buys today; stock-level extension and concentration risk still justify keeping high tactical cash.

## Stock Validation

| Ticker | Latest Quote | Intraday Behavior | Validation |
| --- | ---: | --- | --- |
| MRVL | 204.42 | Flat, holding above intraday low 199.35 | Still valid; use staged buy limits. |
| AMD | 513.29 | -0.93%, above intraday low 507.66 | Still valid, but extended; buy only on pullbacks. |
| WDC | 536.00 | +0.91%, strong versus market | Valid and acting best among current buy list. |
| STX | 897.90 | +1.95%, strongest current follow-through | Valid but high price/volatility; use smaller staged entries. |
| CIEN | 546.36 | -4.18%, sharp intraday weakness | Downgrade to conditional buy only; do not catch falling knife. |
| INTC | 118.65 | -1.85%, heavy volume and weak intraday behavior | Keep speculative only; smaller and lower limits. |

## Staged Limit-Order Plan

Assumption: no existing positions; total account value USD 20,000; fractional shares allowed. If only whole shares are allowed, round down and keep unused cash.

| Ticker | Max Weight | Max Amount | Order Plan | Stop / Invalidation |
| --- | ---: | ---: | --- | --- |
| MRVL | 12% | $2,400 | $800 near 202.50; $800 near 199.50; $800 near 194.50 | Reduce if close below 194 or if QQQ/SMH both lose 20-day trend. |
| AMD | 10% | $2,000 | $800 near 511; $600 near 505; $600 near 492 | Reduce if close below 492; hard risk cut around -15% from average entry. |
| WDC | 8% | $1,600 | $600 near 532; $500 near 524; $500 near 510 | Reduce if close below 500 or if memory/storage group reverses broadly. |
| STX | 7% | $1,400 | $500 near 890; $500 near 878; $400 near 850 | Reduce if close below 840; take partial profit if it extends another 20%-25% quickly. |
| CIEN | 0%-5% | Up to $1,000 | No immediate buy. Either $500 near 535 only if market remains strong, or buy on reclaim above 555/560 after stabilization. | Avoid if closes below 535 or underperforms SMH for another session. |
| INTC | 0%-5% | Up to $1,000 | $500 near 117.80; $500 near 113.50 only if QQQ/SMH remain positive. | Stop near 108.50; keep tactical only. |

## Revised Initial Exposure

- Active buy orders if all fill: about $9,400, but CIEN and INTC should be treated as conditional, not automatic.
- More conservative first-day fill target: about $6,900-$7,900, excluding or partially filling CIEN/INTC.
- Keep at least $10,000 cash unless the market pulls back into limits without damaging the trend.

## Decision Change Versus Initial Recommendation

- WDC and STX are upgraded as the cleanest acting names today.
- MRVL remains a core candidate because it is holding trend without overheating as much as memory names.
- AMD remains valid but should not be chased above the current zone.
- CIEN is downgraded from "buy small" to "conditional buy" because the intraday drawdown is sharp.
- INTC remains speculative only and should not exceed 5%.

## Next Check

Recheck after the US close:

- Whether QQQ and SMH closed near highs or faded.
- Whether CIEN recovered above 555/560 or closed weak.
- Whether WDC/STX held gains without reversal.
- Whether any limit orders filled and what the new average price/risk is.
