import importlib.util
import unittest
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("ranking", HERE / "evaluate_capital_constrained_ranking.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BACKTEST = MODULE.BACKTEST


def feature_panel(values):
    index = pd.to_datetime(["2026-01-02", "2026-01-05"])
    symbols = ["A", "B", "C"]
    frames = {}
    for name, row in values.items():
        frames[name] = pd.DataFrame([row, row], index=index, columns=symbols)
    return frames, index, symbols


class CapitalConstrainedRankingTests(unittest.TestCase):
    def test_formal_composite_preserves_current_score_order(self):
        features, dates, symbols = feature_panel(
            {
                "score": [4.0, 6.0, 5.0],
                "rs20": [0.03, 0.04, 0.05],
                "volume_ratio": [1.2, 1.3, 1.4],
                "close_location": [0.6, 0.7, 0.8],
                "atr_pct": [0.03, 0.02, 0.01],
            }
        )
        ranked = BACKTEST["rank_entry_candidates"](
            features, dates[0], symbols, "formal_composite"
        )
        self.assertEqual([row["symbol"] for row in ranked], ["B", "C", "A"])

    def test_balanced_rank_uses_only_requested_close(self):
        features, dates, symbols = feature_panel(
            {
                "score": [4.0, 6.0, 5.0],
                "rs20": [0.06, 0.04, 0.03],
                "volume_ratio": [1.8, 1.3, 1.2],
                "close_location": [0.9, 0.6, 0.5],
                "atr_pct": [0.01, 0.03, 0.04],
            }
        )
        before = BACKTEST["rank_entry_candidates"](
            features, dates[0], symbols, "balanced_rank"
        )
        for frame in features.values():
            frame.loc[dates[1], :] = [999.0, -999.0, 500.0]
        after = BACKTEST["rank_entry_candidates"](
            features, dates[0], symbols, "balanced_rank"
        )
        self.assertEqual(before, after)
        self.assertEqual(before[0]["symbol"], "A")

    def test_profit_concentration_aggregates_repeated_symbol_wins(self):
        result = MODULE.profit_concentration(
            [
                {"symbol": "A", "pnl": 10.0},
                {"symbol": "A", "pnl": 5.0},
                {"symbol": "B", "pnl": 15.0},
                {"symbol": "C", "pnl": -20.0},
            ]
        )
        self.assertEqual(result["profitable_symbols"], 2)
        self.assertAlmostEqual(result["top_symbol_profit_share"], 0.5)

    def test_unknown_ranking_mode_is_rejected(self):
        features, dates, symbols = feature_panel(
            {
                "score": [1.0, 2.0, 3.0],
                "rs20": [0.03, 0.04, 0.05],
                "volume_ratio": [1.2, 1.3, 1.4],
                "close_location": [0.6, 0.7, 0.8],
                "atr_pct": [0.03, 0.02, 0.01],
            }
        )
        with self.assertRaises(ValueError):
            BACKTEST["rank_entry_candidates"](features, dates[0], symbols, "future_return")

    def _screen_fixture(self):
        rows = []
        for nav in MODULE.NAVS:
            for slippage in MODULE.SLIPPAGES:
                for period in MODULE.PERIODS:
                    for policy in MODULE.POLICIES:
                        challenger = policy != "formal_composite"
                        rows.append(
                            {
                                "initial_nav": nav,
                                "slippage": slippage,
                                "period": period,
                                "policy": policy,
                                "total_return": 0.12 if challenger else 0.10,
                                "max_drawdown": -0.10,
                                "sharpe": 1.1 if challenger else 1.0,
                                "win_rate": 0.60,
                                "ranking_contention_decisions": 6,
                                "profitable_symbols": 4,
                                "top_symbol_profit_share": 0.30,
                            }
                        )
        return pd.DataFrame(rows)

    def test_screen_requires_cross_period_contention(self):
        metrics = self._screen_fixture()
        metrics.loc[
            (metrics["policy"] == "balanced_rank")
            & (metrics["period"] == "heldout_2026"),
            "ranking_contention_decisions",
        ] = 0
        screen, _ = MODULE.challenger_screen(metrics)
        row = screen.loc[screen["policy"] == "balanced_rank"].iloc[0]
        self.assertEqual(row["status"], "insufficient")
        self.assertFalse(row["passes"])

    def test_screen_selects_highest_minimum_return_improvement(self):
        metrics = self._screen_fixture()
        metrics.loc[metrics["policy"] == "rs_only", "total_return"] = 0.13
        metrics.loc[metrics["policy"] == "low_atr_first", "total_return"] = 0.125
        metrics.loc[metrics["policy"] == "balanced_rank", "total_return"] = 0.12
        screen, winner = MODULE.challenger_screen(metrics)
        self.assertTrue(screen["passes"].all())
        self.assertEqual(winner, "rs_only")


if __name__ == "__main__":
    unittest.main()
