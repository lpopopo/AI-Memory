from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

DECISION_REGISTER = RESULTS / "research_decision_register.md"
FORWARD_STATUS = RESULTS / "forward_shadow_status.json"
OPPORTUNITY_STATUS = RESULTS / "forward_opportunity_outcomes.json"
SELECTION_STATUS = RESULTS / "selection_bias_audit_summary.json"
PIT_EXACT_STATUS = RESULTS / "pit_exact_filter_summary.json"
POWER_STATUS = RESULTS / "forward_power_duration_summary.json"
RISK_ACTION_STATUS = RESULTS / "forward_risk_action_counterfactual.json"
OBJECTIVE_FRONTIER_STATUS = RESULTS / "objective_frontier_summary.json"
HISTORICAL_UNCERTAINTY_STATUS = RESULTS / "historical_uncertainty_audit.json"
MECHANISM_CLOCK_STATUS = RESULTS / "forward_mechanism_evidence_clock.json"

HISTORICAL_CLOSED = {
    "Below-SMH-MA50 relative-strength exception",
    "Breadth repair exception",
    "Fixed profit target",
    "Conditional winner extension",
    "High-volatility trend sleeve",
    "V9 two-month exit confirmation",
    "Increase stock-sleeve allocation",
    "V9 index-core ceiling",
    "Point-in-time low-volatility proxy",
    "Point-in-time exact ATR/close-location transfer",
    "ATR/close-location parameter-selection bias",
    "Capital-constrained entry ranking",
    "RSR2 half-position profit taking",
}
FROZEN_FORWARD = {
    "RSR1 ATR + close-location filter",
    "RSR2 +15%/+5% profit lock",
}
RETAINED_CONTROLS = {
    "Backtest implementation integrity",
    "Economic edge and opportunity-cost decomposition",
    "Forward economic-edge attribution",
    "Forward zero-signal bottleneck",
    "RSR1 position weight",
    "Forward economic-evidence scorecard",
    "Forward statistical power and duration",
    "Forward risk-action counterfactual",
    "Multi-objective evidence frontier",
    "Historical edge uncertainty audit",
    "Forward mechanism evidence clock",
}
EXTERNAL_CONDITIONAL = {"Residual-cash yield"}


