from items.BasicItem import BasicItem


class InventoryItem(BasicItem):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, asset_id, title, tradable, market_price,
                 item_type, exterior, unlock_date):
        self.tradable = tradable
        self.item_type = item_type
        self.unlock_date = unlock_date
        self.exterior = exterior
        super().__init__(asset_id, title, market_price)