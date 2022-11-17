'''module that loads all the variables in to the app'''

import configparser
from pathlib import Path

JSON_QOUTES_FIXER = {"\'": "\""}
JSON_DICTIONARY_FIXER = {"\'": "\"", 'True': '\"True\"', ' False': '\"False\"', 'None': '\"None\"'}
TIME_TABLE = {'minute': -3, 'hour': -6, 'day': -9, 'month': -12, 'year': -15}
COLORS = ['\u001b[32;1m', '\u001b[32;1m', '\u001b[31;1m', '\u001b[31;1m', '\u001b[32;0m', '\u001b[32;0m', '\u001b[31;0m', '\u001b[31;0m']
ROW_PRINT_MASKS = {'InventoryItemRow': [0, 5, 3, 2, 4], 'ListingRow': [0, 6, 3, 2, 4], 'PurcheseRow': [0, 6, 2, 4]}
SIGNATURE_PREFIX = "dmar ed25519 "
CLEAR_SHELL = "\033[H\033[J"

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


LOGGING = general_config.getboolean('GENERAL', 'LOGGING')

TABLEFMT =  general_config['TABLE']['TABLEFMT']
NUMALIGN = general_config['TABLE']['NUMALIGN']
STRALIGN = general_config['TABLE']['STRALIGN']
FLOATFMT = general_config['TABLE']['FLOATFMT']
SHOWINDEX = general_config['TABLE']['SHOWINDEX']

TABLE_LINE = general_config['TABLE']['TABLE_LINE']

CREATE_LISTINGS_ITEMS = general_config['QUESTIONS_TEXT']['REMOVE_LISTINGS_ITEMS']
REMOVE_LISTINGS_AMOUNT = general_config['QUESTIONS_TEXT']['REMOVE_LISTINGS_AMOUNT']
CREATE_LISTINGS_ITEMS = general_config['QUESTIONS_TEXT']['CREATE_LISTINGS_ITEMS']
CREATE_LISTINGS_AMOUNT = general_config['QUESTIONS_TEXT']['CREATE_LISTINGS_AMOUNT']
CREATE_LISTINGS_PRICE = general_config['QUESTIONS_TEXT']['CREATE_LISTINGS_PRICE']
SUCCESSFULLY_CREATED = general_config['QUESTIONS_TEXT']['SUCCESSFULLY_CREATED']
SUCSESSFULLY_DELETED = general_config['QUESTIONS_TEXT']['SUCSESSFULLY_DELETED']
UNSUCSESSFULLY_CREATED = general_config['QUESTIONS_TEXT']['UNSUCSESSFULLY_CREATED']
UNSUCSESSFULLY_DELETED = general_config['QUESTIONS_TEXT']['UNSUCSESSFULLY_DELETED']

RECIVED_ITEMS = general_config['SPINNER_TEXT']['RECIVED_ITEMS']
LISTING_ZERO_ITEMS = general_config['SPINNER_TEXT']['LISTING_ZERO_ITEMS']
INVENTORY_ZERO_ITEMS = general_config['SPINNER_TEXT']['INVENTORY_ZERO_ITEMS']
ATTEMPTING_GET_ITEMS = general_config['SPINNER_TEXT']['ATTEMPTING_GET_ITEMS']
ATTEMPTING_CREATE_ITEMS = general_config['SPINNER_TEXT']['ATTEMPTING_CREATE_ITEMS']
ATTEMPTING_DELETE = general_config['SPINNER_TEXT']['ATTEMPTING_DELETE']

BALANCE_TEXT = general_config['NORMAL_TEXT']['BALANCE_TEXT']
EMPTY_TABLE = general_config['NORMAL_TEXT']['EMPTY_TABLE']

RAINBOW_TABLE = general_config.getboolean('RAINBOW', 'RAINBOW_TABLE')
RAINBOW_SPEED = general_config.getfloat('RAINBOW', 'RAINBOW_SPEED')
RAINBOW_DURATION = general_config.getfloat('RAINBOW', 'RAINBOW_DURATION')
MAXIMUM_ROWS = general_config.getint('RAINBOW', 'MAXIMUM_ROWS')
