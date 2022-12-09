'''This module Is used to log the API requests'''
import os
import time
import json
import pprint
from types import NoneType
from halo import Halo
from common.config import PROJECT_PATH, JSON_DICTIONARY_FIXER, JSON_QOUTES_FIXER, SPINNER_CONF


def json_fixer(json_str: str, fixer: dict) -> str:
    '''changes the everything to the json convention'''
    for key, value in fixer.items():
        json_str = json_str.replace(key, value)
    return json_str


def write_content(content: dict, func_name: str):
    '''Creates a file and loads all the json content into it'''
    fixed_json = []
    file_name = time.strftime(f"{func_name}-%Y-%m-%d_%H:%M:%S.json")
    path_to_file = PROJECT_PATH / f'logs/{file_name}'
    fixed_json = json.loads(json_fixer(str(content), JSON_DICTIONARY_FIXER))
    os.makedirs(os.path.dirname(PROJECT_PATH / 'logs/'), exist_ok=True)
    with open(path_to_file, "wb") as file:
        file.write((json_fixer(pprint.pformat(fixed_json), JSON_QOUTES_FIXER)).encode("UTF-8"))


def log(response: dict, func_name: str):
    '''logging of an API json with animation wrapping'''
    logging_spinner = Halo(text='Logging API request', spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])
    logging_spinner.start()
    write_content(response, func_name)
    logging_spinner.info(text="API request was logged")


def merge_dicts(responses: list) -> dict:
    '''merge a list of dictionary to one'''
    merged_dictionary = responses[0].json()
    for response in responses[1:]:
        merged_dictionary = combine_2_dict(merged_dictionary, response.json())
    return merged_dictionary


def combine_2_dict(dict1: dict, dict2: dict) -> dict:
    '''merge 2 dictionaries'''
    for key, *value in dict1.items():
        for key2, *value2 in dict2.items():
            if key2 == key and value2 != value and value2[0]:
                if (isinstance(dict1[key], list) or
                    isinstance(dict2[key2], list)):
                    if isinstance(dict1[key], NoneType):
                        dict1[key2] = []
                    dict1[key2].extend(value2[0])


                elif (isinstance(dict1[key], int) or
                      isinstance(dict2[key2], int)):
                    dict1[key2] += value2[0]

                elif (isinstance(dict1[key], str) or
                      isinstance(dict2[key2], str)):
                    dict1[key2] += ', ' + value2[0]
    return dict1
