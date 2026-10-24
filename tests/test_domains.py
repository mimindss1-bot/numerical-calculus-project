import unittest
import numpy as np
from numerical_methods import forward_difference, central_difference, richardson_difference, midpoint, trapezoid
from analysis_tools import observed_order


class DomainTests(unittest.TestCase):
    def test_one_sided_method_can_stay_inside_domain(self):
        self.assertTrue(np.isfinite(forward_difference(np.log, 0.01, 0.02)))
        for method in (central_difference, richardson_difference):
            with self.assertRaises(ValueError):
                method(np.log, 0.01, 0.02)
        self.assertLess(abs(central_difference(np.log, 0.01, 1e-5)-100), 1e-3)

    def test_a_numerical_value_does_not_establish_differentiability(self):
        self.assertEqual(central_difference(np.abs, 0, 0.1), 0)
        self.assertEqual(forward_difference(np.abs, 0, 0.1), 1)
        self.assertEqual((abs(-0.1)-abs(0))/(-0.1), -1)

    def test_endpoint_singularity_changes_convergence(self):
        counts = np.array([128, 256, 512, 1024])
        for method in (trapezoid, midpoint):
            errors = [abs(method(np.sqrt, 0, 1, int(n))-2/3) for n in counts]
            order = observed_order(1/counts, errors)
            self.assertGreater(order, 1.4)
            self.assertLess(order, 1.6)

    def test_midpoints_can_avoid_undefined_endpoint_values(self):
        def interior_only(x):
            if np.any(x == 0):
                raise ValueError("function is unavailable at the endpoint")
            return x*x
        self.assertTrue(np.isfinite(midpoint(interior_only, 0, 1, 10)))
        with self.assertRaises(ValueError):
            trapezoid(interior_only, 0, 1, 10)
