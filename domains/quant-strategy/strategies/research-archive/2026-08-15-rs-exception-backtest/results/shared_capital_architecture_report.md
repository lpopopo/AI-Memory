# Whole-share shared-capital architecture audit

## Scope

This audit puts the V9 index core and frozen RSR2 stock path into one cash ledger. SPY, QQQ and stocks use whole shares, USD 1 per order and 10 bps slippage. The formal comparison is 70% core plus RSR's frozen 25% internal cap; the challenger is 80% core plus 20% RSR. No signal parameter changes.

## Results

| NAV | Period | Architecture | Return | Max DD | Sharpe | Monthly win | Avg core | Max stock | Stock trades | Stock win | Stock PnL | Min cash |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $6,000.00 | train_2024_2025 | formal_70_25 | 42.04% | -8.38% | 1.81 | 62.50% | 56.49% | 25.12% | 20 | 70.00% | $1,163.57 | $963.13 |
| $5,751.77 | train_2024_2025 | formal_70_25 | 41.71% | -8.62% | 1.78 | 62.50% | 56.22% | 24.88% | 20 | 70.00% | $1,133.27 | $832.31 |
| $6,000.00 | train_2024_2025 | challenger_80_20 | 41.76% | -9.08% | 1.64 | 62.50% | 63.97% | 18.50% | 16 | 75.00% | $947.17 | $1,055.20 |
| $5,751.77 | train_2024_2025 | challenger_80_20 | 41.68% | -9.41% | 1.63 | 62.50% | 64.78% | 18.89% | 16 | 75.00% | $880.04 | $802.58 |
| $6,000.00 | heldout_2026 | formal_70_25 | 1.66% | -7.09% | 0.30 | 50.00% | 52.67% | 16.25% | 3 | 66.67% | $49.08 | $1,238.11 |
| $5,751.77 | heldout_2026 | formal_70_25 | 1.43% | -6.38% | 0.29 | 50.00% | 44.68% | 16.94% | 3 | 66.67% | $49.08 | $1,674.64 |
| $6,000.00 | heldout_2026 | challenger_80_20 | 2.56% | -7.09% | 0.41 | 50.00% | 58.11% | 16.25% | 3 | 66.67% | $49.08 | $1,057.98 |
| $5,751.77 | heldout_2026 | challenger_80_20 | 2.67% | -7.39% | 0.41 | 50.00% | 60.59% | 16.93% | 3 | 66.67% | $49.08 | $809.75 |
| $6,000.00 | full_2024_2026 | formal_70_25 | 46.92% | -8.38% | 1.48 | 59.38% | 56.04% | 25.12% | 23 | 69.57% | $1,270.29 | $963.13 |
| $5,751.77 | full_2024_2026 | formal_70_25 | 45.42% | -8.62% | 1.46 | 59.38% | 54.76% | 24.88% | 23 | 69.57% | $1,189.05 | $832.31 |
| $6,000.00 | full_2024_2026 | challenger_80_20 | 46.03% | -9.08% | 1.35 | 59.38% | 62.52% | 18.50% | 19 | 73.68% | $1,047.19 | $1,055.20 |
| $5,751.77 | full_2024_2026 | challenger_80_20 | 45.36% | -9.41% | 1.32 | 59.38% | 63.79% | 18.89% | 19 | 73.68% | $935.82 | $802.58 |

## Challenger screen

- NAV `$6,000.00`: `fail`; failed: train_2024_2025_return_higher, train_2024_2025_sharpe_within_005, full_2024_2026_return_higher, full_2024_2026_sharpe_within_005
- NAV `$5,751.77`: `fail`; failed: train_2024_2025_return_higher, train_2024_2025_sharpe_within_005, full_2024_2026_return_higher, full_2024_2026_sharpe_within_005

## Stock-cap opportunity difference

- NAV `$6,000.00`: 20% stock capacity omits `4` training trades with formal-path source PnL `252.04`: CEG@2025-07-31, COHR@2024-11-08, KLAC@2025-06-10, MU@2025-09-08.
  The largest omitted contributor is `MU` at `$253.98`; the architecture difference is therefore concentrated and is not proof that a 25% stock sleeve will always win.
- NAV `$5,751.77`: 20% stock capacity omits `4` training trades with formal-path source PnL `178.66`: CEG@2025-07-31, COHR@2024-11-08, KLAC@2025-06-10, MU@2025-09-08.
  The largest omitted contributor is `MU` at `$189.98`; the architecture difference is therefore concentrated and is not proof that a 25% stock sleeve will always win.

## Decision

- 80/20 fails at least one frozen shared-capital requirement and is removed as an allocation challenger on this history.
- Formal 70/30 governance remains; do not reopen the core-cap grid merely to find a passing threshold.
- The 2026 held-out monitor ends at the latest completed formal local row, not the current calendar date.
- Research-only. No order, live-account mutation, formal V9 change or forward-ledger write is authorized.

See `shared-capital-architecture-preregistration.md` for the frozen comparison.
