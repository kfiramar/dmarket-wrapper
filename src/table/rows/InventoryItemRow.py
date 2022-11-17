from src.items.InventoryItem import InventoryItem
from table.rows.BasicRow import BasicRow


class InventoryItemRow(BasicRow):
    '''InventoryItemRow represents a certain amount of CS:GO item which is in DMarket inventory'''
    def __init__(self, title, asset_ids, total_items,
                 total_price, exterior, tradable, market_price):

        super().__init__(title, asset_ids, total_items,
                         market_price, total_price)
        self.exterior = exterior
        self.tradable = tradable

    @classmethod
    def item_to_row(cls, item: InventoryItem):
        '''creates a new InventoryItemRow from an InventoryItem'''
        return cls(title=item.title,
                   asset_ids=[item.asset_id],
                   exterior=item.exterior,
                   market_price=item.market_price,
                   total_items=1,
                   total_price=item.market_price,
                   tradable=item.tradable)


    def add_to_row(self, item: InventoryItem):
        '''adds an InventoryItem to an existing InventoryItemRow'''
        self.total_items += 1
        self.total_price += float(item.market_price)
        self.asset_ids.append(item.asset_id)
        self.total_price = float(self.total_price)


    def similar_to_item(self, item: InventoryItem):
        '''returns wether an InventoryItem has the same relevent attributes as the InventoryItemRow'''
        return item.title == self.title and item.market_price == self.market_price and item.tradable == self.tradable

def parse_items_list_to_rows(all_items: list) -> list:
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if row.similar_to_item(item):
                row.add_to_row(item)
                break
        else:
            rows.append(InventoryItemRow.item_to_row(item))
    return rows