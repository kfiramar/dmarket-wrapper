from table.rows.BasicRow import BasicRow

class ListingRow(BasicRow):
    '''ListingRow represents a certain amount of CS:GO item which is listed in DMarket'''
    def __init__(self, title, asset_ids, offer_ids, total_items, total_price,
                 listing_price, tradable, market_price=''):
        super().__init__(title, asset_ids, total_items, market_price, total_price)
        self.offer_ids = offer_ids
        self.listing_price = listing_price
        self.tradable = tradable
