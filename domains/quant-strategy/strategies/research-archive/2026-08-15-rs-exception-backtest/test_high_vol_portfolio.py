#!/usr/bin/env python3
from __future__ import annotations

import unittest

from evaluate_high_vol_portfolio import MAX_TARGET, RISK_BUDGET


class HighVolPortfolioTests(unittest.TestCase):
    def test_risk_sizing_declines_as_stop_widens(self):
        target_8 = min(MAX_TARGET, RISK_BUDGET / 0.08)
        target_15 = min(MAX_TARGET, RISK_BUDGET / 0.15)
        self.assertAlmostEqual(target_8, MAX_TARGET)
        self.assertAlmostEqual(target_15, 0.05)
        self.assertLess(target_15, target_8)


if __name__ == "__main__":
    unittest.main()
