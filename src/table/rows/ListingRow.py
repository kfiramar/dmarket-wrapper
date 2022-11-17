'''ListingRow represents a certain amount of CS:GO item which is listed in DMarket'''
from src.items.ListingItem import ListingItem
from table.rows.BasicRow import BasicRow

class ListingRow(BasicRow):
    '''ListingRow represents a certain amount of CS:GO item which are listed in DMarket'''
    def __init__(self, title, asset_ids, offer_ids, total_items, total_price,
                 listing_price, tradable, market_price=''):
        super().__init__(title, asset_ids, total_items, market_price, total_price)
        self.offer_ids = offer_ids
        self.listing_price = listing_price
        self.tradable = tradable

    @classmethod
    def item_to_row(cls, item: ListingItem):
        '''creates a new ListingRow from an ListingItem'''
        return cls(title=item.title,
                         asset_ids=[item.asset_id],
                         listing_price=item.listing_price,
                         total_items=1,
                         total_price=item.listing_price,
                         offer_ids=[item.offer_id],
                         tradable=item.tradable)

    def add_to_row(self, item: ListingItem):
        '''adds a ListingItem to an existing ListingRow'''
        self.total_items += 1
        self.total_price += float(item.listing_price)
        self.asset_ids.append(item.asset_id)
        self.offer_ids.append(item.offer_id)

    def similar_to_item(self, item: ListingItem) -> bool:
        '''returns wether an ListingItem has the same relevent attributes as the ListignRow'''
        return item.title == self.title and item.listing_price == self.listing_price and item.tradable == self.tradable

def parse_items_list_to_rows(all_items: list) -> list:
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if row.similar_to_item(item):
                row.add_to_row(item)
                break
        else:
            rows.append(ListingRow.item_to_row(item))
    return rows
