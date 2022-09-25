'''This module contains the row class which represents a row in a CLI chart'''


class Row:
    '''This class represents a row in a CLI chart'''
    def __init__(self, title, asset_ids, exterior, count, market_price, total_price,offer_ids):
        self.title = title
        self.asset_ids = asset_ids
        self.offer_ids = offer_ids
        self.exterior = exterior
        self.market_price = market_price
        self.count = count
        self.total_price = total_price
