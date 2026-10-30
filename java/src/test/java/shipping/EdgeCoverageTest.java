package shipping;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * Test suite derived from EDGE COVERAGE (EC) of the CFG of ShippingRef.fee.
 *
 * Rules:
 *   - Hand-calculated expected values from specification rules.
 *   - Minimal suite: 5 tests covering all 17 edges.
 */
public class EdgeCoverageTest {

    @Test
    public void test_ec_01_invalid_input() {
        // Edge: (n1, n2)
        assertEquals(-1, Target.fee(0, 100, false, false));
    }

    @Test
    public void test_ec_02_refused_input() {
        // Edges: (n1, n3), (n3, n4)
        assertEquals(-2, Target.fee(55, 100, false, false));
    }

    @Test
    public void test_ec_03_heavy_long_express_member_discount() {
        // Edges: (n3, n5), (n5, n6), (n6, n7), (n7, n10), (n10, n11), (n11, n12), (n12, n13), (n13, n14)
        assertEquals(405, Target.fee(20, 600, true, true));
    }

    @Test
    public void test_ec_04_heavy_only_no_express_non_member() {
        // Edges: (n6, n8), (n8, n9), (n9, n10), (n10, n12), (n12, n14)
        assertEquals(180, Target.fee(20, 300, false, false));
    }

    @Test
    public void test_ec_05_standard_parcel_skips_surcharge() {
        // Edge: (n8, n10)
        assertEquals(100, Target.fee(5, 100, false, false));
    }
}
