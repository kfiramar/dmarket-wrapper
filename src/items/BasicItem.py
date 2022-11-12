'''This module contains the BasicItem class which represends a DMarket item'''

class BasicItem:
    '''This class represends a DMarket item'''
    def __init__(self, asset_id, title, market_price):
        self.asset_id = asset_id
        self.title = title
        self.market_price = market_price

    @classmethod
    def from_json_to_item(cls):
        '''parse json to item'''
        raise NotImplementedError

def parse_jsons_to_items_list(json_items):
    '''parses json items to items'''
    raise NotImplementedError

def parse_name_dict_to_dict(json_dict):
    raise NotImplementedError

def listing_error_parsing(responses: list) -> list:
    raise NotImplementedError
