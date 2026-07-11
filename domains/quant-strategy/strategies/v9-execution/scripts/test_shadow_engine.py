#!/usr/bin/env python3
"""Stateful shadow-engine invariants."""
import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from v9_information_strategy import V9Backtester, V9Config, load_event_store
from v9_data import load_data
from shadow_v9_engine import ShadowV9Engine


class TestShadowEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panels, cls.vix, _ = load_data()
        root = Path(__file__).resolve().parent.parent
        cls.events, _ = load_event_store(root / "datasets" / "v9_information_events.json", use_retrospective=True)
        cls.cfg = V9Config(entry_rule_version="E", score_threshold=70.0)

    def engine(self):
        return ShadowV9Engine(self.panels, self.vix, self.events, self.cfg, Path(tempfile.mkdtemp()) / "state.json")

    def test_incremental_equivalence_across_serialization(self):
        start, end = "2026-06-18", "2026-06-25"
        full = V9Backtester(self.panels, self.vix, self.events, self.cfg)
        full.run(warmup_start=start, trading_start=start, trading_end=end)
        dates = self.panels["close"].loc[start:end].index
        state = None
        shadow = None
        for dt in dates:
            shadow = self.engine()
            if state:
                shadow.load_state(json.loads(json.dumps(state)))
            shadow.execute_day(dt)
            state = shadow.export_state(dt)
        self.assertAlmostEqual(full.cash, shadow.bt.cash, places=8)
        self.assertAlmostEqual(full.value, shadow.bt.value, places=8)
        self.assertEqual(set(full.positions), set(shadow.bt.positions))
        self.assertEqual(len(full.waitlist), len(shadow.bt.waitlist))

    def test_shadow_step_processes_only_requested_session(self):
        shadow = self.engine()
        dt = pd.Timestamp("2026-06-22")
        shadow.execute_day(dt)
        dates = {row["date"] for row in shadow.bt.audit + shadow.bt.ledger + shadow.bt.funnel if "date" in row}
        self.assertTrue(dates <= {"2026-06-22"})

    def test_state_key_decoder_does_not_execute_code(self):
        shadow = self.engine()
        state = shadow.export_state(pd.Timestamp("2026-06-22"))
        state["waitlist"] = {"__import__('os').system('echo unsafe')": {}}
        with self.assertRaises((ValueError, SyntaxError)):
            shadow.load_state(state)


if __name__ == "__main__":
    unittest.main()
