from IBoard import *


class View:

    @classmethod
    def clear(cls):
        cls._renderEmptyStrings(30)

    @classmethod
    def renderErrors(cls, errors):
        if len(errors) > 0:
            print("ERROR:")
            print(" - "+errors)
        cls._renderEmptyStrings(1)

    @classmethod
    def renderBoard(cls, board: IBoard):
        board.render()
        cls._renderEmptyStrings(1)

    @classmethod
    def renderWarnings(cls, warnings):
        if len(warnings) > 0:
            print("  " + warnings)
        cls._renderEmptyStrings(1)

    @classmethod
    def renderPrompt(cls, prompt):
        print(prompt)
        cls._renderEmptyStrings(1)

    @staticmethod
    def _renderEmptyStrings(count=1):
        for i in range(count):
            print()
