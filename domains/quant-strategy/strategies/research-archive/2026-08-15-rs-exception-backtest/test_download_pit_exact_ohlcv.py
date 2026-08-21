import unittest

import pandas as pd

import download_pit_exact_ohlcv as target


class PitExactDownloadTests(unittest.TestCase):
    def test_frozen_symbols_require_membership_overlap_and_existing_price_column(self):
        membership = pd.DataFrame(
            {
                "symbol": ["ACTIVE", "OLD", "MISSING"],
                "opt-in": ["2010-01-01", "2000-01-01", "2010-01-01"],
                "opt-out": [None, "2014-12-31", None],
            }
        )
        prices = pd.DataFrame(columns=["ACTIVE", "OLD"])
        self.assertEqual(target.frozen_symbols(membership, prices), ["ACTIVE"])

    def test_provider_symbol_maps_dot_to_yahoo_dash(self):
        self.assertEqual(target.provider_symbol("BRK.B"), "BRK-B")

    def test_extract_series_supports_field_first_multiindex(self):
        index = pd.to_datetime(["2014-01-02", "2014-01-03"])
        columns = pd.MultiIndex.from_tuples([("Close", "ABC")])
        data = pd.DataFrame([[10.0], [11.0]], index=index, columns=columns)
        result = target.extract_series(data, "Close", "ABC")
        self.assertEqual(result.tolist(), [10.0, 11.0])

    def test_merge_download_adds_complete_symbol_without_fragmented_inserts(self):
        index = pd.bdate_range("2014-01-02", periods=35)
        columns = pd.MultiIndex.from_product([target.FIELDS, ["ABC"]])
        data = pd.DataFrame(1.0, index=index, columns=columns)
        panels = {field: pd.DataFrame() for field in target.FIELDS}
        completed = target.merge_download(panels, data, ["ABC"])
        self.assertEqual(completed, {"ABC"})
        self.assertTrue(all("ABC" in panels[field] for field in target.FIELDS))


if __name__ == "__main__":
    unittest.main()
