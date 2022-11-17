'''Creates json body for API request'''


def create_listing_body(amount: int, price: float, asset_ids: list) -> str:
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


def delete_listing_body(amount: int, price: float, asset_ids: list, offer_ids: list) -> str:
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
