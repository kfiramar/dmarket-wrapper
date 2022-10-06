'''This module Is used to log the API requests'''
import time
import os
import json
import pprint
from halo import Halo
from parsing import json_fixer
from config import SRC_PATH


def write_content(content, func_name):
    '''Creates a file and loads all the json content into it'''
    fixed_json = []
    file_name = time.strftime(f"{func_name}-%Y-%m-%d_%H:%M:%S.json")
    path_to_file = os.path.join(SRC_PATH, f'../logs/{file_name}')
    fixed_json = json.loads(json_fixer(str(content)))
    with open(path_to_file, "wb") as file:
        file.write((pprint.pformat(fixed_json)).encode('utf-8'))


def log(response, func_name):
    '''logging of an API json with animation wrapping'''
    logging_spinner = Halo(text='Logging API request', spinner='dots', color='green')
    logging_spinner.start()
    write_content(response, func_name)
    logging_spinner.succeed(text="SUCCESSFUL - the API request was logged")
