import unittest
import numpy as np
from numerical_methods import central_difference, richardson_difference


class RichardsonTests(unittest.TestCase):
    def test_cubic_and_quartic_exactness(self):
        for power in (3, 4):
            self.assertAlmostEqual(richardson_difference(lambda x: x**power, 1, 0.125), power, places=12)

    def test_fourth_order_convergence(self):
        errors = [abs(richardson_difference(np.exp, 1, h)-np.e) for h in (0.2, 0.1)]
        self.assertGreater(errors[0]/errors[1], 15.5)
        self.assertLess(errors[0]/errors[1], 16.5)
        self.assertLess(errors[1], abs(central_difference(np.exp, 1, 0.1)-np.e))

    def test_four_sample_evaluations(self):
        calls = []
        def counted(x):
            calls.append(x)
            return x*x
        richardson_difference(counted, 1, 0.2)
        self.assertEqual(len(calls), 4)
        np.testing.assert_allclose(sorted(calls), [0.8, 0.9, 1.1, 1.2])

    def test_unresolvable_half_step(self):
        with self.assertRaises(ValueError):
            richardson_difference(np.sin, 1, np.spacing(1))
