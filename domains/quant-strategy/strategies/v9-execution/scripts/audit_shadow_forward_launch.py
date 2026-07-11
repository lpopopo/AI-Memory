#!/usr/bin/env python3
"""Audit and optionally rehearse the formal shadow-forward launch path."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rehearse-dry-run", action="store_true")
    parser.add_argument("--as-of", default=None)
    args = parser.parse_args()

    event_stats = count_reliable_events()
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
            "git_dirty": git_dirty(),
            "events": event_stats,
        },
    }

    if not PYTHON.exists():
        audit["blockers"].append("project venv python missing")
    if not (SCRIPTS / "v9_research_monitors.py").exists():
        audit["blockers"].append("research monitors missing from freeze set")
    if event_stats["reliable_point_in_time"] < 50:
        audit["warnings"].append(
            f"only {event_stats['reliable_point_in_time']} reliable PIT events; Rule E statistical promotion blocked"
        )
    if audit["prerequisites"]["git_dirty"]:
        audit["warnings"].append("git worktree is dirty; formal freeze should use a clean commit")
    if not FROZEN.exists():
        audit["blockers"].append("frozen artifacts missing; run freeze_v9_rule_e.py after clean commit")

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

    if not audit["blockers"]:
        audit["next_action"] = "After clean commit, freeze then init_forward_accounts and run append-only forward."
    else:
        audit["next_action"] = "Resolve blockers before formal forward launch."
        audit["formal_forward_authorized"] = False

    out = ROOT / "results" / "validation" / "shadow_forward_launch_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    if audit["blockers"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
