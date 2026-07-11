#!/usr/bin/env python3
"""Create an auditable Rule-E dry-run/forward baseline."""
from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
import subprocess
import sys
import pandas as pd
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
FROZEN_DIR = ROOT / "results" / "shadow_portfolio" / "frozen"


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def git_value(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def write_frozen(path: Path, value, replace: bool):
    if path.exists() and not replace:
        raise FileExistsError(f"freeze already exists: {path}; use --replace only during engineering dry-runs")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")


def hash_file(path: Path) -> str:
    if not path.exists():
        return ""
    with path.open("rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replace", action="store_true", help="Replace an engineering freeze; never use after forward launch")
    args = parser.parse_args()
    config = {
        "v8_core_weight": .70, "info_sleeve_weight": .30,
        "max_single": .10, "max_theme": .30, "max_names": 3,
        "risk_per_name": .015, "hard_stop": .08, "event_life_days": 40,
        "transaction_cost": .002, "stress_transaction_cost": .005,
        "score_threshold": 70., "tech_weight": 1., "crowding_multiplier": 1.,
        "min_fundamental": 10, "entry_rule_version": "E",
        "dynamic_atr_max": 2.5, "wait_days_max": 10,
        "time_stop_days": 3, "obs_size": .02,
    }

    code_files = [
        "scripts/freeze_v9_rule_e.py",
        "scripts/v9_information_strategy.py",
        "scripts/v9_evaluation.py",
        "scripts/v9_data.py",
        "scripts/v9_research_monitors.py",
        "scripts/shadow_v9_engine.py",
        "scripts/run_v9_shadow.py",
        "scripts/export_v9_lifecycle.py",
        "scripts/init_forward_accounts.py",
        "scripts/test_shadow_engine.py",
        "scripts/test_shadow_runner.py",
        "scripts/test_manual_lifecycle.py"
    ]
    file_hashes = {name: hash_file(ROOT / name) for name in code_files}
    if any(not value for value in file_hashes.values()):
        raise FileNotFoundError("one or more result-affecting code files are missing")
    combined_code = "".join(f"{k}:{file_hashes[k]}" for k in sorted(file_hashes))
    packages = {}
    for package in ("numpy", "pandas", "yfinance"):
        try:
            packages[package] = version(package)
        except PackageNotFoundError:
            packages[package] = "missing"
    dirty = bool(git_value("status", "--porcelain"))
    manifest = {}
    manifest["combined_code_hash"] = hashlib.sha256(combined_code.encode()).hexdigest()
    manifest["frozen_at_utc"] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest.update({
        "files": file_hashes,
        "python_version": sys.version,
        "package_versions": packages,
        "git_commit": git_value("rev-parse", "HEAD"),
        "dirty_worktree": dirty,
        "forward_eligible": not dirty,
    })
    events = json.loads((ROOT / "datasets" / "v9_information_events.json").read_text(encoding="utf-8"))
    manifest["baseline_event_snapshot_hash"] = hashlib.sha256(
        json.dumps(events, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    config["code_manifest_hash"] = manifest["combined_code_hash"]
    write_frozen(FROZEN_DIR / "config.json", config, args.replace)
    write_frozen(FROZEN_DIR / "code_manifest.json", manifest, args.replace)
    write_frozen(FROZEN_DIR / "baseline_event_snapshot.json", events, args.replace)
    print(json.dumps({"frozen_dir": str(FROZEN_DIR), "forward_eligible": not dirty, "manifest": manifest}, indent=2))


if __name__ == "__main__":
    main()
