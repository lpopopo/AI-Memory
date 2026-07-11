import unittest

import numpy as np
import pandas as pd

from v9_research_monitors import (
    build_research_diagnostics,
    panic_to_repair_label,
    realized_vol126,
    slow_vol_scale,
)


class ResearchMonitorTests(unittest.TestCase):
    def synthetic_market(self):
        index = pd.bdate_range("2020-01-01", periods=400)
        # Deep drawdown then rebound into the final window.
        path = np.concatenate([
            np.linspace(100, 120, 200),
            np.linspace(120, 80, 100),
            np.linspace(80, 100, 100),
        ])
        close = pd.DataFrame({
            "SPY": path,
            "QQQ": path * 1.02,
            "SMH": path * 1.05,
            "IWM": path * 0.9,
            "RSP": path * 0.95,
            "HYG": np.linspace(90, 95, 400),
            "LQD": np.linspace(100, 102, 400),
        }, index=index)
        vix = pd.DataFrame({
            "^VIX": np.concatenate([np.full(250, 18.0), np.full(80, 32.0), np.full(70, 22.0)]),
            "^VIX3M": np.concatenate([np.full(250, 20.0), np.full(80, 28.0), np.full(70, 23.0)]),
        }, index=index)
        return index, close, vix

    def test_vol126_and_scale_are_bounded(self):
        _, close, _ = self.synthetic_market()
        vol = realized_vol126(close["SPY"]).dropna()
        scale = slow_vol_scale(close["SPY"]).dropna()
        self.assertFalse(vol.empty)
        self.assertTrue((scale >= 0.25).all())
        self.assertTrue((scale <= 1.0).all())

    def test_panic_to_repair_detects_rebound_package(self):
        index, close, vix = self.synthetic_market()
        label = panic_to_repair_label(close, vix, index[-1], prior_drawdown_threshold=-0.10, rebound_threshold=0.05)
        self.assertIn(label["label"], {"panic_to_repair", "post_drawdown_watch", "normal"})
        self.assertFalse(label["authorizes_trade"])

    def test_diagnostics_are_read_only(self):
        index, close, vix = self.synthetic_market()
        diagnostics = build_research_diagnostics(close, vix, index[-1])
        self.assertFalse(diagnostics["authorizes_trade"])
        self.assertIn(diagnostics["fear_gate_advisory"]["regime"], {"normal", "elevated", "stress", "panic"})
        self.assertIn("absolute_momentum", diagnostics["momentum_families"]["families"]["SPY"])
        self.assertEqual(diagnostics["behavioral_execution_audit"]["violation_count"], 0)


if __name__ == "__main__":
    unittest.main()
