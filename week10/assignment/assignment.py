"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import time

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def write(shared, sem, to_send):
    i = 0 #Initialize the current buffer index
    while shared[BUFFER_SIZE+1] <= to_send:
        #Write to the buffer as long as current pos has been read
        #Or current pos is uninitialized. 
        sem.acquire() #Check that there is space to write
        #1 Write number to buffer location
        shared[i] = shared[BUFFER_SIZE+1]
        shared[BUFFER_SIZE+1] += 1 #Add one to current sending counter
        i += 1
        if i == BUFFER_SIZE:
            i = 0
    shared[BUFFER_SIZE + 2] = 1 #Tell reader that writer is done writing

def read(shared, sem):
    #Read from buffer until the write process sends message to end
    #Print what is read
    i = 0
    time.sleep(2) #Sleep initially to give write space to work
    while shared[BUFFER_SIZE+4] < BUFFER_SIZE: 
        sem.release() #Release semaphore, telling writer that buffer item
        #has been read
        print(shared[i], end=', ', flush=True)
        shared[BUFFER_SIZE+3] += 1 #Add one to read counter
        i += 1 #Move i up
        if i == BUFFER_SIZE:
            i = 0
        
        if shared[BUFFER_SIZE+2] != 0: #Check if writer is done
          shared[BUFFER_SIZE+4]+= 1

def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))
    shared = smm.ShareableList([0]*(BUFFER_SIZE + 5))
    #print(shared)
    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    sem = mp.Semaphore(BUFFER_SIZE) 

    # TODO - create reader and writer processes
    writer = mp.Process(target=write, args = (shared, sem, items_to_send))
    reader = mp.Process(target=read, args=(shared, sem))

    # TODO - Start the processes and wait for them to finish
    reader.start()
    writer.start()
  
    writer.join()
    reader.join()

    print("") #I added this to clean up the ouput a bit
    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')
    print(f'{shared[BUFFER_SIZE + 3]} values received')
    smm.shutdown()


if __name__ == '__main__':
    main()
