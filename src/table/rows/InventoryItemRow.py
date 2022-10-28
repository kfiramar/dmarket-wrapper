from table.rows.BasicRow import BasicRow


class InventoryItemRow(BasicRow):
    '''InventoryItemRow represents a certain amount of CS:GO item which is in DMarket inventory'''
    def __init__(self, title, asset_ids, total_items,
                 total_price, exterior, tradable, market_price):

        super().__init__(title, asset_ids, total_items,
                         market_price, total_price)
        self.exterior = exterior
        self.tradable = tradable