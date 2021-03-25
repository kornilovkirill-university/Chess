from Board import *
from IChessman import *
import Tools
from Exceptions import *


class Explorer:

    def __init__(self, board: IBoard):
        self._board = board
        self._initial_data = board.get()
        self._killedChessmen = board.getKilledChessmen()
        self._numbersOfSteps = {}

        for row in self._initial_data:
            for cell in row:
                if cell:
                    self._numbersOfSteps[cell] = cell.getNumberOfSteps()

    def move(self, initial_position, new_position):
        cell = self._board.getCellValue(initial_position["x"], initial_position["y"])
        if not cell:
            raise EmptyCell
        numberOfSteps = cell.getNumberOfSteps()
        cell.moveTo(new_position["x"], new_position["y"])
        cell.setNumberOfSteps(numberOfSteps)
        return self

    def reverse(self):
        for row in self._initial_data:
            for cell in row:
                if cell:
                    cell.setNumberOfSteps(self._numbersOfSteps[cell])
        self._board.setData(self._initial_data)

        board_killed = self._board.getKilledChessmen()
        for chessman in board_killed:
            if chessman not in self._killedChessmen:
                self._board.removeChessmanFromKilled(chessman)
        for chessman in self._killedChessmen:
            if chessman not in board_killed:
                self._board.addKilledChessman(chessman)
        # self._killedChessmen = self._board.getKilledChessmen()

    def doesChessmenUnderAttack(self, chessmen: IChessman):
        return chessmen in self.getChessmenUnderAttack(chessmen.getColor())

    def getChessmenUnderAttack(self, attacked_player):
        data = self._board.get()
        result = []
        for row in data:
            for cell in row:
                if not cell:
                    continue
                if cell.getColor() == attacked_player:
                    continue
                current_position = self._board.getChessmanPosition(cell)
                for available_position in cell.getAvailablePositions():
                    explorer = Explorer(self._board)
                    explorer.move(current_position, available_position)
                    for chessman in explorer._board.getKilledChessmen():
                        if chessman not in explorer._killedChessmen:
                            result.append(chessman)
                    explorer.reverse()
        return result





    # def __getPositionsUnderAttack(self, attacked_player):
    #     data = self._board.get()
    #     result = []
    #     for row in data:
    #         for cell in row:
    #             if not cell:
    #                 continue
    #             if cell.getColor() == attacked_player:
    #                 continue
    #             for available_position in cell.getAvailablePositions():
    #                 result.append(available_position)
    #     return result



    # def _willPositionUnderAttack(self, position, attacked_player):
    #     cell = self._board.getCellValue(position["x"], position["y"])
    #     self._board.clearCell(position["x"], position["y"])
    #     dangerous_positions = self._getPositionsUnderAttack(attacked_player)
    #     result = Tools.isPositionInArray(position, dangerous_positions)
    #     self._board.setCellValue(position["x"], position["y"], cell)
    #     return result