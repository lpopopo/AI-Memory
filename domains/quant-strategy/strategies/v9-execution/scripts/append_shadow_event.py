#!/usr/bin/env python3
"""Append a newly observed information event to a shadow event hash chain.

Never edits the frozen baseline snapshot. Use for dry-run or formal forward only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from shadow_integrity import TamperAlarmException, digest  # noqa: E402

SHADOW = ROOT / "results" / "shadow_portfolio"
FROZEN = SHADOW / "frozen"
BASELINE = FROZEN / "baseline_event_snapshot.json"

REQUIRED = (
    "event_id",
    "source",
    "author",
    "post_id",
    "first_seen_at",
    "content_summary",
    "theme",
    "symbols",
    "source_completeness",
    "thesis_novelty",
    "fundamental_validation",
    "crowding_penalty",
)


def validate_event(event: dict, known_ids: set[str]) -> dict:
    missing = [k for k in REQUIRED if k not in event]
    if missing:
        raise ValueError(f"missing fields: {missing}")
    event_id = str(event["event_id"]).strip()
    if not event_id:
        raise ValueError("empty event_id")
    if event_id in known_ids:
        raise TamperAlarmException(f"event_id already known: {event_id}")
    symbols = event["symbols"]
    if not isinstance(symbols, list) or not symbols or len(set(symbols)) != len(symbols):
        raise ValueError("symbols must be a non-empty unique list")
    for key in ("source_completeness", "thesis_novelty", "fundamental_validation", "crowding_penalty"):
        value = int(event[key])
        if not 0 <= value <= 20:
            raise ValueError(f"{key} out of range: {value}")
        event[key] = value
    # Normalize timestamps and content hash.
    first_seen = pd.Timestamp(event["first_seen_at"])
    event["first_seen_at"] = first_seen.isoformat()
    if event.get("published_at"):
        event["published_at"] = pd.Timestamp(event["published_at"]).isoformat()
    summary = str(event["content_summary"])
    digest_hex = hashlib.sha256(summary.encode("utf-8")).hexdigest()
    if event.get("content_hash") and event["content_hash"] != digest_hex:
        raise ValueError("content_hash does not match content_summary")
    event["content_hash"] = digest_hex
    event["symbols"] = [str(s).strip().upper() for s in symbols]
    return event


def known_event_ids(mode_dir: Path) -> set[str]:
    known: set[str] = set()
    if BASELINE.exists():
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        known.update(row["event_id"] for row in baseline.get("events", []))
    append_path = mode_dir / "shared" / "event_append_log.jsonl"
    if append_path.exists():
        for line in append_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                known.add(json.loads(line)["event"]["event_id"])
    return known


def last_event_hash(mode_dir: Path) -> str:
    append_path = mode_dir / "shared" / "event_append_log.jsonl"
    previous = ""
    if not append_path.exists():
        return previous
    for line in append_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        expected = digest({"previous_event_hash": previous, "event": record["event"]})
        if record.get("previous_event_hash", "") != previous or record.get("event_hash") != expected:
            raise TamperAlarmException("broken event append chain")
        previous = record["event_hash"]
    return previous


def append_event(mode_dir: Path, event: dict) -> dict:
    mode_dir.mkdir(parents=True, exist_ok=True)
    shared = mode_dir / "shared"
    shared.mkdir(parents=True, exist_ok=True)
    append_path = shared / "event_append_log.jsonl"
    event = validate_event(event, known_event_ids(mode_dir))
    previous = last_event_hash(mode_dir)
    event_hash = digest({"previous_event_hash": previous, "event": event})
    record = {"previous_event_hash": previous, "event_hash": event_hash, "event": event}
    with append_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--forward", action="store_true", help="Append into formal forward log")
    parser.add_argument("--dry-run-id", default=None, help="Append into dry_run/<id> log")
    parser.add_argument("--event-json", required=True, help="Path to a single-event JSON object")
    args = parser.parse_args()

    if args.forward == bool(args.dry_run_id):
        raise SystemExit("choose exactly one of --forward or --dry-run-id")
    if not FROZEN.exists():
        raise SystemExit("frozen artifacts missing; freeze before appending events")

    mode_dir = SHADOW / "forward" if args.forward else SHADOW / "dry_run" / args.dry_run_id
    event = json.loads(Path(args.event_json).read_text(encoding="utf-8"))
    if "event" in event and isinstance(event["event"], dict):
        event = event["event"]
    record = append_event(mode_dir, event)
    print(json.dumps({
        "mode_dir": str(mode_dir),
        "event_id": record["event"]["event_id"],
        "event_hash": record["event_hash"],
        "source_completeness": record["event"]["source_completeness"],
        "note": "Appended to hash chain only; baseline snapshot unchanged.",
    }, indent=2))


if __name__ == "__main__":
    main()
