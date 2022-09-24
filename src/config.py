'''This module contains the main loop of the program and prints'''
import os
import configparser

JSON_DICTIONARY_FIXER = {"\'": "\"" ,'True': '\"True\"',' False': '\"False\"','None':'\"None\"'}

SRC_PATH= os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(SRC_PATH, '../config.ini'),  encoding='utf-8')