#This is the main player function 
#Default player also is essentially stanley

class Player(object):

    def __init__(self,cash=1000,name="Sucker"):
        #This is the first 
        """
        KNOWLEDGE OF EACH PLAYER:
        Their hand
        Dealer has
        Table has
        Table history
        """
        self.hand = [[]]
        self.scores = [] #This is the scores per hand per point
        self.cash = cash
        self.name = name
        self.bet = 5 #This is the bet that is currently on the table

        """
        MOVES
        H: HIT
        S: STAND
        P: SPLIT
        D: DOUBLE DOWN
        """
        self.currMove = "S" #PLAYERS WILL BE FED AS SOON AS THEY PUT THE MINIMUM BET ON THE TABLE

        """
        INSURANCE
        (Insurance is only used when the player is given an ace on the dealer)
        True: INSURANCE
        False: NO INSURANCE
        """
        self.inMove = False #Insurance is a scam ;)

        """
        STATUS
        W: WIN
        L: LOSS
        P: PUSH
        """
        #[int of wins, int of losses, int of pushes]
        self.winLoss = [0,0,0]

    #This function takes a card
    def take(self,card,pos=0):
        print(self.name+" took a "+str(card))
        self.hand[pos].append(card)

    def betPrompt(self):
        return self.bet

    def movePrompt(self):
        return self.currMove

    def insurancePrompt(self):
        return self.inMove

    def showHand(self):
        print(self.hand)
        return self.hand

    def calcHand(self):
        li = []
        for i in self.hand:
            Aces = 0
            temp = 0

            for j in i:
                if j != 'A':
                    temp += j
                else:
                    Aces += 1
                
            for k in range(0,Aces):
                if (temp + 11 <= 21):
                    temp += 11
                else:
                    temp += 1


            li.append(temp)

        self.scores = li
        return li

    def scoresHand(self,d=False):
        if (d):
            self.calcHand()
        
        return self.scores