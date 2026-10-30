"""Test suite derived from CLAUSE COVERAGE (CC) of shipping_fee.

Rules:
  * Hand-calculated expected values from specification rules.
  * Minimal suite for CC: 5 tests covering True and False for all 13 clauses in D1..D6.
"""
import unittest
from target import fee


class ClauseCoverageTests(unittest.TestCase):

    def test_cc_01_d1_both_clauses_true(self):
        # D1: c1 (weight <= 0)=True, c2 (distance <= 0)=True -> row TT -> fee = -1
        self.assertEqual(fee(0, 0, False, False), -1)

    def test_cc_02_d2_both_clauses_true(self):
        # D1: c1=False, c2=False (55 > 0, 2500 > 0) -> row FF
        # D2: c1 (weight > 50)=True, c2 (distance > 2000)=True -> row TT -> fee = -2
        self.assertEqual(fee(55, 2500, False, False), -2)

    def test_cc_03_all_clauses_true(self):
        # D1: FF, D2: FF
        # D3: c1 (weight > 10)=True, c2 (distance > 500)=True -> row TT -> fee = 300
        # D4: not reached
        # D5: c1 (express)=True, c2 (member)=True, c3 (weight > 5)=True -> row TTT -> fee = 450
        # D6: c1 (member)=True, c2 (fee >= 250)=True -> row TT -> fee = 405
        self.assertEqual(fee(20, 600, True, True), 405)

    def test_cc_04_d3_tf_d4_tf(self):
        # D1: FF, D2: FF
        # D3: c1 (weight > 10)=True, c2 (distance > 500)=False -> row TF
        # D4: c1 (weight > 10)=True, c2 (distance > 500)=False -> row TF -> fee = 180
        # D5: c1 (express)=False, c2 (member)=False, c3 (weight > 5)=True -> row FFT -> fee = 180
        # D6: c1 (member)=False, c2 (fee >= 250)=False -> row FF -> fee = 180
        self.assertEqual(fee(20, 300, False, False), 180)

    def test_cc_05_d3_ft_d4_ft_d5_fff_d6_ff(self):
        # D1: FF, D2: FF
        # D3: c1 (weight > 10)=False, c2 (distance > 500)=True -> row FT
        # D4: c1 (weight > 10)=False, c2 (distance > 500)=True -> row FT -> fee = 180
        # D5: c1 (express)=False, c2 (member)=False, c3 (weight > 5)=False (4 <= 5) -> row FFF -> fee = 180
        # D6: c1 (member)=False, c2 (fee >= 250)=False (180 < 250) -> row FF -> fee = 180
        self.assertEqual(fee(4, 600, False, False), 180)


if __name__ == "__main__":
    unittest.main()
