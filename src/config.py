'''module that loads all the variables in to the app'''
import os
import configparser

JSON_QOUTES_FIXER = {"\'": "\""}
JSON_DICTIONARY_FIXER = {"\'": "\"", 'True': '\"True\"', ' False': '\"False\"', 'None': '\"None\"'}
TIME_TABLE = {'minute': -3, 'hour': -6, 'day': -9, 'month': -12, 'year': -15}
COLORS = ['\u001b[32;1m', '\u001b[32;1m', '\u001b[31;1m', '\u001b[31;1m', '\u001b[32;0m', '\u001b[32;0m', '\u001b[31;0m', '\u001b[31;0m']
ROW_PRINT_MASKS = {'InventoryItemRow': [0, 5, 3, 2, 4], 'ListingRow': [0, 6, 3, 2, 4], 'PurcheseRow': [0, 6, 2, 4]}

SRC_PATH = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(SRC_PATH, '../config.ini'),  encoding='utf-8')

API_URL = config['URLS']['API_URL']

BALANCE_ENDPOINT = config['ENDPOINTS']['BALANCE']
BUY_ORDER_ENDPOINT = config['ENDPOINTS']['BUY_ORDER']
DM_INVENTORY_ENDPOINT = config['ENDPOINTS']['DM_INVENTORY']
STEAM_INVENTORY_ENDPOINT = config['ENDPOINTS']['STEAM_INVENTORY']
SELL_LISTINGS_ENDPOINT = config['ENDPOINTS']['SELL_LISTINGS']
DELETE_LISTING_ENDPOINT = config['ENDPOINTS']['DELETE_LISTING']
PURCHASE_HISTORY_ENDPOINT = config['ENDPOINTS']['PURCHASE_HISTORY']

PUBLIC_KEY = config['KEYS']['PUBLIC_KEY']
SECRET_KEY = config['KEYS']['SECRET_KEY']
SIGNATURE_PREFIX = "dmar ed25519 "

LOGGING = config['GENERAL']['LOGGING']
RAINBOW_TABLE = config['GENERAL']['RAINBOW_TABLE']

COLORS = config['TABLE']['COLORS']
TIME_TABLE = config['TABLE']['TIME_TABLE']
