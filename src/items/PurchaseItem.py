from datetime import datetime
from items.BasicItem import BasicItem


class PurchaseItem(BasicItem):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, asset_id, title, offer_closed_at,
                 offer_created_at,
                 sold_price, offer_id, market_price=''):
        self.offer_id = offer_id
        self.offer_closed_at = offer_closed_at
        self.offer_created_at = offer_created_at
        self.sold_price = sold_price
        super().__init__(asset_id, title, market_price)


    @classmethod
    def parse_json_to_item(cls, json_dict: dict):
        '''parses a JSON into a PurchaseItem'''
        return cls(
                    asset_id=json_dict['AssetID'],
                    title=json_dict['Title'],
                    offer_id=json_dict['OfferID'],
                    sold_price=float(json_dict['Price']['Amount']),
                    offer_closed_at=epoch_time_convertor(json_dict['OfferClosedAt']),
                    offer_created_at=epoch_time_convertor(json_dict['OfferCreatedAt']))


def epoch_time_convertor(epoch_time: str) -> str:
    '''convert epoch time to normal format time, and take handle cases where epoch time is -62135596800'''
    if epoch_time == '-62135596800':
        return '0001-01-01 00:00:01'
    return datetime.fromtimestamp(int(epoch_time)).strftime('%Y-%m-%d %H:%M:%S')


def parse_jsons_to_items_list(json_purchases: dict) -> list:
    '''uses parse_json_to_item to parse all the items from json'''
    purchase_list = []
    for json_purchase in json_purchases['Trades']:
        purchase_list.append(PurchaseItem.parse_json_to_item(json_dict=json_purchase))
    return purchase_list