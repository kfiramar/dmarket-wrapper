'''This module contains the Item class which represends a DMarket item'''


class Item:
    '''This class represends a DMarket item'''
    def __init__(self, asset_id, title, tradable, market_price):
        self.asset_id = asset_id
        self.title = title
        self.tradable = tradable
        self.market_price = market_price


class Listing(Item):
    '''Listing represents a CS:GO item which is listed in DMarket'''
    def __init__(self, asset_id, title, tradable, listing_price,
                 offer_id, market_price=''):

        self.offer_id = offer_id
        self.listing_price = listing_price
        super().__init__(asset_id, title, tradable, market_price)


class InventoryItem(Item):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, asset_id, title, tradable, market_price,
                 item_type, exterior, unlock_date):
        self.item_type = item_type
        self.unlock_date = unlock_date
        self.exterior = exterior
        super().__init__(asset_id, title, tradable, market_price)
