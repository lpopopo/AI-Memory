import unittest

import pandas as pd

from download_v9_data import (
    FIELDS,
    REQUIRED_MARKET_SYMBOLS,
    parse_cboe_history,
    parse_yahoo_chart,
    validate_requested_ohlcv,
    validate_required_close,
)


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

    def test_yahoo_chart_parser_adjusts_ohlc_and_excludes_live_bar(self):
        timestamps = [
            int(pd.Timestamp("2026-08-18 16:00", tz="America/New_York").timestamp()),
            int(pd.Timestamp("2026-08-19 16:00", tz="America/New_York").timestamp()),
        ]
        payload = {
            "chart": {
                "error": None,
                "result": [
                    {
                        "timestamp": timestamps,
                        "indicators": {
                            "quote": [
                                {
                                    "open": [100.0, 110.0],
                                    "high": [105.0, 115.0],
                                    "low": [95.0, 105.0],
                                    "close": [100.0, 110.0],
                                    "volume": [1000, 2000],
                                }
                            ],
                            "adjclose": [{"adjclose": [50.0, 55.0]}],
                        },
                    }
                ],
            }
        }
        parsed = parse_yahoo_chart(payload, pd.Timestamp("2026-08-18"))
        self.assertEqual(list(parsed.index), [pd.Timestamp("2026-08-18")])
        self.assertEqual(parsed.iloc[0]["Open"], 50.0)
        self.assertEqual(parsed.iloc[0]["High"], 52.5)
        self.assertEqual(parsed.iloc[0]["Close"], 50.0)
        self.assertEqual(parsed.iloc[0]["Volume"], 1000)

    def test_requested_ohlcv_rejects_stale_watchlist_symbol(self):
        date = pd.Timestamp("2026-08-18")
        dfs = {field: pd.DataFrame({"ASML": [1.0]}, index=[date]) for field in FIELDS}
        validate_requested_ohlcv(dfs, {"ASML"}, date)
        dfs["Volume"].loc[date, "ASML"] = float("nan")
        with self.assertRaises(RuntimeError):
            validate_requested_ohlcv(dfs, {"ASML"}, date)


if __name__ == "__main__":
    unittest.main()
