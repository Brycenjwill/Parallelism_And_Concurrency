"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      self.url = TOP_API_URL
      self.people = self.url + "/people/"
          
    def run(self):
        response = requests.get(TOP_API_URL)
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

      
    

# TODO Add any functions you need here
def getAll():
    all = requests.get(TOP_API_URL)
    
    all = all.content
    all = json.loads(all)
    return all

def getCharecters(all):
    request = all["people"]
    working = True
    charecterList = []
    i = 1
    while(working == True):
      if(i == 17):
          i = 18
      charecters = requests.get(f"{request}{i}")
      
      if(charecters.status_code == 404):
          working = False
      else:
          charecters = charecters.content
          charecters = json.loads(charecters)
          if f"{TOP_API_URL}/films/6/" in charecters["films"]:
              charecterList.append(charecters["name"])
          i+= 1
          
    
    return charecterList
      


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    
    all = getAll()
    charecters = getCharecters(all)
    print(f"Charecters: {len(charecters)}\n {charecters}")
    # TODO Retrieve Top API urls

    # TODO Retireve Details on film 6

    # TODO Display results

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
