'''Creates json body for API request'''


def buy_order_body(amount: int, price: float, asset_ids: list):
    '''generate body for buy order'''
    item_order = {"Offers": []}
    for _ in range(amount):
        buy_order = {
                    "AssetID": asset_ids.pop(0),
                    "Price": {
                            "Currency": "USD",
                            "Amount": price
                            }
                }
        item_order['Offers'].append(buy_order)
    return item_order


def listings_body(amount: int, price: float, asset_ids: list, offer_ids: list):
    '''generate body for buy order'''
    item_order = {
         "force": True,
         "objects": []}
    for _ in range(amount):
        listing = {
                    "itemId": asset_ids.pop(0),
                    "offerId": offer_ids.pop(0),
                    "Price": {
                            "Currency": "USD",
                            "Amount": price
                            }
                }
        item_order['objects'].append(listing)
    return item_order
