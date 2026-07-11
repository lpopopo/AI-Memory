import unittest
import numpy as np
import pandas as pd
from market_sentiment import compute_sentiment, confirmed_contrarian_state, rolling_percentile


class MarketSentimentTests(unittest.TestCase):
    def data(self, periods=1100):
        i = pd.bdate_range("2018-01-01", periods=periods)
        base = np.linspace(100, 180, periods)
        return pd.DataFrame({
            "SPY": base, "QQQ": base * 1.1, "IWM": base * 0.9,
            "RSP": base * .95, "HYG": 80 + np.linspace(0, 8, periods),
            "LQD": 100 + np.linspace(0, 5, periods), "TLT": 110 - np.linspace(0, 5, periods),
            "^VIX": np.full(periods, 15.), "^VIX3M": np.full(periods, 18.),
        }, index=i)

    def test_percentile_is_causal(self):
        s = pd.Series(np.arange(300, dtype=float))
        before = rolling_percentile(s).iloc[-1]
        s2 = pd.concat([s, pd.Series([10000.])], ignore_index=True)
        self.assertEqual(before, rolling_percentile(s2).iloc[-2])

    def test_score_range_and_components(self):
        out = compute_sentiment(self.data())
        clean = out.sentiment_score.dropna()
        self.assertTrue(((clean >= 0) & (clean <= 100)).all())
        self.assertGreaterEqual(int(out.available_components.dropna().iloc[-1]), 6)

    def test_missing_data_is_not_neutral(self):
        with self.assertRaises(ValueError):
            compute_sentiment(self.data().drop(columns=["TLT"]))

    def test_confirmation_requires_repair(self):
        d = self.data(); s = compute_sentiment(d)
        state = confirmed_contrarian_state(d, s)
        self.assertFalse(state.confirmation.fillna(False).iloc[:252].any())


if __name__ == "__main__":
    unittest.main()
