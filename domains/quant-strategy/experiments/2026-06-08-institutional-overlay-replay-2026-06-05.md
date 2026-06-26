# 2026-06-05 Institutional Overlay Replay

Run date: 2026-06-08

Purpose: replay the 2026-06-05 AI/semiconductor drawdown using the new institutional overlay scorecard. This tests whether the AQR/Citadel Securities/GMO/Man Group-derived overlays would have produced useful warnings for the current model portfolio.

This is a historical diagnostic note, not a real-account instruction.

## 1. Event Summary

Known from existing memory:

- 2026-06-05 close showed a material risk-state change.
- VIX rose to about `21.51`.
- QQQ and semiconductor pressure broadened.
- AMD closed below the existing `492` stop at `466.38`.
- WDC closed near the `500` stop at `511.72`.
- STX closed near the `835` stop at `847.47`.
- MRVL closed at `263.47`, near but not below the `<260` additional reduction line.
- The model portfolio fell from about `USD 21,447.43` to about `USD 20,376.67`, roughly `-4.99%` from the prior marked snapshot.

Interpretation:

This was not a single-stock thesis failure. It was a synchronized AI/semiconductor/storage crowding and risk-state event. The old workflow had single-stock stops and a broad fear gate, but lacked a same-theme correlated-risk review.

## 2. Overlay Scorecard Replay

### 2.1 Flow-Fragility Score

| Component | Score | Replay evidence | Data quality |
| --- | ---: | --- | --- |
| Narrow leadership | 1 | Prior leadership was concentrated in AI infrastructure and semiconductors; breadth pressure broadened on the drawdown day. | medium |
| Semiconductor/AI concentration | 2 | Active holdings MRVL/AMD/WDC/STX all belonged to AI infrastructure or storage; weakness arrived together. | high |
| Options/crowding behavior | 1 | Direct options data unavailable; strong-news/weak-price and crowded theme reversal suggest crowding risk, but evidence is indirect. | low |
| Systematic/vol-control exposure | 1 | Direct CTA/vol-control data unavailable; prior rally and volatility behavior made systematic exposure plausible, not proven. | low |
| Buyback window support | 0 | No direct evidence that buyback support had faded on this exact date. | unknown |
| Hedging complacency | 1 | VIX jump to `21.51` after calmer conditions suggests protection demand repriced; direct skew data unavailable. | medium |
| Levered/thematic crowding | 1 | Direct levered ETF/thematic-flow data unavailable; AI/semiconductor theme crowding was visible in price clustering. | low |
| **Total** | **7 / 14** |  |  |

Replay state:

```text
flow_fragility_state: elevated
strategy_response: block new AI/semiconductor chase buys; run portfolio-level correlated-risk review; prefer trims or defensive holds over fresh adds.
```

### 2.2 Trend-Aligned Entry Score

This score is evaluated for new adds to existing AI infrastructure positions after the selloff.

| Component | Score | Replay evidence |
| --- | ---: | --- |
| Market fear gate permits exposure | 0 | VIX around `21.51` and broad AI/semiconductor pressure imply elevated/stress review, not normal adding. |
| Price trend valid | 0 | AMD breached stop; WDC/STX near stops; MRVL near reduce line. |
| Relative strength valid | 0 | Same-theme holdings fell together; no confirmed relative-strength recovery at close. |
| Pullback quality valid | 0 | Move looked like high-risk theme unwind rather than orderly support test. |
| Catalyst confirmed | 0 | Good AI narratives did not protect price; price rejected the bullish thesis in the short run. |
| **Total** | **0 / 5** |  |

Replay state:

```text
trend_aligned_entry_state: trend_broken
strategy_response: no buy/add; review stop/reduce and near-stop holdings.
```

### 2.3 AI Quality / Capex-Cycle Read-Through

| Ticker | Class | Capex-cycle sensitivity | Replay role | Comment |
| --- | --- | --- | --- | --- |
| MRVL | cyclical_supplier / bottleneck | high | profit-protection review | Strong AI bottleneck upside but exposed to crowded capex-cycle repricing. |
| AMD | cyclical_supplier | high | reduce-review | Existing stop breach means it cannot remain normal hold without rule override. |
| WDC | cyclical_supplier | high | defensive hold / near-stop review | Storage thesis intact but near risk line after same-theme selloff. |
| STX | cyclical_supplier | high | defensive hold / near-stop review | Storage thesis intact but near risk line after same-theme selloff. |

Replay conclusion:

The portfolio had high theme overlap and high capex-cycle sensitivity. The AI quality overlay would not necessarily have predicted the exact selloff, but it would have warned that MRVL/AMD/WDC/STX were not diversified AI exposure.

### 2.4 Factor-Macro Flags

| Flag | State | Evidence |
| --- | --- | --- |
| growth_duration_high | high | AI/semiconductor and growth-sensitive holdings dominated active risk. |
| momentum_reversal_high | high | Prior leaders reversed together as VIX rose. |
| theme_overlap_high | high | All active equity holdings expressed AI infrastructure or storage bottleneck risk. |
| sleeve_correlation_high | high | Practical model account behaved like one theme basket during the selloff. |
| inflation_value_tilt_high | unknown | No direct evidence used in this replay. |

## 3. What The New Overlay Would Have Changed

Under the new framework, the 2026-06-05 close would have required:

1. `flow_fragility = elevated`.
2. `trend_aligned_entry = trend_broken`.
3. No new AI/semiconductor/storage buys.
4. AMD marked `reduce-review` immediately because the stop was breached.
5. WDC/STX marked `defensive hold / near-stop review`, not strong hold.
6. MRVL marked `profit-protection review`, especially because it had recently moved vertically and then failed to hold strength.
7. Portfolio-level correlated-risk review before any single-stock optimism.

## 4. What It Would Not Have Changed

- It would not automatically sell everything.
- It would not short the theme.
- It would not invalidate the AI infrastructure thesis.
- It would not override existing stop rules; it would have made them more visible and urgent.

## 5. Hypothesis Impact

Strengthened:

- H7: Institutional flow-fragility overlay can reduce crowded AI drawdown risk.
- H8: AI quality and capex-cycle classification improves candidate ranking.
- H9: Trend-aligned support buys outperform plain dip-buying.

Still unproven:

- Whether the overlay reduces drawdown without too much cash drag across a larger sample.
- Whether a score threshold of `7` is the right boundary for `elevated`.
- Which public data proxies best approximate options, CTA, and levered ETF crowding.

## 6. Next Test

Replay the next 5 trading days after 2026-06-05:

- Current rules versus overlay-adjusted rules.
- Compare AMD reduce timing.
- Compare WDC/STX defensive-hold treatment.
- Compare MRVL profit-protection treatment.
- Measure portfolio drawdown, missed rebound, and cash drag.
