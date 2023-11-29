"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Brycen Williams
Purpose: Process Task Files

Instructions:  See I-Learn

TODO
Grade Reasoning:
I wrote that this program meets the requirements, as it creates a pool, and uses apply_async and callbacks to process each task file by type. I also added
information below on why I decided to use the pool count that I used. 

Pool Size Reasoning:

Pool Sizes: I decided to use 1/2 the number of cores on the PC as the pool count for every pool. I tested this on two computers to come to this result. 
It wasn'tsuprising that, in accordance with Amdahl's Law, once I went over a certain threshold of 2x the core count, that the time to process stopped 
getting shorter. Interestingly, once I went far enough over this pool count for any of the pools the time for the program to finish started going up 
significantly.




#To do. . .
1st: Define the functions that will be run via asyncronous processing. DONE
2nd: Define the processes (async) that will run these functions. DONE
3rd: Test program until complete. DONE

"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = [] 
result_words = []
result_upper = []
result_sums = []
result_names = []


#A glopal used for pool count based on your cpus core count 
poolCount = int(mp.cpu_count()/2) 


def log_primes(result): #Add result on callback to appropriate list
    result_primes.append(result)
    
def log_word(result): #Add result on callback to appropriate list
    result_words.append(result)

def log_upper(result): #Add result on callback to appropriate list
    result_upper.append(result)

def log_sums(result): #Add result on callback to appropriate list
    result_sums.append(result)

def log_name(result): #Add result on callback to appropriate list
    result_names.append(result)

def is_prime(n: int):
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
 
def task_prime(value): #Done
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    isPrime = is_prime(value)
    if isPrime == True:
        return f"{value} is prime."
    else:
        return f"{value} is not prime."

def task_word(word): #Done
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt") as File:
        words = File.read()#Should check if a given word is in the word file
        if word in words:
            return f"{word} found. "
        else:
            return f"{word} not found. "


def task_upper(text): #Done
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f"{text} ==> {text.upper()}. "

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    print("uh")
    total = 0
    for i in range(start_value, end_value+1): #Not sure if this needs to include the end value in calculations
        total += i
    return f"Sum of {start_value:,} to {end_value:,} = {total:,} "

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    request = requests.get(url)
    if request.status_code == 200: #Check to make sure that the request went through/found a result
        response = json.loads(request.content)
        name = response["name"]
        return f"{url} has name {name}. "
    else:
        return f"{url} had an error receiving the information. "



def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    prime_pool = mp.Pool(poolCount)
    word_pool = mp.Pool(poolCount)
    upper_pool = mp.Pool(poolCount)
    sum_pool = mp.Pool(poolCount)
    name_pool = mp.Pool(poolCount*4)
    # TODO you can change the following
    # TODO start and wait pools
    
    count = 0
    task_files = glob.glob("*.task") #Get all files in directory with ending of .task
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        #print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME: #Change each of these ifs to start a pool instead
            prime_pool.apply_async(task_prime, args=(task['value'],), callback = log_primes)
        elif task_type == TYPE_WORD:
            word_pool.apply_async(task_word, args=(task['word'],), callback = log_word)
        elif task_type == TYPE_UPPER:
            upper_pool.apply_async(task_upper, args=(task['text'],), callback = log_upper)
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(task_sum, args=(task['start'],task["end"]), callback= log_sums)
        elif task_type == TYPE_NAME:
            name_pool.apply_async(task_name, args=(task['url'],), callback = log_name)
        else:
            log.write(f'Error: unknown task type {task_type}')

    prime_pool.close()
    word_pool.close()
    upper_pool.close()
    sum_pool.close()
    name_pool.close() 

    prime_pool.join()
    word_pool.join()
    upper_pool.join()
    sum_pool.join()
    name_pool.join() 

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
