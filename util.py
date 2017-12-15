from constants import *
import json

"""
This file contains various utility functions 
"""

# change the robot's direction to turn right
def turn_right(direction):
    return (direction + 1) % 4

# change the robot's direction to turn left
def turn_left(direction):
    return (direction - 1) % 4

# validate whether the robot still in the valid arena coordinate
def validate_position(row, col):
    if(row >= 1 and row < BOARD_ROW - 1 and col >= 1 and col < BOARD_COL - 1):
        return True
    else:
        return False

# move the robot one step forward towards the current direction
def move_forward(direction, position):
    prev_position = position
    if(direction == DIR_UP):
        position = [position[0] - 1, position[1]]
    elif(direction == DIR_RIGHT):
        position = [position[0], position[1] + 1]
    elif(direction == DIR_DOWN):
        position = [position[0] + 1, position[1]]
    elif(direction == DIR_LEFT):
        position = [position[0], position[1] - 1]

    # validate position, else no movement
    if(validate_position(position[0], position[1])):
        return position
    else:
        return prev_position

# get the transpose for next robot's movement 
def get_movement_transpose(direction):
    if(direction == DIR_UP):
        return [-1, 0]
    elif (direction == DIR_RIGHT):
        return [0, 1]
    elif (direction == DIR_DOWN):
        return [1, 0]
    elif (direction == DIR_LEFT):
        return [0, -1]
    return [0, 0] 

# get the transpose for left and right side of robot
def get_left_right_transpose(direction):
    if(direction == DIR_UP):
        return [0, -1, 0, 1]
    elif(direction == DIR_RIGHT):
        return [-1, 0, 1, 0]
    elif(direction == DIR_DOWN):
        return [0, 1, 0, -1]
    elif(direction == DIR_LEFT):
        return [1, 0, -1, 0]

# sensors for side left and side right
def get_side_transpose(direction):
    if(direction == DIR_UP):
        return [0, -1, 0, 1]
    elif(direction == DIR_RIGHT):
        return [-1, 0, 1, 0]
    elif (direction == DIR_DOWN):
        return [0, 1, 0, -1]
    elif(direction == DIR_LEFT):
        return [1, 0, -1, 0]

# get the transpose for 3 tiles on the upper left of the robot
def getUpperLeft(direction):
    if(direction == DIR_UP):
        return [-2, -2, -3, -2, -4, -2]
    elif(direction == DIR_RIGHT):
        return [-2, 2, -2, 3, -2, 4]
    elif (direction == DIR_DOWN):
        return [2, 2, 3, 2, 4, 2]
    elif(direction == DIR_LEFT):
        return [2, -2, 2, -3, 2, -4]

# get the transpose for tile on the upper right of the robot
def getUpperRight(direction):
    if(direction == DIR_UP):
        return [-2, 2]
    elif(direction == DIR_RIGHT):
        return [2, 2]
    elif (direction == DIR_DOWN):
        return [2, -2]
    elif(direction == DIR_LEFT):
        return [-2, -2]

# get the 3 tiles on the lower left of the robot
def getLowerLeft(direction):
    if(direction == DIR_UP):
        return [1, -3, 1, -4, 1, -5]
    elif(direction == DIR_RIGHT):
        return [-3, -1, -4, -1, -5, -1]
    elif (direction == DIR_DOWN):
        return [-1, 3, -1, 4, -1, 5]
    elif(direction == DIR_LEFT):
        return [3, 1, 4, 1, 5, 1]

# returns transpose to check whether the robot can turn left
def get_check_left_transpose(direction):
    if(direction == DIR_UP):
        return [1, -2, 0, -2, -1, -2]
    elif(direction == DIR_RIGHT):
        return [-2, -1, -2, 0, -2, 1]
    elif(direction == DIR_DOWN):
        return [-1, 2, 0, 2, 1, 2]
    elif(direction == DIR_LEFT):
        return [2, 1, 2, 0, 2, -1]

def get_check_right_transpose(direction):
    if(direction == DIR_UP):
        return [-1, 2, 0, 2, 1, 2]
    elif(direction == DIR_RIGHT):
        return [2, 1, 2, 0, 2, -1]
    elif(direction == DIR_DOWN):
        return [1, -2, 0, -2, -1, 2]
    elif(direction == DIR_LEFT):
        return [-2, -1, -2, 0, -2, 1]
