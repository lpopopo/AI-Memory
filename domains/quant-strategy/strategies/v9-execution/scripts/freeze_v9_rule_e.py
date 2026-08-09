#!/usr/bin/env python3
"""Create an auditable Rule-E dry-run/forward baseline."""
from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
import re
import subprocess
import sys
import pandas as pd
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
SHADOW_DIR = ROOT / "results" / "shadow_portfolio"
FROZEN_DIR = SHADOW_DIR / "frozen"
FORWARD_DIR = SHADOW_DIR / "forward"

RESULT_AFFECTING_FILES = (
    "scripts/freeze_v9_rule_e.py",
    "scripts/v9_information_strategy.py",
    "scripts/v9_signal.py",
    "scripts/v9_account_allocator.py",
    "scripts/v9_fear_gate.py",
    "scripts/v9_source_health.py",
    "scripts/v9_evaluation.py",
    "scripts/v9_data.py",
    "scripts/download_v9_data.py",
    "scripts/v9_research_monitors.py",
    "scripts/shadow_integrity.py",
    "scripts/shadow_v9_engine.py",
    "scripts/run_v9_shadow.py",
    "scripts/run_v9_daily_execution.py",
    "scripts/append_shadow_event.py",
    "scripts/export_v9_lifecycle.py",
    "scripts/init_forward_accounts.py",
    "scripts/preflight_formal_forward.py",
    "scripts/audit_shadow_forward_launch.py",
    "scripts/forward_state_inventory.py",
    "scripts/prepare_forward_generation.py",
    "scripts/generation_readiness.py",
    "scripts/run_market_semiconductor_turn_validation.py",
    "scripts/test_shadow_engine.py",
    "scripts/test_shadow_runner.py",
    "scripts/test_manual_lifecycle.py",
    "scripts/test_download_v9_data.py",
    "scripts/test_forward_integrity.py",
    "scripts/test_forward_state_inventory.py",
    "scripts/test_generation_readiness.py",
    "scripts/test_v9_account_allocator.py",
    "scripts/test_v9_daily_execution.py",
    "scripts/test_v9_information_strategy.py",
    "scripts/test_v9_research_monitors.py",
    "scripts/test_v9_source_health.py",
    "scripts/test_v9_state_machine.py",
    "validation/prereg-market-semiconductor-turn-monitor.md",
    "validation/source-health-recovery-contract.md",
    "../../references/user-selected-watchlist.json",
)


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


def generation_paths(generation_id: str | None, shadow_dir: Path = SHADOW_DIR) -> tuple[Path, Path]:
    if generation_id is None:
        return shadow_dir / "frozen", shadow_dir / "forward"
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,63}", generation_id):
        raise ValueError("generation id must match [a-z0-9][a-z0-9._-]{0,63}")
    generation_root = shadow_dir / "generations" / generation_id
    return generation_root / "frozen", generation_root / "forward"


def forward_has_artifacts(forward_dir: Path = FORWARD_DIR) -> bool:
    if not forward_dir.exists():
        return False
    protected_patterns = (
        "accounts/*/initial_state.json",
        "accounts/*/20*_state.json",
        "reports/shadow_report_*.json",
        "decisions/*/*_close_decision.json",
        "executions/*/*_open_execution.json",
    )
    if any(any(forward_dir.glob(pattern)) for pattern in protected_patterns):
        return True
    append_log = forward_dir / "shared" / "event_append_log.jsonl"
    return append_log.exists() and bool(append_log.read_text(encoding="utf-8").strip())


def hash_file(path: Path) -> str:
    if not path.exists():
        return ""
    with path.open("rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replace", action="store_true", help="Replace an engineering freeze; never use after forward launch")
    parser.add_argument("--generation-id", help="Write an immutable versioned freeze under shadow_portfolio/generations/<id>")
    args = parser.parse_args()
    frozen_dir, forward_dir = generation_paths(args.generation_id)
    if args.replace and forward_has_artifacts(forward_dir):
        raise RuntimeError(
            "refusing --replace: formal forward genesis or states already exist; "
            "create a new versioned freeze/genesis instead"
        )
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

    code_files = list(RESULT_AFFECTING_FILES)
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
        "generation_id": args.generation_id or "legacy-default",
        "layout_version": 2 if args.generation_id else 1,
    })
    events = json.loads((ROOT / "datasets" / "v9_information_events.json").read_text(encoding="utf-8"))
    manifest["baseline_event_snapshot_hash"] = hashlib.sha256(
        json.dumps(events, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    config["code_manifest_hash"] = manifest["combined_code_hash"]
    write_frozen(frozen_dir / "config.json", config, args.replace)
    write_frozen(frozen_dir / "code_manifest.json", manifest, args.replace)
    write_frozen(frozen_dir / "baseline_event_snapshot.json", events, args.replace)
    print(json.dumps({"frozen_dir": str(frozen_dir), "forward_dir": str(forward_dir), "forward_eligible": not dirty, "manifest": manifest}, indent=2))


if __name__ == "__main__":
    main()
