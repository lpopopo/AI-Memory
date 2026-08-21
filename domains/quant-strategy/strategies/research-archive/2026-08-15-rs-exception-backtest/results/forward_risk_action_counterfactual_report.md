# Forward risk-action counterfactual scorecard

## Boundary

- Completed-close as of: `2026-08-20`
- Retrospective seed / genuine-forward events: `3 / 0`
- Paper-only; no broker order, fill, strategy change, or automatic sale is assumed.
- Sell costs: 10 bps adverse slippage plus USD 1 per paper sale.

## Retrospective seed results

| Event / horizon | Execution | Mark | Full-exit net benefit vs hold |
| --- | ---: | ---: | ---: |
| GLW / 1-session | 169.74 on 2026-08-17 | 173.21 on 2026-08-17 | $-8.28 |
| GLW / as_of | 169.74 on 2026-08-17 | 151.45 on 2026-08-20 | $35.24 |
| MRVL / 1-session | 227.75 on 2026-08-17 | 234.33 on 2026-08-17 | $-28.23 |
| MRVL / as_of | 227.75 on 2026-08-17 | 251.01 on 2026-08-20 | $-94.95 |
| MXL / 1-session | 74.45 on 2026-08-19 | 66.43 on 2026-08-19 | $46.67 |
| MXL / as_of | 74.45 on 2026-08-19 | 65.28 on 2026-08-20 | $53.57 |

| Policy / horizon | Mature | Beneficial | Rate | Total net benefit |
| --- | ---: | ---: | ---: | ---: |
| full_exit / 1 | 3 | 1 | 33.33% | $10.16 |
| full_exit / as_of | 3 | 2 | 66.67% | $-6.14 |
| half_exit / 1 | 3 | 1 | 33.33% | $3.58 |
| half_exit / as_of | 3 | 2 | 66.67% | $-4.57 |

The one-session seeds are mixed, and the current `as_of` mark is not a fixed horizon. Three observed events cannot select full reduction, half reduction, or a quality-class exception. Five- and twenty-session fields remain unavailable until mature.

## Decision

Keep measuring. Do not alter formal V9/RSR1/RSR2, the long-term reclassification, or the real account. A genuine-forward event must be frozen before its next-session open; retrospective seeds never count toward policy selection.
