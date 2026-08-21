#!/usr/bin/env python3
from __future__ import annotations

import unittest

from run_backtest import winner_extension_active


class WinnerExtensionTests(unittest.TestCase):
    def test_extension_requires_every_completed_close_condition(self):
        args = dict(
            entry_price=100.0,
            completed_close=110.0,
            ma20=105.0,
            rs20=0.01,
            held_sessions=20,
            base_hold_days=20,
            extension_days=30,
            minimum_return=0.08,
        )
        self.assertTrue(winner_extension_active(**args))
        self.assertFalse(winner_extension_active(**{**args, "completed_close": 107.0}))
        self.assertFalse(winner_extension_active(**{**args, "ma20": 111.0}))
        self.assertFalse(winner_extension_active(**{**args, "rs20": -0.01}))
        self.assertFalse(winner_extension_active(**{**args, "held_sessions": 30}))

    def test_default_none_never_extends(self):
        self.assertFalse(winner_extension_active(100, 120, 110, 0.1, 20, 20, None, 0.08))


if __name__ == "__main__":
    unittest.main()
