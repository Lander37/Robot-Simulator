from util import *
from constants import *

class Grids:
    row = 0
    column = 0
    data = 0
    def __init__(self, row, column, readFromFile, value):
        self.row = row
        self.column = column
        if(readFromFile):
            self.data = read_actual_map(value)
        else:
            # if not reading from file, initialize all grid with value
            self.data = [[value for i in range(column)] for j in range(row)]
    
    def set_value(self, r, c, val):
        """Set the value of a grid"""
        if(not self.check_in_grids(r, c)):
            return
        self.data[r][c] = val
    
    def get_value(self, r, c):
        """Get the value of a grid"""
        if(not self.check_in_grids(r, c)): 
            # return -1
            return OBSTACLE
        return self.data[r][c]
    
    def check_finished(self):
        """Check whether there is any unvisited grid"""
        for i in range(self.row):
            for j in range(self.column):
                if(self.data[i][j] == -1):
                    return False
        return True

    def FreeNode(self, r, c):    
        """Check whether a node is free"""
        neighbours = [[0, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
        for element in neighbours:
            x = r + element[0]
            y = c + element[1]
            # check whether still in the map
            if(x >= 0 and x <= (self.row - 1) and y >= 0 and y <= (self.column - 1)):
                # obstacle, return false 
                if(self.data[x][y] == 1):
                    return False
            else:
                return False
        return True

    def check_in_grids(self, r, c):
        """Function to check whether robot is inside the maze"""
        if(0 <= r < self.row and 0 <= c < self.column):
            return True
        return False

    def copy_data(self, source):
        """ Function to copy maze map"""
        for i in range(self.row):
            for j in range(self.column):
                self.data[i][j] = source.data[i][j]


    def update_robot_graphics(self, r, c, direction):
        """Function to update robot value in the maze"""
        if (direction == DIR_UP):
            for i in range(-1, 2):
                self.data[r-1][c + i] = ROBOT_HEAD
                self.data[r][c + i] = ROBOT_BODY
                self.data[r + 1][c + i] = ROBOT_BODY
        elif(direction == DIR_RIGHT):
            for i in range(-1, 2):
                self.data[r + i][c + 1] = ROBOT_HEAD
                self.data[r + i][c] = ROBOT_BODY
                self.data[r + i][c - 1] = ROBOT_BODY
        elif(direction == DIR_DOWN):
            for i in range(-1, 2):
                self.data[r + 1][c + i] = ROBOT_HEAD
                self.data[r][c + i] = ROBOT_BODY
                self.data[r - 1][c + i] = ROBOT_BODY
        elif(direction == DIR_LEFT):
            for i in range(-1, 2):
                self.data[r + i][c - 1] = ROBOT_HEAD
                self.data[r + i][c] = ROBOT_BODY
                self.data[r + i][c + 1] = ROBOT_BODY
    
    def update_specialzone(self):
        """Function to set start and goal zone value"""
        #start zone
        for i in range(BOARD_ROW-3, BOARD_ROW):
            for j in range(3):
                self.data[i][j] = SPECIAL_ZONE
        
        #goal zone
        for i in range(3):
            for j in range(BOARD_COL-3, BOARD_COL):
                self.data[i][j] = SPECIAL_ZONE
