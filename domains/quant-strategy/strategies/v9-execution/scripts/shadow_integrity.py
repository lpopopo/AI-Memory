import hashlib
import json
import pandas as pd
from typing import Dict, Any, Optional

class TamperAlarmException(Exception):
    """Raised when any state hashing or integrity validation fails."""
    pass

def canonical_json(value: Any) -> str:
    """Consistently stringify a JSON-serializable object."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value: Any) -> str:
    """Generate SHA-256 digest from a canonical JSON string or raw bytes."""
    payload = value if isinstance(value, (bytes, bytearray)) else canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def state_digest(state: Dict[str, Any]) -> str:
    """Digest a state dictionary, excluding its own state_hash field."""
    payload = {k: v for k, v in state.items() if k != "state_hash"}
    return digest(payload)

def verify_genesis(
    state: Dict[str, Any], 
    manifest: Dict[str, Any], 
    frozen_base_config_hash: str,
    account_definition_hash: str,
    account_config_hash: str,
    account_name: str
):
    """Verify that the initial_state.json is exactly as frozen."""
    if state.get("account") != account_name:
        raise TamperAlarmException(f"Genesis mismatch: expected account {account_name}, got {state.get('account')}")
    
    if float(state.get("cash", 0)) != 1.0:
        raise TamperAlarmException("Genesis mismatch: cash must be 1.0")
        
    if state.get("positions") or state.get("pending_orders") or state.get("waitlist") or state.get("capacity_queue"):
        raise TamperAlarmException("Genesis mismatch: holding positions or orders on day 0 is forbidden")
        
    if state.get("code_hash") != manifest.get("combined_code_hash"):
        raise TamperAlarmException("Genesis mismatch: code_hash does not match frozen manifest")
        
    if state.get("frozen_base_config_hash") != frozen_base_config_hash:
        raise TamperAlarmException(f"Genesis mismatch: frozen_base_config_hash mismatch")
        
    if state.get("account_definition_hash") != account_definition_hash:
        raise TamperAlarmException(f"Genesis mismatch: account_definition_hash mismatch")
        
    if state.get("config_hash") != account_config_hash:
        raise TamperAlarmException(f"Genesis mismatch: config_hash {state.get('config_hash')} != expected {account_config_hash}")
        
    if state.get("initialized_at_utc") != manifest.get("frozen_at_utc"):
        raise TamperAlarmException("Genesis mismatch: initialized_at_utc does not match frozen_at_utc")
        
    if state.get("previous_state_hash"):
        raise TamperAlarmException("Genesis mismatch: previous_state_hash must be empty for genesis")

    recalculated_hash = state_digest(state)
    if recalculated_hash != state.get("state_hash"):
        raise TamperAlarmException(f"Genesis tamper: state_hash invalid. got {state.get('state_hash')} != expected {recalculated_hash}")


def verify_daily_state(
    loaded_state: Dict[str, Any], 
    expected_account: str,
    expected_dt: pd.Timestamp,
    manifest: Dict[str, Any],
    account_config_hash: str
):
    """Verify integrity and date alignment of a loaded state."""
    if loaded_state.get("account") != expected_account:
        raise TamperAlarmException(f"State tamper: expected account {expected_account}, got {loaded_state.get('account')}")
        
    recalculated_hash = state_digest(loaded_state)
    if recalculated_hash != loaded_state.get("state_hash"):
        raise TamperAlarmException("State tamper: prior state hash is invalid internally.")

    if loaded_state.get("code_hash") != manifest.get("combined_code_hash"):
        raise TamperAlarmException("State tamper: code_hash mutated mid-run.")
        
    if loaded_state.get("config_hash") != account_config_hash:
        raise TamperAlarmException("State tamper: config_hash mutated mid-run.")
        
    # Check date continuity
    date_str = loaded_state.get("as_of")
    if not date_str and not loaded_state.get("initialized_at_utc"):
        raise TamperAlarmException("State continuity error: Missing date and not genesis.")
    
    if date_str and date_str != expected_dt.strftime("%Y-%m-%d"):
        raise TamperAlarmException(f"State continuity error: expected {expected_dt.date()} but got {date_str}")
            
    # Check finances
    if float(loaded_state.get("cash", 0)) < 0:
        raise TamperAlarmException("State bounds error: negative cash encountered.")
