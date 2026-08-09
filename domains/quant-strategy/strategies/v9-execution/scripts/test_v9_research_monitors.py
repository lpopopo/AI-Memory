import unittest

import numpy as np
import pandas as pd

from v9_research_monitors import (
    build_research_diagnostics,
    compute_fear_snapshot,
    market_semiconductor_turn_snapshot,
    panic_to_repair_label,
    realized_vol126,
    slow_vol_scale,
)
from v9_information_strategy import V9Backtester, V9Config


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
        self.assertFalse(diagnostics["market_semiconductor_turn"]["authorizes_trade"])

    def test_research_and_execution_share_identical_fear_gate(self):
        index, close, vix = self.synthetic_market()
        panels = {
            "open": close.copy(),
            "high": close.copy(),
            "low": close.copy(),
            "close": close.copy(),
            "volume": close * 0 + 1_000_000,
        }
        formal = V9Backtester(panels, vix, [], V9Config())._fear_gate(index[-1])
        research = compute_fear_snapshot(close, vix, index[-1])
        self.assertEqual(research.score, formal["score"])
        self.assertEqual(research.regime, formal["regime"])
        self.assertEqual(research.cash_floor, formal["cash_floor"])
        self.assertEqual(
            [(signal.name, signal.points) for signal in research.signals],
            [(signal["name"], signal["points"]) for signal in formal["signals"]],
        )

    def test_turn_monitor_confirms_only_with_broad_package(self):
        index = pd.bdate_range("2024-01-01", periods=140)
        down = np.linspace(100.0, 82.0, 125)
        rebound = np.linspace(82.0, 96.0, 15)
        qqq = np.concatenate([down, rebound])
        smh = np.concatenate([down * 1.05, np.linspace(86.1, 104.0, 15)])
        close = pd.DataFrame({
            "SPY": qqq * 0.98,
            "QQQ": qqq,
            "SMH": smh,
            "RSP": qqq * np.linspace(0.90, 0.94, 140),
            "HYG": np.linspace(90.0, 96.0, 140),
            "LQD": np.linspace(100.0, 101.0, 140),
        }, index=index)
        vix = pd.DataFrame({
            "^VIX": np.concatenate([np.full(125, 28.0), np.linspace(26.0, 17.0, 15)]),
            "^VIX3M": np.full(140, 22.0),
        }, index=index)
        snapshot = market_semiconductor_turn_snapshot(close, vix, index[-1])
        self.assertEqual(snapshot["stage"], "confirmed_turn")
        self.assertTrue(snapshot["confirmed_turn"])
        self.assertFalse(snapshot["authorizes_trade"])

    def test_turn_monitor_fails_closed_without_credit(self):
        index, close, vix = self.synthetic_market()
        snapshot = market_semiconductor_turn_snapshot(close.drop(columns=["HYG"]), vix, index[-1])
        self.assertEqual(snapshot["stage"], "unavailable")
        self.assertFalse(snapshot["confirmed_turn"])


if __name__ == "__main__":
    unittest.main()
