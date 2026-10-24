import unittest
import numpy as np
from analysis_tools import noise_standard_deviation


class NoiseModelTests(unittest.TestCase):
    def test_independent_variance_formulas(self):
        central = noise_standard_deviation([-0.5, 0.5], 0.01, 0.1)
        richardson = noise_standard_deviation([1/6, -4/3, 4/3, -1/6], 0.01, 0.1)
        self.assertAlmostEqual(central, 0.01/(np.sqrt(2)*0.1))
        self.assertAlmostEqual(richardson, np.sqrt(65/18)*0.01/0.1)
        self.assertAlmostEqual((richardson/central)**2, 65/9)

    def test_zero_noise_and_invalid_parameters(self):
        self.assertEqual(noise_standard_deviation([1, -1], 0, 1), 0)
        for weights, sigma, step in [([], 1, 1), ([np.nan], 1, 1), ([1], -1, 1), ([1], 1, 0)]:
            with self.assertRaises(ValueError):
                noise_standard_deviation(weights, sigma, step)

    def test_seeded_noise_agrees_with_variance_model(self):
        rng = np.random.default_rng(2026)
        samples = rng.normal(0, 0.01, (20000, 2))
        estimates = (samples[:, 1]-samples[:, 0])/0.2
        predicted = noise_standard_deviation([-0.5, 0.5], 0.01, 0.1)
        self.assertLess(abs(np.std(estimates, ddof=1)/predicted-1), 0.03)
