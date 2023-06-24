import random

# Number 1 corresponds to Ace
CARDNAME = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
            11: "Jack", 12: "Queen", 13: "King"}
SUITDICT = {0: "Spades", 1: "Hearts", 2: "Diamonds", 3: "Clubs"}

class Card(object):
    def __init__(self, suit, number):
        if number > 0 and number <= 13:
            self.number = number
        else:
            raise ValueError("Number input is invalid")
        if suit > 0 and suit <= 4:
            self.suit = suit
        else:
            raise ValueError("Suit is invalid")
    
    def __str__(self):
        return CARDNAME[self.number] + "of" + SUITDICT[self.suit]


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []

    def __str__(self):
        return self.name


class Game(object):
    def __init__(self):
        self.deck = []
        for i in range(4):
            for j in range(1, 13):
                self.deck.append(Card(i,j))
        self.players = {}
        playerQueue = []
    
    def addPlayer(self, name):
        if name not in self.players:
            self.players[name] = []
            self.playerQueue.append(Player(name))
        else:
            raise ValueError("Player is already in game")
        
    def shuffleDeck(self):
        random.shuffle(self.deck)
    
    def dealHand(self, noCards):
        if noCards*len(self.players.keys()) > len(self.deck):
            raise ValueError("Too few cards")
        else:
            self.shuffleDeck()

     