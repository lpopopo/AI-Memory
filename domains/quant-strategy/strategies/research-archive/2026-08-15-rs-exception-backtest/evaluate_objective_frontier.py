from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

OUTPUT_CSV = RESULTS / "objective_frontier_matrix.csv"
OUTPUT_JSON = RESULTS / "objective_frontier_summary.json"
OUTPUT_REPORT = RESULTS / "objective_frontier_report.md"

FIELDNAMES = [
    "family",
    "variant",
    "period",
    "initial_nav",
    "cost_assumption",
    "total_return",
    "win_rate",
    "win_rate_type",
    "max_drawdown",
    "sharpe",
    "profit_factor",
    "trade_count",
    "evidence_tier",
    "cross_period_status",
    "formal_status",
    "comparable_group",
    "pareto_status",
    "decision_priority",
    "notes",
    "source",
]

METRIC_SETS = {
    "stock_selection_exit": (
        "total_return",
        "win_rate",
        "max_drawdown",
        "sharpe",
        "profit_factor",
    ),
    "profit_realization": (
        "total_return",
        "win_rate",
        "max_drawdown",
        "sharpe",
        "profit_factor",
    ),
    "winner_extension": (
        "total_return",
        "win_rate",
        "max_drawdown",
        "sharpe",
        "profit_factor",
    ),
    "entry_ranking": (
        "total_return",
        "win_rate",
        "max_drawdown",
        "sharpe",
        "profit_factor",
    ),
    "shared_capital": ("total_return", "win_rate", "max_drawdown", "sharpe"),
    "high_volatility_sleeve": (
        "total_return",
        "win_rate",
        "max_drawdown",
        "sharpe",
        "profit_factor",
    ),
    "core_only_allocation": (
        "total_return",
        "win_rate",
        "max_drawdown",
        "sharpe",
    ),
    "combined_2026_architecture": ("total_return", "max_drawdown", "sharpe"),
}


