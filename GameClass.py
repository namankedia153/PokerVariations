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
        if suit > -1 and suit <= 3:
            self.suit = suit
        else:
            raise ValueError("Suit is invalid")
    
    def __str__(self):
        return CARDNAME[self.number] + " of " + SUITDICT[self.suit]
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bet = 0
        self.stack = 0

    def addCard(self, card):
        self.hand.append(card)

    def __str__(self):
        return self.name

    def printHand(self):
        res = 'Hand: '
        for card in self.hand:
            res += str(card) + ', '
        print (res[:-2])

    def getName(self):
        return self.name


class Game(object):
    def __init__(self):
        self.deck = []
        for i in range(4):
            for j in range(1, 13):
                self.deck.append(Card(i,j))
        self.players = {}
        self.playerQueue = []
        self.pot = 0
    
    def addPlayer(self, name):
        if name not in self.players:
            self.players[name] = []
            self.playerQueue.append(Player(name))
        else:
            raise ValueError("Player is already in game")
    
    def getPlayer(self, name):
        for player in self.playerQueue:
            if player.getName() == name:
                return player
        else:
            raise ValueError ("Player not in game")
        
    def shuffleDeck(self):
        random.shuffle(self.deck)
    
    def dealHand(self, numCards):
        if numCards*len(self.players.keys()) > len(self.deck):
            raise ValueError("Too few cards")
        else:
            self.shuffleDeck()
            total = numCards*len(self.players.keys())
            while total != 0:
                player = self.playerQueue.pop(0)
                print(self.playerQueue)
                print("Current Player", player)
                card = self.deck.pop(0)
                print("Current Card", card)
                player.addCard(card)
                print(player.getName())
                self.players[player.getName()].append(card)
                self.playerQueue.append(player)
                total -= 1

    def resetGame(self):
        self.deck = []
        for i in range(4):
            for j in range(1, 13):
                self.deck.append(Card(i,j))
        self.shuffleDeck()
        self.players = {key:[] for key in self.players}
        for player in self.playerQueue:
            player.hand = []
            player.bet = 0


class TexasHoldEm(Game):

    def __init__(self):
        Game.__init__(self)
        self.board = []

    def __str__(self):
        return "Texas Hold'em Poker"

    def dealHand(self):
        return super().dealHand(2)
    
    def openCard(self):
        self.board.append(self.deck.pop(0))
    
    def burnCard(self):
        self.deck.pop(0)
    