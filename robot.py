import constants
import grids
import WIFI
from util import *


class Robot:
    rPos = 0
    cPos = 0
    wifi = 0
    direction = 0

    def __init__(self, row, column, wifi, direction):
        self.rPos = row
        self.cPos = column
        self.wifi = wifi
        self.direction = direction
    
    def get_sensors(self, data, returnToStartZone):
        """Get sensors reading from Arduino"""
        if((self.rPos == 1 and self.direction == DIR_RIGHT) or (self.cPos == 1 and self.direction == DIR_UP) or\
        (self.rPos == 18 and self.direction == DIR_LEFT) or (self.cPos == 13 and self.direction == DIR_DOWN)):
            reading_type = 3
        elif((self.rPos == 1 and self.direction == DIR_LEFT) or (self.cPos == 1 and self.direction == DIR_DOWN) or\
        (self.rPos == 18 and self.direction == DIR_RIGHT) or (self.cPos == 13 and self.direction == DIR_UP)):
            reading_type = 2
        else:
            reading_type = 4
        print("Waiting for sensors...")
        # send sensors request, and also path to start zone from current position
        # self.wifi.write("hs" + str(reading_type) + "z" + returnToStartZone + "|")
        #self.wifi.write("hs" + str(reading_type) +"|")
        #str_reading = self.wifi.read()
        #str_reading_split = str_reading.split("|")
        while (True):
            str_reading = self.wifi.read()
            str_reading_split = str_reading.split("|")
            if (str_reading_split[0] == "ardu"):
                break;
        str_reading = str_reading_split[1]
        # str_reading = input()
        reading = []
        print("Sensors Received:" + str_reading)
        for i in str_reading:
            reading.append(int(i))
        #self.wifi.write("ao" + str_reading + "|")
        front_transpose = get_movement_transpose(self.direction)
        left_right_transpose = get_left_right_transpose(self.direction)

        # update front left reading
        currentRow = self.rPos + left_right_transpose[0] + front_transpose[0]
        currentCol = self.cPos + left_right_transpose[1] + front_transpose[1]
        if(reading[0] >= 3):    
            for j in range(3):
                currentRow += front_transpose[0]
                currentCol += front_transpose[1]
                #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                data.set_value(currentRow, currentCol, EMPTY)
        else:
            for j in range(reading[0]):
                currentRow += front_transpose[0]
                currentCol += front_transpose[1]
                #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                data.set_value(currentRow, currentCol, EMPTY)
            currentRow += front_transpose[0]
            currentCol += front_transpose[1]
            #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
            data.set_value(currentRow, currentCol, OBSTACLE)

        # update front right reading
        currentRow = self.rPos + left_right_transpose[2] + front_transpose[0]
        currentCol = self.cPos + left_right_transpose[3] + front_transpose[1]
        if(reading[1] >= 2):    
            for j in range(2):
                currentRow += front_transpose[0]
                currentCol += front_transpose[1]
                #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                data.set_value(currentRow, currentCol, EMPTY)
        else:
            for j in range(reading[1]):
                currentRow += front_transpose[0]
                currentCol += front_transpose[1]
                #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                data.set_value(currentRow, currentCol, EMPTY)
            currentRow += front_transpose[0]
            currentCol += front_transpose[1]
            #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
            data.set_value(currentRow, currentCol, OBSTACLE)

        # update left side reading
        if (reading_type == 2 or reading_type == 4):
            left_sensor_transpose = get_left_sensor_transpose(self.direction)
            side_transpose = get_side_transpose(self.direction)
            for i in range(2, 4):
                currentRow = self.rPos + left_sensor_transpose[(i - 2) * 2]
                currentCol = self.cPos + left_sensor_transpose[(i - 2) * 2 + 1]
                if(reading[i] >= 3):    
                    for j in range(3):
                        currentRow += side_transpose[0]
                        currentCol += side_transpose[1]
                        #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                        data.set_value(currentRow, currentCol, EMPTY)
                else:
                    for j in range(reading[i]):
                        currentRow += side_transpose[0]
                        currentCol += side_transpose[1]
                        #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                        data.set_value(currentRow, currentCol, EMPTY)
                    currentRow += side_transpose[0]
                    currentCol += side_transpose[1]
                    #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                    data.set_value(currentRow, currentCol, OBSTACLE)

        # update front middle reading
        for i in range(4, 5):
            currentRow = self.rPos + front_transpose[0]
            currentCol = self.cPos + front_transpose[1]
            if(reading[i] >= 3):    
                for j in range(3):
                    currentRow += front_transpose[0]
                    currentCol += front_transpose[1]
                    #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                    data.set_value(currentRow, currentCol, EMPTY)
            else:
                for j in range(reading[i]):
                    currentRow += front_transpose[0]
                    currentCol += front_transpose[1]
                    #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                    data.set_value(currentRow, currentCol, EMPTY)
                currentRow += front_transpose[0]
                currentCol += front_transpose[1]
                #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                data.set_value(currentRow, currentCol, OBSTACLE)

        # update right side reading
        if (reading_type == 3 or reading_type == 4):
            side_transpose = get_side_transpose(self.direction)
            for i in range(5, 6):
                currentRow = self.rPos + side_transpose[2]
                currentCol = self.cPos + side_transpose[3]
                if(reading[i] >= 3):    
                    for j in range(3):
                        currentRow += side_transpose[2]
                        currentCol += side_transpose[3]
                        #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                        data.set_value(currentRow, currentCol, EMPTY)
                else:
                    for j in range(reading[i]):
                        currentRow += side_transpose[2]
                        currentCol += side_transpose[3]
                        #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                        data.set_value(currentRow, currentCol, EMPTY)
                    currentRow += side_transpose[2]
                    currentCol += side_transpose[3]
                    #if (data.get_value(currentRow, currentCol) == UNEXPLORED):
                    data.set_value(currentRow, currentCol, OBSTACLE)

        sensors = dict()
        for i in range(6):
            if(reading[i] >= 3):
                reading[i] = 100
        sensors['left'] = reading[0]
        sensors['right'] = reading[1]
        sensors['side_left_front'] = reading[2]
        sensors['side_left_middle'] = reading[3]
        sensors['middle'] = reading[4]
        sensors['side_right'] = reading[5]
        return sensors



    def turn_right(self):
        """Robot turns Right"""
        self.direction = (self.direction + 1) % 4
    
    def turn_left(self):
        """Robot turns left"""
        self.direction = (self.direction - 1) % 4

    def forward(self):
        """Robot moves forward"""
        pos = move_forward(self.direction, [self.rPos, self.cPos])
        self.rPos = pos[0]
        self.cPos = pos[1]

    def get_sensors_from_simulator(self, resultMap, actualMap, reading_type):
        """Simulator sensor"""
        sensors = dict()
        transpose = get_movement_transpose(self.direction)
        LRT = get_left_right_transpose(self.direction)

        sensors['left'] = 100
        sensors['middle'] = 100
        sensors['right'] = 100
        sensors['side_left_front'] = 100
        sensors['side_left_middle'] = 100
        sensors['side_right'] = 100
        
        pos = [self.rPos, self.cPos]
        pos[0] += transpose[0]
        pos[1] += transpose[1]

        for i in range(0, 3):
            pos[0] += transpose[0]
            pos[1] += transpose[1]
            if(not (pos[0] >= 0 and pos[0] <= 19 and pos[1] >= 0 and pos[1] <= 14)):
                sensors['middle'] = min(sensors['middle'], i)
                break

            x = pos[0]
            y = pos[1]
            if(actualMap.data[x][y] == 1 and sensors['middle'] == 100):
                sensors['middle'] = i
                resultMap.data[x][y] = 1
            elif sensors['middle'] != 100:
                pass
            else:
                resultMap.data[x][y] = 0

        pos = [self.rPos, self.cPos]
        pos[0] += transpose[0]
        pos[1] += transpose[1]
            
        for i in range(0, 3):
            pos[0] += transpose[0]
            pos[1] += transpose[1]
            if(not (pos[0] >= 0 and pos[0] <= 19 and pos[1] >= 0 and pos[1] <= 14)):
                sensors['left'] = min(sensors['left'], i) 
                sensors['right'] = min(sensors['right'], i)
                break

            x = pos[0]+LRT[0]
            y = pos[1]+LRT[1]
            if(actualMap.data[x][y] == 1 and sensors['left'] == 100):
                sensors['left'] = i
                resultMap.data[x][y] = 1
            elif sensors['left'] != 100:
                pass
            else:
                resultMap.data[x][y] = 0

            if (i < 2):
                x = pos[0]+LRT[2]
                y = pos[1]+LRT[3]
                if(actualMap.data[x][y] == 1 and sensors['right'] == 100):
                    sensors['right'] = i
                    resultMap.data[x][y] = 1
                elif sensors['right'] != 100:
                    pass
                else:
                    resultMap.data[x][y] = 0        


        side_transpose = get_side_transpose(self.direction)
        left_sensor_transpose = get_left_sensor_transpose(self.direction)

        if(reading_type == 2 or reading_type == 4):
            pos = [self.rPos, self.cPos]
            pos[0] += left_sensor_transpose[0]
            pos[1] += left_sensor_transpose[1]
            for i in range(0, 3):
                pos[0] += side_transpose[0]
                pos[1] += side_transpose[1]
                if(not (pos[0] >= 0 and pos[0] <= 19 and pos[1] >= 0 and pos[1] <= 14)):
                    sensors['side_left_front'] = min(sensors['side_left_front'], i) 
                    break
                x = pos[0]
                y = pos[1]
                if(actualMap.data[x][y] == 1 and sensors['side_left_front'] == 100):
                    sensors['side_left_front'] = i
                    resultMap.data[x][y] = 1
                elif sensors['side_left_front'] != 100:
                    pass
                else:
                    resultMap.data[x][y] = 0

            pos = [self.rPos, self.cPos]
            pos[0] += left_sensor_transpose[2]
            pos[1] += left_sensor_transpose[3]
            for i in range(1, 4):
                pos[0] += side_transpose[0]
                pos[1] += side_transpose[1]
                if(not (pos[0] >= 0 and pos[0] <= 19 and pos[1] >= 0 and pos[1] <= 14)):
                    sensors['side_left_middle'] = min(sensors['side_left_middle'], i) 
                    break
                x = pos[0]
                y = pos[1]
                if(actualMap.data[x][y] == 1 and sensors['side_left_middle'] == 100):
                    sensors['side_left_middle'] = i
                    resultMap.data[x][y] = 1
                elif sensors['side_left_middle'] != 100:
                    pass
                else:
                    resultMap.data[x][y] = 0
        
        if(reading_type == 3 or reading_type == 4):
            pos = [self.rPos, self.cPos]
            pos[0] += side_transpose[2]
            pos[1] += side_transpose[3]
            for i in range(0, 4):
                pos[0] += side_transpose[2]
                pos[1] += side_transpose[3]
                if(not (pos[0] >= 0 and pos[0] <= 19 and pos[1] >= 0 and pos[1] <= 14)):
                    sensors['side_right'] = min(sensors['side_right'], i) 
                    break
                x = pos[0]
                y = pos[1]
                if(actualMap.data[x][y] == 1 and sensors['side_right'] == 100):
                    sensors['side_right'] = i
                    resultMap.data[x][y] = 1
                elif sensors['side_right'] != 100:
                    pass
                else:
                    resultMap.data[x][y] = 0
        return sensors
