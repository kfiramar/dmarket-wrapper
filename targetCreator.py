import json
from datetime import datetime
from nacl.bindings import crypto_sign
import requests
import time
from Item import *
from connection_func import *


# change url to prod
rootApiUrl = "https://api.dmarket.com"



  
def generic_request(api_url_path,method='GET'):
  headers = create_headers(api_url_path,method=method)
  method_lower = method.lower()
  resp = requests.__getattribute__(method_lower)(rootApiUrl + api_url_path, headers=headers)
  create_items_list(resp.json())
  write_content(resp.json(),method)
  
def create_items_list(json_list):
  items_list = []
  for json in json_list['Items']:
    print('\n\n\n\n\n\n')
    print('worked!')
    items_list += parse_json_to_item(json=json)
    print('\n\n\n\n\n\n')
  return items_list
  

def write_content(content,method):
  filename = time.strftime(f"{method}_request_%Y-%m-%d_%H:%M:%S")
  f = open(f'./requests_content/{filename}',"x")
  f.write(str(content))
  
  
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
      break




def main():
  print("Welcome! this is Kfir's DMarket trading CLI! ")
  client_choice = input('\n What would you like to do?\n 1 - View inventory \n 2 - Sell items \n 3 - Buy items \n 4 - Filter inventory for a spesific item \n 9 - To quit \n ')
  while(client_choice != 9):
  
    if client_choice == '1':
      print('You choose 1')
      
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
  #main()
  generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=3",method='GET')