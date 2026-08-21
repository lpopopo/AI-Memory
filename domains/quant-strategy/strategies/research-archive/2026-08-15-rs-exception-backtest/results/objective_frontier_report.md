# Win-rate, profit, drawdown and evidence frontier

## Bottom line

**Best historical multi-objective candidate: RSR2. Best currently deployable architecture: unchanged formal V9 70/30, with no correlated additions.**

RSR2's full current-list replay returned 18.11%, won 69.57% of 23 trades and drew down 2.33%. That is the strongest historical stock-sleeve combination in the registered family, but it is not a live conclusion: the exact point-in-time transfer screen failed, selection bias remains uncontained, and the first four genuine-forward sessions contain zero signals/trades.

## Decision matrix

| Family | Retain / observe | Reject / supersede | Why |
| --- | --- | --- | --- |
| Stock selection and exit | Observe RSR2 as a frozen shadow | Do not promote RSR1/RSR2 | Historical dominance is offset by transfer, selection-bias and forward-sample gaps |
| Profit realization | Whole-position RSR2 lock | Half-position scale-out | Scale-out improves DD/Sharpe but lowers return and win rate |
| Winner extension | Frozen RSR2 exit | 30/40-day extensions | The apparent full-period edge fails development stability |
| Entry ranking | Current RS-plus-volume ordering | RS-only, low-ATR-first, balanced challenger | Formal rank has best development return/win; heldout has zero contentions |
| Shared capital | Formal 70/30 | 80/20 challenger | Formal wins train/full with better DD/Sharpe and preserves stock capacity |
| High volatility | Diagnostic only | Tradable sleeve | 17.65% development win rate and 0.32 Sharpe do not support the 2026 appearance |
| Residual cash | Conditional yield review | Automatic SGOV order | Proxy helps, but account mechanics are unverified |

## Comparable Pareto results

Pareto labels below are calculated only within the same family, period, NAV and cost group. They are not ranked across incompatible experiments.

| Family | Variant | Period | Return | Win rate | Max DD | Sharpe | Pareto | Evidence / decision |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| stock_selection_exit | RSR2 | full_2024_2026 | 18.11% | 69.57% | -2.33% | 1.77 | pareto_frontier | historical_leader_forward_unproven |
| profit_realization | RSR2 | full_2024_2026 | 18.11% | 69.57% | -2.33% | 1.77 | pareto_frontier | retain_whole_position_lock |
| profit_realization | partial_half_at_15 | full_2024_2026 | 16.17% | 66.67% | -1.84% | 1.90 | pareto_frontier | reject |
| winner_extension | rsr2_frozen | full_2024_2026 | 18.11% | 69.57% | -2.33% | 1.77 | pareto_frontier | retain_frozen_exit |
| winner_extension | extend30_any_winner | full_2024_2026 | 18.66% | 65.22% | -2.75% | 1.65 | pareto_frontier | reject |
| entry_ranking | formal_composite | development_2024_2025 | 17.18% | 70.00% | -1.91% | 2.13 | pareto_frontier | retain |
| entry_ranking | balanced_rank | development_2024_2025 | 17.05% | 65.00% | -1.91% | 2.16 | pareto_frontier | reject_or_insufficient |
| shared_capital | formal_70_25 | train_2024_2025 | 42.04% | 62.50% | -8.38% | 1.81 | pareto_frontier | retain_deployable_architecture |
| shared_capital | challenger_80_20 | heldout_2026 | 2.56% | 50.00% | -7.09% | 0.41 | pareto_frontier | reject |
| shared_capital | formal_70_25 | full_2024_2026 | 46.92% | 59.38% | -8.38% | 1.48 | pareto_frontier | retain_deployable_architecture |
| high_volatility_sleeve | registered_high_vol_sleeve | development_2024_2025 | 2.12% | 17.65% | -4.36% | 0.32 | descriptive_single_candidate | reject |
| high_volatility_sleeve | registered_high_vol_sleeve | retrospective_2026 | 3.93% | 58.33% | -1.75% | 1.12 | descriptive_single_candidate | reject |
| core_only_allocation | core_70 | full_2006_2025 | 318.34% | 57.50% | -17.94% | 0.82 | pareto_frontier | retain_deployable_architecture |
| core_only_allocation | core_80 | full_2006_2025 | 387.28% | 57.50% | -19.29% | 0.83 | pareto_frontier | local_frontier_not_deployable |
| combined_2026_architecture | v9_core_70 | heldout_2026_through_2026_08_07 | 1.41% | n/a | -7.26% | 0.26 | pareto_frontier | no_change |
| combined_2026_architecture | v9_core_plus_rsr2_sgov_proxy | heldout_2026_through_2026_08_07 | 3.05% | n/a | -7.43% | 0.47 | pareto_frontier | conditional_only |

## Evidence hierarchy

1. **Deployable now:** formal V9 70/30 only; no correlated AI-capex additions are justified by this synthesis.
2. **Strongest historical shadow:** RSR2, because it improves historical return, win rate, drawdown, Sharpe and profit factor versus the matched baseline; it still lacks transfer and forward proof.
3. **Retained mechanics:** current contention ranking and whole-position profit lock specification.
4. **Closed branches:** partial profit taking, winner extension, high-volatility sleeve and 80/20 shared-capital allocation.
5. **Operationally conditional:** residual-cash yield, after account-specific facts are verified.

## What would change the conclusion

- Immutable genuine-forward RSR1/RSR2 trades and closed outcomes.
- Mature five- and twenty-session opportunity outcomes.
- Independent forward contention decisions for the ranking rule.
- Verified broker/tax/settlement facts for cash yield.

No order, formal-rule change or real-account action is authorized by this report.
