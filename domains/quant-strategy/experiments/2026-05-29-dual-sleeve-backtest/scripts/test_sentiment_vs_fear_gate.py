import unittest
import numpy as np
import pandas as pd
from backtest_sentiment_vs_fear_gate import fear_score_series, scale_to_gross


class ReplacementTests(unittest.TestCase):
    def test_scale_preserves_composition(self):
        out = scale_to_gross({"SPY": .5, "QQQ": .5}, .35)
        self.assertAlmostEqual(sum(out.values()), .35)
        self.assertAlmostEqual(out["SPY"], out["QQQ"])

    def test_fear_score_rises_in_stress(self):
        i = pd.bdate_range("2020-01-01", periods=260)
        base = np.linspace(100, 140, 260); vix = np.full(260, 15.)
        d = pd.DataFrame({"SPY":base,"QQQ":base,"IWM":base,"RSP":base,"HYG":base,"LQD":base,"^VIX":vix,"^VIX3M":np.full(260,18.)},index=i)
        calm = fear_score_series(d).fear_score.iloc[-2]
        d.iloc[-1, d.columns.get_loc("SPY")] = 90; d.iloc[-1, d.columns.get_loc("QQQ")] = 90; d.iloc[-1, d.columns.get_loc("^VIX")] = 40
        stressed = fear_score_series(d).fear_score.iloc[-1]
        self.assertGreater(stressed, calm)


if __name__ == "__main__": unittest.main()
