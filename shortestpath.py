import time

class Node:
    def __init__(self, reach, obstacle, number, position):
        self.reach = reach
        self.obstacle = obstacle
        self.number = number
        self.position = position

def getNodePosition(mazeNodes, node):
    """Returns the node position in the maze map [row, column]"""
    for element in mazeNodes:
        for inside in element:
            if inside.number == node:
                return inside.position

def getNodeObstacle(mazeNodes, node):
    """Returns the node obstacle in the maze map [row, column]"""
    for element in mazeNodes:
        for inside in element:
            if inside.number == node:
                return inside.obstacle
            
def checkNode(mazeMap, nodeX, nodeY):
    """Checks whether a node can be visited or not"""
    nodeValue = []
    neighbours = [[0, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
    # Add neighbours
    for element in neighbours:
        x = nodeX + element[0]
        y = nodeY + element[1]
        if x in range(0,20) and y in range(0,15):
            nodeValue.append(mazeMap[x][y])
        
    nodeValueSum = 0
    
    for element in nodeValue:
        if element == -1 or element == 1:
            return 1
    return 0

def checkObstacle(mazeMap, nodeX, nodeY):
    """Checks whether a node is obstacle or not"""
    
    if mazeMap[nodeX][nodeY] == 1:
        return 1
    return 0
        
def mapToNodes(mazeMap):
    """Translate maze map into maze nodes"""
    mazeNodes = []
    counter = 0
    for i in range (0, len(mazeMap)):
        row = []
        for j in range (0, len(mazeMap[i])):
            row.append(Node(checkNode(mazeMap, i, j), checkObstacle(mazeMap, i, j), counter, [i, j]))
            counter += 1
        mazeNodes.append(row)
    return mazeNodes
            
def getPossibleMove(mazeNodes, x, y, graph):
    """Get the possible move from one node to its neighbour"""
    #UP     : 0, -1
    #RIGHT  : 1, 0
    #DOWN   : 0, 1
    #LEFT   : -1, 0
    possibleMoves = []

    try:
        if y-1 <= 0:
            pass
        elif mazeNodes[x][y-1].reach == 0:
            possibleMoves.append(mazeNodes[x][y-1].number)
    except IndexError:
        pass

    try:
        if x+1 >= 19:
            pass                               
        elif mazeNodes[x+1][y].reach == 0:
            possibleMoves.append(mazeNodes[x+1][y].number)
    except IndexError:
        pass
    
    try: 
        if y+1 >= 14:     
            pass                                     
        if mazeNodes[x][y+1].reach == 0:
            possibleMoves.append(mazeNodes[x][y+1].number)
    except IndexError:
        pass
    
    try:
        if x-1 <= 0:
            pass
        elif mazeNodes[x-1][y].reach == 0:
            possibleMoves.append(mazeNodes[x-1][y].number)
    except IndexError:
        pass

    return possibleMoves
    
def generateGraph(mazeNodes):
    """Generate the graph of the maze"""
    graph = dict()
    for i in range(len(mazeNodes)):
        for j in range(len(mazeNodes[i])):
            moveList = getPossibleMove(mazeNodes, i, j, graph)
            graph[mazeNodes[i][j].number] = moveList
    return graph
    
def BFS(graph, start, goal, explore, mazeNodes):
    """Breadth-First Search"""
    queue = []
    queue.append([start])

    while queue:
        path = queue.pop(0)
        node = path[-1]

        grids = get_9_grids(node)
        near_wall = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,29,30,44,45,59,60,74,75,89,90,104,105,119,120,134,135,149,150,164,165,179,180,194,195,209,210,224,225,239,240,254,255,269,270,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299]

        if node == goal and node not in near_wall:
            return path
        elif explore == 1 and goal in grids and node not in near_wall:
            return path

        for child in graph[node]:
            if child in near_wall:
                continue
            checker = 0
            for element in queue:
                if child in element:
                    checker = 1
                    break
                else:
                    continue
            if child in path:
                checker = 1
            if checker == 0:
                nextPath = list(path)
                nextPath.append(child)
                queue.append(nextPath)

    queue = []
    queue.append([start])

    while queue:
        path = queue.pop(0)
        node = path[-1]

        grids = get_9_grids(node)
        can_see = get_view(node, mazeNodes)
        near_wall = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,29,30,44,45,59,60,74,75,89,90,104,105,119,120,134,135,149,150,164,165,179,180,194,195,209,210,224,225,239,240,254,255,269,270,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299]
    
        if explore == 1 and goal in can_see and node not in near_wall:
            path.append(1000)
            return path
        elif explore == 2 and goal in grids and node not in near_wall:
        	return path

        for child in graph[node]:
            checker = 0
            for element in queue:
                if child in element:
                    checker = 1
                    break
                else:
                    continue
            if child in path:
                checker = 1
            if checker == 0:
                nextPath = list(path)
                nextPath.append(child)
                queue.append(nextPath)

