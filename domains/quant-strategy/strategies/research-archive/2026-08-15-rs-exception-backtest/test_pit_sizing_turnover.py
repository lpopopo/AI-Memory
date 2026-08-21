from pathlib import Path
import runpy
import unittest

import pandas as pd


MODULE = runpy.run_path(str(Path(__file__).with_name("pit_sizing_turnover_backtest.py")))


class SizingAndBufferTests(unittest.TestCase):
    def test_soft_vol_weights_keep_all_names_and_sum_to_one(self):
        selected = pd.DataFrame({"rv20": [0.20, 0.30, 0.50]}, index=["A", "B", "C"])
        weights = MODULE["soft_vol_weights"](selected)
        self.assertEqual(set(weights.index), set(selected.index))
        self.assertTrue((weights > 0).all())
        self.assertAlmostEqual(weights.sum(), 1.0)

    def test_buffer_retains_prior_name_inside_top_ten(self):
        symbols = [f"S{i}" for i in range(12)]
        snapshot = pd.DataFrame({"rv20": [0.2] * 12}, index=symbols)
        selected = MODULE["buffered_selection"](snapshot, ["S8", "S1", "S11"])
        self.assertEqual(list(selected.index[:2]), ["S8", "S1"])
        self.assertNotIn("S11", selected.index)
        self.assertEqual(len(selected), 5)


if __name__ == "__main__":
    unittest.main()
