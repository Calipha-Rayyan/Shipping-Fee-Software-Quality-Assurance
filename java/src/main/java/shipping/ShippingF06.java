package shipping;

/** Version f06 of ShippingFee. */
public final class ShippingF06 {

    private ShippingF06() {
    }

    public static int fee(int weight, int distance, boolean express, boolean member) {
        if (weight <= 0 || distance <= 0) {                      // D1
            return -1;
        }
        if (weight > 50 || distance > 2000) {                    // D2
            return -2;
        }
        int fee = 100;
        if (weight > 10 && distance > 500) {                     // D3
            fee = fee + 200;
        } else if (weight > 10 || distance > 500) {              // D4
            fee = fee + 80;
        }
        if (express && !member) {                                // D5
            fee = fee + 150;
        }
        if (member && fee >= 250) {                              // D6
            fee = fee - fee / 10;
        }
        return fee;
    }
}
