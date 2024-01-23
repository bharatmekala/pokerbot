
from RLbot import RlBot
from bot import *

def policy(states):
    policy = {}
    #replace all states with values
    for i in range(len(states) - 2):
        state = states[i]
        total = 1
        for action in state.track:
            if state.track[action]:
                state.track[action] = [s if isinstance(s, int) else states[eval(s)].value for s in state.track[action]]
            total += len(state.track[action])
        
        for action in state.track:
            cur = state.track[action]
            state.track[action] = int(sum(cur) * (len(cur)/total))
        
        policy[state] = max(state.track, key=lambda x: state.track[x])
    
    return policy

class Policy(RlBot):
    
    def __init__(self, name, state_list):
        super().__init__(name, state_list)
        self.policy = policy(state_list)
    
    def bet(self, current_bet):
        
        if self.stack == 0:
            return [self.aggerate_bet, 0]
        
        #for pre-flop defaults to normal case
        if self.game.table == []:
            return super().bet(current_bet)
        
        #calulating the current winning% and then finding the assoicated state
        winning_percentage = int(self.winning_calc())
        
        #picking a random action and adding it as the previous action
        rand_action = self.policy[winning_percentage]
        
        move = 0
        if rand_action == "F":
            return [self.aggerate_bet, -1]
        elif rand_action == "C":
            move = min(current_bet - self.aggerate_bet, self.stack)
        elif rand_action == "x2":
            move = min(2 * current_bet - self.aggerate_bet, self.stack)
        elif rand_action == "x3":
            move = min(3 * current_bet - self.aggerate_bet, self.stack)
        elif rand_action == "A":
            move = self.stack    
        self.aggerate_bet += move
        self.stack -= move
        return [self.aggerate_bet, move]


