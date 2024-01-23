from game import *
from random import shuffle

class Bot(Player):
    ACCURACY = 1000
    SPLIT_MULTPLIER = 0.25
    PREFLOP_THRESHOLD = .5
    RAISE_THRESHOLD = 0.2
    RAISE_CONSTANT = 1.5

    def pre_flop(self, current_bet):
        amount_to_call = current_bet - self.aggerate_bet
        pot_odds = self.pot_odds(current_bet)
        sim = monte_carlo(self.cards, [], self.ACCURACY)
        
        winning_percentage = sim[0]
        split_percentage = sim[2]
        adjusted_winning = winning_percentage + split_percentage * self.SPLIT_MULTPLIER
        
        if adjusted_winning > pot_odds:
            move = min(self.stack, amount_to_call)
            self.stack -= move
            return move
        else:
            return -1

    def bet(self, current_bet):
        if self.stack == 0:
            return [self.aggerate_bet, 0]
        if self.game.table == []:
            move = min(self.pre_floppity(current_bet), self.stack)
            if move != -1:
                self.stack -= move
                self.aggerate_bet += move
            return [self.aggerate_bet, move]
        else:
            amount_to_call = current_bet - self.aggerate_bet
            min_raise = 2 * current_bet - self.aggerate_bet
            pot_odds = self.pot_odds(current_bet)
            sim = monte_carlo(self.cards, self.game.table.copy(), self.ACCURACY)
        
            winning_percentage = sim[0]
            split_percentage = sim[2]
            adjusted_winning = winning_percentage + split_percentage * self.SPLIT_MULTPLIER
            if adjusted_winning - pot_odds > self.RAISE_THRESHOLD:
                move = min(self.stack, int(min_raise + 5 * (adjusted_winning - pot_odds - self.RAISE_THRESHOLD) / self.RAISE_CONSTANT)) 
            elif adjusted_winning > pot_odds:
                move = min(self.stack, amount_to_call)
            else:
                if amount_to_call == 0:
                    move = 0
                else:
                    return [self.aggerate_bet, -1]
            self.aggerate_bet += move
            self.stack -= move
            return [self.aggerate_bet, move]


    def pot_odds(self, bet):
        return bet / (self.game.pot + bet)
    
    def pre_floppity(self, current_bet):
        their_stack = 0
        if self.sb:
            their_stack = self.game.bb.stack
        else:
            their_stack = self.game.sb.stack
        
        if (self.stack - their_stack) / self.stack < - self.PREFLOP_THRESHOLD:
            return min(pre_flop_small_v1(2*current_bet - self.aggerate_bet, self.cards), max(self.stack/4, 2*current_bet - self.aggerate_bet))
        elif (self.stack - their_stack) / self.stack <=  self.PREFLOP_THRESHOLD:
            move = pre_flop_medium_v1(2*current_bet - self.aggerate_bet, current_bet - self.aggerate_bet ,self.cards)
            if move > self.stack/2:
                move = current_bet - self.aggerate_bet
            return move
        else:
            move = pre_flop_big_v1(2*current_bet - self.aggerate_bet, current_bet - self.aggerate_bet ,self.cards)
            if move > self.stack/2:
                move = current_bet - self.aggerate_bet
            return move
    
def pre_flop_small_v1(min_to_raise, hand):
    ranks = [card.rank for card in hand]
    ranks.sort()
    suits = [card.suit for card in hand]
    
    if suits[0] != suits[1]:
        if ranks[0] == 2 and ranks[1] in [3, 4, 5, 6, 7, 8, 9] or ranks[0] == 3 and ranks[1] in [4, 7, 8]:
            return -1
    return int(min_to_raise * 1.5)

def pre_flop_medium_v1(min_to_raise, call, hand):
    ranks = [card.rank for card in hand]
    ranks.sort()
    suits = [card.suit for card in hand]
    
    if suits[0] != suits[1]:
        if ranks[1] in [6, 7, 8, 9] and ranks[0] == 4 or ranks[1] in [4, 5, 6, 7, 8, 9, 10] and ranks[0] == 3 or ranks[1] in [3, 4, 5, 6, 7, 8, 9, 10] and ranks[0] == 2:
            return -1
    else:
        if ranks[1] == 3 and ranks[0] == 2:
            return call
    return int (2.5 * min_to_raise)

def pre_flop_big_v1(min_to_raise, call, hand):
    ranks = [card.rank for card in hand]
    ranks.sort()
    suits = [card.suit for card in hand]
    
    if suits[0] != suits[1]:
        if ranks[1] in [6, 7, 8, 9, 10] and ranks[0] == 5 or ranks[1] in [5, 6, 7, 8, 9, 10, 11] and ranks[0] == 4 or ranks[1] in [4, 5, 6, 7, 8, 9, 10, 11] and ranks[0] == 3 or ranks[1] in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12] and ranks[0] == 2:
            return -1
    else:
        if ranks[1] in [3, 4, 5, 6, 7, 8, 9] and ranks[0] == 2 or ranks[0] == 3 and ranks[1] in [7, 8]:
            return call
    return int (3* min_to_raise)

def simulate(hand, table):
    """Simulates a poker game with a random deck

    Args:
        hand (list of card instances): the current hand of the poker player
        table (list of cards on the table): the flop/turn/river
    """
    
    #creates new shuffled deck
    tmp_deck = Deck()
    deck = tmp_deck.deck
    shuffle(deck)
    
    #makes current full hand (5-7) cards
    full = hand + table
    full_ranks = [card.rank for card in full]
    full_suits = [card.suit for card in full]
    
    #removes the full hand cards from the board
    [deck.remove(card) for card in deck if card.rank in full_ranks and card.suit in full_suits]

    
    #gives opponet their hand
    opponet = tmp_deck.draw(2)
    while len(table) < 5:
        table.extend(tmp_deck.draw(1))
        
    
    return showdown_calc(hand, opponet, table)

def monte_carlo(hand, table, samples):
    # %time you win, %time you lose, %time you split
    dit = [0, 0, 0]
    
    for _ in range(samples):
        result = simulate(hand, table)
        dit[result - 1] += 1
    
    return list(map(lambda x: x/samples, dit))

    


    
    



