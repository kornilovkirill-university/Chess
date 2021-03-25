from IBoard import *
from typing import List, Union
from IChessman import *


class Board(IBoard):

    def __init__(self):
        self._data: List[List[Union[bool, IChessman]]] = [[False for i in range(8)] for j in range(8)]
        self._cells_info = False
        self._killed_chessmen = []
        self.clearCellsInfo()

    def get(self) -> List[List[Union[bool, IChessman]]]:
        return [row[:] for row in self._data]

    def setCellValue(self, x, y, value: IChessman):
        self._data[y][x] = value
        return self

    def getCellValue(self, x, y) -> Union[IChessman, bool]:
        if x < 0 or y < 0:
            raise IndexError
        return self._data[y][x]

    def clearCell(self, x, y):
        self._data[y][x] = False
        return self

    def getChessmanPosition(self, chessman: IChessman):
        for y in range(len(self._data)):
            row = self._data[y]
            for x in range(len(row)):
                value = row[x]
                if value == chessman:
                    return {'x': x, 'y': y}
        return False

    def getChessmanTypePosition(self, chessman_type, color=-1):
        for y in range(len(self._data)):
            row = self._data[y]
            for x in range(len(row)):
                value = row[x]
                if isinstance(value, chessman_type):
                    if color != -1:
                        if value.getColor() != color:
                            continue
                    return {'x': x, 'y': y}
        return False

    def setData(self, data: List[List[Union[IChessman, bool]]] = []):
        self._data = [row[:] for row in data]

    def addKilledChessman(self, chessman: IChessman):
        self._killed_chessmen.append(chessman)

    def getKilledChessmen(self):
        result = []
        for item in self._killed_chessmen:
            result.append(item)
        return result

    def removeChessmanFromKilled(self, chessman: IChessman):
        new_arr = []
        for item in self._killed_chessmen:
            if chessman != item:
                new_arr.append(item)
        self._killed_chessmen = new_arr


###### IT IS BETTER THAT MOVE DOWN FUNCTIONS TO ANOTHER CLASS, FOR EXAMPLE "VIEW"

    def render(self):
        def buildRow(y):
            row = self._data[y]
            res = str(y + 1) + "|"
            for x in range(len(row)):
                el = row[x]
                info = self.getCellInfo(x, y)
                pic = el.getPicture() if el else " "
                res = res + info["info1"] + pic + info["info2"] + "|"
            return res

        print("   A   B   C   D   E   F   G   H  ")
        for i in range(8):
            print(" +---+---+---+---+---+---+---+---+")
            print(buildRow(7 - i))
        print(" +---+---+---+---+---+---+---+---+")

    def clearCellsInfo(self):
        self._cells_info = [[{"info1": " ", "info2": " "} for i in range(8)] for j in range(8)]

    def setCellInfo(self, x, y, info1=False, info2=False):
        if x < 0 or y < 0:
            raise IndexError
        info = self.getCellInfo(x, y)
        info = info if info else {"info1": " ", "info2": " "}
        info["info1"] = info1 if info1 else info["info1"]
        info["info2"] = info2 if info2 else info["info2"]
        self._cells_info[y][x] = info

    def getCellInfo(self, x, y):
        if x < 0 or y < 0:
            raise IndexError
        return self._cells_info[y][x]
