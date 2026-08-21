# Backtest integrity audit

## Bottom line

The frozen audit passed. No implementation issue changes the current strategy decision.
Formal V9 and the real account are unchanged; this audit authorizes no order.

## Frozen checks

| Check | Result |
| --- | --- |
| causal_features | pass |
| execution_chronology | pass |
| price_feasibility | pass |
| corporate_action_consistency | pass |
| portfolio_accounting | pass |
| exit_path_integrity | minor |
| data_invariants | minor |
| cross_engine_consistency | pass |

## Key evidence

- Future-row perturbation left every feature and signal unchanged through 2025-12-31.
- Execution chronology failures: 0; price-feasibility failures: 0.
- Minimum replayed RSR2 cash: USD 4624.17; maximum entry-time exposure: 23.49%; maximum close exposure after price drift: 26.18%; maximum concurrent names: 3.
- Point-in-time OHLC geometry exceptions above floating tolerance: 6; affected held trade paths: 0.
- Point-in-time forced terminal trades across the six period/variant cells: 9.
- Maximum return change when terminal positions remain open and are marked to market: 0.0715%.
- Non-liquidating point-in-time transfer screen passed: False.

## Terminal-liquidation sensitivity

| Period | Variant | Terminal trades | Open at end | Forced return | Mark-to-market return | Delta | Forced win | Closed-only win |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| development_2015_2019 | matched_baseline | 3 | 3 | -7.09% | -7.02% | +0.07% | 37.80% | 37.38% |
| development_2015_2019 | combined_4pct_50pct | 3 | 3 | -5.83% | -5.76% | +0.07% | 37.96% | 37.56% |
| validation_2020_2022 | matched_baseline | 0 | 0 | -8.30% | -8.30% | +0.00% | 34.38% | 34.38% |
| validation_2020_2022 | combined_4pct_50pct | 0 | 0 | -7.58% | -7.58% | +0.00% | 34.44% | 34.44% |
| final_2023_2025 | matched_baseline | 2 | 2 | 0.11% | 0.15% | +0.05% | 41.73% | 40.88% |
| final_2023_2025 | combined_4pct_50pct | 1 | 1 | 1.62% | 1.65% | +0.02% | 42.34% | 41.91% |

## Decision

Retain the existing negative transfer conclusion. Report terminal liquidation explicitly and use non-liquidating mark-to-market sensitivity in future period-boundary audits. Do not alter RSR1/RSR2 parameters or promotion gates.
