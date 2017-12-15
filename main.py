import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json
import sched, time
from constants import *
from util import *
from shortestpath import solveShortestPathBFS
import WIFI
from mapdescriptor import *
from grids import *
from robot import *
from algo import *
import sys

IP = '192.168.8.8'
PORT = 8080
"""
0 - unexplored
1 - revealed, empty
2 - revealed, obstacle
3 - robot's body
4 - robot's head
5 - special zone
6 - robot's trail

0 - move forward
1 - turn left
2 - turn right
"""
actualMap = 0 # map from txt file, only for testing purpose
currentMap = 0 # map that will be sent to client simulation
resultMap = 0 # map topology
visited = 0
counter = 0
answer = 0
step_limit = 200
elapsed_time = 0
time_limit = 0
exploration_end = False
shortest_path_flag = False
coverage_limit = 0
steps = 0
robot_status = EXPLORATION
wifi = 0
return_to_base_steps = 0
return_to_base_steps2 = 0
reach_goal_start = 0
algo = 0
earlyTermination = 0
prevAction = FORWARD
tempMap = 0
actionsHistory = []
fixMap = UNEXPLORED
waypoint = []
prevAlign = 0
fwdCounter = 0
finalListSol = []
tempListSol = []

def calculateCoverage():
    """Calculate percentage of map explored"""
    grids_discovered = 0
    for i in range(0, 20):
        for j in range(0, 15):
            grids_discovered += (resultMap.data[i][j] != -1)
    return float(grids_discovered) / 300.0 * 100.0

def update_map():
    """Update the map topology"""
    currentMap.copy_data(resultMap)
    
    # update robot graphics
    currentMap.update_specialzone()
    currentMap.update_robot_graphics(robot.rPos, robot.cPos, robot.direction)
   

class MainHandler(tornado.web.RequestHandler):
    """Class for Python Tornado, for simulator"""
    def get(self):
        self.render("display.html", mazeMap = read_from_file("maps/initialMap.txt"), row = robot.rPos, col = robot.cPos)

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    """Class for Python Tornado, for simulator"""
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        """Method which is run when received message"""
        global time_limit
        global coverage_limit
        global robot_status
        global steps
        global elapsed_time
        global waypoint
        
        incoming_data = json.loads(message)
        data_type = incoming_data["type"]
        
        # first communication, do nothing
        if(data_type == 0):
            self.write_message(json.dumps({"type": 0}))
            return

        # initialization of limit values    
        if(data_type == 1):
            if(incoming_data["coverageLimit"] == ""):
                coverage_limit = 100.0
            else:
                coverage_limit = float(incoming_data["coverageLimit"])
            if(incoming_data["time"] == ""):
                time_limit = 10000
            else:
                time_limit = float(incoming_data["time"])
                print(time_limit)
            #Waypoint Setting (For Simulator)
            if (wifi is None):
                waypoint = [18,13]
                
            if(wifi is not None):
                while (True):
                    received_string = wifi.read()
                    received_string_split = received_string.split("|")
                    print (received_string_split[0])
                    print (received_string_split[1])
                    if (received_string_split[0] == "andr"):
                        wp = received_string_split[1]
                        wp_split = wp.split(",")
                        waypoint.append(int(wp_split[0]))
                        waypoint.append(int(wp_split[1]))
                        wifi.write('l}')
                        break
                    
                while(True):
                    start = wifi.read()
                    start_split = start.split("|")
                    if (start_split[0] == "andr" and start_split[1] == "ex"):
                        wifi.write("i}") #send i to arduino for initialization
                        break
                
            self.write_message(get_new_map())

        if(data_type == 2):
            elapsed_time = float(incoming_data["elapsed_time"])
            steps = int(incoming_data["steps"])
            self.write_message(get_new_map())
        

    def on_close(self):
        print("WebSocket closed")
        
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/websocket', EchoWebSocket),
    ])


def clear_start_goal_zone():
    """return action to arduino and update simulator display"""
    startZone = [[17, 0], [17, 1], [17, 2], [18, 0], [18, 1], [18, 2], [19, 0], [19, 1], [19, 2]]
    endZone = [[0, 12], [0, 13], [0, 14], [1, 12], [1, 13], [1, 14], [2, 12], [2, 13], [2, 14]]
    for i in startZone:
        resultMap.data[i[0]][i[1]] = EMPTY
    for i in endZone:
        resultMap.data[i[0]][i[1]] = EMPTY

