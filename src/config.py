'''This module contains the main loop of the program and prints'''
import os
import configparser

JSON_DICTIONARY_FIXER = {"\'": "\"" ,'True': '\"True\"',' False': '\"False\"','None':'\"None\"'}

SRC_PATH= os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(SRC_PATH, '../config.ini'),  encoding='utf-8')

API_URL = config['URLS']['API_URL']

BALANCE_ENDPOINT = config['ENDPOINTS']['BALANCE']
BUY_ORDER_ENDPOINT = config['ENDPOINTS']['BUY_ORDER']
INVENTORY_ENDPOINT = config['ENDPOINTS']['INVENTORY']
SELL_LISTINGS_ENDPOINT = config['ENDPOINTS']['SELL_LISTINGS']
DELETE_LISTING_ENDPOINT = config['ENDPOINTS']['DELETE_LISTING']

PUBLIC_KEY_ENDPOINT = config['KEYS']['PUBLIC_KEY']
SECRET_KEY_ENDPOINT = config['KEYS']['SECRET_KEY']

LOGGING = config['GENERAL']['LOGGING']
