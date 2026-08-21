#!/usr/bin/env python3
from __future__ import annotations

import unittest

import pandas as pd

from evaluate_high_vol_trend import TrendDefinition, deduplicated_events, definition_signal


class HighVolTrendTests(unittest.TestCase):
    def test_definition_bounds_are_strict_lower_and_inclusive_upper(self):
        index = pd.to_datetime(["2026-01-02", "2026-01-05", "2026-01-06"])
        columns = ["AAA"]
        frame = lambda values: pd.DataFrame({"AAA": values}, index=index)
        components = {
            "shared": frame([True, True, True]),
            "rs20": frame([0.05, 0.05, 0.05]),
            "volume_ratio": frame([1.5, 1.5, 1.5]),
            "atr_pct": frame([0.04, 0.041, 0.12]),
            "extension": frame([0.13, 0.12, 0.25]),
            "close_location": frame([0.60, 0.61, 0.60]),
        }
        definition = TrendDefinition(0.05, 1.5, 0.04, 0.12, 0.12, 0.25, 0.60)
        signal = definition_signal(components, definition)
        self.assertFalse(signal.iloc[0, 0])
        self.assertFalse(signal.iloc[1, 0])
        self.assertTrue(signal.iloc[2, 0])

    def test_deduplication_requires_more_than_twenty_sessions(self):
        index = pd.bdate_range("2026-01-02", periods=23)
        signal = pd.DataFrame(False, index=index, columns=["AAA"])
        signal.iloc[[0, 20, 21], 0] = True
        events = deduplicated_events(signal, cooldown=20)
        self.assertEqual(events, [(index[0], "AAA"), (index[21], "AAA")])


if __name__ == "__main__":
    unittest.main()
