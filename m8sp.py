import requests
from collections import defaultdict

def getData()->list:
  '''
  Returns list with NBA players Names and Associated heights 
  '''
  r = requests.get('https://mach-eight.uc.r.appspot.com')
  return r.json()['values']

def transform2Dict(data:list)->dict:
  '''
  returns a dictionary with heights as keys to allow hashing and constant access O(1)
  '''
  #using defaultdict to avoid key error
  players_height = defaultdict(list)
  #Create a Hashtable with heigths (in inches) as keys and full name of players with that height as values
  for player in data:
    height = int(player['h_in'])
    players_height[height].append(player['first_name']+" "+player['last_name'])

  return players_height

#Search using list comprehension
def searchPair(players_height:dict, target:int)->list:
  '''
  Returns a list of all pairs of players whose height in inches adds up to the integer target passed as argument

  Args:
    * players_height (dict) : dictionary with heights as keys to allow hashing and constant access O(1)
    * target (int) : The target sum in inches 
  Returns:
    * list : all pairs of players whose height in inches adds up to the integer target
  '''
  return [(p_one, p_two)  #tuple pair of players
        for height in players_height  
            if target - height in players_height
                for p_two in players_height[target - height]
                    for p_one in players_height[height]
                        if p_one < p_two]

def printResult(data:list):
  '''
  Prints the list passed as argument in the console using the requested format
  '''
  if len(data)>1:
    for val in data:
      print(f'- {val[0]: <25}\t{val[1]}')
  else:
      print(f'No matches found')

def getPairs():
  '''
  Function to get a list of all pairs of players whose height in inches adds up to an integer target
  '''
  data = transform2Dict(getData())
  mn = min(data)*2
  mx = max(data)*2
  while 1:
        try:
            target = int(input("Insert target sum: "))
            #If target is not in appropriate range no need to search
            if target < mn or target > mx:
              print(f'No matches found')
              continue
            results = searchPair(data,target)
            printResult(results)
        except ValueError:
            break 
  

if __name__ == "__main__":
    getPairs()
