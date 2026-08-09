#!/usr/bin/env python3
"""Create a versioned V9 freeze and optionally run an isolated rehearsal."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from freeze_v9_rule_e import generation_paths
from generation_readiness import build_readiness_report


SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
SHADOW_DIR = ROOT / "results" / "shadow_portfolio"


def run_checked(command: list[str], env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(command, cwd=ROOT, env=env)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("generation_id")
    parser.add_argument("--initialize-forward", action="store_true")
    parser.add_argument("--rehearse-as-of", action="append", default=[])
    args = parser.parse_args()

    if args.initialize_forward:
        readiness = build_readiness_report(ROOT)
        if not readiness["formal_freeze_allowed"]:
            print(json.dumps({"formal_initialization_refused": True, "readiness": readiness}, ensure_ascii=False, indent=2))
            raise SystemExit("formal initialization refused before freeze: worktree is not clean")

    frozen_dir, forward_dir = generation_paths(args.generation_id, SHADOW_DIR)
    generation_root = frozen_dir.parent
    if frozen_dir.exists() or forward_dir.exists():
        raise SystemExit(f"generation already exists and is immutable: {generation_root}")

    run_checked([sys.executable, str(SCRIPTS / "freeze_v9_rule_e.py"), "--generation-id", args.generation_id])
    manifest = json.loads((frozen_dir / "code_manifest.json").read_text(encoding="utf-8"))

    generation_env = os.environ.copy()
    generation_env.update(
        {
            "V9_SHADOW_DIR": str(generation_root),
            "V9_FROZEN_DIR": str(frozen_dir),
            "V9_FORWARD_DIR": str(forward_dir),
            "V9_VALIDATION_DIR": str(generation_root / "validation"),
        }
    )

    if args.initialize_forward:
        if not manifest.get("forward_eligible", False):
            raise SystemExit("formal initialization refused: generation was frozen from a dirty worktree")
        run_checked([sys.executable, str(SCRIPTS / "init_forward_accounts.py")], env=generation_env)

    if args.rehearse_as_of:
        run_id = "rehearsal"
        run_checked(
            [sys.executable, str(SCRIPTS / "run_v9_shadow.py"), "--dry-run", "--run-id", run_id, "--initialize"],
            env=generation_env,
        )
        for as_of in args.rehearse_as_of:
            run_checked(
                [
                    sys.executable,
                    str(SCRIPTS / "run_v9_shadow.py"),
                    "--dry-run",
                    "--run-id",
                    run_id,
                    "--as-of",
                    as_of,
                ],
                env=generation_env,
            )

    result = {
        "generation_id": args.generation_id,
        "generation_root": str(generation_root),
        "forward_eligible": manifest.get("forward_eligible", False),
        "formal_initialized": args.initialize_forward and manifest.get("forward_eligible", False),
        "rehearsed_sessions": args.rehearse_as_of,
        "evidence_status": "engineering-only" if not manifest.get("forward_eligible", False) else "eligible-after-preflight",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
