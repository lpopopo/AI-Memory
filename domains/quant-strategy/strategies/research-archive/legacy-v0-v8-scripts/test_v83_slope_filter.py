import unittest
import numpy as np
import pandas as pd
from v83_slope_filter import V83Allocator,V83Config


class V83Tests(unittest.TestCase):
    def setUp(self):
        idx=pd.bdate_range("2018-01-01",periods=400)
        self.up=pd.DataFrame({"SPY":np.linspace(100,180,400),"QQQ":np.linspace(100,220,400)},index=idx)

    def test_baseline_is_fully_invested_in_uptrend(self):
        a=V83Allocator(self.up,V83Config()); t=a.target(self.up.index[-1])
        self.assertAlmostEqual(t["SPY"],.5); self.assertAlmostEqual(t["QQQ"],.5)

    def test_positive_slope_confirms_uptrend(self):
        a=V83Allocator(self.up,V83Config(63,.005,"both")); t=a.target(self.up.index[-1])
        self.assertLessEqual(sum(t.values()),1); self.assertGreater(sum(t.values()),0)

    def test_flat_market_fails_positive_slope(self):
        flat=self.up*0+100; a=V83Allocator(flat,V83Config(63,.005,"both"))
        self.assertEqual(a.target(flat.index[-1]),{})

    def test_invalid_config(self):
        with self.assertRaises(ValueError): V83Config(42,0,"both")


if __name__=="__main__": unittest.main()
