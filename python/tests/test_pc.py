"""Test suite derived from PREDICATE COVERAGE (PC) of shipping_fee.

Rules:
  * Hand-calculated expected values from specification rules.
  * Minimal suite for PC: 5 tests covering True and False for each reachable decision D1..D6.
"""
import unittest
from target import fee


class PredicateCoverageTests(unittest.TestCase):

    def test_pc_01_d1_true(self):
        # D1 True (weight <= 0) -> return INVALID (-1)
        self.assertEqual(fee(0, 100, False, False), -1)

    def test_pc_02_d2_true(self):
        # D1 False, D2 True (weight > 50) -> return REFUSED (-2)
        self.assertEqual(fee(55, 100, False, False), -2)

    def test_pc_03_d3_true_d5_true_d6_true(self):
        # D1 False, D2 False
        # D3 True (weight > 10 and distance > 500) -> fee = 100 + 200 = 300
        # D4 not reached
        # D5 True (express and weight > 5) -> fee = 300 + 150 = 450
        # D6 True (member and fee >= 250) -> fee = 450 - 45 = 405
        self.assertEqual(fee(20, 600, True, True), 405)

    def test_pc_04_d3_false_d4_true_d5_false_d6_false(self):
        # D1 False, D2 False
        # D3 False, D4 True (weight > 10) -> fee = 100 + 80 = 180
        # D5 False (express is False) -> fee = 180
        # D6 False (member is False) -> fee = 180
        self.assertEqual(fee(20, 300, False, False), 180)

    def test_pc_05_d4_false(self):
        # D1 False, D2 False
        # D3 False, D4 False (weight <= 10 and distance <= 500) -> fee = 100
        # D5 False -> fee = 100
        # D6 False -> fee = 100
        self.assertEqual(fee(5, 100, False, False), 100)


if __name__ == "__main__":
    unittest.main()
