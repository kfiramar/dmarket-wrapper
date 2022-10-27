'''module that loads all the variables in to the app'''

import configparser
from pathlib import Path

JSON_QOUTES_FIXER = {"\'": "\""}
JSON_DICTIONARY_FIXER = {"\'": "\"", 'True': '\"True\"', ' False': '\"False\"', 'None': '\"None\"'}
TIME_TABLE = {'minute': -3, 'hour': -6, 'day': -9, 'month': -12, 'year': -15}
COLORS = ['\u001b[32;1m', '\u001b[32;1m', '\u001b[31;1m', '\u001b[31;1m', '\u001b[32;0m', '\u001b[32;0m', '\u001b[31;0m', '\u001b[31;0m']
ROW_PRINT_MASKS = {'InventoryItemRow': [0, 5, 3, 2, 4], 'ListingRow': [0, 6, 3, 2, 4], 'PurcheseRow': [0, 6, 2, 4]}


general_config = keys_config = configparser.ConfigParser()
PROJECT_PATH = Path(__file__).parents[2]
general_config.read(PROJECT_PATH / 'config.ini',  encoding='utf-8')
keys_config.read(PROJECT_PATH / 'keys.ini',  encoding='utf-8')

API_URL = general_config['URLS']['API_URL']

BALANCE_ENDPOINT = general_config['ENDPOINTS']['BALANCE']
BUY_ORDER_ENDPOINT = general_config['ENDPOINTS']['BUY_ORDER']
DM_INVENTORY_ENDPOINT = general_config['ENDPOINTS']['DM_INVENTORY']
STEAM_INVENTORY_ENDPOINT = general_config['ENDPOINTS']['STEAM_INVENTORY']
SELL_LISTINGS_ENDPOINT = general_config['ENDPOINTS']['SELL_LISTINGS']
DELETE_LISTING_ENDPOINT = general_config['ENDPOINTS']['DELETE_LISTING']
PURCHASE_HISTORY_ENDPOINT = general_config['ENDPOINTS']['PURCHASE_HISTORY']

PUBLIC_KEY = keys_config['KEYS']['PUBLIC_KEY']
SECRET_KEY = keys_config['KEYS']['SECRET_KEY']
SIGNATURE_PREFIX = "dmar ed25519 "

LOGGING = general_config['GENERAL']['LOGGING']

RAINBOW_TABLE = general_config['TABLE']['RAINBOW_TABLE']
RAINBOW_SPEED = float(general_config['TABLE']['RAINBOW_SPEED'])
RAINBOW_DURATION = float(general_config['TABLE']['RAINBOW_DURATION'])
