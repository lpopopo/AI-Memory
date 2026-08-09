"""Read-only consistency checks for an append-only V9 forward directory."""
from __future__ import annotations

import json
from pathlib import Path


ACCOUNT_NAMES = ("v8_base", "v9_a", "v9_e", "passive_50_50")


def _load_json(path: Path, issues: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues.append(f"invalid JSON at {path}: {exc}")
        return {}


def inspect_forward_state(forward_dir: Path, manifest: dict | None = None) -> dict:
    """Return a JSON-serializable inventory and any integrity inconsistencies."""
    issues: list[str] = []
    dates_by_account: dict[str, list[str]] = {}
    initial_states = 0

    for account in ACCOUNT_NAMES:
        account_dir = forward_dir / "accounts" / account
        initial = account_dir / "initial_state.json"
        if not initial.exists():
            issues.append(f"missing genesis for {account}")
        else:
            initial_states += 1
            state = _load_json(initial, issues)
            if state.get("account") != account:
                issues.append(f"genesis account mismatch for {account}")
            if manifest:
                expected = {
                    "code_hash": manifest.get("combined_code_hash"),
                    "initialized_at_utc": manifest.get("frozen_at_utc"),
                    "baseline_event_snapshot_hash": manifest.get("baseline_event_snapshot_hash"),
                }
                for key, value in expected.items():
                    if state.get(key) != value:
                        issues.append(f"genesis {account} {key} does not match frozen manifest")

        account_dates: list[str] = []
        for path in sorted(account_dir.glob("20*_state.json")):
            date = path.name.removesuffix("_state.json")
            state = _load_json(path, issues)
            if state.get("account") != account:
                issues.append(f"daily state account mismatch at {path}")
            if state.get("as_of") != date:
                issues.append(f"daily state date mismatch at {path}")
            account_dates.append(date)
        dates_by_account[account] = account_dates

    date_sets = {account: set(dates) for account, dates in dates_by_account.items()}
    union_dates = set().union(*date_sets.values()) if date_sets else set()
    common_dates = set.intersection(*date_sets.values()) if date_sets else set()
    if union_dates != common_dates:
        issues.append("forward account date sets are inconsistent")

    report_dates = {
        path.name.removeprefix("shadow_report_").removesuffix(".json")
        for path in (forward_dir / "reports").glob("shadow_report_*.json")
    }
    if report_dates != common_dates:
        issues.append("forward report dates do not match completed account sessions")

    for date in sorted(common_dates):
        for account in ACCOUNT_NAMES:
            execution = forward_dir / "executions" / account / f"{date}_open_execution.json"
            decision = forward_dir / "decisions" / account / f"{date}_close_decision.json"
            if not execution.exists():
                issues.append(f"missing open execution artifact for {account} {date}")
            if not decision.exists():
                issues.append(f"missing close decision artifact for {account} {date}")

    return {
        "initial_states": initial_states,
        "daily_state_files": sum(len(dates) for dates in dates_by_account.values()),
        "completed_sessions": len(common_dates),
        "latest_completed_session": max(common_dates) if common_dates else None,
        "dates_by_account": dates_by_account,
        "report_dates": sorted(report_dates),
        "issues": issues,
    }
