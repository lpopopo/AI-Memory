#!/usr/bin/env python3
"""Build or refresh a PIT universe coverage manifest.

If membership history is unavailable, write an explicit gap report instead of
pretending current-constituent caches are point-in-time.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "datasets" / "data_point_in_time" / "manifest.json"
LEGACY_BUILDER = ROOT.parent / "research-archive" / "legacy-v0-v8-scripts" / "build_point_in_time_data.py"
UNIVERSE_DIR = ROOT / "datasets" / "data_universe"


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    membership_candidates = [
        ROOT / "datasets" / "data_point_in_time" / "membership_history.csv",
        ROOT / "datasets" / "data_point_in_time" / "adjusted_close.csv",
    ]
    existing = [path for path in membership_candidates if path.exists()]
    universe_files = sorted(UNIVERSE_DIR.glob("*_adjusted_close.csv")) if UNIVERSE_DIR.exists() else []

    status = "ready" if existing else "missing_pit_panels"
    manifest = {
        "status": status,
        "decision_grade": False,
        "builder_script": str(LEGACY_BUILDER) if LEGACY_BUILDER.exists() else None,
        "existing_pit_files": [
            {"path": str(path.relative_to(ROOT)), "sha256": file_digest(path), "bytes": path.stat().st_size}
            for path in existing
        ],
        "current_constituent_cache": {
            "path": "datasets/data_universe",
            "symbol_files": len(universe_files),
            "warning": "Current-constituent caches are not PIT and must not promote Rule E or WML results.",
        },
        "required_before_promotion": [
            "S&P 500 / Nasdaq-100 membership by date",
            "permanent security identifiers",
            "deletions and delisting returns",
            "coverage report for missing Yahoo / free-source symbols",
        ],
        "event_gate": {
            "min_reliable_pit_events": 50,
            "note": "Rule E statistical validation remains blocked below this threshold.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
