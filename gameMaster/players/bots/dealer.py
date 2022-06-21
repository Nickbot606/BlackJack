#This is the dealer player
#Essentially all the same as a normal player except 

from .. import Player

class Dealer(Player.Player):
    
    def __init__(self):
        super().__init__(0,"Dealer")
        self.bet = 0
        self.currMove = "H"
    
    #You don't want to show the dealer's hand
    def showHand(self):
            print(self.hand[0][0])

    def movePrompt(self):
        self.calcHand()
        #I decided to not have the dealer hit a soft 17
        if (self.scores[0] <= 17):
            self.currMove = "H"
        else:
            self.currMove = "S"
        return self.currMove
