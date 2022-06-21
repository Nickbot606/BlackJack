import cardsUtil

"""
This is a small tester to make sure my cards are right
It's also a good test bench to ensure everything is working correctly
"""


if __name__ == '__main__':
    #c is my debug cards here

    #This test just checks that the cards are being shuffled and cut correctly. 
    c = cardsUtil.cardsDebug(1)
    while (c.inPlay == [] or c.inPlay[-1] != 'C'):
        c.give()
    
    print("Cut card found!")
    c.hasCut = True

    for i in range(0,3):
        c.give()

    c.showInPlay()
    print("Still in deck:")
    c.showDeck()
    
    c.shuffle()