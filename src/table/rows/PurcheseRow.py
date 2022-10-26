from table.rows.BasicRow import BasicRow


class PurcheseRow(BasicRow):
    '''ListingRow represents a certain amount of CS:GO item which is listed in DMarket'''
    def __init__(self, title, asset_ids, offer_ids, total_items, total_price,
                 sold_price, offer_closed_at, offer_created_at, market_price=''):
        super().__init__(title, asset_ids, total_items, market_price, total_price)
        self.offer_ids = offer_ids
        self.sold_price = sold_price
        self.offer_closed_at = offer_closed_at
        self.offer_created_at = offer_created_at