def parse_decision_branches(text: str) -> set[str]:
    branches = set()
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] in {"Branch", "---"}:
            continue
        branches.add(cells[0])
    return branches


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def count_closed_trades(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(
            1
            for row in csv.DictReader(handle)
            if (row.get("exit_date") or "").strip()
        )


def closed_trades_from_status(
    status: dict, gate_name: str, ledger_name: str
) -> int:
    gate = status.get(gate_name)
    if isinstance(gate, dict) and "closed_trades" in gate:
        return int(gate["closed_trades"])
    return count_closed_trades(RESULTS / ledger_name)


def evaluate() -> dict:
    branches = parse_decision_branches(DECISION_REGISTER.read_text(encoding="utf-8"))
    expected = HISTORICAL_CLOSED | FROZEN_FORWARD | RETAINED_CONTROLS | EXTERNAL_CONDITIONAL
    missing = sorted(expected - branches)
    unclassified = sorted(branches - expected)
    if missing or unclassified:
        raise RuntimeError(
            f"decision register classification incomplete: missing={missing}, unclassified={unclassified}"
        )

    forward = load_json(FORWARD_STATUS)
    opportunity = load_json(OPPORTUNITY_STATUS)
    selection = load_json(SELECTION_STATUS)
    pit_exact = load_json(PIT_EXACT_STATUS)
    power = load_json(POWER_STATUS)
    risk_action = load_json(RISK_ACTION_STATUS)
    objective_frontier = load_json(OBJECTIVE_FRONTIER_STATUS)
    historical_uncertainty = load_json(HISTORICAL_UNCERTAINTY_STATUS)
    mechanism_clock = load_json(MECHANISM_CLOCK_STATUS)

    opportunity_rows = opportunity.get("summary", [])
    matured = sum(int(row.get("matured_primary_episodes", 0)) for row in opportunity_rows)
    forward_sessions = int(forward.get("sessions", 0))
    rsr1_closed = closed_trades_from_status(
        forward, "promotion_gate", "forward_shadow_ledger.csv"
    )
    rsr2_closed = closed_trades_from_status(
        forward,
        "profit_protection_promotion_gate",
        "forward_profit_protection_ledger.csv",
    )

    checks = {
        "all_registered_branches_classified": not missing and not unclassified,
        "point_in_time_transfer_failed": not bool(
            pit_exact.get("transferability_screen_passed", True)
        ),
        "selection_bias_not_contained": not bool(
            selection.get("gate", {}).get("contained", True)
        ),
        "genuine_forward_below_126_sessions": forward_sessions < 126,
        "genuine_forward_below_20_closed_trades": (
            rsr1_closed < 20 or rsr2_closed < 20
        ),
        "opportunity_outcomes_not_mature": matured == 0,
        "twenty_trade_clock_is_binding": bool(
            power.get("interpretation", {}).get("twenty_trade_gate_is_binding_clock", False)
        ),
        "promotion_gate_unchanged": not bool(power.get("changes_promotion_gate", True)),
        "risk_action_is_measurement_only": bool(risk_action.get("research_only", False))
        and not bool(risk_action.get("formal_v9_modified", True))
        and not bool(risk_action.get("real_account_modified", True))
        and not bool(risk_action.get("live_order_authorization", True)),
        "risk_action_has_no_forward_policy_selection": not bool(
            risk_action.get("genuine_forward_policy_selection_available", True)
        ),
        "objective_frontier_is_synthesis_only": bool(
            objective_frontier.get("research_only", False)
        )
        and not bool(objective_frontier.get("new_parameter_search", True))
        and not bool(objective_frontier.get("formal_v9_modified", True))
        and not bool(objective_frontier.get("real_account_modified", True))
        and not bool(objective_frontier.get("live_order_authorization", True)),
        "objective_frontier_separates_historical_and_deployable": (
            objective_frontier.get("best_historical_multi_objective_candidate", {}).get("variant")
            == "RSR2"
            and objective_frontier.get("best_deployable_architecture", {}).get("variant")
            == "formal V9 70/30"
        ),
        "historical_uncertainty_is_measurement_only": bool(
            historical_uncertainty.get("research_only", False)
        )
        and not bool(historical_uncertainty.get("new_parameter_search", True))
        and not bool(historical_uncertainty.get("formal_v9_modified", True))
        and not bool(historical_uncertainty.get("real_account_modified", True))
        and not bool(historical_uncertainty.get("live_order_authorization", True)),
        "historical_uncertainty_keeps_rsr2_sparse": (
            historical_uncertainty.get("rsr2_paired_delta", {}).get("evidence_label")
            == "directional_but_sparse"
        ),
        "mechanism_clock_is_peek_safe_measurement": bool(
            mechanism_clock.get("research_only", False)
        )
        and not bool(mechanism_clock.get("changes_promotion_gate", True))
        and not bool(mechanism_clock.get("new_parameter_search", True))
        and not bool(mechanism_clock.get("formal_v9_modified", True))
        and not bool(mechanism_clock.get("real_account_modified", True))
        and not bool(mechanism_clock.get("live_order_authorization", True)),
        "mechanism_clock_has_fixed_checkpoints": (
            mechanism_clock.get("checkpoints", {}).get("entry_quality") == [5, 10, 20]
            and mechanism_clock.get("checkpoints", {}).get("paired_rsr2") == [5, 10, 20]
            and mechanism_clock.get("checkpoints", {}).get("changed_exit_diagnostic")
            == [1, 2, 5]
        ),
    }
    return {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "as_of": forward.get("as_of"),
        "historical_research_saturated": bool(all(checks.values())),
        "forward_validation_complete": False,
        "new_historical_parameter_search_authorized": False,
        "branch_counts": {
            "historical_closed": len(HISTORICAL_CLOSED),
            "frozen_forward": len(FROZEN_FORWARD),
            "retained_controls": len(RETAINED_CONTROLS),
            "external_conditional": len(EXTERNAL_CONDITIONAL),
            "total": len(branches),
        },
        "branches": {
            "historical_closed": sorted(HISTORICAL_CLOSED),
            "frozen_forward": sorted(FROZEN_FORWARD),
            "retained_controls": sorted(RETAINED_CONTROLS),
            "external_conditional": sorted(EXTERNAL_CONDITIONAL),
        },
        "forward_state": {
            "sessions": forward_sessions,
            "closed_trades_by_variant": {
                "RSR1-shadow": rsr1_closed,
                "RSR2-profit-lock-shadow": rsr2_closed,
            },
            "matured_opportunity_outcomes": matured,
            "risk_action_events": risk_action.get("event_counts", {}),
        },
        "checks": checks,
        "next_evidence": [
            {
                "milestone": "latest completed session",
                "condition": "append only after a fully completed and validated U.S. session",
            },
            {
                "milestone": "first 5-session opportunity outcomes",
                "condition": "five later completed sessions after the earliest 2026-08-17 episode; expected no earlier than 2026-08-24",
            },
            {
                "milestone": "first 20-session opportunity outcomes",
                "condition": "twenty later completed sessions after the earliest episode; expected around mid-September 2026",
            },
            {
                "milestone": "risk-action fixed horizons",
                "condition": "append genuine-forward reviews before their next open and wait for fixed 1/5/20-session marks; never pool the descriptive as-of mark",
            },
            {
                "milestone": "calendar minimum",
                "condition": "126 completed forward sessions; approximately mid-February 2027",
            },
            {
                "milestone": "trade-count minimum",
                "condition": "20 closed candidate trades; historical-rate expectation about 573 sessions / 2.3 years",
            },
        ],
        "reopen_policy": [
            "new independent mechanism plus genuinely fresh data",
            "preregister before observing the new outcome",
            "separate ledger and version; no backfill",
            "no formal or live change without the original governance gates",
        ],
    }


def write_report(summary: dict) -> None:
    counts = summary["branch_counts"]
    state = summary["forward_state"]
    lines = [
        "# Strategy research saturation and forward-evidence roadmap",
        "",
        "## Bottom line",
        "",
        "The currently available historical research is **saturated**: every registered branch is classified, the strongest survivorship-bias follow-up failed, and the multiple-testing concern remains uncontained.",
        "This does not complete strategy validation. It means the next decisive information must come from new forward sessions, not another parameter search on the same history.",
        "",
        "## Branch inventory",
        "",
        f"- Historical branches closed or rejected: {counts['historical_closed']}",
        f"- Frozen forward shadows: {counts['frozen_forward']}",
        f"- Retained measurement/control layers: {counts['retained_controls']}",
        f"- External-account conditional items: {counts['external_conditional']}",
        f"- Total classified branches: {counts['total']}",
        "",
        "## Current forward state",
        "",
        f"- As of completed session: {summary['as_of']}",
        f"- Forward sessions: {state['sessions']}",
        f"- Closed RSR1 shadow trades: {state['closed_trades_by_variant']['RSR1-shadow']}",
        f"- Closed RSR2 shadow trades: {state['closed_trades_by_variant']['RSR2-profit-lock-shadow']}",
        f"- Matured 5/20-session opportunity outcomes: {state['matured_opportunity_outcomes']}",
        f"- Risk-action retrospective / genuine-forward events: {state['risk_action_events'].get('retrospective_seed', 0)} / {state['risk_action_events'].get('genuine_forward', 0)}",
        "",
        "## What is no longer an admissible next step",
        "",
        "- Searching nearby ATR, close-location, stop, hold or ranking parameters.",
        "- Deleting inactive time blocks or redrawing historical periods.",
        "- Expanding the universe merely to reach twenty trades faster.",
        "- Reopening AAOI/high-volatility, 80/20, delayed-core-exit or partial-profit branches because of one later outcome.",
        "",
        "## Forward evidence roadmap",
        "",
        "| Milestone | Condition |",
        "| --- | --- |",
    ]
    for item in summary["next_evidence"]:
        lines.append(f"| {item['milestone']} | {item['condition']} |")
    lines.extend(
        [
            "",
            "## Reopen policy",
            "",
        ]
    )
    for item in summary["reopen_policy"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Freeze the historical research tree. Continue deterministic forward collection, opportunity-outcome maturation and economic scorecards. "
            "Formal V9, RSR1, RSR2 and the real account remain unchanged; no order is authorized.",
        ]
    )
    (RESULTS / "research_saturation_roadmap.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    summary = evaluate()
    (RESULTS / "research_saturation_roadmap.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_report(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
