# V9 core-allocation frontier audit

## Scope

This research-only audit changes only the V9 SPY/QQQ index-core ceiling. The MA150/MA200 vote, Fear Gate, next-session execution and 10 bps one-way proportional transaction cost are unchanged. No stock alpha, cash yield, leverage, tax or broker-specific whole-share assumption is included.

## Cross-period frontier

| Core cap | Validation return | Final return | 2026 return | Full CAGR | Full max DD | Full Sharpe | Monthly win | Balanced screen |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 50.00% | 24.99% | 43.06% | 1.05% | 5.49% | -13.21% | 0.80 | 57.50% | n/a |
| 60.00% | 29.69% | 51.33% | 1.23% | 6.43% | -15.62% | 0.82 | 57.50% | n/a |
| 70.00% | 34.38% | 59.85% | 1.41% | 7.42% | -17.94% | 0.82 | 57.50% | reference |
| 80.00% | 37.92% | 69.16% | 1.64% | 8.24% | -19.29% | 0.83 | 57.50% | pass |
| 90.00% | 35.71% | 76.74% | 1.96% | 8.77% | -21.24% | 0.81 | 57.50% | fail |
| 100.00% | 35.20% | 80.98% | 2.13% | 9.05% | -22.26% | 0.80 | 57.08% | fail |

## Rolling three-year robustness

| Core cap | Windows | Positive | Median CAGR | Minimum CAGR | Median Sharpe | Minimum Sharpe | Worst DD |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 50.00% | 204 | 100.00% | 5.67% | 0.29% | 0.79 | 0.08 | -13.21% |
| 60.00% | 204 | 100.00% | 6.61% | 0.38% | 0.80 | 0.09 | -15.62% |
| 70.00% | 204 | 100.00% | 7.55% | 0.61% | 0.81 | 0.12 | -17.94% |
| 80.00% | 204 | 100.00% | 8.46% | 0.64% | 0.82 | 0.12 | -19.29% |
| 90.00% | 204 | 100.00% | 9.08% | 0.68% | 0.81 | 0.12 | -21.24% |
| 100.00% | 204 | 100.00% | 9.58% | 0.68% | 0.81 | 0.12 | -22.26% |

## Decision

- The lowest passing ceiling is `80.00%`. It raises full-period CAGR by `0.82` percentage points while worsening full-period maximum drawdown by `1.36` percentage points.
- This is only a research challenger. A `80.00%` core leaves at most `20.00%` for all individual stocks at maximum core exposure; the shared-capital core-plus-RSR interaction has not yet passed a separate audit.
- Moving from 70% to 100% raises full-period CAGR from `7.42%` to `9.05%`, but maximum drawdown moves from `-17.94%` to `-22.26%`. Allocation changes profit magnitude, not the underlying signal hit rate.
- Formal V9 remains 70% core / 30% stock ceiling. No order or live allocation change is authorized.

See `core-allocation-frontier-preregistration.md` for the frozen screen.
