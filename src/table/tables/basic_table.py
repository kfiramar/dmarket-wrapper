'''This module contains the row class which represents a row in a CLI chart'''

class BasicTable:
    '''This class represents a row in a CLI chart'''
    def __init__(self, rows_list):
        self.rows = rows_list

    @classmethod
    def parse_jsons_to_table(cls, content) -> list:
        '''This function is used to parse jsons to a table'''
        raise NotImplementedError

    @classmethod
    def parse_jsons_to_purchese_table_from_date(cls, content: dict, date: str) -> list:
        '''
        This function is used to parse jsons to a table
        but only including purchases from the stated date
        Used only on PurchaseTable
        '''
        raise NotImplementedError
    