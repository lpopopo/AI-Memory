from pathlib import Path
import runpy
import unittest

import numpy as np
import pandas as pd


MODULE = runpy.run_path(str(Path(__file__).with_name("pit_low_vol_backtest.py")))


class PointInTimeBacktestTests(unittest.TestCase):
    def test_target_is_applied_to_following_session_return(self):
        dates = pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-06"])
        prices = pd.DataFrame({"A": [100.0, 110.0, 121.0]}, index=dates)
        targets = pd.DataFrame({"A": [1.0]}, index=pd.DatetimeIndex([dates[0]]))
        result, _ = MODULE["simulate"](prices, targets, cost_bps=10.0)
        self.assertAlmostEqual(result.loc[dates[0], "return"], 0.0)
        self.assertAlmostEqual(result.loc[dates[1], "return"], 0.099)
        self.assertAlmostEqual(result.loc[dates[2], "return"], 0.10)

    def test_missing_quote_stress_hits_held_position(self):
        dates = pd.to_datetime(["2020-01-02", "2020-01-03"])
        prices = pd.DataFrame({"A": [100.0, np.nan]}, index=dates)
        targets = pd.DataFrame({"A": [1.0]}, index=pd.DatetimeIndex([dates[0]]))
        result, _ = MODULE["simulate"](prices, targets, cost_bps=0.0, missing_return=-1.0)
        self.assertAlmostEqual(result.loc[dates[1], "return"], -1.0)

    def test_membership_opt_out_is_exclusive(self):
        membership = pd.DataFrame(
            {
                "symbol": ["A", "B"],
                "opt-in": pd.to_datetime(["2020-01-01", "2020-01-01"]),
                "opt-out": pd.to_datetime(["2020-01-03", "2020-01-04"]),
            }
        )
        active = MODULE["active_symbols"](membership, pd.Timestamp("2020-01-03"), pd.Index(["A", "B"]))
        self.assertEqual(list(active), ["B"])


if __name__ == "__main__":
    unittest.main()
