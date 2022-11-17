'''This module contains the row class which represents a row in a CLI chart'''

from table.rows.listing_row import parse_items_list_to_rows
from table.tables.basic_table import BasicTable
from items.listing_item import parse_jsons_to_items_list


class ListingTable(BasicTable):
    '''ListingTable is a table - in this case it is a list of ListingRows'''

    @classmethod
    def parse_jsons_to_table(cls, content: dict) -> list:
        '''This function is used to parse jsons to a table'''
        dm_items = parse_jsons_to_items_list(content)
        dm_rows = parse_items_list_to_rows(dm_items)
        dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
        return cls(dm_rows)
