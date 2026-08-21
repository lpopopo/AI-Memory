# V9 index core plus RSR sleeve audit

## Scope

This 2026 held-out-period audit adds the research-only RSR stock PnL to the formal V9 70% SPY/QQQ core-only path. Dollar PnL is combined rather than averaging two standalone returns: both modules size risk as a fraction of the same initial portfolio, and their unused zero-yield cash is counted only once.

The result is hypothetical. RSR1/RSR2 are not promoted Rule E signals, and the combination cannot authorize an order or modify formal V9.

## Results

| Portfolio | Return | Max DD | Sharpe | Final value | Max combined gross |
| --- | ---: | ---: | ---: | ---: | ---: |
| v9_core_70 | 1.41% | -7.26% | 0.26 | $6,084.75 | 71.63% |
| v9_core_plus_rsr1 | 2.04% | -7.80% | 0.33 | $6,122.12 | 84.82% |
| v9_core_plus_rsr2 | 2.23% | -7.61% | 0.36 | $6,133.84 | 84.82% |
| v9_core_plus_rsr1_sgov_proxy | 2.85% | -7.62% | 0.44 | $6,170.86 | 84.79% |
| v9_core_plus_rsr2_sgov_proxy | 3.05% | -7.43% | 0.47 | $6,182.88 | 84.79% |
| buy_hold_SPY | 12.39% | -8.07% | 1.62 | $6,735.99 | 91.84% |
| buy_hold_QQQ | 16.60% | -10.80% | 1.38 | $6,988.18 | 93.21% |

## Interpretation

- The isolated V9 core returns `1.41%`. Adding RSR1 raises it to `2.04%`; RSR2 raises it to `2.23%`.
- RSR2 adds `0.82%` to the core but worsens maximum drawdown by `0.35` percentage points. The marginal result rests on only `3` closed stock trades.
- With the optimistic fixed-path SGOV residual-cash proxy, core+RSR2 reaches `3.05%`. This is cash-management research, not a tradable assumption.
- Maximum combined risky exposure is `84.82%`; no leverage is introduced. The index core, not the low-frequency stock sleeve, remains the dominant return and drawdown driver.
- The correct profit-maximization question is therefore portfolio allocation between the validated index core, unproven stock sleeve and cash, not simply increasing RSR stock size. Continue separate forward evidence before changing the 70/30 governance.

Research-only. Formal V9, RSR1 and RSR2 remain unchanged.
