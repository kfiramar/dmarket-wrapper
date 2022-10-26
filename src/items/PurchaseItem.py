from items.BasicItem import BasicItem


class PurchaseItem(BasicItem):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, asset_id, title, offer_closed_at,
                 offer_created_at,
                 sold_price, offer_id, market_price=''):
        self.offer_id = offer_id
        self.offer_closed_at = offer_closed_at
        self.offer_created_at = offer_created_at
        self.sold_price = sold_price
        super().__init__(asset_id, title, market_price)