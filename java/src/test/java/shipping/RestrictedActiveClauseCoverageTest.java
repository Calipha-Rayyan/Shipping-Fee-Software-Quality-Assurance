package shipping;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * Test suite derived from RESTRICTED ACTIVE CLAUSE COVERAGE (RACC) of ShippingRef.fee.
 *
 * Minimal suite: 8 tests satisfying RACC requirements for all predicates D1..D6.
 */
public class RestrictedActiveClauseCoverageTest {

    @Test
    public void test_racc_01_d1_tf() {
        assertEquals(-1, Target.fee(0, 100, false, false));
    }

    @Test
    public void test_racc_02_d1_ft() {
        assertEquals(-1, Target.fee(10, 0, false, false));
    }

    @Test
    public void test_racc_03_d2_tf() {
        assertEquals(-2, Target.fee(55, 100, false, false));
    }

    @Test
    public void test_racc_04_d2_ft() {
        assertEquals(-2, Target.fee(10, 2500, false, false));
    }

    @Test
    public void test_racc_05_d3_tt_d5_ttt_d6_tt() {
        assertEquals(405, Target.fee(20, 600, true, true));
    }

    @Test
    public void test_racc_06_d3_tf_d4_tf_d5_ftt_d6_tf() {
        assertEquals(180, Target.fee(20, 300, false, true));
    }

    @Test
    public void test_racc_07_d3_ft_d4_ft_d5_tff_d6_ft() {
        assertEquals(330, Target.fee(4, 600, true, false));
    }

    @Test
    public void test_racc_08_d3_ff_d4_ff_d5_ttf_d6_tf() {
        assertEquals(100, Target.fee(4, 100, true, true));
    }
}
