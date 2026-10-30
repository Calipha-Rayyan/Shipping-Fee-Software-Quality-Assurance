"""Test suite derived from EDGE COVERAGE (EC) of the CFG of shipping_fee.

Rules:
  * Hand-calculated expected values from specification rules.
  * Minimal suite for Edge Coverage: 5 test cases covering all 17 edges.
"""
import unittest
from target import fee


class EdgeCoverageTests(unittest.TestCase):

    def test_ec_01_invalid_input(self):
        # Covers: (n1, n2) [D1 True]
        # Rule 1: weight <= 0 -> -1
        # Input: weight=0, distance=100, express=False, member=False
        self.assertEqual(fee(0, 100, False, False), -1)

    def test_ec_02_refused_input(self):
        # Covers: (n1, n3) [D1 False], (n3, n4) [D2 True]
        # Rule 1: False (55 > 0, 100 > 0)
        # Rule 2: weight > 50 -> -2
        # Input: weight=55, distance=100, express=False, member=False
        self.assertEqual(fee(55, 100, False, False), -2)

    def test_ec_03_heavy_long_express_member_discount(self):
        # Covers: (n3, n5), (n5, n6), (n6, n7) [D3 True], (n7, n10),
        #         (n10, n11) [D5 True], (n11, n12), (n12, n13) [D6 True], (n13, n14)
        # Path: n1 -> n3 -> n5 -> n6 -> n7 -> n10 -> n11 -> n12 -> n13 -> n14
        # fee = 100 + 200 + 150 = 450 -> discount 45 -> 405
        # Input: weight=20, distance=600, express=True, member=True
        self.assertEqual(fee(20, 600, True, True), 405)

    def test_ec_04_heavy_only_no_express_non_member(self):
        # Covers: (n6, n8) [D3 False], (n8, n9) [D4 True], (n9, n10),
        #         (n10, n12) [D5 False], (n12, n14) [D6 False]
        # Path: n1 -> n3 -> n5 -> n6 -> n8 -> n9 -> n10 -> n12 -> n14
        # fee = 100 + 80 = 180
        # Input: weight=20, distance=300, express=False, member=False
        self.assertEqual(fee(20, 300, False, False), 180)

    def test_ec_05_standard_parcel_skips_surcharge(self):
        # Covers: (n8, n10) [D4 False]
        # Path: n1 -> n3 -> n5 -> n6 -> n8 -> n10 -> n12 -> n14
        # D3 False and D4 False (weight <= 10 and distance <= 500)
        # fee = 100
        # Input: weight=5, distance=100, express=False, member=False
        self.assertEqual(fee(5, 100, False, False), 100)


if __name__ == "__main__":
    unittest.main()
