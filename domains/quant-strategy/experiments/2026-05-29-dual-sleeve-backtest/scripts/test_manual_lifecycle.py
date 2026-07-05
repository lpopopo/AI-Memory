#!/usr/bin/env python3
"""Phase 5: Cross-Serialization Lifecycle Tests for Rule E."""
import sys
import json
import hashlib
from pathlib import Path
import pandas as pd
import numpy as np
import unittest

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from v9_information_strategy import V9Backtester, V9Config, V9Event
from shadow_v9_engine import ShadowV9Engine, TamperAlarmException

class TestManualLifecycle(unittest.TestCase):
    def setUp(self):
        # Create synthetic market data spanning 60 days to allow MA20 and ATR
        self.dates = pd.date_range("2026-05-01", "2026-07-15", freq="B")
        
        # We need SPY, QQQ, and our test symbols D1, D2, CAP
        symbols = ["SPY", "QQQ", "DUMMY1", "DUMMY2", "CAP1", "CAP2", "CAP3", "CAP4"]
        
        # Base DataFrames
        base = pd.DataFrame(100.0, index=self.dates, columns=symbols)
        
        panels = {
            "close": base.copy(),
            "open": base.copy(),
            "high": base.copy() * 1.05,
            "low": base.copy() * 0.95,
            "volume": base.copy() * 10000,
        }
        
        # QQQ performs flat
        # DUMMY1 (D1 case) gaps up by 25% on day 2 (waitlist trigger)
        panels["close"].loc["2026-07-02", "DUMMY1"] = 125.0
        panels["open"].loc["2026-07-03", "DUMMY1"] = 125.0
        
        self.panels = panels
        self.vix = pd.DataFrame(15.0, index=self.dates, columns=["^VIX"])
        
        self.events = [
            V9Event(
                event_id="EV_D1",
                source="test",
                author="test",
                post_id="post_1",
                effective_at=pd.Timestamp("2026-07-01"),
                content_hash="abc",
                theme="AI",
                symbols=("DUMMY1",),
                source_completeness=40,
                thesis_novelty=30,
                fundamental_validation=15,
                crowding_penalty=0,
                point_in_time_eligible=True
            ),
            V9Event(
                event_id="EV_CAP",
                source="test",
                author="test",
                post_id="post_2",
                effective_at=pd.Timestamp("2026-07-01"),
                content_hash="def",
                theme="A",
                symbols=("CAP1",),
                source_completeness=40,
                thesis_novelty=30,
                fundamental_validation=5,
                crowding_penalty=0,
                point_in_time_eligible=True
            ),
        ]
        
        self.cfg = V9Config(entry_rule_version="E", score_threshold=70.0, max_names=3, wait_days_max=5)
        
        # Seed an initial state
        self.state_file = Path("test_lifecycle_state.json")
        self.seed_state = {
            "schema_version": 1,
            "account": "test",
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
            "state_hash": "seed"
        }
        
    def tearDown(self):
        if self.state_file.exists():
            self.state_file.unlink()
        tmp_file = self.state_file.with_suffix(".tmp")
        if tmp_file.exists():
            tmp_file.unlink()

    def step_day(self, state, dt):
        """Simulates the runner: destroy engine, re-init, load, execute, export."""
        engine = ShadowV9Engine(self.panels, self.vix, self.events, self.cfg, self.state_file)
        engine.load_state(state)
        engine.execute_day(dt)
        new_state = engine.export_state(dt)
        return new_state, engine
        
    def test_d1_cross_serialization_lifecycle(self):
        """Test D1 discovers, waits, triggers, and executes across daily serialization boundaries."""
        state = self.seed_state.copy()
        idx_07_01 = self.dates.get_loc("2026-07-01")
        
        # Day 1: 2026-07-01
        # Manually inject D1 into waitlist to simulate discovery
        key = json.dumps(("EV_D1", "DUMMY1"))
        state["waitlist"][key] = {
            "rule": "D1", "days_waited": 0, "score": 85.0, "pullback_low": 120.0
        }
        
        # Day 2: 2026-07-02
        # Price is 125, pullback_low is 120. No trigger yet.
        state, engine = self.step_day(state, self.dates[idx_07_01 + 1])
        
        self.assertIn(key, state["waitlist"])
        self.assertEqual(state["waitlist"][key]["days_waited"], 1)
        
        # Day 3: 2026-07-03
        # Price drops to 110. Open must be <= close.
        self.panels["open"].loc["2026-07-03", "DUMMY1"] = 100.0
        self.panels["close"].loc["2026-07-03", "DUMMY1"] = 110.0
        self.panels["low"].loc["2026-07-03", "DUMMY1"] = 110.0
        state, engine = self.step_day(state, self.dates[idx_07_01 + 2])
        
        # Waitlist should be empty, and it should have popped into pending_orders
        self.assertNotIn(key, state["waitlist"])
        self.assertTrue(any(o["symbol"] == "DUMMY1" and o["order_type"] == "buy" for o in state["pending_orders"]))
        
        # Day 4: 2026-07-06
        # Open price is 110. It should execute at Open!
        self.panels["open"].loc["2026-07-06", "DUMMY1"] = 110.0
        state, engine = self.step_day(state, self.dates[idx_07_01 + 3])
        
        self.assertIn("DUMMY1", state["positions"])
        self.assertTrue(state["positions"]["DUMMY1"]["is_observation"])
        
    def test_capacity_queue_cross_serialization(self):
        """Test Capacity Queue releases constraint."""
        state = self.seed_state.copy()
        idx_07_01 = self.dates.get_loc("2026-07-01")
        
        key = json.dumps(("EV_CAP", "CAP1"))
        state["capacity_queue"][key] = {
            "rule": "Capacity", "days_waited": 0, "score": 75.0
        }
        
        # Suppose capacity is full (max_names=3). We use shares=0 so theme weight is 0.
        # We need 3 non-observation positions to be full.
        p_template = {"entry": 100, "shares": 0, "initial_stop": 90, "theme": "A", "score": 80, "r_risk": 1, "peak": 100, "days_held": 1, "trailing_stop": 90, "is_observation": False, "event_day_low": 90, "qqq_entry": 100, "event_id": "old"}
        
        state["positions"]["SPY"] = dict(p_template)
        state["positions"]["CAP2"] = dict(p_template)
        state["positions"]["CAP3"] = dict(p_template)
        
        # Day 2: 2026-07-02
        state, engine = self.step_day(state, self.dates[idx_07_01 + 1])
        self.assertIn(key, state["capacity_queue"])
        self.assertEqual(state["capacity_queue"][key]["days_waited"], 1)
        
        # Day 3: Free up capacity by removing a position
        del state["positions"]["CAP3"]
        
        # We must also ensure CAP1 meets the trigger condition (px > ma20 and rs > 0)
        # SPY is at 100, so CAP1 at 110 will have rs > 0
        self.panels["close"].loc["2026-07-03", "CAP1"] = 110.0
        
        state, engine = self.step_day(state, self.dates[idx_07_01 + 2])
        
        # Now CAP1 should have been popped from capacity_queue and into pending_orders!
        self.assertNotIn(key, state["capacity_queue"])
        self.assertTrue(any(o["symbol"] == "CAP1" for o in state["pending_orders"]))

if __name__ == "__main__":
    unittest.main()
