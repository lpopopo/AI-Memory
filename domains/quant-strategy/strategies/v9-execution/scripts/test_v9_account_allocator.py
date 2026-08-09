import unittest

from v9_account_allocator import reconcile_whole_share_account


class AccountAllocatorTests(unittest.TestCase):
    def test_current_account_is_fee_aware_and_proposal_only(self):
        result = reconcile_whole_share_account(
            cash=3756.49,
            positions={"GLW": 2, "MXL": 6, "MRVL": 4, "QCOM": 2},
            prices={"GLW": 165.68, "MXL": 74.98, "MRVL": 218.72, "QCOM": 167.86, "SPY": 773.26, "QQQ": 723.03},
            desired_core_weights={"SPY": .35, "QQQ": .35},
            stock_symbols={"GLW", "MXL", "MRVL", "QCOM"},
            cash_floor=.05,
            stock_cap=.25,
            fee_per_order=1.0,
            order_authorized=False,
            authorization_reason="missed_month_end_late_fill_not_authorized",
        )
        self.assertEqual(result["target_core_shares"], {"QQQ": 2, "SPY": 2})
        self.assertGreaterEqual(result["ending_cash_weight"], .05)
        self.assertEqual(result["executable_orders"], [])
        self.assertIn("stock_sleeve_over_cap_no_new_stock_risk", result["alerts"])
        self.assertIn("proposal_only_signal_authorization_missing", result["alerts"])

    def test_authorized_plan_exposes_orders_but_never_breaches_cash_floor(self):
        result = reconcile_whole_share_account(
            cash=10000,
            positions={},
            prices={"SPY": 500, "QQQ": 400},
            desired_core_weights={"SPY": .35, "QQQ": .35},
            stock_symbols=set(),
            cash_floor=.05,
            stock_cap=.25,
            order_authorized=True,
            authorization_reason="completed_month_end_signal",
        )
        self.assertEqual(result["executable_orders"], result["proposed_orders"])
        self.assertGreaterEqual(result["ending_cash_weight"], .05)

    def test_missing_price_is_rejected(self):
        with self.assertRaises(ValueError):
            reconcile_whole_share_account(
                cash=1000,
                positions={"GLW": 1},
                prices={"SPY": 500},
                desired_core_weights={"SPY": .35},
                stock_symbols={"GLW"},
                cash_floor=.05,
                stock_cap=.25,
            )


if __name__ == "__main__":
    unittest.main()
