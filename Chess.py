from Board import *
from Chessmen import *
from IGame import *
from Exceptions import *
import Tools
from Explorer import *
from View import *
from Menu import *
from HistoryManager import *


class Chess(IGame):

    def __init__(self):
        self._board = Board()
        self._setChessmen()
        self._currentPlayer = 0
        self._error = ""
        self._warning = ""
        self._working = True
        self._history_manager = HistoryManager(self)
        self._history_manager.commit()

    def run(self):
        while self._working:
            try:
                self._history_manager.goTo(-1).reverse()
                self._checkOnGameOver()

                Menu(self).main()

            except CellAlreadyBelongsToColor:
                self.setError("You cannot kill your chessman")
            except ChessmanIsNotOnBoard:
                self.setError("Chessman is not on board")
            except ImpossibleChessmanMove:
                self.setError("Impossible move")
            except EmptyCell:
                self.setError("Cannot select empty cell")
            except AlienChessman:
                self.setError("Cannot select alien chessman")
            except ValueError:
                self.setError("Cell position out of range")

    def stop(self, matches=False):
        self._working = False

    def clearInfo(self):
        self.clearErrors()
        self.clearWarnings()
        self._board.clearCellsInfo()
        return self

    def getCurrentPlayer(self):
        return self._currentPlayer

    def setCurrentPlayer(self, player):
        self._currentPlayer = player
        return self

    def getBoard(self):
        return self._board

    def getErrors(self):
        return self._error

    def getWarnings(self):
        return self._warning

    def setError(self, error_msg):
        self._error = error_msg
        return self

    def setWarning(self, warning_msg):
        self._warning = warning_msg
        return self

    def clearErrors(self):
        self._error = ""
        return self

    def clearWarnings(self):
        self._warning = ""
        return self

    def getHistoryManager(self) -> HistoryManager:
        return self._history_manager

    def setInfoForChessmenUnderAttack(self):
        for chessman in Explorer(self._board).getChessmenUnderAttack(self._currentPlayer):
            attack_pos = self._board.getChessmanPosition(chessman)
            if not chessman:
                continue
            if chessman.getColor() != self._currentPlayer:
                continue
            if isinstance(chessman, King):
                self.setWarning("CHECK!")
            self._board.setCellInfo(attack_pos["x"], attack_pos["y"], info1="!")
            
    def _checkOnGameOver(self):
        positions = []
        for row in self._board.get():
            for el in row:
                if el:
                    if el.getColor() == self._currentPlayer:
                        positions += self._getAvailablePositions(el)
        if len(positions) == 0:
            self.setWarning("CHECKMATE!")
            self.stop()

    def moveChessman(self, position_from, position_to):
        chessman = self._board.getCellValue(position_from["x"], position_from["y"])
        if not chessman:
            raise EmptyCell
        if chessman.getColor() != self._currentPlayer:
            raise AlienChessman

        available_positions = self._getAvailablePositions(chessman)
        if not Tools.isPositionInArray(position_to, available_positions):
            raise ImpossibleChessmanMove

        chessman.moveTo(position_to["x"], position_to["y"])
        self._changeCurrentPlayer()
        return self

    def setInfoAboutAvailableMoves(self, matches):
        pos = Tools.parseCellPosStr(matches["from"])
        chessman = self._board.getCellValue(pos["x"], pos["y"])
        if not chessman:
            raise EmptyCell
        if chessman.getColor() != self._currentPlayer:
            raise AlienChessman
        self._board.setCellInfo(pos["x"], pos["y"], info2="#")
        for av_pos in self._getAvailablePositions(chessman):
            self._board.setCellInfo(av_pos["x"], av_pos["y"], info2="*")

    def _getAvailablePositions(self, chessman: IChessman):
        king = False
        for row in self._board.get():
            for el in row:
                if el:
                    if isinstance(el, King):
                        if el.getColor() == chessman.getColor():
                            king = el
                            break
        position = self._board.getChessmanPosition(chessman)
        result = []
        for av_pos in chessman.getAvailablePositions():
            if king:
                explorer = Explorer(self._board)
                doesUnderAttack = explorer.move(position, av_pos).doesChessmenUnderAttack(king)
                explorer.reverse()
                if doesUnderAttack:
                    continue
            result.append(av_pos)
        return result

    def _changeCurrentPlayer(self):
        self._currentPlayer = self._nextPlayer(self._currentPlayer)

    @staticmethod
    def _nextPlayer(player):
        if player == 1:
            return 0
        if player == 0:
            return 1

    def _setChessmen(self):
        board = self._board
        for i in range(8):
            board.setCellValue(i, 6, Pawn(board, 1))  # set top side player's pawns
            board.setCellValue(i, 1, Pawn(board, 0))  # set down side player's pawns

        # set top side player's chessmen besides pawns
        board.setCellValue(0, 7, Rook(board, 1)).setCellValue(7, 7, Rook(board, 1)) \
            .setCellValue(1, 7, Horse(board, 1)).setCellValue(6, 7, Horse(board, 1)) \
            .setCellValue(2, 7, Bishop(board, 1)).setCellValue(5, 7, Bishop(board, 1)) \
            .setCellValue(3, 7, Queen(board, 1)).setCellValue(4, 7, King(board, 1))

        # set down side player's chessmen besides pawns
        board.setCellValue(0, 0, Rook(board, 0)).setCellValue(7, 0, Rook(board, 0)) \
            .setCellValue(1, 0, Horse(board, 0)).setCellValue(6, 0, Horse(board, 0)) \
            .setCellValue(2, 0, Bishop(board, 0)).setCellValue(5, 0, Bishop(board, 0)) \
            .setCellValue(3, 0, Queen(board, 0)).setCellValue(4, 0, King(board, 0))


