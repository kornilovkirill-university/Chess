from View import *
import re
from Exceptions import *
import Tools


class Menu:

    def __init__(self, game):
        self._game = game
        self._history_manager = game.getHistoryManager()
        self._common_commands = [{
            "pattern": r"\b(?:e|q|exit|quit)(?:\(\))?\b",
            "action": self._game.stop,
            "prompt": '"e", "exit", "q" or "quit" - to exit'
        }]

    def main(self):
        def move(matches):
            pos_from = Tools.parseCellPosStr(matches["from"])
            pos_to = Tools.parseCellPosStr(matches["to"])
            self._game.moveChessman(pos_from, pos_to)
            self._history_manager.commit()

        def history(matches):
            self._common()
            self.history()

        self._common()
        commands = [{
            "pattern": r"(?P<from>[A-Za-z][0-9]+).+(?P<to>[A-Za-z][0-9]+)",
            "action": move,
            "prompt": '"B2 to D4" or "B2 D4" - to move chessman from B2 to D4'
        }, {
            "pattern": r"(?P<from>[A-Za-z][0-9]+).+show",
            "action": self._game.setInfoAboutAvailableMoves,
            "prompt": '"C2 show" - to show all available moves for the chessman in cell C2'
        }, {
            "pattern": r"history|his|story",
            "action": history,
            "prompt": '"history", "his" or "story" - to show history menu'
        }]
        command = self._requestCommand(commands+self._common_commands)
        self._handleCommand(command, commands+self._common_commands)

    def history(self, matches=False, error=False):
        def history(match):
            self._common()
            self.history()

        if error:
            print(error+"\n")
        commands = [{
            "pattern": r"show",
            "action": self._history_show,
            "prompt": '"show" - to show game history'
        }, {
            "pattern": r"last(?: (?P<number>[0-9]+))?",
            "action": self._history_last,
            "prompt": '"last" - last'
        }, {
            "pattern": r"reverse",
            "action": self._history_reverse,
            "prompt": '"reverse" - to continue game from this savepoint'
        }, {
            "pattern": r"\b(?:c|cancel)(?:\(\))?\b",
            "prompt": '"c or cancel" - to go back'
        }, {
            "pattern": r".*",
            "action": history
        }]
        command = self._requestCommand(commands + self._common_commands, False)
        self._handleCommand(command, commands + self._common_commands)

    def _history_show(self, matches=False):
        self._common()
        save_points_number = self._history_manager.NumberOfSavePoints()
        for i in range(save_points_number):
            self._history_manager.goTo(i).reverse()
            print("Enter", save_points_number-i-1, "for going to this commit:")
            View.renderBoard(self._game.getBoard())
        self.history()

    def _history_reverse(self, matches=False):
        self._history_manager.removeNextSavePoints()

    def _history_last(self, matches=False):
        history_manager = self._history_manager
        max_index = history_manager.NumberOfSavePoints() - 1
        num_to_last = 0
        if matches:
            if "number" in matches.keys():
                if matches["number"]:
                    num_to_last = int(matches["number"])
                    print(num_to_last)
        try:
            if num_to_last > max_index:
                raise NonExistentSavePoint
            history_manager.goTo(max_index-num_to_last).reverse()
            self._common()
            self.history()
        except NonExistentSavePoint:
            self.history(False, "Non existent save point. You can go back max on "+str(max_index)+" steps")

    def _handleCommand(self, command_txt, commands):
        for command in commands:
            matches = re.search(command["pattern"], command_txt, re.IGNORECASE)
            if matches:
                self._game.clearInfo()
                if "action" in command.keys():
                    command["action"](matches.groupdict())
                break

    def _requestCommand(self, commands=False, show_appeal=True):
        if commands:
            appeal = self._getAppealForPLayer(self._game.getCurrentPlayer()) if show_appeal else ""
            prompt = appeal + "enter the command. Examples:"
            for command in commands:
                if "prompt" in command.keys():
                    prompt += "\n"+command["prompt"]
            View.renderPrompt(prompt)
        return input("Command: \n")

    def _common(self):
        self._game.setInfoForChessmenUnderAttack()
        View.clear()
        View.renderErrors(self._game.getErrors())
        View.renderBoard(self._game.getBoard())
        View.renderWarnings(self._game.getWarnings())

    @staticmethod
    def _getAppealForPLayer(player):
        if player == 1:
            return "Player Black(UPPERCASE), "
        if player == 0:
            return "Player White(lowercase), "
