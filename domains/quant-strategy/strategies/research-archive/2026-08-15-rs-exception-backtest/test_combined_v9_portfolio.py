from pathlib import Path
import runpy
import unittest

import pandas as pd


HERE = Path(__file__).resolve().parent
COMBINED = runpy.run_path(str(HERE / "evaluate_combined_v9_portfolio.py"))


class CombinedPortfolioTests(unittest.TestCase):
    def test_combination_adds_module_dollar_pnl_without_double_counting_cash(self):
        dates = pd.to_datetime(["2026-01-02", "2026-01-05"])
        core = pd.Series([6000.0, 6060.0], index=dates)
        stock = pd.Series([6000.0, 6030.0], index=dates)
        combined = COMBINED["combine_curves"](core, stock)
        self.assertEqual(combined.tolist(), [6000.0, 6090.0])


if __name__ == "__main__":
    unittest.main()
