'''module that loads all the variables in to the app'''
import os
import configparser

JSON_DICTIONARY_FIXER = {"\'": "\"", 'True': '\"True\"', ' False': '\"False\"', 'None':'\"None\"'}

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

PUBLIC_KEY = config['KEYS']['PUBLIC_KEY']
SECRET_KEY = config['KEYS']['SECRET_KEY']

LOGGING = config['GENERAL']['LOGGING']
