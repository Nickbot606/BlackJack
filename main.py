import random

class Cards(object):
    def __init__(self,decknum=1):
        self.decknum = decknum
        self.deck = ([2,3,4,5,6,7,8,9,10,10,10,10,'A']*(4*self.decknum))
        self.deck.append('C')
        self.hasCut = False
        self.inPlay = []
        self.discard = []
        self.shuffle()

    def shuffle(self):
        self.hasCut = False
        self.discard = []
        self.inPlay = []
        self.deck = ([2,3,4,5,6,7,8,9,10,10,10,10,'A']*(4*self.decknum))
        self.deck.append('C')
        random.shuffle(self.deck) #todo make this more effiicent later with maybe a random insert?
        #print("\nThe deck has been shuffled!\n")
        if (self.deck.index('C') <= self.decknum*13 or self.deck.index('C') >= self.decknum*39 ):
            self.shuffle()

    def showDeck(self):
        #Keep this for debugging
        print(self.deck)

    def give(self):
        #This is for giving a card out from the deck
        temp = self.deck.pop()
        if (temp == 'C'):
            #print("Found the cut card!")
            self.hasCut = True
            return 0
        else:
            self.inPlay.append(temp)
            return temp

    def newRound(self):
        #for i in range(0,len(self.inPlay)):
        #    self.discard.append(self.inPlay[i])
        self.inPlay = []
        if (self.hasCut):
            self.shuffle()
        #print("New round!")

class Player(object):
    def __init__(self,Cash=1.0,Name="Sucker"):
        self.inHand = []
        self.secHand = [] #This is exclusively for when the player splits
        self.bucks = float(Cash)
        self.Name = Name
        self.hasSplit = False
        self.doubleFir = False
        self.doubleSec = False

        self.wins = 0
        self.loses = 0

    def take(self,card,which=True):
        #This is for taking a card
        if (card == 0):
            return
        if (which):
            self.inHand.append(card)
            #print(self.Name + " has received a " + str(card)+" in second hand")
        else:
            self.secHand.append(card)
            #print(self.Name+" has received a "+str(card))

    def doubledDown(self,which=True):
        if (which):
            self.doubleFir = True
        else:
            self.doubleSec = True

    def getDoubled(self,which=True):
        if (which):
            return self.doubleFir
        else:
            return self.doubleSec

    def roundOver(self):
        #This is to give the cards back over to the dealer
        self.inHand = []
        self.secHand = []
        self.doubleFir = False
        self.doubleSec = False

    def calc(self,lis):
        calc = 0
        numOfAs = 0
        for j in range(0,len(lis)):
            if (lis[j] == 'A'):
                numOfAs += 1
            else:
                calc += lis[j]

        for k in range(0,numOfAs):
            if (calc + 11 <= 21):
                calc += 11
            else:
                calc += 1
        return calc
        #This is the calc for what you have at the table in each hand

    def getHand(self,which=True):
        if (which):
            return self.inHand
        else:
            return self.secHand

    def humanPlay(self):
        self.test()
        move = input("would you like to hit (h), split (S) double down (D) or stand (s):")
        return move

    def calcHand(self,which=True):
        if (which):
            return self.calc(self.inHand)
        else:
            return self.calc(self.secHand)

    def Split(self):
        if (len(self.inHand) == 2 and self.inHand[0] == self.inHand[1]):
            #This checks to see if you can split!
            self.secHand.append(self.inHand.pop())

    def pay(self,amt):
        #print("Player "+self.Name+" has been paid "+str(amt))
        self.bucks += amt
        if (amt > 0):
            self.wins += 1
        else:
            self.loses += 1
        #print("Current amt :"+self.getCash())

    def robotPlay(self):
        t = self.calc(self.inHand)
        if (t <= 12):
            return "d"
        elif (t<=15):
            return "h"
        else:
            return "s"

    def dealerPlay(self):
        #Very complicated AI here
        if (self.calc(self.inHand) <= 16):
            return "h"
        else:
            return "s"

    def test(self):
        print(self.Name+" :")
        print("First hand: "+str(self.inHand))
        print("Calculation of hand: "+str(self.calc(self.inHand)))
        if (len(self.secHand) > 0):
            print("Second hand: "+str(self.secHand))
            print("Calculation of hand: " + str(self.calc(self.secHand)))

    def dealerHand(self):
        return self.inHand[0]

    def getCash(self):
        print("Wins:"+str(self.wins))
        print("Losses: "+str(self.loses))
        return self.bucks

