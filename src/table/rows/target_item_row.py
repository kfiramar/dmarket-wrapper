'''
This module contains the TargetItemRow class (which is a subclass of BasicItem).
TargetItemRow is based on TargetItem,
Each row groups all the identical items into the same row.
'''

from items.target_item import TargetItem
from table.rows.basic_row import BasicRow


class TargetItemRow(BasicRow):
    '''TargetItemRow represents a certain amount of CS:GO item which is in DMarket inventory'''
    def __init__(self, title, amount,
                 exterior, listing_price, market_price, total_price, target_ids=[]):
        self.exterior = exterior
        self.listing_price = listing_price
        self.target_ids = target_ids
        self.total_price = total_price
        super().__init__(title, amount, market_price)

    @classmethod
    def item_to_row(cls, item: TargetItem):
        '''creates a new TargetItemRow from an TargetItem'''
        return cls(title=item.title,
                   amount=item.amount,
                   exterior=item.exterior,
                   listing_price=item.listing_price,
                   market_price=item.market_price,
                   target_ids=[item.target_id],
                   total_price=item.listing_price)


    def add_to_row(self, item: TargetItem):
        '''adds an TargetItem to an existing TargetItemRow'''
        self.amount += item.amount
        self.total_price += float(item.listing_price)
        self.target_ids.append(item.target_id)


    def similar_to_item(self, item: TargetItem):
        '''returns wether an TargetItem has the same relevent attributes as the TargetItemRow'''
        return item.title == self.title and item.listing_price == self.listing_price and item.exterior == self.exterior


def parse_items_list_to_rows(all_items: list) -> list:
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if row.similar_to_item(item):
                row.add_to_row(item)
                break
        else:
            rows.append(TargetItemRow.item_to_row(item))
    return rows
