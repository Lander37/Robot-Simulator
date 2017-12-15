# board size
BOARD_ROW = 20
BOARD_COL = 15

# Robot's direction
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

# Robot's movement
PATH_NOT_FOUND = -2
DO_NOTHING = -1
FORWARD = 0
TURN_LEFT = 1
TURN_RIGHT = 2

# Map description - for client rendering
UNEXPLORED = -1
EMPTY = 0
OBSTACLE = 1
ROBOT_BODY = 2
ROBOT_HEAD = 3
SPECIAL_ZONE = 4
ROBOT_TRAIL = 5

# Robot's status
EXPLORATION = 0
RETURN_TO_START_ZONE = 1
SHORTEST_PATH = 2
FINISHED = 3

# Sensors reading
SFRONT = 1
SLEFT = 2
SRIGHT = 3
SALL = 4

#POSITION
START = [BOARD_ROW-1, 0]
GOAL = [0, BOARD_COL-1]
TOP_LEFT = [0,0]
BOTTOM_RIGHT = [BOARD_ROW-1,BOARD_COL-1]