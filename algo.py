from constants import *
from robot import *
from shortestpath import *
from grids import *
from util import *

no_path = []

def hugTheWall(sensors, robot, obstacleMap, prevAction):
    """
    2###
    .###
    1###
    """
    left = get_check_left_transpose(robot.direction)

    """
    ###
    1#2
    ###
    """
    left_transpose = get_side_transpose(robot.direction)

    """
    .1.
    ###
    ###
    ###
    """
    front_transpose = get_movement_transpose(robot.direction)

    """
    ...1
    ###.
    ###.
    ###.
    """

    movement_transpose = get_left_right_transpose(robot.direction)

    forw = [robot.rPos + movement_transpose[0] + 2 * front_transpose[0], robot.cPos + movement_transpose[1] + 2 * front_transpose[1],
    robot.rPos + movement_transpose[2] + 2 * front_transpose[0], robot.cPos + movement_transpose[3] + 2 * front_transpose[1],
    robot.rPos + 2 * front_transpose[0], robot.cPos + 2 * front_transpose[1]]

    if(not is_left_wall(robot.direction, 20, 15, robot.rPos, robot.cPos) and \
    obstacleMap.data[robot.rPos + left[0]][robot.cPos + left[1]] != 1 and \
    obstacleMap.data[robot.rPos + left[2]][robot.cPos + left[3]] != 1 and \
    obstacleMap.data[robot.rPos + left[4]][robot.cPos + left[5]] != 1 and \
    prevAction == FORWARD):
        return TURN_LEFT

    if(is_front_wall(robot.direction, 20, 15, robot.rPos, robot.cPos) or \
    obstacleMap.data[forw[0]][forw[1]] == 1 or \
    obstacleMap.data[forw[2]][forw[3]] == 1 or \
    obstacleMap.data[forw[4]][forw[5]] == 1):
         return TURN_RIGHT
    return FORWARD    

def possibleLeftTurn(moves, upperLeft, left, lefttranspose, obstacleMap, r, c):

    # if(moves == 1):
    if(moves == 1 or moves == 2):
        if(obstacleMap.get_value(r + upperLeft[0], c + upperLeft[1]) == OBSTACLE or
        obstacleMap.get_value(r + left[2], c + left[3]) == OBSTACLE or
        obstacleMap.get_value(r + lefttranspose[0] * 2, c + lefttranspose[1] * 2) == OBSTACLE):
            return False
        else:
            return True
    else:
        return True

def noNameAlgo(sensors, r, c, direction, resultMap, value):
	global no_path
	frontGrid = [[0,-value], [value,0], [0,value], [-value,0]]
	frontCol = c + frontGrid[direction][0]
	frontRow = r + frontGrid[direction][1]
	indexCheck = validate_position(frontRow, frontCol)
	updatedMap = updateResultMap(resultMap)
	currentPosition = [r, c]

	if (checkGrid(GOAL[0], GOAL[1], resultMap)):
		nextNode = getNextGrid(r, c, resultMap, updatedMap, no_path)
		print("Next node: " + str(nextNode))
		if len(nextNode) == 0:
			path = solveShortestPathBFS(updatedMap, r, c, 18, 1, direction, 0)
		else:
			path = solveShortestPathBFS(updatedMap, r, c, nextNode[0], nextNode[1], direction, 1)
		print("Path: " + str(path))
		if len(path) == 0:
			return DO_NOTHING
		elif path[0] == -1:
			no_path.append(nextNode)
			return PATH_NOT_FOUND
		else:
			return processMove(path)
	else:
		path = solveShortestPathBFS(updatedMap, r, c, 1, 13, direction, 0)
		return processMove(path)

def checkGrid(r, c, resultMap):
    #if visited
    if resultMap.data[r][c] != -1: 
        return True
    #if not visited
    return False

def updateResultMap(resultMap):
    row = []
    for i in range(len(resultMap.data)):
        col = []
        for j in range(len(resultMap.data[i])):
            if resultMap.data[i][j] == -1:
                col.append(0)
            else:
                col.append(resultMap.data[i][j])
        row.append(col)
    return row

def processMove(path):
    move = path[0]
    if path[0] == 0:
        return FORWARD
    elif path[0] == 1:
        return TURN_LEFT
    elif path[0] == 2:
        return TURN_RIGHT

def getNextGrid(r, c, resultMap, updatedMap, no_path):
    temp = checkUnexplored(resultMap, updatedMap)
    distance = 10000
    nextGrid = []
    for element in temp:
    	if element in no_path:
    		continue
    	tempDist = calculateDistance([r,c], element)
    	if tempDist <= distance:
    		distance = tempDist
    		nextGrid = element
    return nextGrid


def checkUnexplored(resultMap, updatedMap):
    result = []

    for i in range(0, len(resultMap.data)):
        for j in range (len(resultMap.data[i])-1, -1, -1):
            if resultMap.data[i][j] == -1:
                result.append([i, j])
    return result

def calculateDistance(ar1, ar2):
    x = ar2[0]-ar1[0]
    y = ar2[1]-ar1[1]
    return x**2 + y**2

def checkLoop(actions):
    if(len(actions) <= 1):
        return False
    cur = len(actions) - 1
    secondStart = 0
    for i in range(len(actions) - 2, -1, -1):
        if(actions[i] == actions[cur]):
            secondStart = i
            break
    cur = secondStart
    if(len(actions) - secondStart <= 4):
        return False
    for i in range(len(actions) - 1, secondStart, -1):
        if(actions[i] != actions[cur]):
            return False
        cur -= 1
    print("LOOP LOOP LOOOP LOOPP LOOP LOOP")
    return True

def checkAlignment(sensors, robot, resultMap, wifi):

    movement = get_movement_transpose(robot.direction)
    left_right = get_left_right_transpose(robot.direction)
    one_front = [robot.rPos + left_right[0] + 2 * movement[0], robot.cPos + left_right[1] + 2 * movement[1],
    robot.rPos + 2 * movement[0], robot.cPos + 2 * movement[1]]
    left_side = get_check_left_transpose(robot.direction)
    right_side = get_check_right_transpose(robot.direction)
    alignValue = 0
    
    #Obstacle on left of robot (LM & LB)
    if (is_left_wall(robot.direction, 20, 15, robot.rPos, robot.cPos) or \
    (resultMap.data[robot.rPos + left_side[2]][robot.cPos + left_side[3]] == 1 and resultMap.data[robot.rPos + left_side[0]][robot.cPos + left_side[1]] == 1)):
        wifi.write("l}")
        alignValue = 1
        
    #Front Left & Front Center (Directly infront of Robot)    
    if (is_front_wall(robot.direction, 20, 15, robot.rPos, robot.cPos) or \
    (resultMap.data[one_front[0]][one_front[1]] == 1 and resultMap.data[one_front[2]][one_front[3]] == 1)): 
        wifi.write("k}")
        alignValue = 2
        
    return alignValue

