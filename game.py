import random
from extra import *
from exceptions import *

#Card class
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.rank = number
    
    def __repr__(self):
        return f'{card_print[self.rank]}{card_print[self.suit]}'

# a function that creates a perfectly sorted 52 card deck with Card obj
def card_generator():
    ret = []
    for x in ['s', 'c', 'h', 'd']:
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            ret.append((x,n))
    
    return [Card(x, y) for x, y in ret]

#Deck class  
class Deck:
    
    def __init__(self):
        #shuffles deck for each game
        self.deck = card_generator()
        random.shuffle(self.deck)
    
    def deal(self, players):
        #removes two cards from deck and adds them to player.cards
        for p in players:
            p.cards = [self.deck.pop()] + [self.deck.pop()]
    
    def draw(self, num):
        #removes num cards from deck and returns them as a list
        ret = []
        for _ in range(num):
            ret.append(self.deck.pop())
        return ret

#player class
class Player:
    
    #fixed attributes
    cards = []
    sb = True
    stack = 200
    game = None
    aggerate_bet = 0
    
    def __init__ (self, name):
        self.name = name
    
    #pre flop betting method
    def pre_flop(self, current_bet):
     
        print(f"\n{self.name} Information:\n"
          f"Hand: {self.cards}\n"
          f"Stack: {self.stack}\n"
          f"Pot: {self.game.pot}")
    
        move = preflop_cannotraise(current_bet - self.aggerate_bet, self.stack)
        
        if move == -1:
            # Player chose to fold
            return move
        else:
            # Player made a bet or call
            self.stack -= move
            return move

    
    def bet(self, current_bet):
        
        #prinintg player information
        print(f"\n{self.name} Information:\n"
          f"Hand: {self.cards}\n"
          f"Table: {self.game.table}\n"
          f"Stack: {self.stack}\n"
          f"Pot: {self.game.pot}\n"
          f"Your Bet So far: {self.aggerate_bet}")
        
        if current_bet == 0:
            move = postflop_check(current_bet, self.stack)
        else:
            print("Miniumun bet to raise: ", min(self.stack, 2*current_bet - self.aggerate_bet))
            move = postflop_bet(current_bet, self.stack, self.aggerate_bet)
        
        if move != -1:
            self.stack -= move
            self.aggerate_bet += move
        return [self.aggerate_bet, move]
    def reset(self):
        self.aggerate_bet = 0

#main game class
class Game:
    #game attriblues, can be changed with game.___ =
    pot = 0
    small_bet = 1
    big_bet = 2
    game_end = False
    
    
    def __init__(self, bb, sb):
        self.table = []
        self.deck = Deck()
        self.players = [sb, bb]
        self.sb = self.players[0]
        self.sb.sb = True
        self.sb.game = self
        self.bb = self.players[1]      
        self.bb.sb = False
        self.bb.game = self
    
        
    def start(self):
        self.deck.deal(self.players)
        self.reset()
        self.pot = self.small_bet + min(self.big_bet, self.bb.stack)
        self.sb.stack -= self.small_bet
        self.sb.aggerate_bet +=self.small_bet
        self.bb.aggerate_bet += min(self.big_bet, self.bb.stack)
        self.bb.stack -= min(self.big_bet, self.bb.stack)
        current = self.big_bet
        
        bet = self.sb.bet(current)
        
        
        if bet[1] == -1:
            return self.endgame(self.bb)
        else:
            current = bet[0]
            self.pot += bet[1]
            bet = self.bb.bet(current)
        
        if bet[1] == -1:
                return self.endgame(self.sb)
        elif bet[0] == current:
            self.pot += bet[1]
            
        else:
            current  = bet[0]
            self.pot += bet[1]
            bet = self.sb.pre_flop(current)
            
            if bet == -1:
                return self.endgame(self.bb)
            else:
                
                self.pot += bet
        
        if self.sb.stack == 0 or self.bb.stack == 0:
            return self.all_in()
        
        return self.flop()
    
    
    
    def bet(self):
        current_bet, bet = 0, 0
        first_bet = True
        while (self.bb.aggerate_bet != self.sb.aggerate_bet or first_bet) and self.bb.stack != 0:
            first_bet = False
            temp1 = self.bb.bet(bet)
            current_bet = temp1[0]
            if temp1[1] == -1:
                return self.endgame(self.sb)
            self.pot += temp1[1]
            if (self.bb.aggerate_bet == self.sb.aggerate_bet and current_bet != 0) or self.sb.stack == 0:
                break
            temp2 = self.sb.bet(current_bet)
            bet = temp2[0]
            if temp2[1] == -1:
                return self.endgame(self.bb)
            self.pot += temp2[1]

        
        if self.sb.stack == 0 or self.bb.stack == 0:
            return self.all_in()
    
    def flop(self):
        self.reset()
        self.table += self.deck.draw(3)
        state = self.bet()
        if self.game_end == True:
            return state
        else:
            return self.turn()
    
    def turn(self):
        self.reset()
        self.table += self.deck.draw(1)
        state = self.bet()
        if self.game_end == True:
            return state
        else:
            return self.river()
    
    def river(self):
        self.reset()
        self.table += self.deck.draw(1)
        state = self.bet()
        if self.game_end == True:
            return state
        else:
            return self.showdown()
    
    
    def showdown(self):
        best = showdown_calc(self.sb.cards, self.bb.cards, self.table)
        if best == 2:
            return self.endgame(self.bb)
        elif best == 1:
            return self.endgame(self.sb)
        else:
            return self.endgame_split()


    def all_in(self):
        for _ in range(5 - len(self.table)):
            self.table += self.deck.draw(1)
        return self.showdown()
    
    def endgame_split(self):
        print(f"\n\n\n It was a split pot, BB will get the higher split \n\n\n")
        self.game_end = True
        self.bb.stack += self.pot % 2 + int(self.pot/2)
        self.sb.stack += int(self.pot/2)
        return self.players
    
    def endgame(self, winner):
        print(f"\n\n\n{winner.name} won this round\n\n\n")
        
        from RLbot import RlBot
        #letting the bot know if it won or lost
        for p in self.players:
            if isinstance(p, RlBot):
                p.endgame(p == winner)
                
        self.game_end = True
        winner.stack += self.pot
        return self.players

    def reset(self):
        for p in self.players:
            p.reset()

