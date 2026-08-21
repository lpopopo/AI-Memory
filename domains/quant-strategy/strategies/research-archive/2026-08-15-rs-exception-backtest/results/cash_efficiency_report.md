# Cash efficiency and passive opportunity-cost audit

## Assumptions

The original simulator pays 0% on uninvested cash. This audit adds an optional SGOV adjusted-close total-return series to post-execution cash at each session close. It is an optimistic cash-sweep proxy, not an executable assumption: taxes, spreads, settlement, broker eligibility and the need to liquidate an ETF before next-open stock entries are not modeled.

SGOV source: `Yahoo Finance via yfinance`; coverage `2023-12-26` through `2026-08-07`; full-period proxy return `12.12%`.

## Active strategies: zero-yield cash versus SGOV proxy

| Period | Variant | Cash mode | Return | Max DD | Sharpe | Average stock exposure | Cash yield earned | Trades |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train_2024_2025 | rsr1 | zero_yield | 15.01% | -2.46% | 1.89 | 5.08% | $0.00 | 20 |
| train_2024_2025 | rsr1 | sgov_proxy | 25.89% | -2.37% | 2.98 | 5.51% | $571.17 | 21 |
| train_2024_2025 | rsr2 | zero_yield | 17.18% | -1.91% | 2.13 | 5.06% | $0.00 | 20 |
| train_2024_2025 | rsr2 | sgov_proxy | 27.19% | -2.24% | 3.15 | 5.43% | $573.92 | 21 |
| 2026 | rsr1 | zero_yield | 0.62% | -1.88% | 0.33 | 2.62% | $0.00 | 3 |
| 2026 | rsr1 | sgov_proxy | 2.75% | -1.58% | 1.37 | 2.60% | $127.84 | 3 |
| 2026 | rsr2 | zero_yield | 0.82% | -1.69% | 0.42 | 2.57% | $0.00 | 3 |
| 2026 | rsr2 | sgov_proxy | 2.95% | -1.55% | 1.47 | 2.56% | $128.14 | 3 |
| full | rsr1 | zero_yield | 15.68% | -2.46% | 1.55 | 4.50% | $0.00 | 23 |
| full | rsr1 | sgov_proxy | 29.28% | -2.37% | 2.67 | 4.78% | $734.50 | 24 |
| full | rsr2 | zero_yield | 18.11% | -2.33% | 1.77 | 4.46% | $0.00 | 23 |
| full | rsr2 | sgov_proxy | 30.88% | -2.24% | 2.83 | 4.69% | $739.37 | 24 |

## Full-period passive benchmarks at 10 bps per side

| Benchmark | Return | Max DD | Sharpe | Exposure |
| --- | ---: | ---: | ---: | ---: |
| SPY | 68.03% | -18.69% | 1.35 | 99.63% |
| QQQ | 81.34% | -22.67% | 1.20 | 99.57% |
| SMH | 242.00% | -35.29% | 1.45 | 98.75% |
| SGOV | 11.83% | -0.09% | 19.42 | 98.77% |

## Interpretation

- RSR1's full return rises from `15.68%` to `29.28%` under the SGOV proxy; RSR2 rises from `18.11%` to `30.88%`.
- Holding the original RSR1 shares and trade dates fixed, the SGOV proxy raises return to `27.94%`. The dynamic full rerun reaches `29.28%`; the extra `1.34%` comes from changed whole-share sizing and capacity.
- The dynamic cash overlay changes RSR1 from `23` to `24` trades and adds a losing ASML trade. Larger share counts elsewhere more than offset it, so the full-rerun gain must not be labeled pure interest.
- Exact fixed-path cash yield is `$735.40`. The zero-yield reconstruction matches the original equity path to within `$0.00000000`.
- Passive indices provide the relevant wealth opportunity cost but carry much larger continuous market exposure and drawdown. The active strategy is a low-exposure timing sleeve, not a substitute for a fully invested core benchmark.
- Do not add an SGOV trade or assume broker interest without verifying the user's broker sweep mechanics, settlement availability, tax treatment and next-open buying power. No RSR3 version is created from this optimistic proxy.

Research-only. No live order or formal V9 change is authorized.
