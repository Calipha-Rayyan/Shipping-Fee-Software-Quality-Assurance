"""Version f03 of ShippingFee."""
INVALID = -1
REFUSED = -2


def shipping_fee(weight, distance, express, member):
    if weight <= 0 or distance <= 0:                      # D1
        return INVALID
    if weight > 50 or distance > 2000:                    # D2
        return REFUSED
    fee = 100
    if weight > 10 and distance >= 500:                   # D3
        fee = fee + 200
    elif weight > 10 or distance > 500:                   # D4
        fee = fee + 80
    if express and (not member or weight > 5):            # D5
        fee = fee + 150
    if member and fee >= 250:                             # D6
        fee = fee - fee // 10
    return fee
