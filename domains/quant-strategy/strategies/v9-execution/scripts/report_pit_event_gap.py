#!/usr/bin/env python3
"""Report reliable PIT information-event counts against the Rule E statistical gate."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "datasets" / "v9_information_events.json"
FORWARD_LOG = ROOT / "results" / "shadow_portfolio" / "forward" / "shared" / "event_append_log.jsonl"
OUT = ROOT / "results" / "validation" / "pit_event_gap_report.json"


def main() -> None:
    raw = json.loads(EVENTS.read_text(encoding="utf-8"))
    backfill = set(raw.get("retrospective_backfill", {}).get("event_ids", []))
    events = raw.get("events", [])
    reliable = [
        e for e in events
        if int(e.get("source_completeness", 0)) >= 15 and e.get("event_id") not in backfill
    ]
    forward_appended = 0
    if FORWARD_LOG.exists():
        forward_appended = sum(1 for line in FORWARD_LOG.read_text(encoding="utf-8").splitlines() if line.strip())

    report = {
        "all_events": len(events),
        "retrospective_backfill": len(backfill),
        "reliable_point_in_time": len(reliable),
        "gate": 50,
        "gap_to_gate": max(0, 50 - len(reliable)),
        "forward_appended_events": forward_appended,
        "source_health": raw.get("source_health"),
        "cannot_reclassify_backfill": True,
        "note": "Forward appends power live shadow decisions; they do not auto-count toward the frozen statistical gate until curated into the archive with true first_seen_at.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
