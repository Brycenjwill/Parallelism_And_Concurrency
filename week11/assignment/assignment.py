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

def cleaner(lightLock, cleanLock, startTime, cleanedCount, id):
    cleanedCount.value = 0
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

    while time.time() < startTime + TIME:
        cleaner_waiting()
        if lightLock.acquire(block=False) == True: #Make sure no party is going on
            cleanLock.acquire() #Don't let party goers in
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(id)
            print(STOPPING_CLEANING_MESSAGE)
            lightLock.release() #Let another person in 
            cleanLock.release() #Let party start if thats what happens next
            cleanedCount.value =+ 1 #Add one to cleaned count
        else:
            pass


def guest(lightLock, cleanLock, startTime, partyCount, guestCount, id):


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
    while time.time() < startTime + TIME:
        guest_waiting()
        if guestCount.value > 0:
            guestCount.value += 1
            guest_partying(id, guestCount.value)
            guestCount.value -= 1
            if guestCount.value == 0:
                print(STOPPING_PARTY_MESSAGE)
                lightLock.release()
                guestCount.value = 0
                break
        elif id == 1:
            print("Trying to party")
            print(STARTING_PARTY_MESSAGE)
            guestCount.value = 1
            partyCount.value += 1
            guest_partying(id, 1)
            time.sleep(2)
            guestCount.value -= 1
        elif lightLock.acquire(block=False) == False:
            guestCount.value = 2
            print(STOPPING_PARTY_MESSAGE)
            lightLock.release()
            guestCount.value = 0
            break



            


    
def main():
    # Start time of the running of the program. 
    start_time = time.time()
    cleanedCount = mp.Value('i', 0)
    partyCount = mp.Value('i', 0)
    guestCount = mp.Value('i', 0)

    # TODO - add any variables, data structures, processes you need
    lightLock = mp.Lock() #A lock that is used to tell if anyone is in the room at all, if only this lock is acquired then
    #more party members can enter the room
    cleanLock = mp.Lock() #A lock that is used to tell if a cleaner is in the room. No one can enter the room if this lock is acquired
    # TODO - add any arguments to cleaner() and guest() that you need

    #Cleaner Processess
    cleaner1 = mp.Process(target=cleaner, args=(lightLock, cleanLock, start_time, cleanedCount, 1))
    cleaner2 = mp.Process(target=cleaner, args=(lightLock, cleanLock, start_time, cleanedCount, 2))

    guest1 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCount, guestCount, 1))
    guest2 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCount, guestCount, 2))
    guest3 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCount, guestCount, 3))
    guest4 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCount, guestCount, 4))
    guest5 = mp.Process(target=guest, args=(lightLock, cleanLock, start_time, partyCount, guestCount, 5))


    cleaner1.start()
    cleaner2.start()
 
    guest1.start()
    guest2.start()
    guest3.start()
    guest4.start()
    guest5.start()


    while time.time() < start_time + TIME:
        pass
    print("Time out")

    cleaner1.join()
    cleaner2.join()

    guest1.join()
    guest2.join()
    guest3.join()
    guest4.join()
    guest5.join()

    cleaned_count = guestCount.value

    party_count = partyCount.value

    #Set cleaned count equal to the returned values of cleaners, gotten from queue
    #Set party count equal to the returned values of party count, gotten from queue
    # Results
    print(f'Room was cleaned {cleaned_count} times, there were {party_count} parties')


if __name__ == '__main__':
    main()