# returns transpose to check whether the robot can turn left
def get_left_sensor_transpose(direction):
    if(direction == DIR_UP):
        return [-1, -1, 1, -1]
    elif(direction == DIR_RIGHT):
        return [-1, 1, -1, -1]
    elif(direction == DIR_DOWN):
        return [1, 1, -1, 1]
    elif(direction == DIR_LEFT):
        return [1, -1, 1, 1]

# check whether the robot is on the right side of the wall
def is_left_wall(direction, r, c, rPos, cPos):
    if(direction == DIR_UP and cPos == 1):
        return True
    if(direction == DIR_RIGHT and rPos == 1):
        return True
    if(direction == DIR_DOWN and cPos == c - 2):
        return True
    if(direction == DIR_LEFT and rPos == r - 2):
        return True
    return False

# check whether the robot is on the left side of the wall
def is_right_wall(direction, r, c, rPos, cPos):
    if(direction == DIR_UP and cPos == c - 2):
        return True
    if(direction == DIR_RIGHT and rPos == r - 2):
        return True
    if(direction == DIR_DOWN and cPos == 1):
        return True
    if(direction == DIR_LEFT and rPos == 1):
        return True
    return False

# check whether the robot is on the left side of the wall
def is_front_wall(direction, r, c, rPos, cPos):
    if(direction == DIR_UP and rPos == 1):
        return True
    if(direction == DIR_RIGHT and cPos == c - 2):
        return True
    if(direction == DIR_DOWN and rPos == r - 2):
        return True
    if(direction == DIR_LEFT and cPos == 1):
        return True
    return False

# reading map from file
def read_actual_map(fileName):
    f = open(fileName)
    lines = f.read().splitlines()
    for i in range(len(lines)):
        lines[i] = list(lines[i])
        for j in range(len(lines[i])):
            lines[i][j] = int(lines[i][j])
    f.close()
    return lines 

# reading map from file
def read_from_file(fileName):
    f = open(fileName)
    lines = f.read().splitlines()
    for i in range(len(lines)):
        lines[i] = list(lines[i])
        for j in range(len(lines[i])):
            lines[i][j] = int(lines[i][j])
            if(lines[i][j] == 0):
                lines[i][j] = -1
    f.close()
    data = json.dumps(lines)
    return data

# convert list of actions into string for arduino
def get_paths(paths):
    solution = ""
    for i in paths:
        if(i == FORWARD):
            solution = solution + "w"
        elif(i == TURN_LEFT):
            solution = solution + "a"
        elif(i == TURN_RIGHT):
            solution = solution + "d"
    return solution

def getDirection(solution, direction):
    for i in solution:
        if(i == 'a'):
            direction = turn_left(direction)
        elif(i == 'd'):
            direction = turn_right(direction)
    return direction

# for robot alignment
def alignRobot(solution, direction):
    direction = getDirection(solution, direction)
    if(direction == DIR_LEFT):
        return "d"
    elif(direction == DIR_RIGHT):
        return "a"
    elif(direction == DIR_UP):
        return "w"
    else:
        return "dd"

def getRobotCenter(solution, direction, rPos, cPos):
    row = rPos
    col = cPos
    curDir = direction
    for i in solution:
        if (curDir == DIR_UP):
            if (i == 'a'):
                curDir = DIR_LEFT
            elif (i == 'd'):
                curDir = DIR_RIGHT
            elif (i == 'w'):
                row -= 1
                
        elif (curDir == DIR_DOWN):
            if (i == 'a'):
                curDir = DIR_RIGHT
            elif (i == 'd'):
                curDir = DIR_LEFT
            elif (i == 'w'):
                row += 1   
                
        elif (curDir == DIR_LEFT):
            if (i == 'a'):
                curDir = DIR_DOWN
            elif (i == 'd'):
                curDir = DIR_UP
            elif (i == 'w'):
                col -= 1              

        elif (curDir == DIR_RIGHT):
            if (i == 'a'):
                curDir = DIR_UP
            elif (i == 'd'):
                curDir = DIR_DOWN
            elif (i == 'w'):
                col += 1 
    center = [row,col]        
    return center