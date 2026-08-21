import importlib.util
import tempfile
import unittest
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "forward_expectancy", HERE / "evaluate_forward_expectancy_scorecard.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ForwardExpectancyScorecardTests(unittest.TestCase):
    def test_wilson_interval_for_fourteen_of_twenty_crosses_half(self):
        low, high = MODULE.wilson_interval(14, 20)
        self.assertLess(low, 0.50)
        self.assertGreater(high, 0.80)
        self.assertAlmostEqual(low, 0.4810, places=3)

    def test_empty_trade_sample_is_awaiting(self):
        score = MODULE.score_trades(
            pd.DataFrame(), {}, "genuine_forward", "RSR1-shadow"
        )
        self.assertEqual(score["evidence_label"], "awaiting_sample")
        self.assertEqual(score["closed_trades"], 0)
        self.assertIsNone(score["expectancy_per_trade"])

    def test_payoff_and_breakeven_are_separate_from_win_rate(self):
        trades = pd.DataFrame(
            [
                {"symbol": "A", "entry_date": "2026-01-02", "exit_date": "2026-01-05", "pnl": 10, "return": 0.10},
                {"symbol": "B", "entry_date": "2026-01-03", "exit_date": "2026-01-06", "pnl": 10, "return": 0.10},
                {"symbol": "C", "entry_date": "2026-01-04", "exit_date": "2026-01-07", "pnl": -5, "return": -0.05},
                {"symbol": "D", "entry_date": "2026-01-05", "exit_date": "2026-01-08", "pnl": -5, "return": -0.05},
            ]
        )
        score = MODULE.score_trades(trades, {}, "test", "variant")
        self.assertAlmostEqual(score["win_rate"], 0.50)
        self.assertAlmostEqual(score["payoff_ratio"], 2.0)
        self.assertAlmostEqual(score["breakeven_win_rate"], 1.0 / 3.0)
        self.assertGreater(score["expectancy_per_trade"], 0.0)

    def test_cluster_bootstrap_is_deterministic_and_positive_for_all_winners(self):
        trades = pd.DataFrame(
            {
                "return": [0.01, 0.02, 0.03, 0.04],
                "entry_cluster": ["a", "a", "b", "c"],
            }
        )
        first = MODULE.clustered_expectancy_bootstrap(trades, samples=1000, seed=7)
        second = MODULE.clustered_expectancy_bootstrap(trades, samples=1000, seed=7)
        self.assertEqual(first, second)
        self.assertGreater(first["p05"], 0.0)
        self.assertEqual(first["probability_nonpositive"], 0.0)

    def test_zero_byte_forward_trade_file_means_zero_trades(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_bytes(b"")
            frame = MODULE.read_csv_if_exists(path)
        self.assertTrue(frame.empty)


if __name__ == "__main__":
    unittest.main()
