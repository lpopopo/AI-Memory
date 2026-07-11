import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from v81_dynamic_enhancer import TrendVote, V81Allocator, V81Config
from v8_signal import target_v81_from_close


def rising_frame(spy_slope=1.0, qqq_slope=2.0, vt_slope=1.5, vt_start=0):
    dates = pd.bdate_range("2020-01-01", periods=420)
    frame = pd.DataFrame(index=dates)
    frame["SPY"] = [100 + spy_slope * i for i in range(420)]
    frame["QQQ"] = [100 + qqq_slope * i for i in range(420)]
    frame["VT"] = [100 + vt_slope * i if i >= vt_start else float("nan") for i in range(420)]
    return frame


class V81StateTest(unittest.TestCase):
    def test_hysteresis_and_two_step_confirmation(self):
        vote = TrendVote()
        self.assertFalse(vote.update(102, 100, 0.01, 2))
        self.assertTrue(vote.update(102, 100, 0.01, 2))
        self.assertTrue(vote.update(99.5, 100, 0.01, 2))  # neutral band
        self.assertTrue(vote.update(98, 100, 0.01, 2))
        self.assertFalse(vote.update(98, 100, 0.01, 2))

    def test_vt_before_inception_is_ineligible(self):
        close = rising_frame(vt_start=350)
        allocator = V81Allocator(close, V81Config(), enhancer=True)
        dt = close.index[300]
        allocator.target(dt)
        self.assertFalse(allocator.audit[-1]["eligible"]["VT"])

    def test_enhancer_never_exceeds_half_and_total_never_exceeds_one(self):
        close = rising_frame(spy_slope=-0.05, qqq_slope=1.0, vt_slope=0.5)
        allocator = V81Allocator(close, V81Config(), enhancer=True)
        for dt in close.index[200::5]:
            target = allocator.target(dt)
            self.assertLessEqual(allocator.audit[-1]["enhancer_budget"], 0.5)
            self.assertLessEqual(sum(target.values()), 1.0 + 1e-12)

    def test_duplicate_qqq_combines_to_full_weight(self):
        close = rising_frame(spy_slope=-0.20, qqq_slope=2.0, vt_slope=-0.10)
        allocator = V81Allocator(close, V81Config(), enhancer=True)
        target = allocator.target(close.index[-1])
        self.assertEqual(allocator.audit[-1]["enhancer_selected"], "QQQ")
        self.assertAlmostEqual(target["QQQ"], 1.0)
        self.assertNotIn("SPY", target)

    def test_floor_fraction_keeps_25_percent_total_core(self):
        close = rising_frame(spy_slope=-0.20, qqq_slope=-0.10, vt_slope=-0.05)
        allocator = V81Allocator(
            close, V81Config(floor_fraction=0.25), enhancer=False
        )
        target = allocator.target(close.index[-1])
        self.assertAlmostEqual(sum(target.values()), 0.25)

    def test_signal_interface_exposes_votes_scores_and_final_weights(self):
        close = rising_frame()
        signal = target_v81_from_close(close)
        self.assertEqual(signal["status"], "research_only_not_promoted")
        self.assertIn("SPY", signal["core_votes"])
        self.assertIn("QQQ", signal["enhancer"]["scores"])
        self.assertLessEqual(signal["target_equity_weight"], 1.0)


if __name__ == "__main__":
    unittest.main()
