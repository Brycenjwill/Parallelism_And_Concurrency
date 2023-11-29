"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(lightLock, cleanLock, startTime, cleanedCountQueue, id):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    """
    while time <= start_time + TIME
    try to enter room 
    When entering the room:
    Acquire light lock -> Acquire cleaning lock
    Add to clean_count
    display STARTING_CLEANING_MESSAGE
    take time to clean
    display STOPPING_CLEANING_MESSAGE

    When leaving:
    Release both
    cleaners will each return their clean_count variable
    """

    while time.time() < startTime + 10:

        cleaner_waiting()
        if random.randint(0,1) == 1:
            lightLock.acquire() #Make sure no party is going on
            cleanLock.acquire() #Don't let party goers in
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(id)
            print(STOPPING_CLEANING_MESSAGE)
            lightLock.release() #Let another person in 
            cleanLock.release() #Let party start if thats what happens next
            cleanedCountQueue.put(1) #Add one to cleaned count


def guest(lightLock, cleanLock, startTime, partyCountQueue, guestsCountQueue, id):

    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    """
    while time <= start_time + TIME
    Try to enter room
    When entering the room:
    First person acquires light lock. First person turns on light after acquiring cleaning lock. First person adds one to
    party_count. First person displays STARTING_PARTY_MESSAGE
    Every person will acquire, then release the cleaning lock, which is how they will check that the person in 
    the room before them was a guest and not a cleaner
    When Leaving:
    If guest is the last to leave, release light lock. Last guest displays STOPPING_PARTY_MESSAGE
    guests will each return their party_count variables.
    """
    while time.time() < startTime + 10:
        count = 0
        guest_waiting()

        if random.randint(0,1) == 1: #Try to join party that is ongoing
            cleanLock.acquire()
            cleanLock.release()
            count = partyCountQueue.get() + 1 #Add one to the count of people in the party
            guest_partying(id, count) #Show that another guest is partyinh
            partyCountQueue.put(count)

            #If this is the only guet at this point, end party


        else:
            break #Reset loop if num was 0, so that not everyone is trying to join rather than start party when its time
                #to start the party again
    else:
        lightLock.acquire() #Start party!
        print(STARTING_PARTY_MESSAGE)

        partyCountQueue.put(1) #Add one to the number of people in the party
        count = partyCountQueue.get()
        partyCountQueue.put(count) 
        guest_partying(id, count)
        partyCountQueue.put(1) #Add one to the amount of parties that have happened
        #leave party after partying, by doing nothing here. Then wait again to rejoin. 
    
def main():
    # Start time of the running of the program. 
    start_time = time.time()
    cleanedCountQueue = mp.Queue()
    partyCountQueue = mp.Queue()
    guestsCountQueue = mp.Queue()

    # TODO - add any variables, data structures, processes you need
    lightLock = mp.Lock() #A lock that is used to tell if anyone is in the room at all, if only this lock is acquired then
    #more party members can enter the room
    cleanLock = mp.Lock() #A lock that is used to tell if a cleaner is in the room. No one can enter the room if this lock is acquired
    # TODO - add any arguments to cleaner() and guest() that you need

    #Cleaner Processess
    cleaner1 = mp.Process(target=cleaner, args=(lightLock, cleanLock, start_time, cleanedCountQueue, 1))
    cleaner2 = mp.Process(target=cleaner, args=(lightLock, cleanLock, start_time, cleanedCountQueue, 2))

    guest1 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCountQueue, guestsCountQueue, 1))
    guest2 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCountQueue, guestsCountQueue, 2))
    guest3 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCountQueue, guestsCountQueue, 3))
    guest4 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCountQueue, guestsCountQueue, 4))
    guest5 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCountQueue, guestsCountQueue, 5))

    
    cleaner1.start()
    cleaner2.start()

    guest1.start()
    guest2.start()
    guest3.start()
    guest4.start()
    guest5.start()


    cleaner1.join()
    cleaner2.join()

    guest1.join()
    guest2.start()
    guest3.start()
    guest4.start()
    guest5.start()

    cleaned_count = 0 
    while not cleanedCountQueue.empty(): #Grab all ones from cleanCountQueue
        cleaned_count += cleanedCountQueue.get()

    party_count = 0
    while not partyCountQueue.empty(): #Grab all ones from partyCountQueue
        party_count += partyCountQueue.get()

    #Set cleaned count equal to the returned values of cleaners, gotten from queue
    #Set party count equal to the returned values of party count, gotten from queue
    # Results
    print(f'Room was cleaned {cleaned_count} times, there were {party_count} parties')


if __name__ == '__main__':
    main()

