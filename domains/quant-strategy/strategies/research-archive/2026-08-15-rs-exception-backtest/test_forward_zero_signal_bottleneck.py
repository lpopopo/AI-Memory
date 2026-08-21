import unittest

import pandas as pd

import evaluate_forward_zero_signal_bottleneck as target


class ForwardZeroSignalBottleneckTests(unittest.TestCase):
    def test_sequential_survivors_use_frozen_order(self):
        index = pd.to_datetime(["2026-08-17"])
        columns = ["A", "B"]
        conditions = {
            name: pd.DataFrame(True, index=index, columns=columns)
            for name in target.FUNNEL
        }
        conditions["smh_ma50"].loc[:, :] = False
        counts, frames = target.sequential_survivors(conditions)
        self.assertEqual(int(counts.iloc[0]["broad_gate"]), 2)
        self.assertEqual(int(counts.iloc[0]["smh_ma50"]), 0)
        self.assertEqual(int(counts.iloc[0]["close_location_at_least_50pct"]), 0)
        self.assertFalse(frames["close_location_at_least_50pct"].to_numpy().any())

    def test_first_zero_step_is_first_binding_layer(self):
        counts = pd.Series({name: 2 for name in target.FUNNEL})
        counts.loc["volume_ratio_at_least_1_2":] = 0
        self.assertEqual(target.first_zero_step(counts), "volume_ratio_at_least_1_2")

    def test_no_zero_returns_none(self):
        counts = pd.Series({name: 1 for name in target.FUNNEL})
        self.assertIsNone(target.first_zero_step(counts))

    def test_binding_symbols_are_prior_survivors_that_fail_current_step(self):
        index = pd.to_datetime(["2026-08-17"])
        columns = ["A", "B"]
        conditions = {
            name: pd.DataFrame(True, index=index, columns=columns)
            for name in target.FUNNEL
        }
        conditions["above_ma20"].at[index[0], "B"] = False
        _, frames = target.sequential_survivors(conditions)
        self.assertEqual(
            target.binding_symbols(index[0], "above_ma20", conditions, frames),
            ["B"],
        )


if __name__ == "__main__":
    unittest.main()
