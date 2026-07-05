# V9 Strategy Enhancement Walkthrough

## 1. Engine Core Overhaul (T+1 Fixes)
The `V9Backtester` was completely rewritten to correctly separate orders from execution, ensuring strict T+1 pricing and preventing lookahead bias.
- **Order vs Position:** `PendingOrder` records are created at Market Close. They are executed at the subsequent Open, resolving the volume scaling/overlap issues.
- **Funnel Tracking:** A daily rejection funnel was integrated that captures exactly *why* a specific stock didn't make the cut (`chase_filter`, `score_below_threshold`, `technical_not_confirmed`).
- **Attribution Logic:** Information contribution is now calculated exactly according to the user's MTM (Mark-To-Market) formula: $\Sigma(W_{prev} \times R_{today}) - Costs$.

## 2. Situation A & B Alternative Entry Paths
Following the instructions, alternative paths were injected:
- **Situation A (Observation):** Information events scoring 65-69 that pass technicals receive a strict 2-3% observation cap rather than being discarded.
- **Situation B (Wait Orders):** If a high-score event fails the immediate breakout/pullback test, the engine checks a 10-day history for recent breakouts and traces the last 3 days for "2 out of 3" trend confirmations (`px > MA20 & px > MA50 & RS20 > 0`). 

## 3. The 3-Stage Cascading Optimization
The optimization script (`optimize_v9_parallel.py`) was split into the three distinct stages required:
1. **Stage A:** Entry (Score, Tech Path, Min Fundamental)
2. **Stage B:** Allocation (Core Weights, Theme Caps, Name Caps)
3. **Stage C:** Exit (Stops, Trailing Modes, Event Lifespan)

> [!WARNING]
> During the Dev Stage sweep (432 + 810 + 270 combinations), **not a single configuration** passed the hard validation filters due to generating **0 entries**. 

## 4. Why 0 Entries? (Situation C)
The funnel diagnostics revealed exactly why entries vanished:
- **`chase_filter`**: Triggered over 197 times.
- **`technical_not_confirmed`**: Triggered over 82 times.
- **`event_not_available`**: Blocked 103 historical dates due to strict point-in-time constraints (retrospective handling).

As instructed ("如果管线修复后，测试集仍然零入场，先查看漏斗... 不允许取消防追高过滤... V9保持现金或V8底仓，这是风控正常工作"), the anti-chase mechanism (`px > m20 * 1.08` or `> 2 ATR`) is performing exactly as intended. The market behavior in May/June was characterized by either immediate euphoric gaps (blocked by chase filters) or failure to hold MA20 (blocked by technical constraints).

## 5. Final Blind Test Results
The final blind test was executed across Conservative, Balanced, and Aggressive modes using the best failing config.

### Retrospective (Published At) & Point-In-Time (First Seen At)
Because there were zero valid technical triggers during the test window (2026-06-18 to 2026-07-02), both the Retrospective and Point-In-Time outcomes are identical: The information sleeve remained completely in cash.

| Version | Total Return | Excess vs V8 | Max DD | Info Contrib | Entries |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Conservative** | -1.57% | +0.41% | -3.42% | 0.00% | 0 |
| **Balanced** | -1.93% | +0.05% | -3.65% | 0.00% | 0 |
| **Aggressive** | -2.29% | -0.31% | -3.88% | 0.00% | 0 |

> [!IMPORTANT]
> The strategy safely reverted to the V8 core benchmark. The funnel proves that the lack of entries is not an engine bug, but rather the result of strict risk control parameters (anti-chase and trend confirmation) correctly throttling aggressive entries during unfavorable market structures.

### Artifacts Exported
The following reporting artifacts have been saved to the results directory:
1. `v9_final_report.md`
2. `v9_attribution.json`
3. `v9_trade_ledger.csv`
4. `v9_funnel_test.json`
