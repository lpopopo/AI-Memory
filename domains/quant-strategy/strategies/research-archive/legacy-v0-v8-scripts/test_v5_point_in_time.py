import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from backtest_v5_point_in_time import Membership, growth_weights_pit
from optimize_v8_robust import CONFIG
from test_v4_stock_alpha import prepare_indicators


class PointInTimeUniverseTest(unittest.TestCase):
    def setUp(self):
        self.history = pd.DataFrame({
            "symbol": ["OLD", "FUTURE"],
            "opt-in": pd.to_datetime(["2020-01-01", "2021-01-01"]),
            "opt-out": pd.to_datetime(["2020-07-01", None]),
        })
        self.membership = Membership(self.history)

    def test_membership_obeys_effective_interval(self):
        self.assertEqual(self.membership.at(pd.Timestamp("2020-06-30")), {"OLD"})
        self.assertEqual(self.membership.at(pd.Timestamp("2020-07-01")), set())
        self.assertEqual(self.membership.at(pd.Timestamp("2021-01-01")), {"FUTURE"})

    def test_event_maps_to_first_trading_date_not_before_event(self):
        calendar = pd.bdate_range("2020-06-29", "2020-07-06")
        events = self.membership.event_dates(calendar)
        self.assertIn(pd.Timestamp("2020-07-01"), events)

    def test_future_member_cannot_enter_ranking(self):
        dates = pd.bdate_range("2019-01-01", periods=400)
        close = pd.DataFrame({
            "OLD": [100 + i * 0.1 for i in range(400)],
            "FUTURE": [100 + i * 1.0 for i in range(400)],
        }, index=dates)
        indicators = prepare_indicators(close)
        dt = dates[300]  # 2020, before FUTURE's 2021 opt-in.
        weights, audit = growth_weights_pit(
            CONFIG, close, indicators, self.membership, dt, 0.70, False
        )
        self.assertIn("OLD", weights)
        self.assertNotIn("FUTURE", weights)
        self.assertEqual(audit["members"], 1)

    def test_coverage_adjustment_reserves_cash(self):
        dates = pd.bdate_range("2019-01-01", periods=400)
        close = pd.DataFrame({
            "OLD": [100 + i * 0.1 for i in range(400)],
            "MISSING": [float("nan")] * 400,
        }, index=dates)
        history = pd.DataFrame({
            "symbol": ["OLD", "MISSING"],
            "opt-in": pd.to_datetime(["2010-01-01", "2010-01-01"]),
            "opt-out": pd.to_datetime([None, None]),
        })
        indicators = prepare_indicators(close)
        weights, audit = growth_weights_pit(
            CONFIG, close, indicators, Membership(history), dates[300], 0.70, True
        )
        self.assertAlmostEqual(audit["coverage"], 0.5)
        self.assertAlmostEqual(sum(weights.values()), 0.035)  # 35% target / top-10 denominator.


if __name__ == "__main__":
    unittest.main()
