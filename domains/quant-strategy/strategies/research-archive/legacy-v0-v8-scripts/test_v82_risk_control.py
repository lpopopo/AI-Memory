import unittest

import numpy as np
import pandas as pd

from v82_risk_control import V82Allocator, V82Config


class V82Tests(unittest.TestCase):
    def setUp(self):
        index = pd.bdate_range("2020-01-01", periods=300)
        self.close = pd.DataFrame({
            "SPY": 100 * np.exp(np.linspace(0, .20, len(index))),
            "QQQ": 100 * np.exp(np.linspace(0, .35, len(index))),
        }, index=index)

    def test_no_leverage(self):
        allocator = V82Allocator(self.close, V82Config("inverse_vol", 60, .10, 20, .50))
        target = allocator.target(self.close.index[-1])
        self.assertLessEqual(sum(target.values()), 1.0 + 1e-10)
        self.assertLessEqual(target.get("QQQ", 0), .50 + 1e-10)

    def test_volatility_target_only_scales_down(self):
        allocator = V82Allocator(self.close, V82Config("fixed", 60, .10, 20, 1.0))
        allocator.target(self.close.index[-1])
        self.assertLessEqual(allocator.audit[-1]["volatility_scale"], 1.0)

    def test_invalid_parameter_rejected(self):
        with self.assertRaises(ValueError):
            V82Config(target_volatility=.20)


if __name__ == "__main__":
    unittest.main()
