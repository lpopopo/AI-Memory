#!/usr/bin/env python3
"""Audit and optionally rehearse the formal shadow-forward launch path."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FROZEN = ROOT / "results" / "shadow_portfolio" / "frozen"
FORWARD = ROOT / "results" / "shadow_portfolio" / "forward"
EVENTS = ROOT / "datasets" / "v9_information_events.json"
PYTHON = Path(r"D:\code\AI-Memory\domains\quant-strategy\.venv\Scripts\python.exe")


def count_reliable_events() -> dict:
    raw = json.loads(EVENTS.read_text(encoding="utf-8"))
    backfill_ids = set(raw.get("retrospective_backfill", {}).get("event_ids", []))
    reliable = [
        e for e in raw.get("events", [])
        if e.get("source_completeness", 0) >= 15 and e.get("event_id") not in backfill_ids
    ]
    return {
        "all_events": len(raw.get("events", [])),
        "reliable_point_in_time": len(reliable),
        "gate_50_met": len(reliable) >= 50,
        "source_health": raw.get("source_health"),
    }


def git_dirty() -> bool:
    repo = ROOT
    for _ in range(5):
        if (repo / ".git").exists():
            break
        repo = repo.parent
    else:
        return False
    result = subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True)
    return bool(result.stdout.strip())


def next_session_after_freeze(frozen_at_utc: str | None) -> str | None:
    if not frozen_at_utc:
        return None
    freeze_et = pd.Timestamp(frozen_at_utc).tz_convert("America/New_York")
    # First eligible completed session is the next NYSE close strictly after freeze.
    candidate = (freeze_et.normalize() + pd.Timedelta(days=1)).tz_localize(None)
    while candidate.weekday() >= 5:
        candidate += pd.Timedelta(days=1)
    return str(candidate.date())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rehearse-dry-run", action="store_true")
    parser.add_argument("--as-of", default=None)
    args = parser.parse_args()

    event_stats = count_reliable_events()
    manifest = {}
    if (FROZEN / "code_manifest.json").exists():
        manifest = json.loads((FROZEN / "code_manifest.json").read_text(encoding="utf-8"))

    initial_states = list((FORWARD / "accounts").glob("*/initial_state.json")) if FORWARD.exists() else []
    daily_states = list((FORWARD / "accounts").glob("*/20*_state.json")) if FORWARD.exists() else []
    first_as_of = next_session_after_freeze(manifest.get("frozen_at_utc"))

    audit = {
        "formal_forward_authorized": False,
        "blockers": [],
        "warnings": [],
        "prerequisites": {
            "venv_python_exists": PYTHON.exists(),
            "freeze_script_exists": (SCRIPTS / "freeze_v9_rule_e.py").exists(),
            "research_monitors_exist": (SCRIPTS / "v9_research_monitors.py").exists(),
            "frozen_dir_exists": FROZEN.exists(),
            "forward_dir_exists": FORWARD.exists(),
            "forward_eligible": bool(manifest.get("forward_eligible")),
            "dirty_worktree_at_freeze": bool(manifest.get("dirty_worktree")),
            "git_dirty_now": git_dirty(),
            "forward_initialized": len(initial_states) >= 4,
            "forward_daily_states": len(daily_states),
            "first_executable_as_of": first_as_of,
            "events": event_stats,
        },
    }

    if not PYTHON.exists():
        audit["blockers"].append("project venv python missing")
    if not (SCRIPTS / "v9_research_monitors.py").exists():
        audit["blockers"].append("research monitors missing from freeze set")
    if not FROZEN.exists():
        audit["blockers"].append("frozen artifacts missing; run freeze_v9_rule_e.py after clean commit")
    elif not manifest.get("forward_eligible"):
        audit["blockers"].append("frozen manifest is not forward_eligible")
    if len(initial_states) < 4:
        audit["blockers"].append("forward accounts not initialized; run run_v9_shadow.py --initialize")
    if event_stats["reliable_point_in_time"] < 50:
        audit["warnings"].append(
            f"only {event_stats['reliable_point_in_time']} reliable PIT events; Rule E statistical promotion blocked"
        )
    if audit["prerequisites"]["git_dirty_now"]:
        audit["warnings"].append("git worktree is dirty now; do not re-freeze until committed")

    if args.rehearse_dry_run:
        if args.as_of is None:
            audit["blockers"].append("--as-of required for dry-run rehearsal")
        elif not audit["blockers"]:
            cmd = [str(PYTHON), str(SCRIPTS / "run_v9_shadow.py"), "--dry-run", "--as-of", args.as_of]
            completed = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            audit["dry_run"] = {
                "returncode": completed.returncode,
                "stdout_tail": completed.stdout[-2000:],
                "stderr_tail": completed.stderr[-2000:],
            }
            if completed.returncode != 0:
                audit["blockers"].append("dry-run failed")

    launch_ready = (
        not audit["blockers"]
        and bool(manifest.get("forward_eligible"))
        and len(initial_states) >= 4
    )
    audit["formal_forward_authorized"] = launch_ready
    if launch_ready:
        audit["next_action"] = (
            f"Append-only formal forward is initialized. First executable completed session is {first_as_of}; "
            "do not backfill earlier dates. Rule E statistical promotion still waits for >=50 reliable PIT events."
        )
    else:
        audit["next_action"] = "Resolve blockers before formal forward launch."

    out = ROOT / "results" / "validation" / "shadow_forward_launch_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    if audit["blockers"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
