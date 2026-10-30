"""Test suite derived from CORRELATED ACTIVE CLAUSE COVERAGE (CACC) of shipping_fee.

Rules:
  * Hand-calculated expected values from specification rules.
  * Minimal suite for CACC: 8 tests satisfying CACC requirements for all predicates D1..D6.
"""
import unittest
from target import fee


class CorrelatedActiveClauseCoverageTests(unittest.TestCase):

    def test_cacc_01_d1_tf(self):
        # D1 row TF: weight <= 0 is True, distance <= 0 is False -> INVALID (-1)
        self.assertEqual(fee(0, 100, False, False), -1)

    def test_cacc_02_d1_ft(self):
        # D1 row FT: weight <= 0 is False, distance <= 0 is True -> INVALID (-1)
        self.assertEqual(fee(10, 0, False, False), -1)

    def test_cacc_03_d2_tf(self):
        # D1 row FF. D2 row TF: weight > 50 is True, distance > 2000 is False -> REFUSED (-2)
        self.assertEqual(fee(55, 100, False, False), -2)

    def test_cacc_04_d2_ft(self):
        # D1 row FF. D2 row FT: weight > 50 is False, distance > 2000 is True -> REFUSED (-2)
        self.assertEqual(fee(10, 2500, False, False), -2)

    def test_cacc_05_d3_tt_d5_ttt_d6_tt(self):
        # D1 FF, D2 FF
        # D3 row TT: weight > 10, distance > 500 -> fee = 300
        # D5 row TTT: express=True, member=True, weight=20 > 5 -> fee = 450
        # D6 row TT: member=True, fee=450 >= 250 -> fee = 405
        self.assertEqual(fee(20, 600, True, True), 405)

    def test_cacc_06_d3_tf_d4_tf_d5_ftt_d6_tf(self):
        # D1 FF, D2 FF
        # D3 row TF: weight > 10, distance <= 500
        # D4 row TF: weight > 10, distance <= 500 -> fee = 180
        # D5 row FTT: express=False, member=True, weight=20 > 5 -> fee = 180
        # D6 row TF: member=True, fee=180 < 250 -> fee = 180
        self.assertEqual(fee(20, 300, False, True), 180)

    def test_cacc_07_d3_ft_d4_ft_d5_tff_d6_ft(self):
        # D1 FF, D2 FF
        # D3 row FT: weight <= 10, distance > 500
        # D4 row FT: weight <= 10, distance > 500 -> fee = 180
        # D5 row TFF: express=True, member=False, weight=4 <= 5 -> fee = 330
        # D6 row FT: member=False, fee=330 >= 250 -> fee = 330
        self.assertEqual(fee(4, 600, True, False), 330)

    def test_cacc_08_d3_ff_d4_ff_d5_ttf_d6_tf(self):
        # D1 FF, D2 FF
        # D3 row FF: weight <= 10, distance <= 500
        # D4 row FF: weight <= 10, distance <= 500 -> fee = 100
        # D5 row TTF: express=True, member=True, weight=4 <= 5 -> fee = 100
        # D6 row TF: member=True, fee=100 < 250 -> fee = 100
        self.assertEqual(fee(4, 100, True, True), 100)


if __name__ == "__main__":
    unittest.main()
