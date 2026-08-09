#!/usr/bin/env python3
"""Read-only worktree readiness audit before creating a formal V9 generation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from freeze_v9_rule_e import RESULT_AFFECTING_FILES


ROOT = Path(__file__).resolve().parents[1]


def repository_root(start: Path = ROOT) -> Path:
    value = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=start, text=True
    ).strip()
    return Path(value).resolve()


def parse_porcelain_z(payload: bytes) -> list[dict]:
    """Parse `git status --porcelain=v1 -z`, retaining both rename paths."""
    parts = payload.decode("utf-8", errors="surrogateescape").split("\0")
    rows = []
    index = 0
    while index < len(parts):
        item = parts[index]
        index += 1
        if not item:
            continue
        status = item[:2]
        paths = [item[3:]]
        if any(marker in status for marker in ("R", "C")) and index < len(parts) and parts[index]:
            paths.append(parts[index])
            index += 1
        rows.append({"status": status, "paths": paths})
    return rows


def git_changes(repo: Path) -> list[dict]:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    return parse_porcelain_z(result.stdout)


def _repo_relative(path: Path, repo: Path) -> str:
    return path.resolve().relative_to(repo).as_posix()


def classify_changes(changes: list[dict], repo: Path, strategy_root: Path = ROOT) -> list[dict]:
    result_affecting = {
        _repo_relative(strategy_root / relative, repo)
        for relative in RESULT_AFFECTING_FILES
    }
    strategy_prefix = _repo_relative(strategy_root, repo).rstrip("/") + "/"
    classified = []
    for row in changes:
        normalized_paths = [path.replace("\\", "/") for path in row["paths"]]
        if any(path in result_affecting for path in normalized_paths):
            category = "result_affecting"
        elif any(path == strategy_prefix[:-1] or path.startswith(strategy_prefix) for path in normalized_paths):
            category = "strategy_scope_other"
        else:
            category = "repository_other"
        classified.append({**row, "paths": normalized_paths, "category": category})
    return classified


def build_readiness_report(start: Path = ROOT) -> dict:
    repo = repository_root(start)
    changes = classify_changes(git_changes(repo), repo, ROOT)
    counts = {"result_affecting": 0, "strategy_scope_other": 0, "repository_other": 0}
    for row in changes:
        counts[row["category"]] += 1
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=repo, text=True).strip()
    clean = not changes
    return {
        "repository_root": str(repo),
        "branch": branch,
        "commit": commit,
        "worktree_clean": clean,
        "formal_freeze_allowed": clean,
        "change_counts": counts,
        "changes": changes,
        "blockers": [] if clean else [
            "formal generation requires a completely clean committed worktree",
            "review and intentionally commit, ignore, or otherwise resolve every listed change before freezing",
        ],
        "note": "classification is explanatory only; repository_other changes still block a formal freeze",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()
    report = build_readiness_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_clean and not report["formal_freeze_allowed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
