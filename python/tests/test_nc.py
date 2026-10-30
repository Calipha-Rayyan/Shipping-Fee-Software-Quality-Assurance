"""Test suite derived from NODE COVERAGE (NC) of the CFG of shipping_fee.

Rules:
  * Hand-calculated expected values from specification rules.
  * Minimal suite for Node Coverage: 4 test cases covering all 14 nodes.
"""
import unittest
from target import fee


class NodeCoverageTests(unittest.TestCase):

    def test_nc_01_invalid_input(self):
        # Covers: n1 -> n2 (return INVALID)
        # Nodes: {n1, n2}
        # Rule 1: weight <= 0 or distance <= 0 -> -1
        # Input: weight=0, distance=100, express=False, member=False
        self.assertEqual(fee(0, 100, False, False), -1)

    def test_nc_02_refused_input(self):
        # Covers: n1 -> n3 -> n4 (return REFUSED)
        # Nodes: {n1, n3, n4}
        # Rule 1: False (55 > 0, 100 > 0)
        # Rule 2: weight > 50 (55 > 50) -> -2
        # Input: weight=55, distance=100, express=False, member=False
        self.assertEqual(fee(55, 100, False, False), -2)

    def test_nc_03_heavy_long_express_member_discount(self):
        # Covers: n1 -> n3 -> n5 -> n6 -> n7 -> n10 -> n11 -> n12 -> n13 -> n14
        # Nodes: {n1, n3, n5, n6, n7, n10, n11, n12, n13, n14}
        # Rule 1: False (20 > 0, 600 > 0)
        # Rule 2: False (20 <= 50, 600 <= 2000)
        # Rule 3: base fee = 100
        # Rule 4: weight > 10 and distance > 500 -> fee = 100 + 200 = 300
        # Rule 5: express and (not member or weight > 5) -> 20 > 5 is True -> fee = 300 + 150 = 450
        # Rule 6: member and fee >= 250 -> 450 >= 250 -> fee = 450 - (450 // 10) = 405
        # Input: weight=20, distance=600, express=True, member=True
        self.assertEqual(fee(20, 600, True, True), 405)

    def test_nc_04_heavy_only_no_express_non_member(self):
        # Covers: n1 -> n3 -> n5 -> n6 -> n8 -> n9 -> n10 -> n12 -> n14
        # Nodes: {n8, n9} (completing all 14 nodes)
        # Rule 1: False (20 > 0, 300 > 0)
        # Rule 2: False (20 <= 50, 300 <= 2000)
        # Rule 3: base fee = 100
        # Rule 4: D3 False, D4 True (weight > 10 is True) -> fee = 100 + 80 = 180
        # Rule 5: express=False -> D5 False -> fee = 180
        # Rule 6: member=False -> D6 False -> fee = 180
        # Input: weight=20, distance=300, express=False, member=False
        self.assertEqual(fee(20, 300, False, False), 180)


if __name__ == "__main__":
    unittest.main()
