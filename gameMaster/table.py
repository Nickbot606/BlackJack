import players
from utils import cardsUtil

"""
GAME MASTER NOTES:

This is essentially a blackjack table
Debug table is for testing purposes
"""

class debugTable(object):

    def __init__(self,min=0,max=-1):
        print("\n<DEBUG> Welcome to blackjack!\n")
        self.players = [] #List of the players 
        self.onTCash = [] #On table cash
        self.onICash = [] #This is the insurance check
        self.onTCards = [] #Cards that are currently on the table
        self.playerlen = 0 #Length of the players
        self.deck = cardsUtil.cards()
        self.minMax = [min,max]
        self.addPlayer(players.dealer.Dealer())
        print("Curr deck:")
        self.deck.showDeck()

    def addPlayer(self,p):
        print("<DEBUG> Added "+p.name)
        self.playerlen += 1
        print("Starting cash: "+str(p.cash))
        self.players.append(p)

    def round(self):
        print("Starting a new round!\n")

        print("Initaite betting: ")
        self.betPrompt()

        print("Initiate card feedings:")
        for j in range(0,self.playerlen):
            #This variable is unnecassary in non-debug 
            for k in range(0,2):
                c = self.deck.give()
                self.players[j].take(c)
                print(self.players[j].name+" has been dealt a "+str(c))

            self.players[j].showHand()
            print()

        #insurance prompt
        if (self.players[0].hand[0][0] == 'A'):
            print("Insurance!\n")
            for i in range(1,self.playerlen):
                self.players[i].insurancePrompt()

            if (self.players[0].hand[0][1] == 10):
                print("Black jack!")
                for j in range(1,self.playerlen):
                    self.players[j].calcHand()
                    if (self.players[j].scores[0] == 21):
                        #If the player has the card and has the 
                        #The 
                        print("Push on insurance")
                    else:
                        print("Time to check insurance")
                        #If they paid their insurance, they get their hand back
                self.clean()
                return 0
            else:
                print("Not a 10. Collect insurance.")
                #Here I need to collect insurance

        
        self.movePrompt()
        #Actual play:
            
        print("Verdict: ")
        #This is where the verdicts will be played
        #Make sure to add the winnings losings and push!
        self.verdict()

        self.clean()
        #Remember to check for the cut card!


    def movePrompt(self):
        for k in range(len(self.players)-1,-1,-1):
            print("Player "+self.players[k].name+"'s turn:")
            mv = self.players[k].movePrompt()
            if (mv == "S"): #Stands
                print("Player stood")
            elif (mv == "H"): #Hit
                print("Hit!")
                c = self.deck.give()
                self.players[k].take(c)
                print(self.players[k].name+" has been dealt a "+str(c))
                mv = self.players[k].movePrompt()

                while (mv != "S"):
                    c = self.deck.give()
                    self.players[k].take(c)
                    print(self.players[k].name+" has been dealt a "+str(c))
                    mv = self.players[k].movePrompt()

            elif (mv == "D"): #Doubled down
                print("Doubled down!")
                c = self.deck.give()
                self.players[k].take(c)
                print(self.players[k].name+" has been dealt a "+str(c))
                self.players[k].cash -= self.onTCash[k]
                self.onTCash *= 2
            
            elif (mv == "P"):
                print("Split!")
                self.splitRoutine(k)


    def splitRoutine(self,player,pos=0):
        print("Split routine")
        self.players[player].cash -= self.onTCash[player]
        self.onTCash[player] *= 2
        self.players[player].hand.append([])
        self.players[player].take(self.players[player].hand[pos].pop(),pos+1)

        for i in range(0,2):
            c = self.deck.give()
            self.players[player].take(c,pos+i)
            print(self.players[player].name+" has been dealt a "+str(c))

        self.players[player].showHand()

    def betPrompt(self):
        self.onTCash = [0] #This is the initalization

        for i in range(1,self.playerlen):
            pr = self.players[i].betPrompt()
            self.players[i].cash -= pr
            print(self.players[i].name+" has bet "+str(pr))
            self.onTCash.append(pr)
        print()
        #TODO add min and max bets on the table here, and also do not feed cards to people who did not bet... except for the dealer
    

    def verdict(self):
        dealerscore = self.players[0].scoresHand(True)[0]
        print("Dealer has a "+str(dealerscore))
        print(self.players[0].hand)
        for i in range(self.playerlen-1,0,-1):
            print("\n"+self.players[i].name+":\n")
            self.players[i].calcHand()
            print(self.players[i].hand)
            for j in range(0,len(self.players[i].scores)):
                playscore = self.players[i].scores[j]
                if ((playscore > dealerscore  or dealerscore >= 22) and playscore < 22):
                    #If they have won the hand
                    print(self.players[i].name+ " has won the hand!")
                    self.players[i].winLoss[0] += 1
                    self.players[i].cash += self.onTCash[i]*2
                elif (playscore == dealerscore and playscore < 22):
                    print(self.players[i].name+ " pushed!")
                    self.players[i].cash += self.onTCash[i]
                    self.players[i].winLoss[1] += 1                    
                else:
                    print(self.players[i].name+ " has lost the hand!")
                    self.players[i].winLoss[2] += 1
            print(self.players[i].name+": "+str(self.players[i].cash))

        
    def clean(self):
        #This cleans the table
        for i in range(0,len(self.players)):
            self.players[i].hand = [[]]
            
        
        if (len(self.deck.deck) <= self.deck.cutcard):
            self.deck.shuffle()
        
        self.onTCash = [] #On table cash
        self.onICash = [] #This is the insurance check
        self.onTCards = [] #Cards that are currently on the table


    """
    PSEUDO:
    1. Everyone bets - done
    2. First, deal each person 2 cards - done
        Add all cards to each player's table history - done 
        Add dealer card to each player - done
        *DO NOT SHOW DEALER'S SECOND CARD* - done
    3. Then start at the top and follow the move orders
        if the dealer has an ace, *done
            prompt each player for insurance * done 
                if the player gets insurance, * done
                    multiply their bet by 1.5 * done
                    if the dealer has a 10,  * done
                        give the player back their inital starting cash () * done
                    else 
                        take insurance, leave rest of bet
                else
                    if the dealer has a 10,
                        if the player has a blackjack, 
                            they push
                        else
                            they lose

        for each player:
            while the player is not done:   
                if the player splits
                    if they have identical cards
                        split their cards and add a new array ['3']['3']
                    else
                        reprompt
                elif the player doubles down
                    if they have the cash to double down and they have not already hit on that hand (len of 2 cards)
                        double player's bet, subtract bet, then hit the player with the card
                    else 
                        reprompt
                elif the player stands, 
                    go to the next player
    4. Dealer's hand (use dealer python card)
        4.5 payout

    5. Check cut card
        if cut card
            shuffle
        
    """