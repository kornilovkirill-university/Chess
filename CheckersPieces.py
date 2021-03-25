from AbstractChessman import *
from Move import *
import Tools
import math


class CheckersPiece(AbstractChessman):
    _shape = "p"
    _name = "CheckersPiece"

    def getPossibleMoves(self):
        board = self._board
        pos = board.getChessmanPosition(self)
        getCellValue = Tools.secureFunc(board.getCellValue, error_message="error")

        def isAlienChessmanInCell(x, y):
            value = getCellValue(x, y)
            if value == "error":
                return False
            return value.getColor() != self.getColor() if value else False

        moves = []
        if pos:
            for vec in [{"x": 1, "y": 1}, {"x": 1, "y": -1}, {"x": -1, "y": -1}, {"x": -1, "y": 1}]:
                if isAlienChessmanInCell(pos["x"]+vec["x"], pos["y"]+vec["y"]):
                    if not getCellValue(pos["x"]+2*vec["x"], pos["y"]+2*vec["y"]):
                        moves.append(Move(2*vec["x"], 2*vec["y"], can_kill=False))
            # если есть ходы, которыми можем срубить, тогда нет смысла добавлять обычные ходы, т.к. рубить обязательно
            if len(moves) == 0:
                color_guide = -1 if self.getColor() == 1 else 1
                moves.append(Move(-1, color_guide, can_kill=False))
                moves.append(Move(1, color_guide, can_kill=False))
        return moves

    def moveTo(self, x, y):
        curr_pos = self._board.getChessmanPosition(self)
        super().moveTo(x, y)
        board = self._board
        getCellValue = Tools.secureFunc(board.getCellValue, error_message="error")
        delta_x = int(math.fabs(curr_pos["x"] - x))
        delta_y = int(math.fabs(curr_pos["y"] - y))
        if delta_x > 1 and delta_y > 1:
            sign_x = 1 if x > curr_pos["x"] else -1
            sign_y = 1 if y > curr_pos["y"] else -1
            for i in range(1, delta_x):
                cell = getCellValue(curr_pos["x"]+sign_x*i, curr_pos["y"]+sign_y*i)
                if cell:
                    cell.kill()
        if (self.getColor() == 0 and y == 7) or (self.getColor() == 1 and y == 0):
            chessman = CheckersQueen(self._board, self.getColor())
            chessman.setNumberOfSteps(self.getNumberOfSteps())
            self._board.clearCell(x, y)
            self._board.setCellValue(x, y, chessman)
            return chessman
        return self


class CheckersQueen(CheckersPiece):
    _shape = "q"
    _name = "CheckersQueen"

    def getPossibleMoves(self):
        board = self._board
        pos = board.getChessmanPosition(self)
        getCellValue = Tools.secureFunc(board.getCellValue, error_message="error")

        def isAlienChessmanInCell(x, y):
            value = getCellValue(x, y)
            if value == "error":
                return False
            return value.getColor() != self.getColor() if value else False

        def searchEmptyCellsLine(vector, i):
            result = []
            if not getCellValue(pos["x"]+i*vector["x"], pos["y"]+i*vector["y"]):
                result = [Move(i*vector["x"], i*vector["y"], can_kill=False)]
                result = result + searchEmptyCellsLine(vector, i+1)
            return result

        moves = []
        if pos:
            for vec in [{"x": 1, "y": 1}, {"x": 1, "y": -1}, {"x": -1, "y": -1}, {"x": -1, "y": 1}]:
                barrier_distance = len(searchEmptyCellsLine(vec, 1)) + 1
                if isAlienChessmanInCell(pos["x"]+vec["x"]*barrier_distance, pos["y"]+vec["y"]*barrier_distance):
                    moves = moves + searchEmptyCellsLine(vec, barrier_distance+1)
            # если есть ходы, которыми можем срубить, тогда нет смысла добавлять обычные ходы, т.к. рубить обязательно
            if len(moves) == 0:
                moves.append(Move(-1, 1, limit=False, can_kill=False))
                moves.append(Move(1, 1, limit=False, can_kill=False))
                moves.append(Move(-1, -1, limit=False, can_kill=False))
                moves.append(Move(1, -1, limit=False, can_kill=False))
        return moves


