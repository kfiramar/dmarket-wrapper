'''This module contains all the parsing done in the program'''
# from typing import Callable
# from datetime import datetime
# from items.ListingItem import ListingItem
# from items.InventoryItem import InventoryItem
# from items.PurchaseItem import PurchaseItem
# from table.rows.PurcheseRow import PurcheseRow
# from table.rows.ListingRow import ListingRow
# from table.rows.InventoryItemRow import InventoryItemRow 
# from common.config import TIME_TABLE


# def parse_jsons_to_rows(content: dict, json_to_items_func: Callable, items_to_rows_func: Callable, sort_by: str) -> list:
#     '''This function is used to parse jsons to sorted rows'''
#     dm_items = json_to_items_func(content)
#     dm_rows = items_to_rows_func(dm_items)
#     dm_rows.sort(key=lambda row: getattr(row, sort_by))
#     return dm_rows


# def parse_jsons_to_purcheserows(content: dict, json_to_items_func: Callable, items_to_rows_func: Callable, sort_by: str, param: str) -> list:
#     '''This function is used to parse jsons to sorted rows'''
#     dm_items = json_to_items_func(content)
#     dm_rows = items_to_rows_func(dm_items, param)
#     dm_rows.sort(key=lambda row: getattr(row, sort_by))
#     return dm_rows

# #####################
# def parse_jsons_to_listings(jsons: dict) -> list:
#     '''uses parse_json_to_item to parse all the items from json'''
#     listing_list = []
#     for json_item in jsons['Items']:
#         listing_list.append(ListingItem.parse_json_to_item(json_dict=json_item))
#     return listing_list

# #################
# def parse_jsons_to_purchases(jsons: dict) -> list:
#     '''uses parse_json_to_item to parse all the items from json'''
#     listing_list = []
#     for json_item in jsons['Trades']:
#         listing_list.append(PurchaseItem.parse_json_to_item(json_dict=json_item))
#     return listing_list


# def parse_purchases_to_purcheserows_merge(all_items: list, merge_by: str) -> list:
#     '''parses items from list(Items) to list(Rows)'''
#     rows = []
#     for item in all_items:
#         for row in rows:
#             if item.title == row.title and item.sold_price == row.sold_price and item.offer_closed_at[:TIME_TABLE[merge_by]] == row.offer_closed_at[:TIME_TABLE[merge_by]]:
#                 row.total_items += 1
#                 row.total_price += float(item.sold_price)
#                 row.asset_ids.append(item.asset_id)
#                 row.offer_ids.append(item.offer_id)
#                 break
#         else:
#             rows.append(PurcheseRow(title=item.title,
#                                     asset_ids=[item.asset_id],
#                                     sold_price=item.sold_price,
#                                     offer_closed_at=item.offer_closed_at,
#                                     offer_created_at=item.offer_created_at,
#                                     total_items=1,
#                                     total_price=item.sold_price,
#                                     offer_ids=[item.offer_id]
#                                     ))
#     return rows


# def parse_purchases_to_purcheserows_by_date(all_items: list, date: datetime) -> list:
#     '''parses items from list(Items) to list(Rows)'''
#     rows = []
#     for item in all_items:
#         item_date = datetime.strptime(item.offer_closed_at, '%Y-%m-%d %H:%M:%S')
#         if item_date >= date:
#             for row in rows:
#                 if item.title == row.title and item.sold_price == row.sold_price:
#                     row.total_items += 1
#                     row.total_price += float(item.sold_price)
#                     row.asset_ids.append(item.asset_id)
#                     row.offer_ids.append(item.offer_id)
#                     break
#             else:
#                 rows.append(PurcheseRow(title=item.title,
#                                         asset_ids=[item.asset_id],
#                                         sold_price=item.sold_price,
#                                         offer_closed_at=item.offer_closed_at,
#                                         offer_created_at=item.offer_created_at,
#                                         total_items=1,
#                                         total_price=item.sold_price,
#                                         offer_ids=[item.offer_id]
#                                         ))
#     return rows


# def parse_listings_to_listingrows(all_items: list) -> list:
#     '''parses items from list(Items) to list(Rows)'''
#     rows = []
#     for item in all_items:
#         for row in rows:
#             if item.title == row.title and item.listing_price == row.listing_price and item.tradable == row.tradable:
#                 row.total_items += 1
#                 row.total_price += float(item.listing_price)
#                 row.asset_ids.append(item.asset_id)
#                 row.offer_ids.append(item.offer_id)
#                 break
#         else:
#             rows.append(ListingRow(title=item.title,
#                                    asset_ids=[item.asset_id],
#                                    listing_price=item.listing_price,
#                                    total_items=1,
#                                    total_price=item.listing_price,
#                                    offer_ids=[item.offer_id],
#                                    tradable=item.tradable))
#     return rows

# ##############
# def parse_jsons_to_inventoryitems(jsons: dict) -> list:
#     '''uses parse_json_to_item to parse all the items from json'''
#     inventoryitem_list = []
#     for json_item in jsons['Items']:
#         inventoryitem_list.append(InventoryItem.parse_json_to_item(json_dict=json_item))
#     return inventoryitem_list


# def parse_inventoryitems_to_inventoryitemrow(all_items: list) -> list:
#     '''parses items from list(Items) to list(Rows)'''
#     rows = []
#     for item in all_items:
#         for row in rows:
#             if item.title == row.title and item.market_price == row.market_price and item.tradable == row.tradable:
#                 row.total_items += 1
#                 row.total_price += float(item.market_price)
#                 row.asset_ids.append(item.asset_id)
#                 row.total_price = float(row.total_price)
#                 break
#         else:
#             rows.append(InventoryItemRow(title=item.title,
#                                          asset_ids=[item.asset_id],
#                                          exterior=item.exterior,
#                                          market_price=item.market_price,
#                                          total_items=1,
#                                          total_price=item.market_price,
#                                          tradable=item.tradable))
#     return rows