'''
This module contains the PurcheseRow class (which is a subclass of BasicItem).
PurcheseRow is based on PurcheseItem,
Each row groups all the identical items into the same row.
'''


from datetime import datetime
from common.config import TIME_TABLE
from items.purchase_item import PurchaseItem
from table.rows.basic_row import BasicRow


class PurcheseRow(BasicRow):
    '''PurceseRow represents past purchese of a CS:GO item(s) which on DMarket'''
    def __init__(self, title, asset_ids, offer_ids, amount, total_price,
                 sold_price, offer_closed_at, offer_created_at, market_price=''):
        super().__init__(title, asset_ids, amount, market_price, total_price)
        self.offer_ids = offer_ids
        self.sold_price = sold_price
        self.offer_closed_at = offer_closed_at
        self.offer_created_at = offer_created_at

    @classmethod
    def item_to_row(cls, item: PurchaseItem):
        '''creates a new PurcheseRow from an PurcheseItem'''
        return cls(title=item.title,
                   asset_ids=[item.asset_id],
                   sold_price=item.sold_price,
                   offer_closed_at=item.offer_closed_at,
                   offer_created_at=item.offer_created_at,
                   amount=1,
                   total_price=item.sold_price,
                   offer_ids=[item.offer_id]
                    )

    def add_to_row(self, item: PurchaseItem):
        '''adds an item to an existing row'''
        self.amount += 1
        self.total_price += float(item.sold_price)
        self.asset_ids.append(item.asset_id)
        self.offer_ids.append(item.offer_id)


    def similar_to_item(self, item: PurchaseItem) -> bool:
        '''returns wether an PurcheseItem has the same relevent attributes as the Purcheserow'''
        return item.title == self.title and item.sold_price == self.sold_price

def parse_items_list_to_rows_from_date(all_items: list, date: datetime) -> list:
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        item_date = datetime.strptime(item.offer_closed_at, '%Y-%m-%d %H:%M:%S')
        if item_date >= date:
            for row in rows:
                if row.similar_to_item(item):
                    row.add_to_row(item)
                    break
            else:
                rows.append(PurcheseRow.item_to_row(item))
    return rows


def parse_items_list_to_rows(all_items: list, merge_by: str  = 'day') -> list:
    '''parses items from list(PurcheseItem) to list(PurcheseRow)'''
    rows = []
    for item in all_items:
        for row in rows:
            if row.similar_to_item(item) and item.offer_closed_at[:TIME_TABLE[merge_by]] == row.offer_closed_at[:TIME_TABLE[merge_by]]:
                row.add_to_row(item)
                break
        else:
            rows.append(PurcheseRow.item_to_row(item))
    return rows