def read_rows(filename: str) -> list[dict[str, str]]:
    with (RESULTS / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select_one(rows: list[dict[str, str]], **criteria: object) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if all(str(row.get(key, "")) == str(value) for key, value in criteria.items())
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one row for {criteria}, found {len(matches)}")
    return matches[0]


def number(value: object) -> float | None:
    text = str(value or "").strip()
    return None if not text else float(text)


def make_row(
    *,
    family: str,
    variant: str,
    period: str,
    source: str,
    raw: dict[str, str],
    comparable_group: str,
    evidence_tier: str,
    cross_period_status: str,
    formal_status: str,
    decision_priority: str,
    notes: str,
    nav_field: str | None = None,
    cost_assumption: str = "",
    return_field: str = "total_return",
    win_field: str | None = "win_rate",
    win_rate_type: str = "trade",
    drawdown_field: str = "max_drawdown",
    sharpe_field: str = "sharpe",
    profit_factor_field: str | None = "profit_factor",
    trade_count_field: str | None = "trade_count",
) -> dict[str, object]:
    return {
        "family": family,
        "variant": variant,
        "period": period,
        "initial_nav": number(raw.get(nav_field)) if nav_field else None,
        "cost_assumption": cost_assumption,
        "total_return": number(raw.get(return_field)),
        "win_rate": number(raw.get(win_field)) if win_field else None,
        "win_rate_type": win_rate_type if win_field else "unavailable",
        "max_drawdown": number(raw.get(drawdown_field)),
        "sharpe": number(raw.get(sharpe_field)),
        "profit_factor": number(raw.get(profit_factor_field))
        if profit_factor_field
        else None,
        "trade_count": number(raw.get(trade_count_field)) if trade_count_field else None,
        "evidence_tier": evidence_tier,
        "cross_period_status": cross_period_status,
        "formal_status": formal_status,
        "comparable_group": comparable_group,
        "pareto_status": "",
        "decision_priority": decision_priority,
        "notes": notes,
        "source": source,
    }


def dominates(a: dict[str, object], b: dict[str, object], metrics: tuple[str, ...]) -> bool:
    values = [(number(a.get(metric)), number(b.get(metric))) for metric in metrics]
    if any(left is None or right is None for left, right in values):
        raise RuntimeError(f"missing Pareto metric in {a['comparable_group']}: {metrics}")
    return all(left >= right for left, right in values) and any(
        left > right for left, right in values
    )


def assign_pareto_status(rows: list[dict[str, object]]) -> None:
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row["comparable_group"])].append(row)
    for candidates in groups.values():
        if len(candidates) == 1:
            candidates[0]["pareto_status"] = "descriptive_single_candidate"
            continue
        metrics = METRIC_SETS[str(candidates[0]["family"])]
        for candidate in candidates:
            candidate["pareto_status"] = (
                "dominated"
                if any(
                    other is not candidate and dominates(other, candidate, metrics)
                    for other in candidates
                )
                else "pareto_frontier"
            )


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    protection = read_rows("profit_protection_metrics.csv")
    stock_specs = [
        (
            "matched_baseline",
            {"period": "full", "slippage": "0.001", "overlay": "frozen", "filter": "matched_baseline"},
            "reference_only",
            "matched reference; not a deployment proposal",
            "reference portfolio",
        ),
        (
            "RSR1",
            {"period": "full", "slippage": "0.001", "overlay": "frozen", "filter": "risk_filter"},
            "observe_forward",
            "frozen shadow only; no promotion",
            "exact point-in-time transfer failed and selection bias remains uncontained",
        ),
        (
            "RSR2",
            {"period": "full", "slippage": "0.001", "overlay": "lock_15_to_5", "filter": "risk_filter"},
            "historical_leader_forward_unproven",
            "separate frozen shadow only; no promotion",
            "best current-list historical metrics; direct exit effect exists in only two trades",
        ),
    ]
    for variant, criteria, priority, status, notes in stock_specs:
        raw = select_one(protection, **criteria)
        rows.append(
            make_row(
                family="stock_selection_exit",
                variant=variant,
                period="full_2024_2026",
                source="profit_protection_metrics.csv",
                raw=raw,
                comparable_group="stock_selection_exit|full|nav6000|10bps",
                evidence_tier="retrospective_current_list",
                cross_period_status=(
                    "reference" if variant == "matched_baseline" else "failed_exact_transfer_and_no_forward_trades"
                ),
                formal_status=status,
                decision_priority=priority,
                notes=notes,
                nav_field="initial_nav",
                cost_assumption="10bps slippage",
            )
        )

    scaleout = read_rows("partial_profit_scaleout_metrics.csv")
    for variant, priority, status, notes in [
        (
            "RSR2",
            "retain_whole_position_lock",
            "frozen profit-lock shadow",
            "profit-and-win objective leader",
        ),
        (
            "partial_half_at_15",
            "reject",
            "rejected overlay",
            "smoother drawdown and higher Sharpe, but lower return and win rate",
        ),
    ]:
        raw = select_one(
            scaleout,
            initial_nav="6000.0",
            slippage="0.001",
            period_name="full",
            variant_name=variant,
        )
        rows.append(
            make_row(
                family="profit_realization",
                variant=variant,
                period="full_2024_2026",
                source="partial_profit_scaleout_metrics.csv",
                raw=raw,
                comparable_group="profit_realization|full|nav6000|10bps",
                evidence_tier="retrospective_current_list",
                cross_period_status="partial_overlay_did_not_improve_profit_objective",
                formal_status=status,
                decision_priority=priority,
                notes=notes,
                nav_field="initial_nav",
                cost_assumption="10bps slippage",
            )
        )

    extension = read_rows("winner_extension_metrics.csv")
    for variant, priority, status, notes in [
        (
            "rsr2_frozen",
            "retain_frozen_exit",
            "frozen profit-lock shadow",
            "stable choice after cross-period review",
        ),
        (
            "extend30_any_winner",
            "reject",
            "rejected extension",
            "full-period return edge reverses in 2024-2025 and worsens drawdown/win rate",
        ),
        (
            "extend40_gain8",
            "reject",
            "rejected extension",
            "dominated full-period risk/return and unstable across periods",
        ),
    ]:
        raw = select_one(extension, variant=variant, period="full", cost_bps="10")
        rows.append(
            make_row(
                family="winner_extension",
                variant=variant,
                period="full_2024_2026",
                source="winner_extension_metrics.csv",
                raw=raw,
                comparable_group="winner_extension|full|nav6000|10bps",
                evidence_tier="retrospective_current_list_cross_period_checked",
                cross_period_status=(
                    "retained_across_period_review" if variant == "rsr2_frozen" else "failed_development_stability"
                ),
                formal_status=status,
                decision_priority=priority,
                notes=notes,
                cost_assumption="10bps",
            )
        )

    ranking = read_rows("capital_constrained_ranking_metrics.csv")
    for variant in ["formal_composite", "rs_only", "low_atr_first", "balanced_rank"]:
        raw = select_one(
            ranking,
            initial_nav="6000.0",
            slippage="0.001",
            period="development_2024_2025",
            policy=variant,
        )
        rows.append(
            make_row(
                family="entry_ranking",
                variant=variant,
                period="development_2024_2025",
                source="capital_constrained_ranking_metrics.csv",
                raw=raw,
                comparable_group="entry_ranking|development|nav6000|10bps",
                evidence_tier="historical_development_with_short_heldout",
                cross_period_status="heldout_2026_had_zero_contention_decisions",
                formal_status=("retain current ordering" if variant == "formal_composite" else "challenger rejected or insufficient"),
                decision_priority=("retain" if variant == "formal_composite" else "reject_or_insufficient"),
                notes=("highest development return and win rate" if variant == "formal_composite" else "no heldout conflict evidence to displace formal ordering"),
                nav_field="initial_nav",
                cost_assumption="10bps slippage",
            )
        )

    shared = read_rows("shared_capital_architecture_metrics.csv")
    for period in ["train_2024_2025", "heldout_2026", "full_2024_2026"]:
        for variant in ["formal_70_25", "challenger_80_20"]:
            raw = select_one(shared, initial_nav="6000.0", period=period, architecture=variant)
            rows.append(
                make_row(
                    family="shared_capital",
                    variant=variant,
                    period=period,
                    source="shared_capital_architecture_metrics.csv",
                    raw=raw,
                    comparable_group=f"shared_capital|{period}|nav6000",
                    evidence_tier=("short_heldout" if period == "heldout_2026" else "historical_multi_period"),
                    cross_period_status=(
                        "dominates_train_and_full; loses_short_heldout_return"
                        if variant == "formal_70_25"
                        else "wins_short_heldout_only; loses_train_and_full"
                    ),
                    formal_status=("retain formal 70/30 architecture" if variant == "formal_70_25" else "challenger rejected"),
                    decision_priority=("retain_deployable_architecture" if variant == "formal_70_25" else "reject"),
                    notes=("stock sleeve cap is 25%; residual cash remains explicit" if variant == "formal_70_25" else "20% stock cap omitted four development trades"),
                    nav_field="initial_nav",
                    win_field="monthly_win_rate",
                    win_rate_type="monthly",
                    profit_factor_field=None,
                    trade_count_field="closed_stock_trades",
                )
            )

    high_vol = read_rows("high_vol_portfolio_metrics.csv")
    for period in ["development_2024_2025", "retrospective_2026"]:
        raw = select_one(high_vol, period=period, cost_bps="10")
        rows.append(
            make_row(
                family="high_volatility_sleeve",
                variant="registered_high_vol_sleeve",
                period=period,
                source="high_vol_portfolio_metrics.csv",
                raw=raw,
                comparable_group=f"high_volatility_sleeve|{period}|10bps",
                evidence_tier=("historical_development" if period.startswith("development") else "short_retrospective_2026"),
                cross_period_status="inconsistent_development_vs_2026",
                formal_status="rejected as sleeve; diagnostic only",
                decision_priority="reject",
                notes="development win rate and Sharpe are too weak to support the 2026 appearance",
                cost_assumption="10bps",
            )
        )

    core = read_rows("core_allocation_frontier_metrics.csv")
    for cap in ["0.7", "0.8"]:
        raw = select_one(core, period="full_2006_2025", core_cap=cap)
        variant = f"core_{int(float(cap) * 100)}"
        rows.append(
            make_row(
                family="core_only_allocation",
                variant=variant,
                period="full_2006_2025",
                source="core_allocation_frontier_metrics.csv",
                raw=raw,
                comparable_group="core_only_allocation|full_2006_2025",
                evidence_tier="historical_multi_period_core_only",
                cross_period_status=("formal_reference" if cap == "0.7" else "passed_core_only_but_failed_shared_capital"),
                formal_status=("formal 70% core retained" if cap == "0.7" else "80% challenger superseded and rejected"),
                decision_priority=("retain_deployable_architecture" if cap == "0.7" else "local_frontier_not_deployable"),
                notes=("formal core ceiling" if cap == "0.7" else "local return edge does not survive shared cash and stock capacity"),
                win_field="monthly_win_rate",
                win_rate_type="monthly",
                profit_factor_field=None,
                trade_count_field=None,
            )
        )

    combined = read_rows("combined_v9_portfolio_metrics.csv")
    for variant in [
        "v9_core_70",
        "v9_core_plus_rsr1",
        "v9_core_plus_rsr2",
        "v9_core_plus_rsr1_sgov_proxy",
        "v9_core_plus_rsr2_sgov_proxy",
    ]:
        raw = select_one(combined, portfolio=variant)
        is_sgov = variant.endswith("sgov_proxy")
        rows.append(
            make_row(
                family="combined_2026_architecture",
                variant=variant,
                period="heldout_2026_through_2026_08_07",
                source="combined_v9_portfolio_metrics.csv",
                raw=raw,
                comparable_group="combined_2026_architecture|heldout_2026|nav6000",
                evidence_tier=("conditional_proxy" if is_sgov else "short_heldout_with_three_stock_trades"),
                cross_period_status="short_2026_only; not a promotion sample",
                formal_status=("operationally conditional; no order" if is_sgov else "research comparison only"),
                decision_priority=("conditional_only" if is_sgov else "no_change"),
                notes=("requires broker, tax, settlement and liquidity facts" if is_sgov else "stock sleeve has only three historical 2026 trades"),
                win_field=None,
                profit_factor_field=None,
                trade_count_field=None,
            )
        )

    assign_pareto_status(rows)
    return rows


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    frontiers = [
        {
            "family": row["family"],
            "variant": row["variant"],
            "period": row["period"],
            "evidence_tier": row["evidence_tier"],
            "decision_priority": row["decision_priority"],
        }
        for row in rows
        if row["pareto_status"] == "pareto_frontier"
    ]
    return {
        "research_only": True,
        "formal_v9_modified": False,
        "real_account_modified": False,
        "live_order_authorization": False,
        "new_parameter_search": False,
        "comparability_rule": "Pareto dominance is computed only within fixed family-period-NAV-cost groups.",
        "row_count": len(rows),
        "comparable_group_count": len({str(row["comparable_group"]) for row in rows}),
        "pareto_frontier_rows": frontiers,
        "best_historical_multi_objective_candidate": {
            "variant": "RSR2",
            "return": 0.18106117055994786,
            "win_rate": 0.6956521739130435,
            "max_drawdown": -0.023258890167864976,
            "status": "frozen shadow leader; not promoted",
            "evidence_gap": "exact point-in-time transfer failed, selection bias remains uncontained, and genuine-forward signals/trades are zero through 2026-08-20",
        },
        "best_deployable_architecture": {
            "variant": "formal V9 70/30",
            "stock_sleeve_action": "no correlated additions",
            "status": "unchanged",
            "reason": "80/20 loses on train/full shared-capital replay and omits stock opportunities; equity challengers lack forward proof",
        },
        "retained": [
            "formal V9 70/30 shared-capital architecture",
            "current RS-plus-volume contention ordering",
            "whole-position RSR2 profit-lock specification as a frozen shadow",
        ],
        "rejected": [
            "automatic RSR2 half-position scale-out",
            "conditional winner extension",
            "high-volatility sleeve",
            "80/20 shared-capital challenger",
        ],
        "conditional": [
            "residual-cash yield only after broker, tax, settlement, fee and liquidity verification"
        ],
        "interpretation": [
            "Historical RSR2 has the strongest return-win-drawdown combination on the current-list sample.",
            "Its evidence strength is insufficient for formal or live promotion.",
            "A Pareto label is descriptive and never overrides cross-period failure or governance gates.",
            "The next useful evidence is immutable forward trades and matured opportunity outcomes, not another historical parameter search.",
        ],
    }


