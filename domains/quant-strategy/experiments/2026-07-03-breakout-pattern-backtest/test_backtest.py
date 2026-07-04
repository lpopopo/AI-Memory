import importlib.util
import pathlib
import sys
import unittest

import pandas as pd


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("breakout_backtest", HERE / "run_backtest.py")
bt = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bt
SPEC.loader.exec_module(bt)


def frame(rows):
    df = pd.DataFrame(rows, index=pd.date_range("2025-01-01", periods=len(rows), freq="B"))
    for col, default in {
        "Volume": 100.0, "ma20": 100.0, "ma50": 95.0, "high20": 110.0,
        "prev_high20": 109.0, "upper_wick": 0.0, "body": 1.0,
    }.items():
        if col not in df:
            df[col] = default
    return df


class ExecutionSemanticsTest(unittest.TestCase):
    def test_close_signal_enters_next_open(self):
        df = frame([
            {"Open": 100, "High": 102, "Low": 99, "Close": 101},
            {"Open": 105, "High": 107, "Low": 104, "Close": 106},
            {"Open": 106, "High": 108, "Low": 105, "Close": 107},
        ])
        t = bt.simulate_trade(df, {"ticker": "T", "entry_idx": 0, "stop": 90,
                                  "breakout_level": 90}, pattern="C")
        self.assertEqual(t.signal_date, df.index[0])
        self.assertEqual(t.entry_date, df.index[1])
        self.assertEqual(t.entry_price, 105)

    def test_intraday_stop_fills_at_stop_not_close(self):
        df = frame([
            {"Open": 100, "High": 101, "Low": 99, "Close": 100},
            {"Open": 100, "High": 102, "Low": 99, "Close": 101},
            {"Open": 101, "High": 120, "Low": 94, "Close": 118},
        ])
        t = bt.simulate_trade(df, {"ticker": "T", "entry_idx": 0, "stop": 95,
                                  "breakout_level": 90}, pattern="C")
        self.assertEqual(t.exit_reason, "stop_loss")
        self.assertEqual(t.exit_price, 95)
        self.assertLess(t.net_return, 0)

    def test_gap_through_stop_pays_gap_open(self):
        df = frame([
            {"Open": 100, "High": 101, "Low": 99, "Close": 100},
            {"Open": 100, "High": 102, "Low": 99, "Close": 101},
            {"Open": 90, "High": 94, "Low": 88, "Close": 93},
        ])
        t = bt.simulate_trade(df, {"ticker": "T", "entry_idx": 0, "stop": 95,
                                  "breakout_level": 90}, pattern="C")
        self.assertEqual(t.exit_price, 90)

    def test_pattern_c_does_not_use_breakout_exit(self):
        df = frame([
            {"Open": 100, "High": 101, "Low": 99, "Close": 100},
            {"Open": 100, "High": 101, "Low": 99, "Close": 100},
            {"Open": 100, "High": 101, "Low": 99, "Close": 89},
        ])
        t = bt.simulate_trade(df, {"ticker": "T", "entry_idx": 0, "stop": 80,
                                  "breakout_level": 95}, pattern="C")
        self.assertNotEqual(t.exit_reason, "false_breakout")


if __name__ == "__main__":
    unittest.main()
