'''This module contains the Item class which represends a DMarket item'''


class Item:
    '''This class represends a DMarket item'''
    def __init__(self, asset_id, title, market_price):
        self.asset_id = asset_id
        self.title = title
        self.market_price = market_price


class Listing(Item):
    '''Listing represents a CS:GO item which is listed in DMarket'''
    def __init__(self, asset_id, title, tradable, listing_price,
                 offer_id, market_price=''):
        self.tradable = tradable
        self.offer_id = offer_id
        self.listing_price = listing_price
        super().__init__(asset_id, title, market_price)


class InventoryItem(Item):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, asset_id, title, tradable, market_price,
                 item_type, exterior, unlock_date):
        self.tradable = tradable
        self.item_type = item_type
        self.unlock_date = unlock_date
        self.exterior = exterior
        super().__init__(asset_id, title, market_price)


class Purchase(Item):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, asset_id, title, offer_closed_at,
                 offer_created_at,
                 sold_price, offer_id, market_price=''):
        self.offer_id = offer_id
        self.offer_closed_at = offer_closed_at
        self.offer_created_at = offer_created_at
        self.sold_price = sold_price
        super().__init__(asset_id, title, market_price)

