import unittest
import numpy as np
from analysis_tools import observed_order, first_budget_meeting
from numerical_methods import forward_difference, central_difference, trapezoid, midpoint


class AnalysisTests(unittest.TestCase):
    def test_observed_orders_from_independent_polynomial_errors(self):
        hs = np.array([0.1, 0.05, 0.025])
        forward = [abs(forward_difference(lambda x: x*x, 1, h)-2) for h in hs]
        central = [abs(central_difference(lambda x: x**3, 1, h)-3) for h in hs]
        self.assertAlmostEqual(observed_order(hs, forward), 1, places=10)
        self.assertAlmostEqual(observed_order(hs, central), 2, places=10)
        counts = np.array([10, 20, 40])
        for method in (midpoint, trapezoid):
            errors = [abs(method(lambda x: x*x, 0, 1, int(count))-1/3) for count in counts]
            self.assertAlmostEqual(observed_order(1/counts, errors), 2, places=9)

    def test_zero_errors_are_not_silently_logged(self):
        for hs, errors in [([1, 0.5], [1, 0]), ([1, 1], [1, 2]), ([1], [1]),
                           ([1, 0.5], [1, np.nan]), ([1, 0.5], [1])]:
            with self.assertRaises(ValueError):
                observed_order(hs, errors)

    def test_budget_is_cheapest_tested_not_first_list_item(self):
        rows = [dict(sampled_values=100, absolute_error=1e-6),
                dict(sampled_values=10, absolute_error=1e-4)]
        self.assertEqual(first_budget_meeting(rows, 1e-3)["sampled_values"], 10)
        self.assertIsNone(first_budget_meeting(rows, 1e-8))
        for target in (0, -1, np.inf):
            with self.assertRaises(ValueError):
                first_budget_meeting(rows, target)
