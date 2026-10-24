"""Independent exact values, input contracts, and representability checks."""
import unittest
import numpy as np
from numerical_methods import forward_difference, central_difference, left_rectangle, trapezoid


class DerivativeTests(unittest.TestCase):
    def test_affine_and_constant(self):
        for method in (forward_difference, central_difference):
            self.assertAlmostEqual(method(lambda x: 3*x+2, 1, 0.01), 3)
            self.assertEqual(method(lambda x: 7, 2, 0.01), 0)

    def test_quadratic_central_exactness(self):
        self.assertAlmostEqual(central_difference(lambda x: x*x, 2, 0.01), 4)

    def test_invalid_parameters(self):
        for method in (forward_difference, central_difference):
            for step in (0, -1, np.nan, np.inf, 1e-30, 1j, [0.1]):
                with self.subTest(method=method.__name__, step=step), self.assertRaises(ValueError):
                    method(np.sin, 1, step)
            with self.assertRaises(ValueError):
                method(np.sin, np.inf, 0.1)

    def test_invalid_function_values(self):
        for method in (forward_difference, central_difference):
            for value in (np.nan, np.inf, 1j, [1, 2]):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    method(lambda x: value, 1, 0.01)

    def test_overflowing_sample_position(self):
        with self.assertRaises(ValueError):
            central_difference(np.sin, 1e308, 1e308)


class IntegralTests(unittest.TestCase):
    def test_constant_and_equal_bounds(self):
        for method in (left_rectangle, trapezoid):
            self.assertAlmostEqual(method(lambda x: 3, -1, 2, 10), 9)
            self.assertEqual(method(lambda x: np.nan, 2, 2, 10), 0)

    def test_affine_trapezoid_exactness(self):
        self.assertAlmostEqual(trapezoid(lambda x: 2*x+1, 0, 1, 5), 2)

    def test_known_quadratic_integral(self):
        self.assertLess(abs(trapezoid(lambda x: x*x, 0, 1, 1000)-1/3), 2e-7)

    def test_reversed_bounds(self):
        self.assertAlmostEqual(trapezoid(np.exp, 1, 0, 100), -trapezoid(np.exp, 0, 1, 100))
        # Left along reversed traversal is not simply negative left on ascending nodes.
        self.assertAlmostEqual(left_rectangle(lambda x: x, 1, 0, 100), -0.505)

    def test_invalid_grids(self):
        for method in (left_rectangle, trapezoid):
            for intervals in (0, -1, 1.5, True):
                with self.subTest(intervals=intervals), self.assertRaises(ValueError):
                    method(np.exp, 0, 1, intervals)
            with self.assertRaises(ValueError):
                method(np.exp, 0, np.inf, 10)
            with self.assertRaises(ValueError):
                method(np.exp, 1.0, np.nextafter(1.0, 2.0), 100)

    def test_bad_samples(self):
        for method in (left_rectangle, trapezoid):
            for function in (lambda x: np.nan, lambda x: 1j, lambda x: [1, 2, 3]):
                with self.subTest(function=function), self.assertRaises(ValueError):
                    method(function, 0, 1, 10)


if __name__ == "__main__":
    unittest.main()
