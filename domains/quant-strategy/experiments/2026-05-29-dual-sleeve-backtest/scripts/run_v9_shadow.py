#!/usr/bin/env python3
"""Advance four isolated V9 shadow accounts by exactly one completed session."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from v9_information_strategy import V9Backtester, V9Config, load_event_store
from validate_v9_information_strategy import load_data
from shadow_integrity import TamperAlarmException, canonical_json as canonical, digest, state_digest, verify_genesis, verify_daily_state
from shadow_v9_engine import ShadowV9Engine

SHADOW_DIR = ROOT / "results" / "shadow_portfolio"
FROZEN_DIR = SHADOW_DIR / "frozen"

ACCOUNTS = {
    "v8_base": {"v8_core_weight": 1.0, "info_sleeve_weight": 0.0, "entry_rule_version": "A"},
    "v9_a": {"v8_core_weight": 0.70, "info_sleeve_weight": 0.30, "entry_rule_version": "A"},
    "v9_e": {"v8_core_weight": 0.70, "info_sleeve_weight": 0.30, "entry_rule_version": "E"},
    "passive_50_50": {"v8_core_weight": 1.0, "info_sleeve_weight": 0.0, "entry_rule_version": "A"},
}


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def atomic_freeze(path: Path, value: dict | list):
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
    if path.exists():
        if canonical(json.loads(path.read_text(encoding="utf-8"))) != canonical(value):
            raise TamperAlarmException(f"frozen artifact changed: {path}")
        return "unchanged"
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    tmp.replace(path)
    return "written"


def verify_code_manifest() -> dict:
    path = FROZEN_DIR / "code_manifest.json"
    if not path.exists():
        raise TamperAlarmException("missing code_manifest.json")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for rel_path, expected in manifest["files"].items():
        actual = hash_file(ROOT / rel_path)
        if actual != expected:
            raise TamperAlarmException(f"code changed: {rel_path}")
    baseline = FROZEN_DIR / "baseline_event_snapshot.json"
    if hash_file(baseline) == "":
        raise TamperAlarmException("missing baseline event snapshot")
    baseline_obj = json.loads(baseline.read_text(encoding="utf-8"))
    if digest(baseline_obj) != manifest.get("baseline_event_snapshot_hash"):
        raise TamperAlarmException("baseline event snapshot changed")
    return manifest


def visible_event_snapshot(mode_dir: Path, as_of: pd.Timestamp) -> tuple[Path, str, list[str]]:
    baseline_path = FROZEN_DIR / "baseline_event_snapshot.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    known = {row["event_id"] for row in baseline.get("events", [])}
    append_path = mode_dir / "shared" / "event_append_log.jsonl"
    visible = []
    accepted_hashes = []
    previous_hash = ""
    if append_path.exists():
        for number, line in enumerate(append_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            event = record["event"]
            expected = digest({"previous_event_hash": previous_hash, "event": event})
            if record.get("previous_event_hash", "") != previous_hash or record.get("event_hash") != expected:
                raise TamperAlarmException(f"broken event hash chain at line {number}")
            if event["event_id"] in known:
                raise TamperAlarmException(f"event id modified or duplicated: {event['event_id']}")
            first_seen = pd.Timestamp(event["first_seen_at"])
            if first_seen.tzinfo is not None:
                first_seen = first_seen.tz_convert("UTC").tz_localize(None)
            if first_seen.normalize() <= as_of.normalize():
                visible.append(event)
                accepted_hashes.append(expected)
            known.add(event["event_id"])
            previous_hash = expected
    combined = dict(baseline)
    combined["events"] = list(baseline.get("events", [])) + visible
    snapshot = mode_dir / "shared" / "event_snapshots" / f"{as_of.date()}.json"
    atomic_freeze(snapshot, combined)
    return snapshot, digest(combined), accepted_hashes


def market_snapshot(panels, vix, dt: pd.Timestamp) -> dict:
    result = {"date": str(dt.date()), "panels": {}}
    for name in ("open", "high", "low", "close", "volume"):
        row = panels[name].loc[dt].dropna()
        result["panels"][name] = {str(k): float(v) for k, v in sorted(row.items())}
    if dt in vix.index:
        result["vix"] = {str(k): float(v) for k, v in sorted(vix.loc[dt].dropna().items())}
    else:
        result["vix"] = {}
    return result


def previous_market_date(index: pd.DatetimeIndex, dt: pd.Timestamp):
    location = index.get_loc(dt)
    return None if location == 0 else index[location - 1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-id", help="Dry-run namespace; defaults to the frozen code-hash prefix")
    parser.add_argument("--initialize", action="store_true", help="Create the first state in this mode")
    args = parser.parse_args()
    dt = pd.Timestamp(args.as_of)

    manifest = verify_code_manifest()
    if not args.dry_run and not manifest.get("forward_eligible", False):
        raise TamperAlarmException("forward mode requires a clean committed freeze; current manifest is engineering-only")
    config_base = json.loads((FROZEN_DIR / "config.json").read_text(encoding="utf-8"))
    
    if args.dry_run:
        run_id = args.run_id or manifest["combined_code_hash"][:8]
        mode_dir = SHADOW_DIR / "dry_run" / run_id
    else:
        mode_dir = SHADOW_DIR / "forward"
    
    # 2. Load Data
    panels, vix, meta = load_data()
    events, _ = load_event_store(FROZEN_DIR / "baseline_event_snapshot.json", use_retrospective=False)
    
    if dt not in panels["close"].index:
        print(f"Holiday or no market data for {dt.date()}, skipping.")
        return
        
    frozen_at_utc = manifest.get("frozen_at_utc")
    if frozen_at_utc and not args.dry_run:
        frozen_dt = pd.Timestamp(frozen_at_utc, tz="UTC")
        # Assume session close is dt at 16:00 ET
        session_close_utc = pd.Timestamp(dt).tz_localize("America/New_York").replace(hour=16, minute=0).tz_convert("UTC")
        if session_close_utc <= frozen_dt:
            raise TamperAlarmException(f"Forbidden: Cannot execute {dt.date()}. Session close {session_close_utc} is not after freeze time {frozen_dt}.")
            
    event_snapshot_path, event_hash, new_event_hashes = visible_event_snapshot(mode_dir, dt)
    market = market_snapshot(panels, vix, dt)
    market_path = mode_dir / "shared" / "market_snapshots" / f"{dt.date()}.json"
    atomic_freeze(market_path, market)
    market_hash = digest(market)

    daily_stats = {}
    for acc_name, overrides in ACCOUNTS.items():
        acc_dir = mode_dir / "accounts" / acc_name
        cfg_kwargs = {**config_base, **overrides}
        cfg_kwargs.pop("stress_transaction_cost", None)
        cfg_kwargs.pop("code_manifest_hash", None)
        acc_config_hash = digest(cfg_kwargs)
        cfg = V9Config(**cfg_kwargs)
        state_file = acc_dir / f"{dt.date()}_state.json"
        shadow = ShadowV9Engine(panels, vix, events, cfg, state_file)

        # Determine previous state
        dt_idx = panels["close"].index.get_loc(dt)
        prev_state = None
        if dt_idx > 0:
            prev_dt = panels["close"].index[dt_idx - 1]
            prev_state_file = acc_dir / f"{prev_dt.date()}_state.json"
            if prev_state_file.exists():
                prev_state = json.loads(prev_state_file.read_text())
                verify_daily_state(prev_state, acc_name, prev_dt, manifest, acc_config_hash)
                shadow.load_state(prev_state)
            else:
                existing_states = list(acc_dir.glob("20*_state.json"))
                if len(existing_states) > 0:
                    raise TamperAlarmException(f"Missing T-1 state for {acc_name} at {prev_dt.date()} (Skip day detected!)")
                
                initial_file = acc_dir / "initial_state.json"
                if initial_file.exists():
                    prev_state = json.loads(initial_file.read_text())
                    verify_genesis(prev_state, manifest, digest(config_base), digest(overrides), acc_config_hash, acc_name)
                    shadow.load_state(prev_state)
                else:
                    raise TamperAlarmException(f"Missing T-1 state for {acc_name} at {prev_dt.date()} and no initial_state.json found.")
        else:
            raise TamperAlarmException(f"Cannot execute {dt.date()} without prior timeline.")
                
        # Execute Day
        if acc_name == "passive_50_50":
            shadow.bt.v8_base_weights = {date: {"SPY": .5, "QQQ": .5} for date in panels["close"].index}

        shadow.execute_day(dt)
        execution_rows = [row for row in shadow.bt.ledger if row.get("date") == str(dt.date())]
        decision_rows = [row for row in shadow.bt.audit if row.get("date") == str(dt.date())]
        funnel_rows = [row for row in shadow.bt.funnel if row.get("date") == str(dt.date())]
        execution_payload = {"as_of": str(dt.date()), "account": acc_name, "rows": execution_rows}
        decision_payload = {"as_of": str(dt.date()), "account": acc_name, "audit": decision_rows, "funnel": funnel_rows}
        execution_hash = digest(execution_payload)
        decision_hash = digest(decision_payload)
        atomic_freeze(mode_dir / "executions" / acc_name / f"{dt.date()}_open_execution.json", execution_payload)
        atomic_freeze(mode_dir / "decisions" / acc_name / f"{dt.date()}_close_decision.json", decision_payload)

        # Calculate State Hash
        new_state = shadow.export_state(dt)
        previous_hash = prev_state.get("state_hash", "") if prev_state else ""
        new_state["previous_state_hash"] = previous_hash
        new_state["genesis_state_hash"] = prev_state.get("genesis_state_hash", previous_hash) if prev_state else previous_hash
        new_state.update({
            "as_of": str(dt.date()),
            "account": acc_name,
            "mode": "dry_run" if args.dry_run else "forward",
            "config_hash": acc_config_hash,
            "code_hash": manifest["combined_code_hash"],
            "market_data_hash": market_hash,
            "event_snapshot_hash": event_hash,
            "new_event_hashes": new_event_hashes,
            "execution_hash": execution_hash,
            "decision_hash": decision_hash,
        })
        new_state["state_hash"] = state_digest(new_state)
        atomic_freeze(state_file, new_state)
        daily_stats[acc_name] = {
            "nav": float(shadow.bt.value),
            "cash": float(shadow.bt.cash),
            "info_pnl": float(getattr(shadow.bt, "cum_info_official_pnl", 0) + getattr(shadow.bt, "cum_info_obs_pnl", 0)),
            "state_hash": new_state["state_hash"],
        }

    report = {
        "as_of": str(dt.date()),
        "mode": "dry_run" if args.dry_run else "forward",
        "accounts": daily_stats,
        "rule_e_incremental_alpha": daily_stats["v9_e"]["info_pnl"] - daily_stats["v9_a"]["info_pnl"],
    }
    atomic_freeze(mode_dir / "reports" / f"shadow_report_{dt.date()}.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
