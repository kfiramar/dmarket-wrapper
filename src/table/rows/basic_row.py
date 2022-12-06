'''This module contains the row class which represents a row in a CLI chart'''

from common.config import ROW_PRINT_MASKS, ROW_PRINT_MASKS_WORDS
from common.formatting import format_floats_to_usd

class BasicRow:
    '''This class represents a row in a CLI chart'''
    def __init__(self, title: str, amount: int, market_price):
        self.title = title
        self.amount = amount
        self.market_price = market_price

    def get_rows_values(self) -> list:
        '''get list of all the items of the ListingRow'''
        values_dict = vars(self)
        relevent_keys = ROW_PRINT_MASKS_WORDS[self.__class__.__name__]
        relevent_values = []
        for key, val in values_dict.items():
            if key in relevent_keys:
                relevent_values.insert(relevent_keys.index(key), val)
        # return relevent_values
        # relevent_values = [val for key, val in values_dict.items() if key in relevent_keys]
        
        return format_floats_to_usd(relevent_values)

    def get_rows_headers(self) -> list:
        '''get list of the keys of the ListingRow'''
        return ROW_PRINT_MASKS_WORDS[self.__class__.__name__]

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
