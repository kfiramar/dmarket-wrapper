from operator import truediv
import time
import requests

from Item import *
from connection_func import *
from tabulate import tabulate
from Row import *

rootApiUrl = "https://api.dmarket.com"
  
def generic_request(api_url_path,method='GET'):
  headers = create_headers(api_url_path,method=method)
  method_lower = method.lower()
  resp = requests.__getattribute__(method_lower)(rootApiUrl + api_url_path, headers=headers)
  #write_content(resp.json(),method)
  return resp
  
# uses parse_json_to_item to parse all the items from json
def create_items_list(json_list):
  items_list = []
  for json in json_list['Items']:
    items_list.append(parse_json_to_item(json=json))
  return items_list
  
# Creates a file and loads all the API request result into it
def write_content(content,method):
  #f = open(os.path.join(f'',time.strftime(f"{method}_request_%Y-%m-%d_%H:%M:%S"),"x"))
  f = open(time.strftime(f"{method}_request_%Y-%m-%d_%H:%M:%S"),"x")
  f.write(str(content))
  
# parses a JSON into an item
def parse_json_to_item(json):
  
  item = Item(
    AssetID=json['AssetID'],Title=json['Title'],Tradable=json['Tradable'],
    tradeLock=['tradeLock'],MarketPrice=json['Offer']['Price']['Amount'])
    
  exterior = False
  itemtype = False
  tradelock = False
  unlockDate = False
  
  for attribute in json['Attributes']:
    
    if attribute['Name'] == 'exterior':
      item.exterior = attribute['Value']
      exterior = True
      
    elif attribute['Name'] == 'tradeLock':
      item.tradeLock = attribute['Value']
      itemtype = True
      
    elif attribute['Name'] == 'itemType':
      item.itemType = attribute['Value']
      tradelock = True
      
    elif attribute['Name'] == 'unlockDate':
      item.itemType = attribute['Value']
      unlockDate = True
      
    if (exterior and itemtype and tradelock and unlockDate):
      return item
    
    
    
def get_rows(all_items):
  rows = []
  for item in all_items:
    for row in rows:
      if item.Title == row.title:
        row.count += 1
        break
    else:
      rows.append(Row(title=item.Title,exterior = '' ,tradable = '' ,count = 1))
  return rows

def print_table(rows):
  table = [['name','exterior','tradeLock','count']]
  for row in rows:
    temp_row = [row.title,  row.exterior, row.tradeLock, row.count]
    table.append(temp_row)
  print(tabulate(table))


def cli_loop():
    response = generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=10000",method='GET')
    all_items = create_items_list(response.json())
    print("Welcome! this is Kfir's DMarket trading CLI! ")
    client_choice = input('\n What would you like to do?\n 1 - View inventory \n 2 - Sell items \n 3 - Buy items \n 4 - Filter inventory for a spesific item \n 9 - To quit \n ')
    while(client_choice != 9):
        
        if client_choice == '1':
            rows = get_rows(all_items)
            print_table(rows)
            
        elif client_choice == '2':
            print('You choose 2')
            
        elif client_choice == '3':
            print('You choose 3')
            
        elif client_choice == '4':
            print('You choose 4')
            
        elif client_choice == '9':
            exit()
            
        else:
            print(' Wrong input, try again')
            
        client_choice = input('\n What would you like to do?\n 1 - View inventory \n 2 - Sell items \n 3 - Buy items \n 4 - Filter inventory for a spesific item \n 9 - To quit \n ')


if __name__ == '__main__':
  cli_loop()