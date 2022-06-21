#This is a human player
#This is basically an interactive version of the player just to make sure everyhting is okay.
from .. import Player


class human(Player.Player):

    def __init__(self):
        super().__init__(1000,"Player")
        self.bet = 0

    def movePrompt(self):
        print("S stand, H hit, P split, D double down")
        self.showHand()
        mv = input("What move would you like to make? :").upper()
        if (mv == "S" or mv == "H" or mv == "P" or mv == "D"):
            return mv
        else:
            self.movePrompt()

    def betPrompt(self):
        print("Current cash:"+str(self.cash))
        return int(input("How much would you like to wager?:"))