#This is how the player will play for general testing
class gameMaster(object):
    def __init__(self,decknum):
        #*Sits down at the table and freshly shuffles deck*
        self.decks = decknum
        self.c = Cards(int(self.decks))
        self.Players = []
        self.addPlayer(0, "Dealer")

    def addPlayer(self,startingCash,Name):
        #Add players to the table
        self.Players.append(Player(startingCash,Name))
        print("Added "+Name+" to the game with "+str(startingCash)+" Bucks!")

    def feedCard(self,ind,which=True):
        #This is to feed a card to a player
        #ind is the index of the player at the table
        self.Players[ind].take(self.c.give(),which)

    def move(self,ind,mv):
        if (mv == "h"):
            self.feedCard(ind)
        if (mv == "s"):
            print("I have stood")
        if (mv == "d"):
            #doubled down!
            print("doubled down!")


    def determineWinner(self):
        dealerhas = self.Players[0].calcHand()
        checkHands = True

        if (dealerhas == 21):
            if (len(self.Players[0].getHand()) == 2):
                # IF the dealer has a blackjack
                for i in range(len(self.Players)-1,0,-1):
                    for j in range(0,2):
                        if (j == 0):
                            checkHands = True
                        else:
                            checkHands = False
                        currHand = self.Players[i].calcHand(self.Players[i].getHand(checkHands))
                        #Check this player's hand for non-blackjacks
                        if (not(currHand == 21 and len(self.Players[i].getHand(checkHands)) == 2) and currHand != 0):
                            if (self.Players[i].getDoubled(checkHands)):
                                self.Players[i].pay(-2)
                            else:
                                self.Players[i].pay(-1)

            else:
                for i in range(len(self.Players)-1,0,-1):
                    #If the dealer has a soft 21
                    for j in range(0,2):
                        if (j == 0):
                            checkHands = True
                        else:
                            checkHands = False
                        currHand = self.Players[i].calcHand(self.Players[i].getHand(checkHands))
                        #Check this player's hand for non-blackjacks
                        if (currHand == 21 and len(self.Players[i].getHand(checkHands)) == 2 and currHand != 0):
                            self.Players[i].pay(1.5)
                        elif (currHand != 0):
                            if (self.Players[i].getDoubled(checkHands)):
                                self.Players[i].pay(-2)
                            else:
                                self.Players[i].pay(-1)
        elif (dealerhas > 21):
            # If the dealer has busted
            for i in range(len(self.Players)-1,0,-1):
                # If the dealer has a soft 21
                for j in range(0, 2):
                    if (j == 0):
                        checkHands = True
                    else:
                        checkHands = False
                    currHand = self.Players[i].calcHand(self.Players[i].getHand(checkHands))
                    if (currHand == 21 and len(self.Players[i].getHand(checkHands)) == 2):
                        self.Players[i].pay(.5)
                    if (currHand <= 21 and currHand != 0):
                        if (self.Players[i].getDoubled(checkHands)):
                            self.Players[i].pay(2)
                        else:
                            self.Players[i].pay(1)
                    else:
                        if (self.Players[i].getDoubled() and currHand != 0):
                            self.Players[i].pay(-2)
                        elif (currHand != 0):
                            self.Players[i].pay(-1)
        else:
            # If the dealer has a non bust hand that's not 21
            for i in range(len(self.Players)-1,0,-1):
                # If the dealer has a soft 21
                for j in range(0, 2):
                    if (j == 0):
                        checkHands = True
                    else:
                        checkHands = False
                    currHand = self.Players[i].calcHand(self.Players[i].getHand(checkHands))
                    #If the players have a Blackjack
                    if (currHand == 21 and len(self.Players[i].getHand(checkHands)) == 2):
                        self.Players[i].pay(1.5)
                    elif (currHand > dealerhas and currHand < 22):
                        if (self.Players[i].getDoubled(checkHands)):
                            self.Players[i].pay(2)
                        else:
                            self.Players[i].pay(1)
                    else:
                        if (currHand != 0 and currHand != dealerhas):
                            if (self.Players[i].getDoubled(checkHands)):
                                self.Players[i].pay(-2)
                            else:
                                self.Players[i].pay(-1)

        #print("The dealer has paid out!")

    def PlayRound(self):
        #First give all players 2 cards
        #print("\nLet's play a round!")
        for j in range(0,len(self.Players)):
            for i in range(0,2):
                self.feedCard(j)
        #print()
        #Show the dealercard
        dealercard = str(self.Players[0].dealerHand())
        print("The dealer has:"+dealercard)
        #print()
        for j in range(len(self.Players)-1,-1,-1):
            currMov = "f"
            while (currMov != "s" and currMov != "b" and currMov != "bj" and currMov != "d"):
                self.move(j,currMov)
                if (self.Players[j].calcHand() == 21):
                    if (len(self.Players[j].inHand) == 2):
                        print("Blackjack!")
                        #self.Players[j].test()
                        currMov = "bj"
                    else:
                        #self.Players[j].test()
                        print("21!")
                        currMov = "s"
                elif (self.Players[j].calcHand() > 21):
                    self.Players[j].test()
                    print("Bust!")
                    currMov = "b"
                else:
                    #self.Players[j].test()
                    if (j == 0):
                        currMov = self.Players[0].dealerPlay()
                    else:
                        if (currMov == "S"):
                            self.Players[j].Split()
                            self.feedCard(j)
                            self.feedCard(j,False)
                        currMov = self.Players[j].humanPlay()
                        #currMov = "s"
                if (currMov == "d"):
                    #print("\nDoubled down!\n")
                    self.feedCard(j)
                    self.Players[j].doubledDown()
                    self.Players[j].test()
                print()

        self.determineWinner()
        for j in range(len(self.Players) - 1, -1, -1):
            self.Players[j].roundOver()
        self.c.newRound()
        print(self.Players[1].getCash())
        #Give the players the chance to do something

if __name__ == '__main__':
    #decks = input("how many decks would you like to play with :")
    g = gameMaster(6)
    g.addPlayer(0,"Splitter")
    for i in range(0, 1000000):
        g.PlayRound()
