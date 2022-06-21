import random

#This is the cards that are debugged to print out more when I need them to be debugged
class cardsDebug(object):

    def __init__(self,decknum=1):
        print("\n<DEBUG> New deck. "+str(decknum)+" shoe deck.\n")
        self.decknum = decknum
        self.deck = ([2,3,4,5,6,7,8,9,10,10,10,10,'A']*(4*self.decknum))
        self.hasCut = False
        self.inPlay = []
        self.cutcard = 0
        self.shuffle()

    def showDeck(self):
        print(self.deck)

    def showInPlay(self):
        print("In Play:")
        print(self.inPlay)
        print()

    def getCut(self):
        return self.hasCut

    def shuffle(self):
        self.inPlay = []
        self.deck = ([2,3,4,5,6,7,8,9,10,10,10,10,'A']*(4*self.decknum))
        random.shuffle(self.deck)
        #This isn't really based on any math, I just liked the cut card around here it here
        #I'll make sure to mention this in the video
        self.cutcard = (random.randrange((self.decknum*30),(self.decknum*46)))
        print("<DEBUG> Deck shuffled. current deck:")
        self.showDeck()
        print()

    def give(self):
        temp = self.deck.pop()
        self.inPlay.append(temp)
        print("<DEBUG> Gave a "+str(temp)+" card")
        return temp


class cards(object):
    def __init__(self,decknum=1):
        self.decknum = decknum
        self.deck = ([2,3,4,5,6,7,8,9,10,10,10,10,'A']*(4*self.decknum))
        self.cutcard = 0
        self.inPlay = []
        self.shuffle()

    def showDeck(self):
        print(self.deck)

    def shuffle(self):
        self.inPlay = []
        self.deck = ([2,3,4,5,6,7,8,9,10,10,10,10,'A']*(4*self.decknum))
        random.shuffle(self.deck)
        #This isn't really based on any math, I just liked the cut card around here it here
        #I'll make sure to mention this in the video
        self.cutcard = (random.randrange((self.decknum*30),(self.decknum*46)))


    def give(self):
        temp = self.deck.pop()
        self.inPlay.append(temp)
        return temp
