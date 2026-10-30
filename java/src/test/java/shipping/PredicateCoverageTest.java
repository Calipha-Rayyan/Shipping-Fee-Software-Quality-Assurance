package shipping;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * Test suite derived from PREDICATE COVERAGE (PC) of ShippingRef.fee.
 *
 * Minimal suite: 5 tests covering True and False for each reachable decision D1..D6.
 */
public class PredicateCoverageTest {

    @Test
    public void test_pc_01_d1_true() {
        assertEquals(-1, Target.fee(0, 100, false, false));
    }

    @Test
    public void test_pc_02_d2_true() {
        assertEquals(-2, Target.fee(55, 100, false, false));
    }

    @Test
    public void test_pc_03_d3_true_d5_true_d6_true() {
        assertEquals(405, Target.fee(20, 600, true, true));
    }

    @Test
    public void test_pc_04_d3_false_d4_true_d5_false_d6_false() {
        assertEquals(180, Target.fee(20, 300, false, false));
    }

    @Test
    public void test_pc_05_d4_false() {
        assertEquals(100, Target.fee(5, 100, false, false));
    }
}