def get_9_grids(node):
    grids = []
    top = [i for i in range(1, 14)]
    left = [i for i in range(15, 285, 15)]
    bottom = [i for i in range(286, 299)]
    right = [i for i in range(29, 299, 15)]
    if node in top:
        transpose = [-1, 0, 1, 14, 15, 16]
    elif node in left:
        transpose = [-15,-14, 0 , 1, 15, 16]
    elif node in bottom:
        transpose = [-16, -15, -14, -1, 0, 1]
    elif node in right:
        transpose = [-16, -15, -1, 0, 14, 15]
    elif node == 0:
        transpose = [0, 1, 15, 16]
    elif node == 14:
        transpose = [-1, 0, 14, 15]
    elif node == 285:
        transpose = [-15, -14, 0, 1]
    elif node == 299:
        transpose = [-16, -15, -1, 0]
    else:
        transpose = [-16, -15, -14, -1, 0, 1, 14, 15, 16]
    for i in transpose:
        temp_num = node + i
        grids.append(temp_num)
    return grids

def get_view(node, mazeNodes):
    grids = []
    top = [i for i in range(0, 15)]
    left = [i for i in range(0, 300, 15)]
    bottom = [i for i in range(285, 300)]
    right = [i for i in range(14, 314, 15)]

    transpose_view_top = -15
    transpose_view_left = -1
    transpose_view_bottom = 15
    transpose_view_right = 1

    for i in range(-1, 2):
        wall = 0
        for j in range(0, 5):
            temp_num = node + transpose_view_top * j + i
            if temp_num in top or getNodeObstacle(mazeNodes, temp_num):
                wall = 1
                break
            if j > 1:
                grids.append(temp_num)
        if wall == 1:
            continue

    for i in range(-15, 30, 15):
        wall = 0
        for j in range(0, 5):
            temp_num = node + transpose_view_left * j + i
            if temp_num in left or getNodeObstacle(mazeNodes, temp_num):
                wall = 1
                break
            if j > 1:
                grids.append(temp_num)
        if wall == 1:
            continue

    for i in range(-1, 2):
        wall = 0
        for j in range(0, 5):
            temp_num = node + transpose_view_bottom * j + i
            if temp_num in bottom or getNodeObstacle(mazeNodes, temp_num):
                wall = 1
                break
            if j > 1:
                grids.append(temp_num)
        if wall == 1:
            continue

    for i in range(-15, 30, 15):
        wall = 0
        for j in range(0, 5):
            temp_num = node + transpose_view_right * j + i
            if temp_num in right or getNodeObstacle(mazeNodes, temp_num):
                wall = 1
                break
            if j > 1:
                grids.append(temp_num)
        if wall == 1:
            continue

    return grids

def getMove(mazeNodes, node1, node2):
    """Returns the move (left, up, right, down)"""
    try:
        availableMoves = [[-1,0], [0,1], [1,0], [0,-1]]
        node1Position = getNodePosition(mazeNodes, node1)
        node2Position = getNodePosition(mazeNodes, node2)
        move = []
        for i in range(2):
            move.append(node2Position[i]-node1Position[i])
        robotMove = availableMoves.index(move)
        return robotMove
    except ValueError:
        return -1

def getRealMove(move, robotHead):
    """Returns the actual robot movement"""
    value = move - robotHead
    if value == 1 or value == -3:
        return [2,0,(robotHead+1)%4]
    elif value == -1 or value == 3:
        return [1,0, (robotHead-1)%4]
    elif value == 2 or value == -2:
        return [2,2,0, (robotHead+2)%4]
    elif value == 0:
        return [0, robotHead]

def pathToMoves(mazeNodes, path, robotHead):
    """Returns the complete movement for the robot"""
    realMove = []
    
    for i in range(len(path)-1):
        if path[i+1] == 1000:
            robotMove = [2,2,2,(robotHead-1)%4]
        else:
            robotMove = getMove(mazeNodes, path[i], path[i+1])
            robotMove = getRealMove(robotMove, robotHead)
        realMove = realMove + robotMove[0:-1]
        robotHead = robotMove[-1]

    return realMove
    
def solveShortestPathBFS(mazeMap, startRow, startCol, endRow, endCol, direction, explore):
    """Solve the shortest path problem"""
    # set start and goal zone to be always empty
    neighbours = [[0, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
    nodeX = 18
    nodeY = 1
    for element in neighbours:
        x = nodeX + element[0]
        y = nodeY + element[1]
        mazeMap[x][y] = 0

    nodeX = 1
    nodeY = 13
    for element in neighbours:
        x = nodeX + element[0]
        y = nodeY + element[1]
        mazeMap[x][y] = 0        
    
    # if(checkNode(mazeMap, endRow, endCol)):
    #     return []

    # for i in mazeMap:
    #     print(i)
    mazeNodes = mapToNodes(mazeMap)
    mazeGraph = generateGraph(mazeNodes)
    height = len(mazeMap)
    width = len(mazeMap[0])
    start = mazeNodes[startRow][startCol].number
    goal = mazeNodes[endRow][endCol].number

    print(mazeMap)
    path = BFS(mazeGraph, start, goal, explore, mazeNodes)
    if path is None:
        return [-1]
    realMove = pathToMoves(mazeNodes, path, direction)
    for key in mazeGraph:
        mazeGraph[key] = sorted(mazeGraph[key])
    path2 = BFS(mazeGraph, start, goal, explore, mazeNodes)
    realMove2 = pathToMoves(mazeNodes, path2, direction)
    if len(realMove2) <= len(realMove):
        return realMove2
    else:
        return realMove