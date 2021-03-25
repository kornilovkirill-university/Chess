from IChessman import *
from IBoard import *
from Exceptions import *
from Move import *
import Tools
import copy


class AbstractChessman(IChessman):
    _shape = False
    _name = False

    def __init__(self, board: IBoard, color):
        self._board = board
        self._color = color
        self._stepsCounter = 0

    def getPicture(self):
        if self.getColor() == 1:
            return self._shape.upper()
        if self.getColor() == 0:
            return self._shape.lower()

    @classmethod
    def getName(cls):
        return cls._name

    def getColor(self):
        return self._color

    def getNumberOfSteps(self):
        return self._stepsCounter

    def setNumberOfSteps(self, number):
        self._stepsCounter = number

    def getPossibleMoves(self) -> [Move]:
        return []

    def getAvailablePositions(self):
        current_position = self._board.getChessmanPosition(self)
        if not current_position:
            raise ChessmanIsNotOnBoard
        result = []
        for move in self.getPossibleMoves():
            positions = move.getPossiblePositions(self._board, current_position["x"], current_position["y"])
            for pos in positions:
                cell_val = self._board.getCellValue(pos["x"], pos["y"])
                if cell_val:
                    if cell_val.getColor() == self.getColor():
                        continue
                result.append(pos)

        return result

    def moveTo(self, x, y):
        current_position = self._board.getChessmanPosition(self)
        if not current_position:
            raise ChessmanIsNotOnBoard
        if not self._isPossibleMove(current_position["x"], current_position["y"], x, y):
            raise ImpossibleChessmanMove

        cell_val = self._board.getCellValue(x, y)
        if cell_val:
            if cell_val.getColor() == self.getColor():
                raise CellAlreadyBelongsToColor
            cell_val.kill()
        self._board.clearCell(current_position["x"], current_position["y"])
        self._board.setCellValue(x, y, self)
        self._incrementCounter()
        return self

    def kill(self):
        position = self._board.getChessmanPosition(self)
        self._board.clearCell(position["x"], position["y"])
        self._board.addKilledChessman(self)

    def _isPossibleMove(self, current_x, current_y, new_x, new_y):
        possible_moves = self.getPossibleMoves()
        for move in possible_moves:
            if move.check(self._board, current_x, current_y, new_x, new_y):
                return True
        return False

    def _incrementCounter(self):
        self._stepsCounter += 1
