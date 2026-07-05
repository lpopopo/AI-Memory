#!/usr/bin/env python3
"""Phase 5: Official Forward Shadow Portfolio Initialization."""
import json
import hashlib
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
SHADOW_DIR = ROOT / "results" / "shadow_portfolio"
FORWARD_DIR = SHADOW_DIR / "forward"
FROZEN_DIR = SHADOW_DIR / "frozen"

from shadow_v9_engine import TamperAlarmException

ACCOUNTS = ["v8_base", "v9_a", "v9_e", "passive_50_50"]

def get_hash(obj):
    payload = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()

def main():
    if not FROZEN_DIR.exists():
        raise FileNotFoundError("Frozen directory missing. Cannot initialize forward accounts.")
        
    manifest = json.loads((FROZEN_DIR / "code_manifest.json").read_text())
    config = json.loads((FROZEN_DIR / "config.json").read_text())
    events_raw = (FROZEN_DIR / "baseline_event_snapshot.json").read_text(encoding="utf-8")
    
    frozen_at_utc = manifest.get("frozen_at_utc")
    code_hash = manifest.get("combined_code_hash", "")
    config_hash = get_hash(config)
    
    events_obj = json.loads(events_raw)
    baseline_events_hash = hashlib.sha256(json.dumps(events_obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    
    accounts_dir = FORWARD_DIR / "accounts"
    accounts_dir.mkdir(parents=True, exist_ok=True)
    
    # Pre-flight check
    for acc in ACCOUNTS:
        acc_dir = accounts_dir / acc
        if acc_dir.exists():
            for f in acc_dir.glob("*_state.json"):
                if f.name != "initial_state.json":
                    raise TamperAlarmException(f"Forbidden: Forward execution already started. Found {f.name} in {acc}.")
    
    new_states = {}
    for acc in ACCOUNTS:
        base_state = {
            "schema_version": 1,
            "account": acc,
            "mode": "forward",
            "cash": 1.0,
            "current_nav": 1.0,
            "highwater_nav": 1.0,
            "v8_shares": {"SPY": 0.0, "QQQ": 0.0},
            "positions": {},
            "waitlist": {},
            "capacity_queue": {},
            "pending_orders": [],
            "cum_v8_pnl": 0.0,
            "cum_info_official_pnl": 0.0,
            "cum_info_obs_pnl": 0.0,
            "cum_cost": 0.0,
            "turnover": 0.0,
            "code_hash": code_hash,
            "config_hash": config_hash,
            "baseline_event_snapshot_hash": baseline_events_hash,
            "initialized_at_utc": frozen_at_utc,
            "previous_state_hash": ""
        }
        
        # Calculate state_hash
        state_hash = get_hash(base_state)
        base_state["state_hash"] = state_hash
        new_states[acc] = base_state

    # Check existing status for idempotency
    existing_files = {acc: (accounts_dir / acc / "initial_state.json") for acc in ACCOUNTS}
    exists_count = sum(1 for f in existing_files.values() if f.exists())
    
    if exists_count > 0 and exists_count < len(ACCOUNTS):
        raise TamperAlarmException("Partial initialization detected! Some initial_state.json are missing.")
        
    if exists_count == len(ACCOUNTS):
        # Verify contents
        for acc, file_path in existing_files.items():
            current = json.loads(file_path.read_text())
            if get_hash(current) != get_hash(new_states[acc]):
                raise TamperAlarmException(f"Tamper Alarm: {acc} initial_state.json differs from expected genesis!")
        print("unchanged")
        return

    # Write states atomically
    for acc, state in new_states.items():
        acc_dir = accounts_dir / acc
        acc_dir.mkdir(parents=True, exist_ok=True)
        file_path = acc_dir / "initial_state.json"
        
        tmp_file = file_path.with_suffix(".tmp")
        tmp_file.write_text(json.dumps(state, indent=2, sort_keys=True))
        tmp_file.replace(file_path)
        print(f"[{acc}] Created initial_state.json. Hash: {state['state_hash']}")
        
    # Write event chain genesis
    shared_dir = FORWARD_DIR / "shared"
    shared_dir.mkdir(parents=True, exist_ok=True)
    event_genesis = {
        "baseline_event_snapshot_hash": baseline_events_hash,
        "frozen_at_utc": frozen_at_utc,
        "config_hash": config_hash,
        "previous_event_hash": get_hash({"baseline": baseline_events_hash, "frozen_at": frozen_at_utc})
    }
    event_genesis_file = shared_dir / "event_chain_genesis.json"
    event_genesis_file.write_text(json.dumps(event_genesis, indent=2, sort_keys=True))
    print(f"[shared] Created event_chain_genesis.json. Initial Hash: {event_genesis['previous_event_hash']}")
    
    # Initialize empty append log
    append_log = shared_dir / "event_append_log.jsonl"
    if not append_log.exists():
        append_log.touch()
        
if __name__ == "__main__":
    main()
