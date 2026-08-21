# Operational cash-sweep break-even audit

## Current official inputs

| Instrument | Price | 30-day SEC yield | Expense ratio | Median spread | Official date |
| --- | ---: | ---: | ---: | ---: | --- |
| SGOV | $100.56 | 3.60% | 0.0900% | 0.01% | yield 2026-08-13; price 2026-08-14 |
| BIL | $91.53 | 3.57% | 0.1353% | 0.01% | yield 2026-08-13; price 2026-08-14 |

Working inputs: USD `3,756.49` cash, USD `5,751.77` NAV, USD `1.00` commission per side, whole shares, and an 8% RSR target weight. SEC yield is already net of fund operating expenses but not investor-specific tax, brokerage or FX.

## SGOV net-dollar focus

| Cash allocation | Shares | Immediate cash | Tax haircut | Days | Income after haircut | Round-trip cost | Net income | Break-even |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 50% | 18 | $1,945.41 | 0% | 30 | $5.36 | $5.62 | $-0.26 | 31.5 days |
| 50% | 18 | $1,945.41 | 0% | 60 | $10.71 | $5.62 | $5.09 | 31.5 days |
| 50% | 18 | $1,945.41 | 0% | 90 | $16.07 | $5.62 | $10.45 | 31.5 days |
| 50% | 18 | $1,945.41 | 30% | 30 | $3.75 | $5.62 | $-1.87 | 45.0 days |
| 50% | 18 | $1,945.41 | 30% | 60 | $7.50 | $5.62 | $1.88 | 45.0 days |
| 50% | 18 | $1,945.41 | 30% | 90 | $11.25 | $5.62 | $5.63 | 45.0 days |
| 100% | 37 | $34.77 | 0% | 30 | $11.01 | $9.44 | $1.57 | 25.7 days |
| 100% | 37 | $34.77 | 0% | 60 | $22.02 | $9.44 | $12.58 | 25.7 days |
| 100% | 37 | $34.77 | 0% | 90 | $33.03 | $9.44 | $23.59 | 25.7 days |
| 100% | 37 | $34.77 | 30% | 30 | $7.71 | $9.44 | $-1.73 | 36.8 days |
| 100% | 37 | $34.77 | 30% | 60 | $15.41 | $9.44 | $5.97 | 36.8 days |
| 100% | 37 | $34.77 | 30% | 90 | $23.12 | $9.44 | $13.68 | 36.8 days |

## RSR liquidity reserve

| Reserved future RSR entries | Required cash | Max SGOV shares | SGOV notional | Remaining cash | Sweep % of cash |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | $461.14 | 32 | $3,217.92 | $537.57 | 85.66% |
| 2 | $922.28 | 28 | $2,815.68 | $939.81 | 74.96% |
| 3 | $1,383.42 | 23 | $2,312.88 | $1,442.61 | 61.57% |

## Decision

- SGOV has a slightly higher SEC yield and lower expense ratio than BIL, but BIL's lower share price deploys nearly all of this small cash balance. At whole-share size their estimated annual pre-tax income is nearly identical: `$133.95` versus `$133.97`.
- Under the conservative 10 bps-per-side stress plus commissions, a 50% SGOV tranche breaks even after `31.5` days pre-tax and `45.0` days with a 30% distribution haircut. A 30-day hold is not reliably economic under that stress.
- Reserving cash for all three possible 8% RSR positions permits at most `23` SGOV shares, or `61.57%` of working cash. A simple 50% tranche leaves `$1945.41` immediately available, more than the three-entry reserve.
- Do not automate or treat SGOV/BIL as cash until the broker confirms USD settlement, sale-proceeds availability, distribution withholding/tax, commissions/platform fees and whether the account already pays interest on idle cash.

Research-only. This audit authorizes no ETF order.
