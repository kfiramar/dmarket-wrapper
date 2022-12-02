'''
This module contains the InventoryItemRow class (which is a subclass of BasicItem).
InventoryItemRow is based on InventoryItem,
Each row groups all the identical items into the same row.
'''

from items.inventory_item import InventoryItem
from items.dmrket_item import DMarketItem
from table.rows.basic_row import BasicRow


class DMarketItemRow(BasicRow):
    '''InventoryItemRow represents a certain amount of CS:GO item which is in DMarket inventory'''
    def __init__(self, title, asset_ids, amount,
                 total_price, exterior, tradable, market_price, discount):

        super().__init__(title, amount, market_price, total_price)
        self.asset_ids = asset_ids
        self.total_price = 
        self.exterior = exterior
        self.tradable = tradable
        self.discount = discount

        

    @classmethod
    def item_to_row(cls, item: DMarketItem):
        '''creates a new DMarketItemRow from an DMarketItem'''
        return cls(
                   title = item.title,
                   asset_ids = [item.asset_id],
                   amount = item.amount,
                   exterior = item.exterior,
                   tradable = item.tradable,
                   market_price = item.market_price,
                   total_price = item.market_price*item.amount,
                   discount = item.discount)
                              
                   
        


    def add_to_row(self, item: DMarketItem):
        '''adds an DMarketItem to an existing DMarketItemRow'''
        self.amount += item.amount
        self.total_price += item.market_price
        self.asset_ids.append(item.asset_id)


    def similar_to_item(self, item: DMarketItem):
        '''returns wether an DMarketItem has the same relevent attributes as the DMarketItemRow'''
        return item.title == self.title and item.market_price == self.market_price

def parse_items_list_to_rows(all_items: list) -> list:
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if row.similar_to_item(item):
                row.add_to_row(item)
                break
        else:
            rows.append(DMarketItemRow.item_to_row(item))
    return rows
