from IBoard import *


class Move:

    def __init__(self, x, y, limit=1, can_kill=True):
        self._vector = {"x": x, "y": y}
        self._limit = limit  # max steps count
        self._can_kill = can_kill

    def check(self, board: IBoard, current_x, current_y, new_x, new_y):
        vec = self._vector
        return self._deepCheck(board, current_x+vec["x"], current_y+vec["y"], new_x, new_y, 1)

    def getPossiblePositions(self, board: IBoard, current_x, current_y):
        vec = self._vector
        return self._deepSearch(board, current_x+vec["x"], current_y+vec["y"], 1)

    def getLimit(self):
        return self._limit

    def getVector(self):
        return self._vector

    def _deepCheck(self, board: IBoard, from_x, from_y, to_x, to_y, count):
        try:
            if self._limit:
                if count > self._limit:
                    return False
            cell_value = board.getCellValue(from_x, from_y)  # if this cell isn't exist we will get IndexError
            if cell_value and not self._can_kill:            # if cell is not empty and cannot kill return False
                return False
            if from_x == to_x and from_y == to_y:
                return True
            if cell_value:                                   # if cell is not empty return False
                return False
            vec = self._vector
            return self._deepCheck(board, from_x+vec["x"], from_y+vec["y"], to_x, to_y, count+1)
        except IndexError:
            return False

    def _deepSearch(self, board: IBoard, x, y, count):
        try:
            if self._limit:
                if count > self._limit:
                    return []
            cell_value = board.getCellValue(x, y)  # if this cell isn't exist we will get IndexError
            if cell_value:
                if not self._can_kill:
                    return []
                return [{"x": x, "y": y}]
            vec = self._vector
            return [{"x": x, "y": y}] + self._deepSearch(board, x+vec["x"], y+vec["y"], count+1)
        except IndexError:
            return []
