import unittest

import pandas as pd

from download_v9_data import REQUIRED_MARKET_SYMBOLS, parse_cboe_history, validate_required_close


class DownloadV9DataTests(unittest.TestCase):
    def complete_close(self, last="2026-08-07"):
        index = pd.DatetimeIndex([pd.Timestamp(last)])
        return pd.DataFrame({symbol: [1.0] for symbol in REQUIRED_MARKET_SYMBOLS}, index=index)

    def test_required_market_data_must_reach_declared_completed_session(self):
        validate_required_close(self.complete_close(), pd.Timestamp("2026-08-07"))

    def test_stale_required_proxy_is_rejected_before_cache_overwrite(self):
        close = self.complete_close()
        close.loc[:, "SMH"] = float("nan")
        with self.assertRaises(RuntimeError):
            validate_required_close(close, pd.Timestamp("2026-08-07"))

    def test_missing_required_proxy_is_rejected_before_cache_overwrite(self):
        close = self.complete_close().drop(columns="^VIX3M")
        with self.assertRaises(RuntimeError):
            validate_required_close(close, pd.Timestamp("2026-08-07"))

    def test_cboe_history_parser_normalizes_columns_and_completed_date(self):
        raw = pd.DataFrame(
            {
                "DATE": ["08/06/2026", "08/07/2026", "08/10/2026"],
                " OPEN": [18.0, 18.1, 18.2],
                "HIGH": [19.0, 19.1, 19.2],
                "LOW": [17.0, 17.1, 17.2],
                "CLOSE": [18.69, 18.72, 18.80],
            }
        )
        parsed = parse_cboe_history(raw, pd.Timestamp("2026-08-07"))
        self.assertEqual(list(parsed.columns), ["Open", "High", "Low", "Close"])
        self.assertEqual(parsed.index[-1], pd.Timestamp("2026-08-07"))
        self.assertEqual(parsed.loc[pd.Timestamp("2026-08-07"), "Close"], 18.72)

    def test_cboe_history_parser_requires_close(self):
        with self.assertRaises(ValueError):
            parse_cboe_history(pd.DataFrame({"DATE": ["08/07/2026"]}), pd.Timestamp("2026-08-07"))


if __name__ == "__main__":
    unittest.main()
