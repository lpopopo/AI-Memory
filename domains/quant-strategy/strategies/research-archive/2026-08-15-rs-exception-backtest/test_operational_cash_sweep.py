#!/usr/bin/env python3
from __future__ import annotations

import unittest

from evaluate_operational_cash_sweep import INSTRUMENTS, WORKING_CASH, scenario_rows, whole_share_position


class OperationalCashSweepTests(unittest.TestCase):
    def test_whole_share_position_never_exceeds_cash(self):
        position = whole_share_position(WORKING_CASH, 1.0, INSTRUMENTS["SGOV"]["price"])
        self.assertEqual(position["shares"], 37)
        self.assertGreaterEqual(position["immediate_cash"], 0.0)

    def test_tax_and_friction_increase_break_even(self):
        rows = scenario_rows().set_index(
            ["ticker", "allocation", "friction_scenario", "tax_haircut", "holding_days"]
        )
        low = rows.at[("SGOV", 0.50, "quoted_spread_roundtrip_1bp", 0.0, 30), "break_even_days"]
        high = rows.at[("SGOV", 0.50, "strategy_stress_10bps_each_side", 0.30, 30), "break_even_days"]
        self.assertGreater(high, low)

    def test_longer_holding_increases_net_income(self):
        rows = scenario_rows().set_index(
            ["ticker", "allocation", "friction_scenario", "tax_haircut", "holding_days"]
        )
        net_30 = rows.at[("SGOV", 0.50, "strategy_stress_10bps_each_side", 0.30, 30), "net_income"]
        net_60 = rows.at[("SGOV", 0.50, "strategy_stress_10bps_each_side", 0.30, 60), "net_income"]
        self.assertGreater(net_60, net_30)


if __name__ == "__main__":
    unittest.main()
