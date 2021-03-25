from AbstractChessman import *
from Move import *
import Tools
import math


class Pawn(AbstractChessman):
    _shape = "p"
    _name = "Pawn"

    def getPossibleMoves(self):
        board = self._board
        pos = board.getChessmanPosition(self)
        getCellValue = Tools.secureFunc(board.getCellValue)

        def isAlienChessmanInCell(x, y):
            value = getCellValue(x, y)
            return value.getColor() != self.getColor() if value else False

        moves = []
        color_guide = -1 if self.getColor() == 1 else 1
        if pos:
            if isAlienChessmanInCell(pos["x"]-1, pos["y"]+color_guide): # it is for simple murder (left)
                moves.append(Move(-1, color_guide))
            if isAlienChessmanInCell(pos["x"]+1, pos["y"]+color_guide): # it is for simple murder (right)
                moves.append(Move(1, color_guide))
            if (color_guide == -1 and pos["y"] == 3) or (color_guide == 1 and pos["y"] == 4):
                cell = getCellValue(pos["x"]-1, pos["y"])
                if cell:
                    if cell.getColor() != self.getColor() and isinstance(cell, Pawn):
                        if cell.getNumberOfSteps() == 1:
                            moves.append(Move(-1, color_guide))
                cell = getCellValue(pos["x"]+1, pos["y"])
                if cell:
                    if cell.getColor() != self.getColor() and isinstance(cell, Pawn):
                        if cell.getNumberOfSteps() == 1:
                            moves.append(Move(1, color_guide))

            if self.getNumberOfSteps() == 0:
                moves.append(Move(0, color_guide, limit=2, can_kill=False))
                return moves
        moves.append(Move(0, color_guide, can_kill=False))
        return moves

    def moveTo(self, x, y):
        pos = self._board.getChessmanPosition(self)
        super().moveTo(x, y)
        getCellValue = Tools.secureFunc(self._board.getCellValue)
        color_guide = 1 if self.getColor() == 1 else -1

        if math.fabs(pos["x"]-x) == 1 and math.fabs(pos["y"]-y) == 1:
            if (color_guide == 1 and y == 2) or (color_guide == -1 and y == 5):
                cell = getCellValue(x, y+color_guide)
                if cell:
                    if cell.getColor() != self.getColor() and isinstance(cell, Pawn):
                        if cell.getNumberOfSteps() == 1:
                            cell.kill()

        if (y == 7 and color_guide == -1) or (y == 0 and color_guide == 1):
            chessmenTypes = [Queen, Rook, Horse, Bishop]
            newType = False
            while not newType:
                print("Select new chessman's type:")
                for i in range(len(chessmenTypes)):
                    print(str(i+1)+". "+chessmenTypes[i].getName())
                txt = input("\n")
                if txt.isdigit():
                    num = int(txt) - 1
                    if 0 <= num < len(chessmenTypes):
                        newType = chessmenTypes[num]
            chessman = newType(self._board, self.getColor())
            chessman.setNumberOfSteps(self.getNumberOfSteps())
            self._board.clearCell(x, y)
            self._board.setCellValue(x, y, chessman)
            return chessman
        return self


class Rook(AbstractChessman):
    _shape = "r"
    _name = "Rook"

    def getPossibleMoves(self):
        return [
            Move(0, 1, False),
            Move(1, 0, False),
            Move(0, -1, False),
            Move(-1, 0, False)
        ]


class Horse(AbstractChessman):
    _shape = "h"
    _name = "Horse"

    def getPossibleMoves(self):
        return [
            Move(1, 2),
            Move(2, 1),
            Move(2, -1),
            Move(1, -2),
            Move(-1, -2),
            Move(-2, -1),
            Move(-2, 1),
            Move(-1, 2)
        ]


class Bishop(AbstractChessman):
    _shape = "b"
    _name = "Bishop"

    def getPossibleMoves(self):
        return [
            Move(1, 1, False),
            Move(1, -1, False),
            Move(-1, -1, False),
            Move(-1, 1, False)
        ]


class Queen(AbstractChessman):
    _shape = "q"
    _name = "Queen"

    def getPossibleMoves(self):
        return [
            Move(0, 1, False),
            Move(1, 0, False),
            Move(0, -1, False),
            Move(-1, 0, False),
            Move(1, 1, False),
            Move(1, -1, False),
            Move(-1, -1, False),
            Move(-1, 1, False)
        ]


class King(AbstractChessman):
    _shape = "k"
    _name = "King"

    def getPossibleMoves(self):
        return [
            Move(0, 1),
            Move(1, 0),
            Move(0, -1),
            Move(-1, 0),
            Move(1, 1),
            Move(1, -1),
            Move(-1, -1),
            Move(-1, 1)
        ]
