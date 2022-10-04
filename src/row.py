'''This module contains the row class which represents a row in a CLI chart'''


LISTING_MASK = [0, 7, 3, 6, 2, 4]
INVENTORY_MASK = [0, 5, 3, 2, 4]
INVENTORY_MASK_TRADABLE = [0, 5, 6, 3, 2, 4]


class Row:
    '''This class represents a row in a CLI chart'''
    def __init__(self, title, asset_ids, total_items, market_price, total_price):
        self.title = title
        self.asset_ids = asset_ids
        self.total_items = total_items
        self.market_price = market_price
        self.total_price = total_price


class ListingRow(Row):
    '''ListingRow represents a certain amount of CS:GO item which is listed in DMarket'''
    def __init__(self, title, asset_ids, offer_ids, total_items, total_price,
                 listing_price, tradable, market_price=''):
        super().__init__(title, asset_ids, total_items, market_price, total_price)
        self.offer_ids = offer_ids
        self.listing_price = listing_price
        self.tradable = tradable

    def get_list(self):
        '''get list of all the items of the ListingRow'''
        listingrow_list = list(vars(self).values())
        return [listingrow_list[i] for i in LISTING_MASK]

    def get_keys(self):
        '''get list of the keys of the ListingRow'''
        listingrow_list = list(vars(self).keys())
        return [listingrow_list[i] for i in LISTING_MASK]


class InventoryItemRow(Row):
    '''InventoryItemRow represents a certain amount of CS:GO item which is in DMarket inventory'''
    def __init__(self, title, asset_ids, total_items,
                 total_price, exterior, tradable, market_price):

        super().__init__(title, asset_ids, total_items,
                         market_price, total_price)
        self.exterior = exterior
        self.tradable = tradable

    def get_list(self):
        '''get list of all of the InventoryItemRow'''
        inventoryrow_list = list(vars(self).values())
        return [inventoryrow_list[i] for i in INVENTORY_MASK]
    
    def get_list_tradable(self):
        '''get list of all of the InventoryItemRow'''
        inventoryrow_list = list(vars(self).values())
        return [inventoryrow_list[i] for i in INVENTORY_MASK_TRADABLE]

    def get_keys(self):
        '''get list of the keys of the InventoryItemRow'''
        keysrow_list = list(vars(self).keys())
        return [keysrow_list[i] for i in INVENTORY_MASK]
    
    def get_keys_tradable(self):
        '''get list of the keys of the InventoryItemRow'''
        keysrow_list = list(vars(self).keys())
        return [keysrow_list[i] for i in INVENTORY_MASK_TRADABLE]