def get_new_map():
    global return_to_base_steps
    global return_to_base_steps2
    global robot_status
    global reach_goal_start
    global exploration_end
    global prevAction
    global algo
    global earlyTermination
    global prevAlign
    
    # reading type: 1 for front only, 2 for front + left side, 3 for front + right side, 4 for all
    if(robot_status == EXPLORATION and not exploration_end and earlyTermination == 0):
        if(wifi is not None):
            clear_start_goal_zone()
            # get actions to return to start zone in case WIFI is disconnected
            if(reach_goal_start >= 1):
                returnToStartZone = ""
            else:
                returnToStartZone = ""
            sensors = robot.get_sensors(resultMap, returnToStartZone)
        else:
            sensors = robot.get_sensors_from_simulator(resultMap, actualMap, 4)
        
    if(0 <= robot.rPos <= 2 and 12 <= robot.cPos <= 14 and reach_goal_start == 0):
        reach_goal_start += 1
        
        shift = False
        for w in range(11, -1, -1):
            if(resultMap.get_value(0, w) == OBSTACLE):
                shift = True
                resultMap.set_value(0, w, fixMap)
            else:
                break
        if(shift):
            robot.rPos = 1
    if(17 <= robot.rPos <= 19 and 0 <= robot.cPos <= 2 and reach_goal_start == 1):
        reach_goal_start += 1
        
        shift = False
        for w in range(3, 15):
            if(resultMap.get_value(19, w) == OBSTACLE):
                shift = True
                resultMap.set_value(19, w, fixMap)
            else:
                break
        if(shift):
            robot.rPos = 18

    if(not(calculateCoverage() < coverage_limit and elapsed_time < time_limit)):
        earlyTermination = 1

    if(earlyTermination == 0 and not exploration_end):
        action = None
        if(algo == 0):
            action = hugTheWall(sensors, robot, resultMap, prevAction)
            if(not(reach_goal_start < 2)):
                algo = 1 
            prevAction = action
        elif(algo == 1):
            action = noNameAlgo(sensors, robot.rPos, robot.cPos, robot.direction, resultMap, 5) 
            if(action == DO_NOTHING and robot.rPos == 18 and robot.cPos == 1):
                exploration_end = True
                
        if(wifi is not None):
            prevAlign = checkAlignment(sensors, robot, resultMap, wifi)
             
        process_move(action, True)
      
        if(wifi is not None):
            md1 = generateMapDescriptor(resultMap.data)
            md2 = generateMapDescriptor2(resultMap.data)
            wifi.write("x//" + md1 + "//" + md2 + "}")

    else:
        clear_start_goal_zone()
        if(robot_status == EXPLORATION):
            robot_status = RETURN_TO_START_ZONE
            return_to_base_steps = solveShortestPathBFS(resultMap.data, robot.rPos, robot.cPos, 18, 1, robot.direction, 0)
            solution = get_paths(return_to_base_steps)
            
            #Edit Solution to send to Arduino
            solution = convertSolution(solution)
            
            #After entering Start Zone, do FrontAlign before turning
            solution += "k"
            
            # align robot to always face up
            alignment = alignRobot(solution, robot.direction)
            if not(alignment == "w"):
                solution = solution + alignment
            for i in alignment:
                if not(i == "w"):
                    return_to_base_steps.append(2) 

            print("back to base: " + solution)
            
            if(wifi is not None):
                wifi.write(solution + "}")

        if(robot_status == RETURN_TO_START_ZONE):
            if(len(return_to_base_steps) > 0):
                process_move(return_to_base_steps[0], False)
                return_to_base_steps = return_to_base_steps[1:]
                update_map()
                return json.dumps({"mazeMap": currentMap.data, "row": robot.rPos, "col":robot.cPos, "type": 1, "status": "Returning to start zone", "coverage": calculateCoverage()})
            else:
                # send map descriptor to android    
                md1 = generateMapDescriptor(resultMap.data)
                md2 = generateMapDescriptor2(resultMap.data)
                
                print(md1)
                print(md2)

                if(wifi is not None):
                    wifi.write("x//" + md1 + "//" + md2 + "}")

                robot_status = SHORTEST_PATH

                # check for path
                return_to_base_steps = solveShortestPathBFS(resultMap.data, robot.rPos, robot.cPos, 1, 13, DIR_UP, 0)
                if (return_to_base_steps == [-1]):
                    return json.dumps({"type": 2, "status": "Unable to Find Path"})

                # find path to waypoint
                return_to_base_steps = solveShortestPathBFS(resultMap.data, robot.rPos, robot.cPos, waypoint[0], waypoint[1], DIR_UP, 2)
                solution = get_paths(return_to_base_steps)
                
                center = getRobotCenter(solution, robot.direction, robot.rPos, robot.cPos)
                
                solution = convertSolution(solution)
                print("go to waypoint:" + solution)

                waypoint_direction = getDirection(solution, robot.direction)

                # find path from waypoint to goal
                return_to_base_steps2 = solveShortestPathBFS(resultMap.data, center[0], center[1], 1, 13, waypoint_direction, 0)
                solution2 = get_paths(return_to_base_steps2)
                
                #Edit Solution to send to Arduino
                solution2 = convertSolution(solution2)
                print("waypoint to goal: " + solution2)
                
                solution = solution + solution2
                
                # wait for command from android
                if(wifi is not None):
                    while(True):
                        a = wifi.read()
                        if(a == 'andr|fp'):
                            break

                #Send Solution to Arduino
                if(wifi is not None):
                    wifi.write(solution + "}")
                    
        if(robot_status == SHORTEST_PATH):
            if(len(return_to_base_steps) > 0):
                process_move(return_to_base_steps[0], False)
                return_to_base_steps = return_to_base_steps[1:]
                update_map()
            
            elif (len(return_to_base_steps2) > 0):
                process_move(return_to_base_steps2[0], False)
                return_to_base_steps2 = return_to_base_steps2[1:]
                update_map()

                return json.dumps({"mazeMap": currentMap.data, "row": robot.rPos, "col":robot.cPos, "type": 1, "status": "Shortest Path", "coverage": calculateCoverage()})
                
            else:
                return json.dumps({"type": 3, "status": "Finished"})

    update_map()
    if(robot_status == EXPLORATION):
        return json.dumps({"mazeMap": currentMap.data, "row": robot.rPos, "col":robot.cPos, "type": 1, "status": "Exploration", "coverage": calculateCoverage()})
    elif(robot_status == RETURN_TO_START_ZONE):
        return json.dumps({"mazeMap": currentMap.data, "row": robot.rPos, "col":robot.cPos, "type": 1, "status": "Returning to start zone", "coverage": calculateCoverage()})
    else:
        return json.dumps({"mazeMap": currentMap.data, "row": robot.rPos, "col":robot.cPos, "type": 1, "status": "Shortest Path", "coverage": calculateCoverage()})

