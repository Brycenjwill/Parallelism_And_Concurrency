"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 07 Team Activity

Instructions:

1) Make a copy of your assignment 2 program.  Since you are 
   working in a team, you can decide which assignment 2 program 
   that you will use for the team activity.

2) Convert the program to use a process pool and use 
   apply_async() with a callback function to retrieve data 
   from the Star Wars website.  Each request for data must 
   be a apply_async() call.

3) You can continue to use the Request_Thread() class from 
   assignment 02 that makes the call to the server.

"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    def __init__(self, urlList, iterator, startVal):
      threading.Thread.__init__(self)
      self.urlList = urlList
      self.iterator = iterator
      self.startVal = startVal
      self.returnList = []
                
    def run(self):
        working = True
        while working == True:
            if(self.startVal <= len(self.urlList)-1):
                response = requests.get(self.urlList[self.startVal])
                if response.status_code == 200:
                    response = response.content
                    self.response = json.loads(response)
                    self.returnList.append(self.response["name"])
                    self.startVal += self.iterator
                    global call_count
                    call_count += 1
            else:
                working = False
    def getList(self):
        return self.returnList
    

# TODO Add any functions you need here
def getAll():
    global call_count
    all = requests.get(TOP_API_URL)
    call_count += 1
    all = all.content
    all = json.loads(all)
    
    return all

def getFilm(all):
    request = all["films"]
    film = requests.get(f"{request}6")
    film = film.content
    film = json.loads(film)
    global call_count
    call_count += 1
    return film

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    
    
    
    
    # TODO Retrieve Top API urls
    all = getAll()

    # TODO Retireve Details on film 6
    film = getFilm(all)
    Title = film["title"]
    Director = film["director"]
    Producer = film["producer"]
    Released = film["release_date"]

   #Start changing from here
    Pool = mp.Pool(4)
    char1 = Pool.Request_thread(film["characters"], 5, 0)
    char2 = Request_thread(film["characters"], 5, 1)
    char3 = Request_thread(film["characters"], 5, 2)
    char4 = Request_thread(film["characters"], 5, 3)
    char5 = Request_thread(film["characters"], 5, 4)
    
    plan1 = Request_thread(film["planets"], 2, 0)
    plan2 = Request_thread(film["planets"], 2, 1)

    ship1 = Request_thread(film["starships"], 2, 0)
    ship2 = Request_thread(film["starships"], 2, 1)

    vehicle1 = Request_thread(film["vehicles"], 2, 0)
    vehicle2 = Request_thread(film["vehicles"], 2, 1)

    species1 = Request_thread(film["species"], 3, 0)
    species2 = Request_thread(film["species"], 3, 1)
    species3 = Request_thread(film["species"], 3, 2)

    #Start all
    
    Charecters = char1.getList() + char2.getList() + char3.getList() + char4.getList() + char5.getList()
    Planets = plan1.getList() + plan2.getList()
    Ships = ship1.getList() + ship2.getList()
    vehicles = vehicle1.getList() + vehicle2.getList()
    species = species1.getList() + species2.getList() + species3.getList()

    Charecters.sort()
    Planets.sort()
    Ships.sort()
    vehicles.sort()
    species.sort()

    charString = ",".join(str(e) for e in Charecters)    
    planetString = ",".join(str(e) for e in Planets)
    shipString = ",".join(str(e) for e in Ships)
    vehicleString = ",".join(str(e) for e in vehicles)
    speciesString = ",".join(str(e) for e in species)
    # TODO Display results
        
    log.write("----------------------------------------")
    log.write(f"Title: {Title}")
    log.write(f"Directer: {Director}")
    log.write(f"Producer: {Producer}")
    log.write(f"Released: {Released}")
    log.write()
    log.write(f"Characters: {len(Charecters)}")
    log.write(charString)
    log.write()
    log.write(f"Planets: {len(Planets)}")
    log.write(planetString)
    log.write()
    log.write(f"Starships: {len(Ships)}")
    log.write(shipString)
    log.write()
    log.write(f"Vehicles: {len(vehicles)}")
    log.write(vehicleString)
    log.write()
    log.write(f"Species: {len(species)}")
    log.write(speciesString)
    log.write()
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()