from pathlib import Path
import runpy
import unittest

import pandas as pd


HERE = Path(__file__).resolve().parent
TEMPORAL = runpy.run_path(str(HERE / "evaluate_temporal_concentration.py"))


class TemporalConcentrationTests(unittest.TestCase):
    def test_profit_concentration_uses_winners_only(self):
        frame = pd.DataFrame(
            {
                "signal_date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03"],
                "pnl": [60.0, -50.0, 30.0, 10.0],
            }
        )
        result = TEMPORAL["positive_profit_concentration"](frame, "signal_date")
        self.assertEqual(result["gross_profit"], 100.0)
        self.assertAlmostEqual(result["max_group_profit_share"], 0.60)
        self.assertAlmostEqual(result["top_3_group_profit_share"], 1.00)


if __name__ == "__main__":
    unittest.main()
