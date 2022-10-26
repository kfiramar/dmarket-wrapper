from items.BasicItem import BasicItem


class ListingItem(BasicItem):
    '''ListingItem represents a CS:GO item which is listed in DMarket'''
    def __init__(self, asset_id, title, tradable, listing_price,
                 offer_id, market_price=''):
        self.tradable = tradable
        self.offer_id = offer_id
        self.listing_price = listing_price
        super().__init__(asset_id, title, market_price)