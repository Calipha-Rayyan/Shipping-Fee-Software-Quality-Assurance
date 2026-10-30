"""Extra tests (Part C4) to kill all killable surviving faults.

Motivated by:
  - Boundary Value Analysis (BVA) for relational operator boundaries.
  - Internal state boundary analysis for derived variable thresholds.
"""
import unittest
from target import fee


class ExtraTests(unittest.TestCase):

    def test_extra_01_kills_f03_distance_boundary_500(self):
        # Kills f03: distance = 500 on boundary of distance > 500
        # Reference: 500 > 500 is False -> takes D4 -> fee = 100 + 80 = 180
        # f03: 500 >= 500 is True -> takes D3 -> fee = 100 + 200 = 300
        self.assertEqual(fee(20, 500, False, False), 180)

    def test_extra_02_kills_f08_fee_boundary_250(self):
        # Kills f08: fee = 250 exactly on boundary of fee >= 250
        # weight = 8, distance = 200, express = True, member = True
        # Base = 100; D3/D4 False; D5 True (+150) -> fee = 250
        # Reference: fee >= 250 is True -> discount 25 -> fee = 225
        # f08: fee > 250 is False -> no discount -> fee = 250
        self.assertEqual(fee(8, 200, True, True), 225)


if __name__ == "__main__":
    unittest.main()
