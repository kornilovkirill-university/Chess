import math


def isPositionInArray(position, array):
    for row in array:
        if "x" not in row or "y" not in row:
            continue
        if position["x"] == row["x"] and position["y"] == row["y"]:
            return True
    return False


def getLinePositionsBetweenPositions(position_from, position_to):
    delta_x = int(math.fabs(position_to["x"] - position_from["x"]))
    delta_y = int(math.fabs(position_to["x"] - position_from["x"]))
    if delta_x != delta_y and position_from["x"] != position_to["x"] and position_from["y"] != position_to["y"]:
        return False
    sign_x = 1 if position_to["x"] > position_from["x"] else -1
    sign_y = 1 if position_to["y"] > position_from["y"] else -1
    result = []
    for i in range(1, delta_x):
        x = position_from["x"]+sign_x*i
        y = position_from["y"]+sign_y*i
        result.append({"x": x, "y": y})
    return result


def parseCellPosStr(s):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    nums = ['1', '2', '3', '4', '5', '6', '7', '8']
    if len(s) != 2:
        raise ValueError
    return {"x": letters.index(s[0:1].upper()), "y": nums.index(s[1:])}


def secureFunc(func, error_message=False):
    def safeFunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return error_message
    return safeFunc


def circularList(array):
    def getItem(num):
        lastIndex = len(array)-1
        while num > lastIndex:
            num = num - lastIndex -1
        return array[num]
    return getItem
