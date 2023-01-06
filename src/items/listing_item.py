'''
This module contains the ListingItem class (which is a subclass of BasicItem)
ListingItem represends a listing of one item on DMarket
'''

from items.basic_item import BasicItem


class ListingItem(BasicItem):
    '''ListingItem represents a CS:GO item which is listed in DMarket'''

    def __init__(self, asset_id, title, tradable, listing_price,
                 offer_id, market_price=''):
        self.tradable = tradable
        self.offer_id = offer_id
        self.listing_price = listing_price
        self.asset_id = asset_id
        super().__init__(title, market_price)

    @classmethod
    def parse_json_to_item(cls, json_dict: dict):
        '''parses a JSON into an ListingItem'''
        return cls(
            asset_id=json_dict['AssetID'],
            title=json_dict['Title'],
            tradable=str(json_dict['Tradable']),
            listing_price=float(json_dict['Offer']['Price']['Amount']),
            offer_id=json_dict['Offer']['OfferID'])


def parse_jsons_to_items_list(jsons: dict) -> list:
    '''parses json items to ListingItem list'''
    listing_list = []
    for json_item in jsons['Items']:
        listing_list.append(
            ListingItem.parse_json_to_item(json_dict=json_item))
    return listing_list


def listing_error_parsing(responses: list) -> list:
    '''parse list if responses to an error list'''
    error_list = []
    for response_content in responses:
        for listing in response_content['Result']:
            if listing['Error'] is not None:
                error_list.append({listing['Error']['Message']})
    return error_list