#showdown calc
def showdown_calc(hand_1, hand_2, table):
    hand_1 = hand_1 + table 
    hand_2 = hand_2 + table
    funcs = [pair, straight, flush, straight_flush]
    hands = {1 : max(map(lambda x: x(hand_1), funcs)), 2 : max(map(lambda x: x(hand_2), funcs))}

    if hands[1] == hands[2]:
        return 3
    
    return 1 if max(hands[1], hands[2]) == hands[1] else 2

#consider 7766448 edge case
def pair(hand):
    """ returns a list [strenght, [high card in pair, high card out of pair]] """
    
    #ranks is initally sorted so that the highest pairs are considred first
    extraced = [(card.suit, card.rank) for card in hand]
    hand = [Card(s, 14) if n == 1 else Card(s, n) for s, n in extraced]
    ranks = [card.rank for card in hand]
    ranks.sort(reverse=True)
    for r in ranks:
        
        #four of a kind case
        if ranks.count(r) == 4:
            #print(ranks)
            ranks = [num for num in ranks if num != r]
            #print(ranks)
            if ranks:
                ret = ranks[0]
            else:
                ret = 0
            return [8, [r,ret]]
        elif ranks.count(r) == 3:
            #runs the functon on the rest of the deck
            temp = [c for c in hand if c.rank != r]
            if temp and temp.count(temp[0]) == 4:
                return [8, [temp[0], r]]
            rest = pair(temp)
            
            #fullhouse case 1 (rest is a 3 of a kind)
            if rest[0] == 4:
                return [7, [r] + rest[1][:1]]
            #fullhouse case 2 (rest is a 2 pair)
            elif rest[0] == 3:
                return [7, [r] + rest[1][:1]]
            #fullhouse case 3 (rest is a pair)
            elif rest[0] == 2:
                return [7, [r] + rest[1][:1]]
            #three of a kind
            else:
                return [4, [r] + rest[1][:2]]
        elif ranks.count(r) == 2:
            #runs the functon on the rest of the deck
            rest = pair([c for c in hand if c.rank != r])
            
            #two pair case 1 (rest is a two pair)
            if rest[0] == 3:
                return [3, [r] + rest[1][:2]]
            #two pair case 2 (rest is a pair)
            elif rest[0] == 2:
                return [3, [r] + rest[1][:2]]
            #just a pair
            else:
                return [2, [r] + rest[1][:3]]

    return [1, ranks[:5]]
                
def straight(hand):
    """returns a list [strength, high card]"""
    ranks = [card.rank for card in hand]
    ranks.sort()
    num = 0
    listHigh = 0
    for i in range(len(ranks)-1):
        if ranks[i] + 1 == ranks[i + 1]:
            num += 1
            if num >= 4:
                listHigh = ranks[i+1]
        else:
            num = 0
    if ranks[len(ranks)-1] == 13 and num >=3 and ranks[0] == 1:
        listHigh = 14
    if listHigh == 0:
        return []
    return [5, [listHigh]]
    
def flush(hand):
    """ return [strength, [list of ranks]]"""
    suit = [card.suit for card in hand]
    flush = []

    if suit.count("h") >= 5:
        for i in range(len(hand)):
            if hand[i].suit == "h":
                flush.append(hand[i].rank)
    elif suit.count("s") >= 5:
        for i in range(len(hand)):
            if hand[i].suit == "s":
                flush.append(hand[i].rank)
    elif suit.count("c") >= 5:
        for i in range(len(hand)):
            if hand[i].suit == "c":
                flush.append(hand[i].rank)
    elif suit.count("d") >= 5:
        for i in range(len(hand)):
            if hand[i].suit == "d":
                flush.append(hand[i].rank)
    flush.sort(reverse = True)
    if len(flush) > 4:
        return [6, flush[:5]]
    return []

def straight_flush(hand):
    """" returns [strength, high card]"""
    flus = flush(hand)
    if flus == []:
        return []
    flushhand = flus[1]
    staigh = straight([Card("s", r) for r in flushhand])
    if staigh == []:
        return []
    return [9, staigh[1]]
