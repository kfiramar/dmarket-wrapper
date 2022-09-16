'''This module contains the Item class which represends a DMarket item'''


class Item:
    '''This class represends a DMarket item'''
    def __init__(self, asset_id = '', title = '',tradable = '',exterior = '',trade_lock = '',item_type = '',market_price = '',unlock_date = ''):
        self.asset_id = asset_id
        self.title = title
        self.tradable = tradable
        self.exterior = exterior
        self.trade_lock = trade_lock
        self.item_type = item_type
        self.market_price = market_price
        self.unlock_date = unlock_date
