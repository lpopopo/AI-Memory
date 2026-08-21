from pathlib import Path
import runpy
import unittest


MODULE = runpy.run_path(str(Path(__file__).with_name("evaluate_risk_filter_ablation.py")))


class RiskFilterAblationTests(unittest.TestCase):
    def test_ablation_variants_change_only_intended_fields(self):
        variants = MODULE["VARIANTS"]
        baseline = variants["matched_baseline"].__dict__
        atr_only = variants["atr_only"].__dict__
        location_only = variants["close_location_only"].__dict__
        combined = variants["combined"].__dict__
        self.assertEqual(
            {key for key in baseline if baseline[key] != atr_only[key]},
            {"max_atr_pct"},
        )
        self.assertEqual(
            {key for key in baseline if baseline[key] != location_only[key]},
            {"min_close_location"},
        )
        self.assertEqual(
            {key for key in baseline if baseline[key] != combined[key]},
            {"max_atr_pct", "min_close_location"},
        )

    def test_block_bootstrap_is_deterministic(self):
        baseline = {f"2026-01-{day:02d}": 100.0 for day in range(1, 11)}
        candidate = {f"2026-01-{day:02d}": 100.0 + day for day in range(1, 11)}
        first = MODULE["paired_block_bootstrap"](baseline, candidate, samples=100, block=3, seed=7)
        second = MODULE["paired_block_bootstrap"](baseline, candidate, samples=100, block=3, seed=7)
        self.assertEqual(first, second)
        self.assertEqual(first["probability_higher_return"], 1.0)


if __name__ == "__main__":
    unittest.main()
