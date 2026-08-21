# V9 core month-end whipsaw audit

## Scope

This research-only audit isolates the formal 70% SPY/QQQ core with no information sleeve. Signals use completed month-end closes; transactions remain next-session close. The frozen V9 implementation is not modified.

The candidate set was fixed before comparison: current one-month response, two-month confirmation on both directions, exit only, entry only, and MA200-only. A challenger must be non-worse on return, drawdown and Sharpe in both calendar-2025 training and 2026 held-out data.

## Results

| Period | Variant | Return | Max DD | Sharpe | Turnover | Core trades |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| train_2025 | current_1m | 6.95% | -7.46% | 0.79 | 2.03 | 8 |
| train_2025 | confirm_2m_both | 3.78% | -10.54% | 0.42 | 2.03 | 10 |
| train_2025 | confirm_2m_exit | 7.22% | -10.54% | 0.73 | 2.03 | 10 |
| train_2025 | confirm_2m_entry | 3.51% | -7.46% | 0.44 | 2.03 | 8 |
| train_2025 | ma200_only | 6.95% | -7.46% | 0.79 | 2.03 | 8 |
| test_2026 | current_1m | 1.41% | -7.26% | 0.26 | 2.04 | 6 |
| test_2026 | confirm_2m_both | 5.99% | -7.26% | 0.88 | 1.35 | 6 |
| test_2026 | confirm_2m_exit | 5.99% | -7.26% | 0.88 | 1.35 | 6 |
| test_2026 | confirm_2m_entry | -3.75% | -9.56% | -0.53 | 2.04 | 6 |
| test_2026 | ma200_only | 1.41% | -7.26% | 0.26 | 2.04 | 6 |

## 2026 whipsaw anatomy

- The current rule sold both core ETFs on `2026-04-01` after the March month-end signal and repurchased them on `2026-05-01` after the April month-end signal.
- This was a joint gate event. The MA150/MA200 vote cut each ETF's base target from 50% to 0%, while the independent `panic` risk regime (score `14`; positive components: `vix_level:2; spy_drawdown_63d:1; spy_trend_break:3; qqq_drawdown_63d:2; qqq_trend_break:3; smh_drawdown_63d:2; smh_trend_break:1`) reduced the total 70% core budget to `35.00%`. The current rule therefore exited fully; the delayed-exit variant still cut to `35.00%` total core exposure.
- From the exit close to the re-entry close, SPY returned `9.98%` and QQQ returned `15.38%`. A fully invested 35%/35% core missed approximately `8.88%`; the tested delayed-exit path retained only 17.5%/17.5%, so its directly retained contribution was approximately `4.44%` before costs and sizing drift.
- Requiring two consecutive month-end exit signals improved 2026 return by `4.58%`, but its 2025 maximum drawdown worsened by `3.08` percentage points.

## Decision

`0` of `4` challengers passed the cross-period promotion gate. MA200-only was behaviorally identical to current V9 in both samples and is not counted as an improvement. Therefore the April opportunity is classified as the known insurance cost of the trend and risk-budget gates, not sufficient evidence of an implementation defect or a rule change.

Keep formal V9 unchanged. Track future one-month exits as a named forward diagnostic; reconsider only after repeated independent cases, not this single favorable counterfactual.
