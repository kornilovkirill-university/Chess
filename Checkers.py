from Chess import *
from CheckersPieces import *
from typing import List, Union


class Checkers(Chess):

    def __init__(self):
        super().__init__()
        self._walking_chessman: Union[List, bool] = False
        self._killed_positions = []

    def moveChessman(self, position_from, position_to):
        current_player = self.getCurrentPlayer()

        # По правилам шашек нельзя прохдить одну и ту же фигуру за один ход,
        # так что тут ищем все позиции, на которых находятся фигуры, которые будут съедены
        # Если ход правильный, эти фигуры будут добавлены в общий массив
        positions_will_be_killed = []
        getCellValue = Tools.secureFunc(self._board.getCellValue, error_message="error")
        for pos in Tools.getLinePositionsBetweenPositions(position_from, position_to):
            # В этом цикле проверяем, есть ли эта позиция в списке съеденых
            cell = getCellValue(pos["x"], pos["y"])
            if cell:
                if cell.getColor() != current_player:
                    positions_will_be_killed.append({"x": pos["x"], "y": pos["y"]})
        # конец поиска позиций фигур, которые будут съедены

        super().moveChessman(position_from, position_to)

        self._killed_positions += positions_will_be_killed
        next_player = self.getCurrentPlayer()
        self.setCurrentPlayer(current_player)

        chessman = self._board.getCellValue(position_to["x"], position_to["y"])
        self._walking_chessman = chessman
        killer_positions = self._getKillerPositions(chessman)
        if len(killer_positions) == 0 or len(self._killed_positions) == 0:
            self._walking_chessman = False
            self._killed_positions = []
            self.setCurrentPlayer(next_player)

        return self

    def _getAvailablePositions(self, chessman: IChessman):
        if self._walking_chessman:
            if self._walking_chessman != chessman:
                return []
        attacked_rival_pieces = Explorer(self._board).getChessmenUnderAttack(self._nextPlayer(self._currentPlayer))
        if len(attacked_rival_pieces) == 0:
            return chessman.getAvailablePositions()
        return self._getKillerPositions(chessman)

    def _getKillerPositions(self, chessman: IChessman):
        position = self._board.getChessmanPosition(chessman)
        result = []
        killedChessmenNumber = len(self.getBoard().getKilledChessmen())
        for av_pos in chessman.getAvailablePositions():
            explorer = Explorer(self._board)
            explorer.move(position, av_pos)
            can_append = True
            if killedChessmenNumber >= len(self.getBoard().getKilledChessmen()):
                can_append = False  # если переход на эту позицию не съест фигуру, то добавлять не надо
            explorer.reverse()
            if can_append:
                for pos in Tools.getLinePositionsBetweenPositions(position, av_pos):
                    if Tools.isPositionInArray(pos, self._killed_positions):
                        # проверяем, чтоб по пути к новой позиции мы не пересекали позицию, которая была съедена
                        can_append = False
                if can_append:
                    result.append(av_pos)
        return result

    def _setChessmen(self):
        board = self._board
        for color in [0, 1]:
            for y in range(3):
                y = int(math.fabs(y - color*7))
                for x in range(8):
                    if (x + y) % 2 == 0:
                        board.setCellValue(x, y, CheckersPiece(board, color))

    def _setChessmen_test(self):
        board = self._board
        board.setCellValue(2, 2, CheckersPiece(board, 0))\
            .setCellValue(6, 6, CheckersPiece(board, 0))

        board.setCellValue(1, 1, CheckersPiece(board, 1))\
            .setCellValue(3, 1, CheckersPiece(board, 1))\
            .setCellValue(1, 3, CheckersPiece(board, 1))

    def _setChessmen_test_queen(self):
        board = self._board
        board.setCellValue(6, 6, CheckersPiece(board, 0)) \
            .setCellValue(4, 4, CheckersQueen(board, 0))

        board.setCellValue(3, 3, CheckersPiece(board, 1)) \
            .setCellValue(3, 1, CheckersPiece(board, 1)) \
            .setCellValue(1, 3, CheckersPiece(board, 1))

