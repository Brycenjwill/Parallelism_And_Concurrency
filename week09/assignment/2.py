"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

I would have each new created thread initialize with a list containing the path that was taken to get to 
where that thread was started. 

Why would it work?

I would have a separate thread that's sole purpose is to listen/ wait for a response from all the other threads,
and the main function of the program would be waiting for this thread to return a path list, which would be stored
as the path to the finish. So, when one thread reached the end, it would send the path to this listener, and then back
to the main funciton. The listener would then signal to all the other threads to finish.

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED
threads = []

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def endThreads(): #End all threads.
    global threads
    #TODO
    #1 Join all threads
    #2 Reset thread list

    #1
    for thread in threads:
        thread.join()
    #2
    threads = []

def solve_find_end(maze, pos, thread):
    global stop # Whether or not the exit has been found
    if thread == None:
        stop = False

    """ finds the end position using threads.  Nothing is returned """
    global threads #A list of all threads that have been created
    global thread_count #A tally of the number of threads created
    Pos = pos #initialize Pos as the given position
    color = get_color() #Set a unique color that this thread will use.
    temp = []
    while stop == False: #Loop to run while global stop == False
        possibleMoves = maze.get_possible_moves(Pos[0], Pos[1]) #Check how many possible moves there are at current pos   
        if len(possibleMoves) == 1: #If there is only one path from Pos
        #TODO
        #1 Moves current thread along path, storing new postion as Pos. Still True.    
            #1
            Pos = possibleMoves[0] #Set position to where the thread is moving
            maze.move(Pos[0], Pos[1], color) #Move to new position


        elif len(possibleMoves) > 1: #If at an intersection
        #TODO
        #1 Creates len(possibleMoves)-1 new threads, giving each a position from the possibleMoves[!=random(not 0)] 
        #2 Moves current thread to possibleMoves[!=random(not 0)], storing new position as Pos. Still True.            
            2
            for Move in possibleMoves:
                if Move != possibleMoves[len(possibleMoves)-1]: #1
                    thread = threading.Thread(target=solve_find_end, args=(maze, Pos, 1)) #Create new thread
                    threads.append(thread) #Add new thread to global list of threads
                    temp.append(thread)
                    thread_count += 1
                    

                else: #2
                    Pos = Move
                    maze.move(Pos[0], Pos[1], color) 
                    
            
            #Start threads
            for thread in temp:
                thread.start()

            temp = []

        elif len(possibleMoves) == 0: #If at an end
        #TODO
        #1 Checks if at the end of the maze using maze.at_end(Pos). If at end, signal to stop other threads. DONE
        #2 If not at the end, stop the while loop/ break. 
        
            if maze.at_end(Pos[0], Pos[1]) == True: #1 Check if the maze has been solved by this thread...
                stop = True #Signal that it is time for threads to stop
                #print("Threads should stop. (Test)")

            else: #2 Break since at dead end
                break
        else: #IF something went wrong. . .
            print("ERROR")
    #TODO
    #Once the loop is over, return nothing. 
    #1 Have the main thread end the others
    if thread == None: 
        endThreads()
    return
    
                

    

def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze, maze.get_start_pos(), None) #Solve mazew

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()