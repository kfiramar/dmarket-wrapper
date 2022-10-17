'''This module contains the row class which represents a row in a CLI chart'''

from config import ROW_PRINT_MASKS


class Row:
    '''This class represents a row in a CLI chart'''
    def __init__(self, title: str, asset_ids: list, total_items: int, market_price: float, total_price: float):
        self.title = title
        self.asset_ids = asset_ids
        self.total_items = total_items
        self.market_price = market_price
        self.total_price = total_price

    def get_values_list(self) -> list:
        '''get list of all the items of the ListingRow'''
        listingrow_list = list(vars(self).values())
        for i, value in enumerate(listingrow_list):
            if isinstance(value, float):
                listingrow_list[i] = f"{value:0.2f}$"
        return [listingrow_list[i] for i in ROW_PRINT_MASKS[self.__class__.__name__]]

    def get_keys_list(self) -> list:
        '''get list of the keys of the ListingRow'''
        listingrow_list = list(vars(self).keys())
        return [listingrow_list[i] for i in ROW_PRINT_MASKS[self.__class__.__name__]]


class ListingRow(Row):
    '''ListingRow represents a certain amount of CS:GO item which is listed in DMarket'''
    def __init__(self, title, asset_ids, offer_ids, total_items, total_price,
                 listing_price, tradable, market_price=''):
        super().__init__(title, asset_ids, total_items, market_price, total_price)
        self.offer_ids = offer_ids
        self.listing_price = listing_price
        self.tradable = tradable


class InventoryItemRow(Row):
    '''InventoryItemRow represents a certain amount of CS:GO item which is in DMarket inventory'''
    def __init__(self, title, asset_ids, total_items,
                 total_price, exterior, tradable, market_price):

        super().__init__(title, asset_ids, total_items,
                         market_price, total_price)
        self.exterior = exterior
        self.tradable = tradable


class PurcheseRow(Row):
    '''ListingRow represents a certain amount of CS:GO item which is listed in DMarket'''
    def __init__(self, title, asset_ids, offer_ids, total_items, total_price,
                 sold_price, offer_closed_at, offer_created_at, market_price=''):
        super().__init__(title, asset_ids, total_items, market_price, total_price)
        self.offer_ids = offer_ids
        self.sold_price = sold_price
        self.offer_closed_at = offer_closed_at
        self.offer_created_at = offer_created_at
