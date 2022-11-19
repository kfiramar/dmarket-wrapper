'''This module contains the row class which represents a row in a CLI chart'''

from common.config import ROW_PRINT_MASKS

class BasicRow:
    '''This class represents a row in a CLI chart'''
    def __init__(self, title: str, asset_ids: list, amount: int, market_price: float, total_price: float):
        self.title = title
        self.asset_ids = asset_ids
        self.amount = amount
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

    @classmethod
    def item_to_row(cls, item):
        '''creates a new row from an item'''
        raise NotImplementedError

    def add_to_row(self, item):
        '''adds an item to an existing Row'''
        raise NotImplementedError

    def similar_to_item(self, item):
        '''returns wether an Item has the same relevent attributes as the Row'''
        raise NotImplementedError

def parse_items_list_to_rows(all_items: list, merge_by: str):
    '''parses items from list(Items) to list(Rows)'''
    raise NotImplementedError
