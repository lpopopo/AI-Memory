import unittest

import numpy as np
import pandas as pd

import evaluate_selection_bias_audit as target


class SelectionBiasAuditTests(unittest.TestCase):
    def toy_paths(self, count=120):
        rng = np.random.default_rng(7)
        names = [row[0] for row in target.grid()]
        baseline = rng.normal(0.0001, 0.01, count)
        data = {}
        for offset, name in enumerate(names):
            data[name] = baseline + rng.normal(0.0, 0.0005, count)
        data[target.BASELINE_ID] = baseline
        data[target.FIXED_ID] = baseline + rng.normal(0.0005, 0.0002, count)
        return pd.DataFrame(data, index=pd.bdate_range("2024-01-02", periods=count))[names]

    def test_grid_is_frozen_twenty_cell_family(self):
        cells = target.grid()
        self.assertEqual(len(cells), 20)
        self.assertEqual(len({row[0] for row in cells}), 20)
        self.assertIn((target.BASELINE_ID, 1.0, 0.0), cells)
        self.assertIn((target.FIXED_ID, 0.04, 0.5), cells)

    def test_contiguous_blocks_cover_each_observation_once(self):
        blocks = target.contiguous_blocks(103)
        self.assertEqual(len(blocks), 10)
        self.assertEqual(np.concatenate(blocks).tolist(), list(range(103)))
        self.assertLessEqual(max(map(len, blocks)) - min(map(len, blocks)), 1)

    def test_cscv_runs_all_252_splits(self):
        splits, summary = target.cscv(self.toy_paths())
        self.assertEqual(len(splits), 252)
        self.assertEqual(summary["splits"], 252)
        self.assertGreaterEqual(summary["pbo"], 0.0)
        self.assertLessEqual(summary["pbo"], 1.0)

    def test_familywise_bootstrap_is_deterministic(self):
        paths = self.toy_paths(80)
        first = target.familywise_reality_check(paths, samples=100, block=5, seed=11)
        second = target.familywise_reality_check(paths, samples=100, block=5, seed=11)
        self.assertEqual(first, second)
        self.assertGreater(first["familywise_p_value"], 0.0)
        self.assertLessEqual(first["familywise_p_value"], 1.0)

    def test_gate_requires_every_registered_condition(self):
        passed = target.interpretation_gate(
            {"pbo": 0.49},
            {"familywise_p_value": 0.09},
            {"positive_return_blocks": 7, "positive_sharpe_blocks": 7},
        )
        self.assertTrue(passed["contained"])
        failed = target.interpretation_gate(
            {"pbo": 0.50},
            {"familywise_p_value": 0.09},
            {"positive_return_blocks": 7, "positive_sharpe_blocks": 7},
        )
        self.assertFalse(failed["contained"])


if __name__ == "__main__":
    unittest.main()
