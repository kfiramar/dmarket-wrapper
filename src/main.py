from Item import Item
from tabulate import tabulate
from Row import Row
import numpy as np
from api_requests import generic_request

response = generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=10000",method='GET')
total = response.json()['Total']
  
# uses parse_json_to_item to parse all the items from json
def parse_json_to_items(json_list):
  items_list = []
  for json in json_list['Items']:
    items_list.append(parse_json_to_item(json=json))
  return items_list
  

# parses a JSON into an item
def parse_json_to_item(json):
  exterior = False
  itemtype = False
  tradelock = False
  unlockDate = False
  
  item = Item(
    AssetID=json['AssetID'],Title=json['Title'],Tradable=json['Tradable'],
    tradeLock=['tradeLock'],MarketPrice=json['Offer']['Price']['Amount'])
  
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
    
# parses items from list(Items) to list(Rows)
def parse_items_to_rows(all_items):
  rows = []
  for item in all_items:
    for row in rows:
      if item.Title == row.title:
        row.count += 1
        break
    else:
      rows.append(Row(title=item.Title,exterior = item.exterior ,marketPrice = item.MarketPrice ,count = 1))
  return rows

#Prints tables with headers and total at the end
def print_table(rows):
  table = [list(vars(rows[0]).keys())]
  columns = len(list(vars(rows[0]).keys()))
  for row in rows:
    table.append(list(vars(row).values())) 
  list_test = list(np.full((columns),''))
  list_test[-1] = total
  table.append(list_test)
  print(tabulate(table))


# main function - it is a cli loop that uses all the other functions
def cli_loop():
    
    all_items = parse_json_to_items(response.json())
    print("Welcome! this is Kfir's DMarket trading CLI! ")
    client_choice = input('\n What would you like to do?\n 1 - View inventory \n 2 - Sell items \n 3 - Buy items \n 4 - Filter inventory for a spesific item \n 9 - To quit \n ')
    while(client_choice != 9):
        
        if client_choice == '1':
            rows = parse_items_to_rows(all_items)
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