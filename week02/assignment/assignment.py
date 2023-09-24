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
    def __init__(self, urlList, iterator, startVal, ):
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
    return film

def getCharecters(film,iterator, startVal):
    global call_count
    charecterList = []
    charURLs = film["characters"]
    charLen = range(len(charURLs))
    i = iterator
    while i < charLen:
        payload = requests.get(f"{charURLs[i]}")
        charecters = payload.content
        charecters = json.loads(charecters)
        charecterList.append(charecters['name'])
        call_count += 1
        i += iterator

    return charecterList

def getPlanets(film):
    global call_count
    planetList = []
    planetURLs = film["planets"]
    planetLen = range(len(planetURLs))
    for i in planetLen:
        payload = requests.get(f"{planetURLs[i]}")
        planets = payload.content
        planets = json.loads(planets)
        planetList.append(planets["name"])
        call_count += 1
    return planetList

def getStarships(film):
    global call_count
    shipList = []
    shipURLs = film["starships"]
    shipLen = range(len(shipURLs))
    for i in shipLen:
        payload = requests.get(f"{shipURLs[i]}")
        ships = payload.content
        ships = json.loads(ships)
        shipList.append(ships["name"])
        call_count += 1
    return shipList

def getVehicles(film):
    global call_count
    vehicleList = []
    vehicleURLs = film["vehicles"]
    vehicleLen = range(len(vehicleURLs))
    for i in vehicleLen:
        payload = requests.get(f"{vehicleURLs[i]}")
        vehicles = payload.content
        vehicles = json.loads(vehicles)
        vehicleList.append(vehicles["name"])
        call_count += 1
    return vehicleList

def getStarships(film):
    global call_count
    shipList = []
    shipURLs = film["starships"]
    shipLen = range(len(shipURLs))
    for i in shipLen:
        payload = requests.get(f"{shipURLs[i]}")
        ships = payload.content
        ships = json.loads(ships)
        shipList.append(ships["name"])
        call_count += 1
    return shipList

def getSpecies(film):
    global call_count
    speciesList = []
    speciesURLs = film["species"]
    speciesLen = range(len(speciesURLs))
    for i in speciesLen:
        payload = requests.get(f"{speciesURLs[i]}")
        speciess = payload.content
        speciess = json.loads(speciess)
        speciesList.append(speciess["name"])
        call_count += 1
    return speciesList

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

    char1 = Request_thread(film["characters"], 4, 0)
    char2 = Request_thread(film["characters"], 4, 1)
    
    plan1 = Request_thread(film["planets"], 4, 0)
    plan2 = Request_thread(film["planets"], 4, 0)
    char1.start()
    char2.start()
    
    plan1.start()
    plan2.start()

    char1.join()
    char2.join()

    plan1.join()
    plan2.join()
    
    Charecters = char1.getList() + char2.getList() 
    Planets = plan1.getList() + plan2.getList()

    #Charecters = getCharecters(film)
    Charecters.sort()
    Planets.sort()

    
    Ships = getStarships(film)
    Ships.sort()
    vehicles = getVehicles(film)
    vehicles.sort()
    species = getSpecies(film)
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
