"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: <Add name here>

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
SLOW_SPEED = 100
FAST_SPEED = 1
speed = SLOW_SPEED

# TODO add any functions



def solve_path(maze, Path, pos):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
    # TODO start add code here
    possibleMoves = maze.get_possible_moves(pos[0], pos[1]) #Check how many possible moves there are
    while len(possibleMoves) >= 1:
        possibleMoves = maze.get_possible_moves(pos[0], pos[1]) #Check how many possible moves there are
        if maze.at_end(pos[0], pos[1]) == True: #If not at exit. . .
            return Path

        if maze.at_end(pos[0], pos[1]) != True: #If not at exit. . .
            if len(possibleMoves) >= 1: #Logic for when not at end of Path
                Path.append(possibleMoves[0]) #Add move taken to Path
                pos = possibleMoves[0]
                maze.move(possibleMoves[0][0], possibleMoves[0][1], (0,0,255)) #Move to next square

    #When at a dead end...
    ran = len(Path) - 1
    for i in range(0, len(Path)-1): #Loop through the Path list backwards
        index = i
        position = Path[ran-index]
        if len(maze.get_possible_moves(position[0], position[1])) >= 1: #Check to make sure position in loop isnt an intersection. . .
            solve_path(maze, Path, position)
            return Path
            
        else:
            maze.restore(position[0], position[1])
            Path.pop()






def get_path(log, filename):
    """ Do not change this function """
    #  'Maze: Press "q" to quit, "1" slow drawing, "2" faster drawing, "p" to play again'
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze, [[0,1]], [0,1],)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()