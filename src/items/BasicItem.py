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

    @classmethod
    def parse_jsons_to_items(cls, json_items):
        '''parses json items to items'''
        raise NotImplementedError