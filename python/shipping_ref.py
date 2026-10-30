"""Program under test: ShippingFee (reference implementation).

Specification (see the assignment handout, Algorithm 1):

  Inputs : weight (kg), distance (km), express (bool), member (bool)
  Output : the shipping fee, or one of two error codes
           INVALID (-1)  - weight or distance is not a positive number
           REFUSED (-2)  - parcel is too heavy (> 50 kg) or too far (> 2000 km)

  Fee rules (integers only):
    * every parcel starts with a base fee of 100
    * heavy AND long parcels (> 10 kg and > 500 km) pay +200
    * otherwise parcels that are heavy OR long pay +80
    * express delivery costs +150, except that members get free express
      delivery on light parcels (weight <= 5)
    * members get 10% off (integer division) when the fee so far is 250 or more

The line comments D1..D6 label the six decisions of the program. They are the
same labels used in the handout.
"""

INVALID = -1
REFUSED = -2


def shipping_fee(weight, distance, express, member):
    if weight <= 0 or distance <= 0:                      # D1
        return INVALID
    if weight > 50 or distance > 2000:                    # D2
        return REFUSED
    fee = 100
    if weight > 10 and distance > 500:                    # D3
        fee = fee + 200
    elif weight > 10 or distance > 500:                   # D4
        fee = fee + 80
    if express and (not member or weight > 5):            # D5
        fee = fee + 150
    if member and fee >= 250:                             # D6
        fee = fee - fee // 10
    return fee
