package shipping;

/**
 * Program under test: ShippingFee (reference implementation).
 *
 * <p>Specification (see the assignment handout, Algorithm 1):
 * <ul>
 *   <li>Inputs: weight (kg), distance (km), express, member.</li>
 *   <li>Output: the shipping fee, or an error code: INVALID (-1) if weight or distance is
 *       not positive; REFUSED (-2) if weight &gt; 50 or distance &gt; 2000.</li>
 *   <li>Every parcel starts at 100. Heavy AND long parcels (&gt; 10 kg and &gt; 500 km) pay +200;
 *       otherwise heavy OR long parcels pay +80.</li>
 *   <li>Express costs +150, except members get free express on light parcels (weight &lt;= 5).</li>
 *   <li>Members get 10% off (integer division) when the fee so far is 250 or more.</li>
 * </ul>
 * The comments D1..D6 label the six decisions, as in the handout.
 */
public final class ShippingRef {

    public static final int INVALID = -1;
    public static final int REFUSED = -2;

    private ShippingRef() {
    }

    public static int fee(int weight, int distance, boolean express, boolean member) {
        if (weight <= 0 || distance <= 0) {                      // D1
            return INVALID;
        }
        if (weight > 50 || distance > 2000) {                    // D2
            return REFUSED;
        }
        int fee = 100;
        if (weight > 10 && distance > 500) {                     // D3
            fee = fee + 200;
        } else if (weight > 10 || distance > 500) {              // D4
            fee = fee + 80;
        }
        if (express && (!member || weight > 5)) {                // D5
            fee = fee + 150;
        }
        if (member && fee >= 250) {                              // D6
            fee = fee - fee / 10;
        }
        return fee;
    }
}
