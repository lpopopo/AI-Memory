import unittest

import evaluate_forward_power_duration as target


class ForwardPowerDurationTests(unittest.TestCase):
    def test_wilson_matches_frozen_scorecard_calibration(self):
        low, high = target.wilson_interval(15, 23)
        self.assertAlmostEqual(low, 0.44890335377263)
        self.assertAlmostEqual(high, 0.8118872406120227)

    def test_critical_wins_is_first_tail_below_alpha(self):
        boundary = target.critical_wins(20, 0.50)
        self.assertLessEqual(target.binomial_sf(boundary - 1, 20, 0.50), target.ALPHA)
        self.assertGreater(target.binomial_sf(boundary - 2, 20, 0.50), target.ALPHA)

    def test_minimum_one_sample_reaches_target_power(self):
        trials, power, _ = target.minimum_one_sample(0.50, 0.70)
        self.assertGreaterEqual(power, target.TARGET_POWER)
        prior_power, _ = target.one_sample_power(trials - 1, 0.50, 0.70)
        self.assertLess(prior_power, target.TARGET_POWER)

    def test_two_sample_equal_rates_do_not_have_high_power(self):
        power = target.two_sample_z_power(50, 0.50, 0.50)
        self.assertLess(power, 0.10)

    def test_minimum_two_sample_is_first_power_crossing(self):
        trials, power = target.minimum_two_sample(15 / 23, 19 / 44)
        self.assertGreaterEqual(power, target.TARGET_POWER)
        self.assertLess(
            target.two_sample_z_power(trials - 1, 15 / 23, 19 / 44),
            target.TARGET_POWER,
        )

    def test_wilson_event_requires_one_event_definition(self):
        with self.assertRaises(ValueError):
            target.wilson_event_probability(20, 0.65)
        with self.assertRaises(ValueError):
            target.wilson_event_probability(
                20, 0.65, lower_threshold=0.50, maximum_half_width=0.10
            )

    def test_minimum_wilson_event_is_first_probability_crossing(self):
        trials, probability = target.minimum_wilson_event(
            15 / 23, lower_threshold=0.50
        )
        self.assertGreaterEqual(probability, target.TARGET_POWER)
        self.assertLess(
            target.wilson_event_probability(
                trials - 1, 15 / 23, lower_threshold=0.50
            ),
            target.TARGET_POWER,
        )

    def test_poisson_completion_quantile_is_minimal(self):
        sessions = target.completion_quantile(20, 0.80)
        self.assertGreaterEqual(target.probability_reach(20, sessions), 0.80)
        self.assertLess(target.probability_reach(20, sessions - 1), 0.80)

    def test_poisson_reach_probability_decreases_with_target(self):
        probabilities = [target.probability_reach(value, 126) for value in (20, 27, 32, 48)]
        self.assertTrue(all(value > 0.0 for value in probabilities))
        self.assertTrue(all(left > right for left, right in zip(probabilities, probabilities[1:])))


if __name__ == "__main__":
    unittest.main()
