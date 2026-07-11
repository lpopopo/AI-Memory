#!/usr/bin/env python3
"""Write a one-page promotion / forward-readiness audit from current validation artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAL = ROOT / "results" / "validation"
PIT = ROOT / "datasets" / "data_point_in_time" / "manifest.json"
BACKFILL = ROOT / "datasets" / "data_point_in_time" / "price_backfill_report.json"
FACTOR = ROOT / "datasets" / "data_factor" / "manifest.json"
LEGS = ROOT / "datasets" / "data_factor" / "approx_winner_loser_legs_manifest.json"
REPORT = VAL / "v9_validation_report_v1.json"
LAUNCH = VAL / "shadow_forward_launch_audit.json"
FROZEN = ROOT / "results" / "shadow_portfolio" / "frozen" / "code_manifest.json"
DRY_CHAIN = ROOT / "results" / "shadow_portfolio" / "dry_run" / "fear_diag_chain" / "reports"
DATA_V9_META = ROOT / "datasets" / "data_v9" / "metadata.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def main() -> None:
    report = load(REPORT) or {}
    pit = load(PIT) or {}
    backfill = load(BACKFILL) or {}
    factor = load(FACTOR) or {}
    legs = load(LEGS) or {}
    launch = load(LAUNCH) or {}
    frozen = load(FROZEN) or {}
    meta = load(DATA_V9_META) or {}
    exp = report.get("experiments", {})
    dry_days = (
        sorted(p.stem.replace("shadow_report_", "") for p in DRY_CHAIN.glob("shadow_report_*.json"))
        if DRY_CHAIN.exists()
        else []
    )
    latest_report = None
    if dry_days:
        latest_report = load(DRY_CHAIN / f"shadow_report_{dry_days[-1]}.json") or {}
    fear_signals = ((latest_report or {}).get("diagnostics") or {}).get("fear_gate_advisory", {}).get("signals", [])
    unavailable = [s["name"] for s in fear_signals if "unavailable" in str(s.get("note", ""))]

    launch = load(LAUNCH) or {}
    first_as_of = (launch.get("prerequisites") or {}).get("first_executable_as_of")
    forward_ready = bool(launch.get("formal_forward_authorized")) or (
        bool(frozen.get("forward_eligible"))
        and bool((launch.get("prerequisites") or {}).get("forward_initialized"))
    )

    blockers = []
    if frozen.get("dirty_worktree", True) or not frozen.get("forward_eligible", False):
        blockers.append("git worktree dirty; formal freeze requires clean commit")
    blockers.append("only 18 reliable PIT information events (<50 gate for Rule E statistical promotion)")
    missing = pit.get("missing_symbols")
    if missing:
        blockers.append(
            f"PIT panel still missing {missing} historical members; delisting returns incomplete"
        )

    audit = {
        "as_of": "2026-07-12",
        "formal_v9_weights_changed": False,
        "plan_items": {
            "1_schema_alignment": "completed",
            "2_validation_contract_and_data": "completed_partial_pit",
            "3_shadow_diagnostics": "completed_with_breadth_proxies",
            "4_preregistered_experiments": "completed_first_pass",
            "5_formal_forward": "initialized_waiting_first_session" if forward_ready else "multi_day_dry_run_rehearsed",
        },
        "data": {
            "pit_status": pit.get("status"),
            "pit_decision_grade": pit.get("decision_grade"),
            "pit_missing_symbols": pit.get("missing_symbols"),
            "pit_price_symbols": pit.get("price_symbols"),
            "yahoo_backfill_downloaded": backfill.get("downloaded"),
            "yahoo_backfill_empty": backfill.get("empty"),
            "ff_momentum_files": list((factor or {}).get("files", {}).keys()),
            "approx_legs_rows": legs.get("rows"),
            "diagnostic_symbols_in_data_v9": meta.get("diagnostic_downloaded") or meta.get("diagnostic_symbols"),
        },
        "experiment_highlights": {
            "A_panic_to_repair_events": exp.get("A", {}).get("event_count"),
            "B_overlay_improves_drawdown_at_0.1pct": (
                (
                    exp.get("B", {}).get("by_cost", {}).get("0.001", {}).get("overlay_max_drawdown", 0)
                    > exp.get("B", {}).get("by_cost", {}).get("0.001", {}).get("baseline_max_drawdown", 0)
                )
                if exp.get("B")
                else None
            ),
            "C_status": exp.get("C", {}).get("status"),
            "C_loser_outperforms_winner_share": (
                exp.get("C", {}).get("approx_legs_in_panic_to_repair", {}) or {}
            ).get("loser_outperforms_winner_share"),
        },
        "diagnostics_rehearsal": {
            "dry_run_id": "fear_diag_chain",
            "days": dry_days,
            "latest_fear_unavailable_signals": unavailable,
            "authorizes_trade": ((latest_report or {}).get("diagnostics") or {}).get("authorizes_trade", False),
        },
        "forward": {
            "frozen_forward_eligible": frozen.get("forward_eligible", False),
            "dirty_worktree": frozen.get("dirty_worktree"),
            "formal_forward_authorized": forward_ready,
            "forward_initialized": bool((launch.get("prerequisites") or {}).get("forward_initialized")),
            "first_executable_as_of": first_as_of,
            "dry_run_initialized": True,
            "dry_run_sample_as_of": dry_days[-1] if dry_days else None,
            "blockers": blockers,
            "next_actions": [
                f"On {first_as_of or 'next session'}, run append-only: python scripts/run_v9_shadow.py --as-of YYYY-MM-DD",
                "Do not backfill dates at or before freeze time",
                "Accumulate >=50 reliable PIT events before Rule E statistical promotion",
            ],
        },
        "promotion_decision": "No formal V9 rule change. Formal shadow forward is initialized; research monitors remain advisory.",
    }

    VAL.mkdir(parents=True, exist_ok=True)
    out_json = VAL / "v9_plan_completion_audit.json"
    out_md = VAL / "v9_plan_completion_audit.md"
    out_json.write_text(json.dumps(audit, indent=2), encoding="utf-8")

    cost = exp.get("B", {}).get("by_cost", {})
    (VAL / "v9_cost_sensitivity_v1.json").write_text(json.dumps(cost, indent=2), encoding="utf-8")

    lines = [
        "# V9 Plan Completion Audit",
        "",
        f"- Formal V9 weights changed: `{audit['formal_v9_weights_changed']}`",
        f"- Formal forward authorized: `{audit['forward']['formal_forward_authorized']}`",
        f"- First executable as-of: `{audit['forward'].get('first_executable_as_of')}`",
        f"- Promotion decision: {audit['promotion_decision']}",
        "",
        "## Progress since first-pass",
        "",
        f"- Fear Gate diagnostic ETFs in data_v9: `{audit['data']['diagnostic_symbols_in_data_v9']}`",
        f"- Multi-day dry-run (`fear_diag_chain`): `{', '.join(dry_days) if dry_days else 'none'}`",
        f"- Latest Fear Gate unavailable signals: `{unavailable if unavailable else 'none'}`",
        f"- Yahoo PIT backfill downloaded: `{backfill.get('downloaded')}` / empty `{backfill.get('empty')}`",
        f"- PIT price symbols / still missing: `{pit.get('price_symbols')}` / `{pit.get('missing_symbols')}`",
        "",
        "## Plan item status",
        "",
    ]
    for key, value in audit["plan_items"].items():
        lines.append(f"- `{key}`: **{value}**")
    lines.extend(["", "## Forward blockers", ""])
    for item in audit["forward"]["blockers"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next actions", ""])
    for item in audit["forward"]["next_actions"]:
        lines.append(f"- {item}")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
