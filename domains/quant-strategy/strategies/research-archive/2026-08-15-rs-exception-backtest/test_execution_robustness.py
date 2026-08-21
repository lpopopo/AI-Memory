from pathlib import Path
import runpy
import unittest

import pandas as pd


MODULE = runpy.run_path(str(Path(__file__).with_name("run_backtest.py")))


class ExecutionRobustnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panels, cls.symbols = MODULE["load_panels"]()

    def candidate_config(self, **overrides):
        values = dict(
            rs20_min=0.03,
            volume_ratio_min=1.20,
            max_extension=0.12,
            max_hold_days=20,
            stop_loss=0.08,
            max_atr_pct=0.04,
            min_close_location=0.50,
        )
        values.update(overrides)
        return MODULE["Config"](**values)

    def test_two_session_delay_never_executes_early(self):
        result = MODULE["simulate"](
            self.panels,
            self.symbols,
            self.candidate_config(entry_delay_sessions=2),
            "strict_veto",
            "2024-01-02",
            "2026-08-07",
        )
        dates = self.panels["close"].index
        positions = pd.Series(range(len(dates)), index=dates)
        for trade in result["trades"]:
            waited = positions[pd.Timestamp(trade["entry_date"])] - positions[pd.Timestamp(trade["signal_date"])]
            self.assertGreaterEqual(waited, 2)

    def test_entry_gap_cap_is_enforced_at_execution(self):
        result = MODULE["simulate"](
            self.panels,
            self.symbols,
            self.candidate_config(max_entry_gap=0.03),
            "strict_veto",
            "2024-01-02",
            "2026-08-07",
        )
        self.assertTrue(result["trades"])
        self.assertTrue(all(trade["entry_gap"] <= 0.03 + 1e-12 for trade in result["trades"]))

    def test_invalid_same_session_delay_is_rejected(self):
        with self.assertRaises(ValueError):
            MODULE["simulate"](
                self.panels,
                self.symbols,
                self.candidate_config(entry_delay_sessions=0),
                "strict_veto",
                "2024-01-02",
                "2026-08-07",
            )


if __name__ == "__main__":
    unittest.main()
