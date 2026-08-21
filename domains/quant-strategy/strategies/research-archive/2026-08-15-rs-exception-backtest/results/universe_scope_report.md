# SMH/common-factor universe-scope audit

## Why this audit exists

The user list has 36 symbols, of which QQQM is excluded as an index duplicate. The prior simulator applied the SMH gate to all remaining 35, while the preregistered hypothesis says semiconductor/common-factor entries. The following scopes are fixed from existing watchlist theme labels, not from trade outcomes.

- `all_35` (35): DRAM, MU, WDC, STX, SNDK, SKHY, MRVL, AVGO, ALAB, COHR, LITE, AAOI, MXL, AXTI, CRDO, SMCI, ORCL, META, TER, ASML, AMAT, KLAC, LRCX, RKLB, RDW, TSLA, QCOM, NVDA, AMD, INTC, GLW, NOK, TTMI, CEG, KO
- `ai_capex_broad` (32): DRAM, MU, WDC, STX, SNDK, SKHY, MRVL, AVGO, ALAB, COHR, LITE, AAOI, MXL, AXTI, CRDO, SMCI, ORCL, META, TER, ASML, AMAT, KLAC, LRCX, TSLA, QCOM, NVDA, AMD, INTC, GLW, NOK, TTMI, CEG
- `direct_semiconductor_chain` (28): DRAM, MU, WDC, STX, SNDK, SKHY, MRVL, AVGO, ALAB, COHR, LITE, AAOI, MXL, AXTI, CRDO, SMCI, TER, ASML, AMAT, KLAC, LRCX, QCOM, NVDA, AMD, INTC, GLW, NOK, TTMI
- `legacy_supergroup_mapped` (31): DRAM, MU, WDC, STX, SNDK, SKHY, MRVL, AVGO, ALAB, COHR, LITE, AAOI, MXL, AXTI, CRDO, SMCI, ORCL, META, TER, ASML, AMAT, KLAC, LRCX, RKLB, RDW, QCOM, NVDA, AMD, INTC, GLW, NOK

## Paired results at 10 bps

| Universe | Period | Baseline return | Candidate return | Delta | Candidate DD | Sharpe | Win rate | Trades | Winning themes | Max symbol profit share |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_35 | train_2024_2025 | 6.31% | 17.15% | +10.84% | -1.91% | 2.19 | 70.00% | 20 | 9 | 27.88% |
| all_35 | 2026 | -2.18% | 0.61% | +2.80% | -1.89% | 0.32 | 50.00% | 4 | 2 | 93.15% |
| all_35 | full | 5.91% | 17.81% | +11.90% | -2.33% | 1.77 | 66.67% | 24 | 9 | 25.78% |
| ai_capex_broad | train_2024_2025 | 5.78% | 15.01% | +9.23% | -2.46% | 1.89 | 65.00% | 20 | 8 | 24.22% |
| ai_capex_broad | 2026 | -2.17% | 0.62% | +2.80% | -1.88% | 0.33 | 66.67% | 3 | 2 | 93.15% |
| ai_capex_broad | full | 5.39% | 15.68% | +10.30% | -2.46% | 1.55 | 65.22% | 23 | 8 | 22.26% |
| direct_semiconductor_chain | train_2024_2025 | 7.06% | 11.62% | +4.57% | -3.10% | 1.41 | 60.00% | 20 | 7 | 26.18% |
| direct_semiconductor_chain | 2026 | -0.23% | 1.55% | +1.78% | -1.60% | 0.81 | 100.00% | 2 | 2 | 93.15% |
| direct_semiconductor_chain | full | 8.61% | 13.17% | +4.56% | -3.10% | 1.29 | 63.64% | 22 | 7 | 23.96% |
| legacy_supergroup_mapped | train_2024_2025 | 8.03% | 14.33% | +6.30% | -2.45% | 1.76 | 72.22% | 18 | 8 | 24.26% |
| legacy_supergroup_mapped | 2026 | -2.17% | 0.62% | +2.80% | -1.88% | 0.33 | 66.67% | 3 | 2 | 93.15% |
| legacy_supergroup_mapped | full | 7.64% | 15.00% | +7.37% | -2.45% | 1.45 | 71.43% | 21 | 8 | 22.29% |

## Interpretation

- Candidate improves return, drawdown and Sharpe in both training and 2026 for `4/4` predefined scopes.
- Scope must be resolved from strategy intent before forward accumulation; selecting the best historical scope would be another form of overfitting.
- Full-watchlist analysis may still discuss every symbol, but an SMH-gated shadow ledger should not silently treat a defensive beverage or unrelated space exposure as a semiconductor/common-factor trade.

Research-only. This report does not authorize exclusion, inclusion or an order by itself.
