from IBoard import *


class IChessman:

    def getPicture(self):
        pass

    def getColor(self):
        pass

    def getNumberOfSteps(self):
        pass

    def setNumberOfSteps(self, number):
        pass

    def getPossibleMoves(self):
        pass

    def getAvailablePositions(self):
        pass

    def moveTo(self, x, y):
        pass

    def kill(self):
        pass