def convertSolution(solution):
    global fwdCounter
    global tempListSol
    global finalListSol
    
    tempListSol = list(solution)
    finalListSol = []
    for i in range(len(tempListSol)):
        if (tempListSol[i] == "w"):
            fwdCounter +=1
            if (fwdCounter == 9):
                finalListSol.append("9")
                fwdCounter = 0                       
        else:
            if (fwdCounter != 0):
                finalListSol.append(str(fwdCounter))
                fwdCounter = 0
            finalListSol.append(tempListSol[i])

    finalListSol.append(str(fwdCounter))
    fwdCounter = 0
    solution = "".join(finalListSol) 
    return solution
    
def process_move(move, sendToArduino):
    global actionsHistory

    if(move == FORWARD):
        if(wifi is not None and sendToArduino):
            wifi.write("w}")
        robot.forward()
    elif(move == TURN_RIGHT):
        if(wifi is not None and sendToArduino):
            wifi.write("d}")
        robot.turn_right()
    elif(move == TURN_LEFT):
        if(wifi is not None and sendToArduino):
            wifi.write("a}")
        robot.turn_left()
    actionsHistory.append([robot.rPos, robot.cPos])
    
if __name__ == "__main__":
    exploration_end = False
    # initialize map from text file, all unexplored
    currentMap = Grids(20, 15, True, "maps/initialMap.txt")
    actualMap = Grids(20, 15, True, "maps/week9.txt")
    tempMap = Grids(20, 15, False, -1)
    resultMap = Grids(20, 15, False, -1)
    wifi = None

    simulation = 1 # set to 1 if running simulation from text file
    if(simulation == 0):
        wifi = WIFI.WIFI(IP, PORT)
        wifi.start()

    robot = Robot(18, 1, wifi, 0)
    for i in range(resultMap.row - 3, resultMap.row):
        for j in range(0, 3):
            resultMap.set_value(i, j, 0)
    dfs_visited = [[0 for i in range(15)] for j in range(20)]
    visited = [[0 for j in range(15)] for k in range(20)]
    visited[robot.rPos][robot.cPos] = 1
    
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

