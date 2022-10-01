'''module that loads all the variables in to the app'''
from config import config

API_URL = config['URLS']['API_URL']

BALANCE_ENDPOINT = config['ENDPOINTS']['BALANCE']
BUY_ORDER_ENDPOINT = config['ENDPOINTS']['BUY_ORDER']
INVENTORY_ENDPOINT = config['ENDPOINTS']['INVENTORY']
SELL_LISTINGS_ENDPOINT = config['ENDPOINTS']['SELL_LISTINGS']

PUBLIC_KEY_ENDPOINT = config['KEYS']['PUBLIC_KEY']
SECRET_KEY_ENDPOINT = config['KEYS']['SECRET_KEY']

LOGGING = config['GENERAL']['LOGGING']
