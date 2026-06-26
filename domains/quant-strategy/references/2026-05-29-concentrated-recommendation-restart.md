# 2026-05-29 Concentrated Recommendation Restart

Purpose: restart the current buy recommendation using the new concentration rules.

Assumption: USD 20,000 hypothetical account, no existing positions, fractional shares allowed. This is a research plan, not guaranteed return or personalized financial advice.

## Market Fear Gate

- Regime: `normal`
- Score: `0`
- VIX: about `15.35`
- Risk multiplier: `100%`
- Max new buy exposure from fear gate: `50%`
- Cash floor from fear gate: `5%`

Market panic layer allows staged buying.

## Concentration Rule

- Target active holdings: 4 to 6 stocks.
- Hard maximum active holdings: 8 stocks.
- Target themes: 2 to 3.
- Current selected themes:
  - AI interconnect/custom silicon.
  - AI compute/inference.
  - AI storage.

## Core Recommendation

Recommended initial deployment: 45% / USD 9,000.

Cash reserve: 55% / USD 11,000.

| Ticker | Theme | Action | Target Weight | Amount | Entry Style | Risk Control |
| --- | --- | --- | ---: | ---: | --- | --- |
| MRVL | AI interconnect/custom silicon | Buy | 13% | $2,600 | Staged limits around 202, 199, 195 | Reduce if close below 194 or if SMH/QQQ lose 20-day trend. |
| AMD | AI compute/inference | Buy | 12% | $2,400 | Staged limits around 511, 505, 492 | Reduce if close below 492 or if momentum breaks. |
| WDC | AI storage | Buy | 10% | $2,000 | Staged limits around 528, 520, 508 | Reduce if close below 500. |
| STX | AI storage | Buy | 10% | $2,000 | Staged limits around 878, 860, 840 | Reduce if close below 835-840. |

## Optional Satellite

| Ticker | Theme | Status | Max Weight | Reason |
| --- | --- | --- | ---: | --- |
| INTC | Tactical semiconductor turnaround | Optional only | 3%-5% | Momentum is strong, but thesis quality is lower. Only add if a core name does not fill or if portfolio remains below target exposure. |

Do not buy CIEN now. It is still theme-relevant, but its intraday behavior and relative score are weaker than MRVL/AMD/WDC/STX.

## Watchlist, Not Buy Now

| Ticker | Reason |
| --- | --- |
| SNDK | Strongest momentum but too extended; avoid chasing. |
| MU | Correct theme but high extension; wait for pullback. |
| ARM | Strong but too stretched above 20-day trend. |
| ALAB | Excellent theme, but extension is too high for fresh entry. |
| CIEN | Wait for recovery above key levels and better relative strength. |

## Practical Execution

- Place only limit orders, no market orders.
- Prefer filling MRVL/AMD/WDC/STX first.
- If all four core positions fill, do not add INTC.
- If only two or three core positions fill and market remains strong, INTC can be used as a 3%-5% tactical satellite.
- Keep at least 50% cash while memory/storage and AI semiconductor names remain extended.

## Difference Versus Previous Recommendation

- Removed default CIEN and INTC holdings from the core list.
- Raised the importance of concentration: 4 core names across 3 themes.
- Kept the same AI infrastructure direction, but reduced overlap and avoided chasing too many names.
