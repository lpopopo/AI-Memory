#!/usr/bin/env python3
"""Preflight checks before an append-only formal forward day."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "results" / "shadow_portfolio" / "frozen" / "code_manifest.json"
FORWARD = ROOT / "results" / "shadow_portfolio" / "forward"
DATA_CLOSE = ROOT / "datasets" / "data_v9" / "close.csv"
REQUIRED_SYMBOLS = ("SPY", "QQQ", "SMH", "IWM", "RSP", "HYG", "LQD", "^VIX", "^VIX3M")


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
    as_of = None
    if len(sys.argv) > 1:
        as_of = pd.Timestamp(sys.argv[1]).normalize()

    blockers: list[str] = []
    warnings: list[str] = []

    if not FROZEN.exists():
        blockers.append("missing frozen code_manifest.json")
        manifest = {}
    else:
        manifest = json.loads(FROZEN.read_text(encoding="utf-8"))
        if not manifest.get("forward_eligible"):
            blockers.append("forward_eligible is false")
        bad = []
        for rel, expected in manifest.get("files", {}).items():
            path = ROOT / rel
            actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
            if actual != expected:
                bad.append(rel)
        if bad:
            blockers.append(f"code hash mismatch: {bad}")

    inits = list(FORWARD.glob("accounts/*/initial_state.json")) if FORWARD.exists() else []
    dailies = list(FORWARD.glob("accounts/*/20*_state.json")) if FORWARD.exists() else []
    if len(inits) < 4:
        blockers.append("forward genesis incomplete (<4 initial_state.json)")

    if not DATA_CLOSE.exists():
        blockers.append("datasets/data_v9/close.csv missing; run download_v9_data.py")
        last_date = None
        missing_syms = list(REQUIRED_SYMBOLS)
    else:
        close = pd.read_csv(DATA_CLOSE, index_col=0, parse_dates=True)
        last_date = close.index.max().normalize()
        missing_syms = [s for s in REQUIRED_SYMBOLS if s not in close.columns]
        if missing_syms:
            warnings.append(f"data_v9 missing diagnostic symbols: {missing_syms}")

    if as_of is not None:
        freeze_ts = pd.Timestamp(manifest.get("frozen_at_utc")) if manifest.get("frozen_at_utc") else None
        if freeze_ts is not None:
            session_close = as_of.tz_localize("America/New_York").replace(hour=16, minute=0).tz_convert("UTC")
            if session_close <= freeze_ts.tz_convert("UTC"):
                blockers.append(f"{as_of.date()} session close is not after freeze time {freeze_ts}")
        if last_date is not None and last_date < as_of:
            blockers.append(f"data_v9 last bar {last_date.date()} < requested as-of {as_of.date()}; refresh data first")
        if dailies:
            dates = sorted(pd.Timestamp(p.stem.replace("_state", "")) for p in dailies)
            expected_prev = None
            # Contiguity is enforced by the runner; here only warn if as-of already exists.
            if any(p.stem.startswith(str(as_of.date())) for p in dailies):
                blockers.append(f"forward state for {as_of.date()} already exists")
            latest = dates[-1]
            if as_of <= latest:
                blockers.append(f"requested as-of {as_of.date()} is not after latest forward state {latest.date()}")

    if git_dirty():
        warnings.append("git worktree dirty; formal forward can still run on frozen hashes, but do not re-freeze")

    report = {
        "ok": not blockers,
        "as_of": None if as_of is None else str(as_of.date()),
        "forward_eligible": bool(manifest.get("forward_eligible")),
        "frozen_at_utc": manifest.get("frozen_at_utc"),
        "data_v9_last_date": None if last_date is None else str(last_date.date()),
        "forward_initial_states": len(inits),
        "forward_daily_states": len(dailies),
        "blockers": blockers,
        "warnings": warnings,
    }
    out = ROOT / "results" / "validation" / "formal_forward_preflight.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if blockers:
        sys.exit(2)


if __name__ == "__main__":
    main()
