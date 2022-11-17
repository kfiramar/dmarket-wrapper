'''This module contains the row class which represents a row in a CLI chart'''

from table.tables.basic_table import BasicTable
from table.rows.prchese_row import parse_items_list_to_rows, parse_items_list_to_rows_from_date
from items.purchase_item import parse_jsons_to_items_list


class PurcheseTable(BasicTable):
    '''PurcheseTable is a table - in this case it is a list of PurcheseRows'''

    @classmethod
    def parse_jsons_to_table(cls, content: dict) -> list:
        '''This function is used to parse jsons to a table'''
        dm_items = parse_jsons_to_items_list(content)
        dm_rows = parse_items_list_to_rows(dm_items)
        dm_rows.sort(key=lambda row: getattr(row, 'offer_closed_at'))
        return cls(dm_rows)


    @classmethod
    def parse_jsons_to_purchese_table_from_date(cls, content: dict, date) -> list:
        '''This function is used to parse jsons to a table, but only including purchases from the stated date'''
        dm_items = parse_jsons_to_items_list(content)
        dm_rows = parse_items_list_to_rows_from_date(dm_items, date)
        dm_rows.sort(key=lambda row: getattr(row, 'offer_closed_at'))
        return cls(dm_rows)
    