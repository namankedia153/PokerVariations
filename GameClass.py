import random
from collections import Counter

# Number 1 corresponds to Ace
CARDNAME = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
            11: "Jack", 12: "Queen", 13: "King"}
SUITDICT = {0: "Spades", 1: "Hearts", 2: "Diamonds", 3: "Clubs"}

HANDRANKING = {9: "Royal Flush", 8: "Straight Flush", 7: "Four of a Kind", 6: "Full House", 5: "Flush", 4: "Straight",
               3: "Three of a Kind", 2: "Two Pair", 1: "Pair", 0: "High Card"}

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


# Add cards to an output which is a straight dont check for flush here. if you count later you can get flush. do all possible straight combinations outputted here. Return them sorted.
    # def isSeq(self, cards):
    #     start = 0
    #     end = 0
    #     full = sorted(cards, reverse = True, key= (lambda x: x.number))
    #     # Ace can go front or back
    #     if full[-1].number == 1:
    #         full.insert(Card(full[-1].suit, 1), 0)
    #     max = full[0]
    #     prev = full[0]
    #     for i in range(1,len(full)):
    #         if prev.number == full[i].number:
    #             continue
    #         elif prev.number == full[i].number + 1 or (prev.number == 1 and full[i].number == 13):
    #             count += 1
    #         else:

    #         if count == 5:
    #             straight = True 


    def isSeq(self, cards):
        full = sorted(list(set([card.number for card in cards])), reverse = True)
        if len(full) < 5:
            return []
        final = []
        start = 0
        end = 0
        tmp = [full[start]]
        while end != len(full) - 1:
            end += 1
            if full[end] == (tmp[-1] - 1):
                tmp.append(full[end])
            else:
                start = end
                tmp = [full[start]]
            if (end - start) == 4: # zero indexing means 4
                final.append(tmp.copy())
                tmp.pop(0)
                start += 1
# Check for ace at top
        if sum(full[:4]) == 46 and full[-1] == 1:
            final.insert(0, [1, 13, 12, 11, 10])
        return final




# Function for evaluating highest straight combinations and includes straight flushes.

    def checkStraightFlush(self,  straights, cards, suitCounts):
        fail = (False, None)
        if len(straights) == 0:
            return fail
        flushSuit = max(suitCounts, key = lambda x: suitCounts[x])
        index = 0
        straight_ind = 0
        for straight in straights:
            print(straight)
            # at maximum there can be 3 aces while still having a straight 
            if straight[0] == 1:
                index = -3
            while straight_ind != 5:
                print("Card Index: " + str(index))
                print("Straight Index: " + str(straight_ind))
                curr = straight[straight_ind]
                while straight_ind == 0 and cards[index].number != curr:
                    index += 1
                if cards[index].suit == flushSuit:
                    straight_ind += 1
                    index += 1
                elif cards[index].number == cards[index + 1].number:
                    index += 1
                else:
                    index = 0
                    straight_ind = 0
                    break
            if straight_ind == 5:
                return (True, straight[0])
        return fail



    def evaluateHand(self, board, hand):
        full = board + hand
        full = sorted(full, reverse = True, key= (lambda x: x.number))
        possibleHands = list(range(10))
        suits = [card.suit for card in full]
        numbers = sorted([card.number for card in full])
        suitCounts = Counter(suits)
        numberCounts = Counter(numbers)
        maxSuit = max(suitCounts.values())
        maxNums = sorted(numberCounts.values(), reverse = True)[:2]
        straights = self.isSeq(full)
        if maxSuit >= 5:  
            if len(straights) == 0:
                return ### Flush
            else:
                seq, straight_max = self.checkStraightFlush(straights, full, suitCounts)
                if seq:
                    if straight_max == 1:
                        return ### Royal Flush
                    else:
                        return ### Straight Flush
        else:
            if len(straights) > 0:
                return ### Straight
            else:
                if maxNums[0] == 4:
                    return ### Four of a Kind
                elif maxNums[0] == 3:
                    if maxNums[1] >= 2:
                        return ### Full House
                    else:
                        return ### Three of a Kind
                elif maxNums[0] == 2:
                    if maxNums[1] >= 2:
                        return ### Two Pair
                    else:
                        return ### Pair
                else:
                    return ### High Card
    #     # make a list of functions to evaluate on the output to stop nesting if else statements
        
            
        

    