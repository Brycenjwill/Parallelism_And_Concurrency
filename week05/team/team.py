"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_thread(queue):
    with open("data.txt", "r") as f:
        for line in f:
            queue.put(int(line))
        queue.put(False)
    

# TODO create prime_process function
def prime_process(queue, primes):
    on = True
    while on == True:
        if queue.queue[0] == False:
            on = False
            return
        else:
            item = queue.read()
            if is_prime(item) == True:
                primes.append(item)

        

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    queue = mp.Queue()
    primes = []
    
    # TODO create reading 
    readingThread = threading.Thread(target=read_thread, args=(queue,))
    # TODO create prime processes
    p1 = mp.Process(target=prime_process, args=(queue, primes))
    p2 = mp.Process(target=prime_process, args=(queue, primes))
    p3 = mp.Process(target=prime_process, args=(queue, primes))
    # TODO Start them all
    readingThread.start()
    readingThread.join()
    p1.start()
    p2.start()
    p3.start()
    # TODO wait for them to complete

    p1.join()
    p2.join()
    p3.join()

     

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

