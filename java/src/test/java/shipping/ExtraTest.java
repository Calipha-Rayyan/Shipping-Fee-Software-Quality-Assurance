package shipping;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * Extra tests (Part C4) to kill all killable surviving faults.
 *
 * Motivated by:
 *   - Boundary Value Analysis (BVA) for relational operator boundaries.
 *   - Internal state boundary analysis for derived variable thresholds.
 */
public class ExtraTest {

    @Test
    public void test_extra_01_kills_f03_distance_boundary_500() {
        // Kills f03: distance = 500 on boundary of distance > 500
        // Reference: fee = 180; f03: fee = 300
        assertEquals(180, Target.fee(20, 500, false, false));
    }

    @Test
    public void test_extra_02_kills_f08_fee_boundary_250() {
        // Kills f08: fee = 250 exactly on boundary of fee >= 250
        // Reference: discount applied -> 225; f08: no discount -> 250
        assertEquals(225, Target.fee(8, 200, true, true));
    }
}
