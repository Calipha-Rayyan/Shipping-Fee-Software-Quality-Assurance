package shipping;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * Test suite derived from NODE COVERAGE (NC) of the CFG of ShippingRef.fee.
 *
 * Rules:
 *   - Hand-calculated expected values from specification rules.
 *   - Minimal suite: 4 tests covering all 14 nodes.
 */
public class NodeCoverageTest {

    @Test
    public void test_nc_01_invalid_input() {
        // Path: n1 -> n2
        // Nodes: {n1, n2}
        assertEquals(-1, Target.fee(0, 100, false, false));
    }

    @Test
    public void test_nc_02_refused_input() {
        // Path: n1 -> n3 -> n4
        // Nodes: {n1, n3, n4}
        assertEquals(-2, Target.fee(55, 100, false, false));
    }

    @Test
    public void test_nc_03_heavy_long_express_member_discount() {
        // Path: n1 -> n3 -> n5 -> n6 -> n7 -> n10 -> n11 -> n12 -> n13 -> n14
        // Nodes: {n1, n3, n5, n6, n7, n10, n11, n12, n13, n14}
        // fee = 100 + 200 + 150 = 450 -> discount 45 -> 405
        assertEquals(405, Target.fee(20, 600, true, true));
    }

    @Test
    public void test_nc_04_heavy_only_no_express_non_member() {
        // Path: n1 -> n3 -> n5 -> n6 -> n8 -> n9 -> n10 -> n12 -> n14
        // Nodes: {n8, n9}
        // fee = 100 + 80 = 180
        assertEquals(180, Target.fee(20, 300, false, false));
    }
}
