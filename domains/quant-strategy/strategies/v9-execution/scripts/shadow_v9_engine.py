#!/usr/bin/env python3
"""Phase 4: Shadow V9 Engine with Point-in-Time Daily Execution."""
import json
import hashlib
import ast
from pathlib import Path
import pandas as pd
from typing import Dict, Any, List

from v9_information_strategy import V9Backtester, V9Config, PositionState, PendingOrder, V9Event
from shadow_integrity import TamperAlarmException

class ShadowV9Engine:
    def __init__(self, panels: Dict[str, pd.DataFrame], vix: pd.DataFrame, events: List[V9Event], config: V9Config, 
                 state_file: Path, prev_state_hash: str = ""):
        self.bt = V9Backtester(panels, vix, events, config)
        self.state_file = state_file
        self.prev_state_hash = prev_state_hash
        self.bt.cash = 1.0
        self.bt.value = 1.0
        self.bt.highwater = 1.0
        self.bt.equity = pd.Series(dtype=float)
        self.bt.ledger = []
        self.bt.audit = []
        self.bt.funnel = []
        
    def load_state(self, state_json: Dict[str, Any]):
        """Load from dict"""
        self.bt.cash = state_json.get("cash", 1.0)
        self.bt.value = state_json.get("current_nav", 1.0)
        self.bt.highwater = state_json.get("highwater_nav", 1.0)
        
        self.bt.v8_shares = state_json.get("v8_shares", {})
        self.bt.cum_v8_pnl = state_json.get("cum_v8_pnl", 0.0)
        self.bt.cum_info_official_pnl = state_json.get("cum_info_official_pnl", 0.0)
        self.bt.cum_info_obs_pnl = state_json.get("cum_info_obs_pnl", 0.0)
        self.bt.cum_cost = state_json.get("cum_cost", 0.0)
        self.bt.turnover = state_json.get("turnover", 0.0)
        self.bt.prev_v8_val = state_json.get("prev_v8_val", 0.0)
        self.bt.prev_info_off_val = state_json.get("prev_info_off_val", 0.0)
        self.bt.prev_info_obs_val = state_json.get("prev_info_obs_val", 0.0)
        
        self.bt.positions = {}
        for s, p in state_json.get("positions", {}).items():
            state = PositionState(p["entry"], p["shares"], p["initial_stop"], p["theme"], p["score"], p["r_risk"])
            state.peak = p["peak"]
            state.days_held = p["days_held"]
            state.trimmed = p.get("trimmed", False)
            state.trailing_stop = p["trailing_stop"]
            state.is_observation = p["is_observation"]
            state.event_day_low = p["event_day_low"]
            state.qqq_entry = p["qqq_entry"]
            state.event_id = p.get("event_id", "")
            self.bt.positions[s] = state
            
        def decode_key(value):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                parsed = ast.literal_eval(value)  # backward-compatible dry-run states only
            if not isinstance(parsed, (list, tuple)) or len(parsed) != 2:
                raise ValueError(f"invalid lifecycle key: {value}")
            return tuple(str(x) for x in parsed)
        self.bt.waitlist = {decode_key(k): v for k, v in state_json.get("waitlist", {}).items()}
        self.bt.capacity_queue = {decode_key(k): v for k, v in state_json.get("capacity_queue", {}).items()}
        
        self.bt.pending_orders = []
        for o in state_json.get("pending_orders", []):
            self.bt.pending_orders.append(PendingOrder(
                symbol=o["symbol"],
                target_weight=o["target_weight"],
                signal_date=pd.Timestamp(o["signal_date"]),
                score=o["score"],
                stop_price=o["stop_price"],
                order_type=o["order_type"],
                theme=o.get("theme", ""),
                r_risk=o.get("r_risk", 0.0),
                is_observation=o.get("is_observation", False)
            ))
            if "high_vol_entry" in o:
                self.bt.pending_orders[-1].high_vol_entry = o["high_vol_entry"]
            if "event_day_low" in o:
                self.bt.pending_orders[-1].event_day_low = o["event_day_low"]
            self.bt.pending_orders[-1].event_id = o.get("event_id", "")
            
    def export_state(self, dt: pd.Timestamp) -> Dict[str, Any]:
        """Export to dict"""
        return {
            "as_of": str(dt.date()),
            "cash": self.bt.cash,
            "current_nav": self.bt.value,
            "highwater_nav": self.bt.highwater,
            "cum_v8_pnl": getattr(self.bt, "cum_v8_pnl", 0.0),
            "cum_info_official_pnl": getattr(self.bt, "cum_info_official_pnl", 0.0),
            "cum_info_obs_pnl": getattr(self.bt, "cum_info_obs_pnl", 0.0),
            "cum_cost": getattr(self.bt, "cum_cost", 0.0),
            "turnover": getattr(self.bt, "turnover", 0.0),
            "prev_v8_val": getattr(self.bt, "prev_v8_val", 0.0),
            "prev_info_off_val": getattr(self.bt, "prev_info_off_val", 0.0),
            "prev_info_obs_val": getattr(self.bt, "prev_info_obs_val", 0.0),
            "v8_shares": self.bt.v8_shares,
            "positions": {s: {
                "entry": p.entry, "shares": p.shares, "initial_stop": p.initial_stop, "trailing_stop": p.trailing_stop,
                "theme": p.theme, "score": p.score, "r_risk": p.r_risk, "peak": p.peak,
                "days_held": p.days_held, "trimmed": p.trimmed, "is_observation": getattr(p, "is_observation", False),
                "event_day_low": getattr(p, "event_day_low", 0.0), "qqq_entry": getattr(p, "qqq_entry", 0.0),
                "event_id": getattr(p, "event_id", "")
            } for s, p in self.bt.positions.items()},
            "waitlist": {json.dumps(list(k), ensure_ascii=False): v for k, v in self.bt.waitlist.items()},
            "capacity_queue": {json.dumps(list(k), ensure_ascii=False): v for k, v in self.bt.capacity_queue.items()},
            "pending_orders": [{
                "symbol": o.symbol, "target_weight": o.target_weight, "signal_date": str(o.signal_date),
                "score": o.score, "stop_price": o.stop_price, "order_type": o.order_type,
                "theme": getattr(o, "theme", ""), "r_risk": getattr(o, "r_risk", 0.0),
                "high_vol_entry": getattr(o, "high_vol_entry", False),
                "is_observation": getattr(o, "is_observation", False),
                "event_day_low": getattr(o, "event_day_low", 0.0)
                ,"event_id": getattr(o, "event_id", "")
            } for o in self.bt.pending_orders]
        }
        
    def execute_day(self, dt: pd.Timestamp):
        """Execute a single day (Open + Close) using V9Backtester's internal loop."""
        
        old_ledger = self.bt.ledger
        old_audit = self.bt.audit
        old_funnel = self.bt.funnel
        old_equity = self.bt.equity
        
        self.bt.run(warmup_start=str(dt.date()), trading_start=dt, trading_end=dt, _shadow_step=True)
        
        self.bt.ledger = old_ledger + self.bt.ledger
        self.bt.audit = old_audit + self.bt.audit
        self.bt.funnel = old_funnel + self.bt.funnel
        if old_equity is not None and not old_equity.empty:
            self.bt.equity = pd.concat([old_equity, self.bt.equity])