############# IT IS TESTING ARRANGEMENT ###########

    def _setChessmen_test_checkmate(self):
        board = self._board

        board.setCellValue(1, 1, King(board, 0))

        board.setCellValue(2, 2, Rook(board, 1))\
            .setCellValue(2, 1, Rook(board, 1))\
            .setCellValue(1, 2, Rook(board, 1))

    def _setChessmen_with_other_chessman(self):
        board = self._board

        board.setCellValue(0, 0, King(board, 0)).setCellValue(0, 1, Rook(board, 0))

        board.setCellValue(2, 2, Rook(board, 1))\
            .setCellValue(2, 1, Rook(board, 1))\
            .setCellValue(0, 3, Rook(board, 1))

    def _setChessmen_pawns(self):
        board = self._board

        board.setCellValue(1, 1, Pawn(board, 0)).setCellValue(3, 1, Pawn(board, 0)).setCellValue(2, 3, Pawn(board, 1))
        board.setCellValue(6, 6, Pawn(board, 1)).setCellValue(4, 6, Pawn(board, 1)).setCellValue(5, 4, Pawn(board, 0))





# self._renderEmptyStrings(50)
# self._board.render()
# self._renderEmptyStrings(1)
# chessman = self._offerSelectChessman()
# self._renderEmptyStrings(1)
# new_pos = self._offerSelectNewPos()
# chessman.moveTo(new_pos["x"], new_pos["y"])
# self._changeCurrentPlayer()

# def _offerSelectNewPos(self):
#     appeal = self._getAppealForPLayer(self._currentPlayer)
#     cell_pos_str = input(appeal + 'select new position (example "D5")\n')
#     return Tools.parseCellPosStr(cell_pos_str)
#
#
# def _offerSelectChessman(self):
#     appeal = self._getAppealForPLayer(self._currentPlayer)
#     cell_pos_str = input(appeal + 'select chessman (example "D5")\n')
#     pos = Tools.parseCellPosStr(cell_pos_str)
#     cell = self._board.getCellValue(pos["x"], pos["y"])
#     if not cell:
#         raise EmptyCell
#     if cell.getColor() != self._currentPlayer:
#         raise AlienChessman
#     return cell