def write_outputs(rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    OUTPUT_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Win-rate, profit, drawdown and evidence frontier",
        "",
        "## Bottom line",
        "",
        "**Best historical multi-objective candidate: RSR2. Best currently deployable architecture: unchanged formal V9 70/30, with no correlated additions.**",
        "",
        "RSR2's full current-list replay returned 18.11%, won 69.57% of 23 trades and drew down 2.33%. That is the strongest historical stock-sleeve combination in the registered family, but it is not a live conclusion: the exact point-in-time transfer screen failed, selection bias remains uncontained, and the first four genuine-forward sessions contain zero signals/trades.",
        "",
        "## Decision matrix",
        "",
        "| Family | Retain / observe | Reject / supersede | Why |",
        "| --- | --- | --- | --- |",
        "| Stock selection and exit | Observe RSR2 as a frozen shadow | Do not promote RSR1/RSR2 | Historical dominance is offset by transfer, selection-bias and forward-sample gaps |",
        "| Profit realization | Whole-position RSR2 lock | Half-position scale-out | Scale-out improves DD/Sharpe but lowers return and win rate |",
        "| Winner extension | Frozen RSR2 exit | 30/40-day extensions | The apparent full-period edge fails development stability |",
        "| Entry ranking | Current RS-plus-volume ordering | RS-only, low-ATR-first, balanced challenger | Formal rank has best development return/win; heldout has zero contentions |",
        "| Shared capital | Formal 70/30 | 80/20 challenger | Formal wins train/full with better DD/Sharpe and preserves stock capacity |",
        "| High volatility | Diagnostic only | Tradable sleeve | 17.65% development win rate and 0.32 Sharpe do not support the 2026 appearance |",
        "| Residual cash | Conditional yield review | Automatic SGOV order | Proxy helps, but account mechanics are unverified |",
        "",
        "## Comparable Pareto results",
        "",
        "Pareto labels below are calculated only within the same family, period, NAV and cost group. They are not ranked across incompatible experiments.",
        "",
        "| Family | Variant | Period | Return | Win rate | Max DD | Sharpe | Pareto | Evidence / decision |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        if row["pareto_status"] == "dominated":
            continue
        win = "n/a" if row["win_rate"] is None else f"{float(row['win_rate']):.2%}"
        lines.append(
            f"| {row['family']} | {row['variant']} | {row['period']} | "
            f"{float(row['total_return']):.2%} | {win} | {float(row['max_drawdown']):.2%} | "
            f"{float(row['sharpe']):.2f} | {row['pareto_status']} | {row['decision_priority']} |"
        )
    lines.extend(
        [
            "",
            "## Evidence hierarchy",
            "",
            "1. **Deployable now:** formal V9 70/30 only; no correlated AI-capex additions are justified by this synthesis.",
            "2. **Strongest historical shadow:** RSR2, because it improves historical return, win rate, drawdown, Sharpe and profit factor versus the matched baseline; it still lacks transfer and forward proof.",
            "3. **Retained mechanics:** current contention ranking and whole-position profit lock specification.",
            "4. **Closed branches:** partial profit taking, winner extension, high-volatility sleeve and 80/20 shared-capital allocation.",
            "5. **Operationally conditional:** residual-cash yield, after account-specific facts are verified.",
            "",
            "## What would change the conclusion",
            "",
            "- Immutable genuine-forward RSR1/RSR2 trades and closed outcomes.",
            "- Mature five- and twenty-session opportunity outcomes.",
            "- Independent forward contention decisions for the ranking rule.",
            "- Verified broker/tax/settlement facts for cash yield.",
            "",
            "No order, formal-rule change or real-account action is authorized by this report.",
        ]
    )
    OUTPUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    summary = build_summary(rows)
    write_outputs(rows, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
