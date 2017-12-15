import copy
from grids import *

def get_hex(ar):
    """Get hex value of the binary map"""
    current = 0
    val = 8
    ans = ''
    if((len(ar) % 4) != 0):
        return ""
    for i in range(len(ar)):
        current = current + val * ar[i]
        val //= 2
        if(val == 0):
            ans = ans + hex(current)[2:]
            val = 8
            current = 0
    return ans


def generateMapDescriptor(resultMap):
    """Generate map descriptor"""
    temp = copy.copy(resultMap)
    mapDescriptor = [1,1]
    for i in range(len(temp) - 1, -1, -1):
    # for i in range(len(temp)):
        for j in range(len(temp[i])):
            if temp[i][j] == -1:
                mapDescriptor.append(0)
            else:
                mapDescriptor.append(1)
    mapDescriptor += [1,1]
    print (mapDescriptor)
    print (len(mapDescriptor))
    return get_hex(mapDescriptor)


def generateMapDescriptor2(maze):
    """Generate map descriptor 2"""
    length = 0
    ans = []
    for i in range(len(maze) - 1, -1, -1):
    # for i in range(len(maze)):
        for j in range(len(maze[i])):
            if(maze[i][j] == -1):
                continue
            ans.append(maze[i][j])
            length += 1
    while(length % 8 != 0):
        ans.append(0)
        length += 1
    return get_hex(ans)


def main():
    actualMap = [[0 for i in range(15)] for i in range(20)]
    f = open("maps/test.txt", "r")
    for i in range(20):
        for j in range(15):
            r = f.read(1)
            if r == '\n' :
                r = f.read(1)
            if r == '2':
                w = -1
            else:
                w = int(r)
            actualMap[i][j] = w
    print (actualMap)
    print (generateMapDescriptor(actualMap))
    print (generateMapDescriptor2(actualMap))

main()