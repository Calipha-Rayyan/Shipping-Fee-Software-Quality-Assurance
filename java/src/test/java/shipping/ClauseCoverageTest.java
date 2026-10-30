package shipping;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * Test suite derived from CLAUSE COVERAGE (CC) of ShippingRef.fee.
 *
 * Minimal suite: 5 tests covering True and False for all 13 clauses in D1..D6.
 */
public class ClauseCoverageTest {

    @Test
    public void test_cc_01_d1_both_clauses_true() {
        assertEquals(-1, Target.fee(0, 0, false, false));
    }

    @Test
    public void test_cc_02_d2_both_clauses_true() {
        assertEquals(-2, Target.fee(55, 2500, false, false));
    }

    @Test
    public void test_cc_03_all_clauses_true() {
        assertEquals(405, Target.fee(20, 600, true, true));
    }

    @Test
    public void test_cc_04_d3_tf_d4_tf() {
        assertEquals(180, Target.fee(20, 300, false, false));
    }

    @Test
    public void test_cc_05_d3_ft_d4_ft_d5_fff_d6_ff() {
        assertEquals(180, Target.fee(4, 600, false, false));
    }
}
