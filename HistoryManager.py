from IBoard import *
from Exceptions import *
from Explorer import *


class HistoryManager:

    def __init__(self, game):
        self._game = game
        self._board = game.getBoard()
        self._save_points = []
        self._current_savepoint_num = -1  # -1 is last save point

    def goTo(self, savepoint_number=-1):
        if savepoint_number == -1:
            savepoint_number = len(self._save_points)-1
        if 0 <= savepoint_number < len(self._save_points):
            self._current_savepoint_num = savepoint_number
        else:
            raise NonExistentSavePoint
        return self

    def commit(self):
        savepoint = {
            "explorer": Explorer(self._board),
            "current_player": self._game.getCurrentPlayer(),
            "errors": self._game.getErrors(),
            "warnings": self._game.getWarnings()
        }
        self._save_points.append(savepoint)
        return self

    def reverse(self):
        explorer = self._save_points[self._current_savepoint_num]["explorer"]
        current_player = self._save_points[self._current_savepoint_num]["current_player"]
        errors = self._save_points[self._current_savepoint_num]["errors"]
        warnings = self._save_points[self._current_savepoint_num]["warnings"]
        explorer.reverse()
        self._game.setCurrentPlayer(current_player)
        # self._game.setError(errors)
        self._game.setWarning(warnings)
        return self

    def removeNextSavePoints(self):
        savepoint_number = self._current_savepoint_num
        if savepoint_number == -1:
            savepoint_number = len(self._save_points)-1
        self._save_points = self._save_points[:savepoint_number+1]
        return self

    def NumberOfSavePoints(self):
        return len(self._save_points)

    def getCurrentSavePointNumber(self):
        return self._current_savepoint_num
