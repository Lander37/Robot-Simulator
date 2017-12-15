import copy
def get_hex(ar):
    """Get hex value of the binary map"""
    current = 0
    val = 8
    ans = ''
    if(len(ar) % 4 != 0):
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
    while(length % 4 != 0):
        ans.append(0)
        length += 1
    return get_hex(ans)

def descriptor1_to_map(f):
    """Translate map descriptor 1 to maze map"""
    print("descriptor 1")
    descriptor_binary = ''
    for i in range (len(f)):
        descriptor_binary += hexToBinary(f[i])
    
    for i in range(len(descriptor_binary[2:-2])):
        if i % 15 == 0:
            print()
        print(descriptor_binary[i+2], end="")
    return descriptor_binary[2:-2]

def descriptor2_to_map(f1, f2):
    """Translate map descriptor 2 to maze map"""
    descriptor1Map = descriptor1_to_map(f1)
    descriptor_binary = ''
    for i in range (len(f2)):
        descriptor_binary += hexToBinary(f2[i])
    print()
    print("descriptor 2")
    index = 0
    for i in range(300):
        if i % 15 == 0:
            print()
        if int(descriptor1Map[i]) == 0:
            print(2,end="")
        else:
            print(descriptor_binary[index], end = "")
            index += 1

def hexToBinary(hex):
    """Translate hex to binary"""
    binary = bin(int(hex, 16))[2:]
    result = ''
    for i in range(4 - len(binary)):
        result += '0'
    result += binary 
    return result
