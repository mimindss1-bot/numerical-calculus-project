import unittest
import numpy as np
from numerical_methods import midpoint


class MidpointTests(unittest.TestCase):
    def test_affine_exactness(self):
        for count in (1, 3, 100):
            self.assertAlmostEqual(midpoint(lambda x: 2*x+1, 0, 1, count), 2)
            self.assertAlmostEqual(midpoint(lambda x: 3, -1, 2, count), 9)

    def test_quadratic_error_constant(self):
        for count in (2, 10, 100):
            error = 1/3 - midpoint(lambda x: x*x, 0, 1, count)
            self.assertAlmostEqual(error, 1/(12*count*count), places=14)

    def test_sample_count_and_locations(self):
        observed = []
        def function(x):
            observed.extend(x)
            return x
        midpoint(function, 0, 1, 4)
        np.testing.assert_allclose(observed, [0.125, 0.375, 0.625, 0.875])

    def test_orientation(self):
        self.assertAlmostEqual(midpoint(np.exp, 1, 0, 20), -midpoint(np.exp, 0, 1, 20))
        self.assertEqual(midpoint(lambda x: np.nan, 2, 2, 1), 0)

    def test_invalid_input_and_unrepresentable_midpoint(self):
        for intervals in (0, -1, True, 2.5):
            with self.assertRaises(ValueError):
                midpoint(np.exp, 0, 1, intervals)
        with self.assertRaises(ValueError):
            midpoint(np.exp, 1, np.nextafter(1.0, 2.0), 1)
        with self.assertRaises(ValueError):
            midpoint(lambda x: np.nan, 0, 1, 10)
