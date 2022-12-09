'''module that loads all the variables in to the app'''

from pathlib import Path
from configobj import ConfigObj

JSON_QOUTES_FIXER = {"\'": "\""}
JSON_DICTIONARY_FIXER = {"\'": "\"", 'True': '\"True\"', ' False': '\"False\"', 'None': '\"None\"'}
TIME_TABLE = {'minute': -3, 'hour': -6, 'day': -9, 'month': -12, 'year': -15}
COLORS = ['\u001b[32;1m', '\u001b[32;1m', '\u001b[31;1m', '\u001b[31;1m', '\u001b[32;0m', '\u001b[32;0m', '\u001b[31;0m', '\u001b[31;0m']
ROW_PRINT_MASKS_WORDS = {'InventoryItemRow': ['title', 'market_price', 'amount', 'total_price'], 'ListingRow': ["title", "listing_price", "market_price", "amount", "total_price"], 'PurcheseRow': ["title", "sold_price", "amount", "total_price"], 'DMarketItemRow': ["title", "amount", "market_price", "discount"], "TargetItemRow": ["title", "amount", "listing_price", "market_price", "total_price"]}
SIGNATURE_PREFIX = "dmar ed25519 "
CLEAR_SHELL = "\033[H\033[J"

# config = keys_config = configparser.ConfigParser()
# PROJECT_PATH = Path(__file__).parents[2]
# config.read(PROJECT_PATH / 'config.ini',  encoding='utf-8')
# keys_config.read(PROJECT_PATH / 'keys.ini',  encoding='utf-8')


PROJECT_PATH = Path(__file__).parents[2]
config = ConfigObj(str(PROJECT_PATH / 'config_obj.ini'),  encoding='utf-8')
keys_config = ConfigObj(str(PROJECT_PATH / 'keys.ini'),  encoding='utf-8')



API_URL = config['URLS']['API_URL']

BALANCE_REQUEST = config['REQUESTS']['BALANCE']
BUY_ORDER_REQUEST = config['REQUESTS']['BUY_ORDER']
DM_INVENTORY_REQUEST = config['REQUESTS']['DM_INVENTORY']
STEAM_INVENTORY_REQUEST = config['REQUESTS']['STEAM_INVENTORY']
SELL_LISTINGS_REQUEST = config['REQUESTS']['LISTINGS']
DELETE_LISTING_REQUEST = config['REQUESTS']['DELETE_LISTING']
PURCHASE_HISTORY_REQUEST = config['REQUESTS']['PURCHASE_HISTORY']
MARKET_ITEMS_REQUEST = config['REQUESTS']['MARKET_ITEMS']
CREATE_TARGET_REQUEST = config['REQUESTS']['CREATE_TARGET']
VIEW_TARGETS_REQUEST = config['REQUESTS']['VIEW_TARGETS']

PUBLIC_KEY = keys_config['KEYS']['PUBLIC_KEY']
SECRET_KEY = keys_config['KEYS']['SECRET_KEY']


LOGGING = config['GENERAL'].as_bool('LOGGING')

TABLEFMT =  config['TABLE']['APPEARANCE']['TABLEFMT']
NUMALIGN = config['TABLE']['APPEARANCE']['NUMALIGN']
STRALIGN = config['TABLE']['APPEARANCE']['STRALIGN']
FLOATFMT = config['TABLE']['APPEARANCE']['FLOATFMT']
SHOWINDEX = config['TABLE']['APPEARANCE']['SHOWINDEX']
TABLE_LINE = config['TABLE']['APPEARANCE']['TABLE_LINE']

RAINBOW_TABLE = config['TABLE']['RAINBOW'].as_bool('RAINBOW_TABLE')
RAINBOW_SPEED = config['TABLE']['RAINBOW'].as_float('RAINBOW_SPEED')
RAINBOW_DURATION = config['TABLE']['RAINBOW'].as_float('RAINBOW_DURATION')
MAXIMUM_ROWS = config['TABLE']['RAINBOW'].as_int('MAXIMUM_ROWS')


# DELETE_LISTING = config['TEXT']['DELETE_LISTING']
# DELETE_LISTING = config['TEXT']['CREATE_LISTING']
# DELETE_LISTING = config['TEXT']['BALANCE']
# DELETE_LISTING = config['TEXT']['ERRORS']
# DELETE_LISTING = config['TEXT']['CLI_HELP']
# DELETE_LISTING = config['TEXT']['SPINNER']

CREATE_LISTINGS_ITEMS = config['TEXT']['QUESTIONS_TEXT']['REMOVE_LISTING_ITEM']
REMOVE_LISTING_AMOUNT = config['TEXT']['QUESTIONS_TEXT']['REMOVE_LISTING_AMOUNT']
CREATE_LISTINGS_ITEMS = config['TEXT']['QUESTIONS_TEXT']['CREATE_LISTINGS_ITEMS']
CREATE_LISTINGS_AMOUNT = config['TEXT']['QUESTIONS_TEXT']['CREATE_LISTINGS_AMOUNT']
CREATE_LISTINGS_PRICE = config['TEXT']['QUESTIONS_TEXT']['CREATE_LISTINGS_PRICE']
SUCCESSFULLY_CREATED = config['TEXT']['QUESTIONS_TEXT']['SUCCESSFULLY_CREATED']
REMOVE_LISTING_SUCCESSFULLY = config['TEXT']['QUESTIONS_TEXT']['REMOVE_LISTING_SUCCESSFULLY']
UNSUCSESSFULLY_CREATED = config['TEXT']['QUESTIONS_TEXT']['UNSUCSESSFULLY_CREATED']
REMOVE_LISTING_UNSUCCESSFULLY = config['TEXT']['QUESTIONS_TEXT']['REMOVE_LISTING_UNSUCCESSFULLY']

RECIVED_ITEMS = config['SPINNER']['TEXT']['RECIVED_ITEMS']
LISTING_ZERO_ITEMS = config['SPINNER']['TEXT']['LISTING_ZERO_ITEMS']
INVENTORY_ZERO_ITEMS = config['SPINNER']['TEXT']['INVENTORY_ZERO_ITEMS']
GETTING_ITEMS = config['SPINNER']['TEXT']['GETTING_ITEMS']
ATTEMPTING_CREATE_ITEMS = config['SPINNER']['TEXT']['ATTEMPTING_CREATE_ITEMS']
ATTEMPTING_DELETE = config['SPINNER']['TEXT']['ATTEMPTING_DELETE']

SPINNER_CONF = config['SPINNER']['CONFIGURATION']

BALANCE_TEXT = config['TEXT']['NORMAL_TEXT']['BALANCE_TEXT']
EMPTY_TABLE = config['TEXT']['NORMAL_TEXT']['EMPTY_TABLE']
