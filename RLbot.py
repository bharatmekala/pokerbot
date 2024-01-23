from bot import Bot
from bot import monte_carlo
import dill
from extra import print_colored_number
import random
        

class State:
    def __init__(self, reward, terminate, winning):
        self.reward = reward
        self.terminate = terminate
        self.winning = winning
        self.value = 0
        self.activate = 0
        ##F is fold, C is call, x2 is twice the bet, x3 three times the bet, A is all in
        self.track = {"F":[], "C":[], "x2":[], "x3":[], "A":[]}
    
    def update_func(self, action, next_state):
        if action in self.track:
            self.track[action].append(str(next_state.winning))
    
    def update_terminate(self, action, next_state):
        if action in self.track:
            self.track[action].append(next_state.reward)
    
    def __repr__(self):
        return f"{self.winning}"
    
    def save_state(self, filename):
        """Save the state, including the value function, to a file."""
        with open(filename, "wb") as file:
            dill.dump(self, file)

    @classmethod
    def load_state(cls, filename):
        """Load the state, including the value function, from a file."""
        with open(filename, "rb") as file:
            loaded_state = dill.load(file)
        return loaded_state
            
class State_terminate:
    
    def __init__(self, winner):
        self.value = 0
        self.winner = winner
        self.rewards = []
    
    def reward_update(self, reward):
        self.rewards.append(reward)
        self.reward = reward
        self.value = reward


class TD:
    lam = 0.7
    gam = 0.9
    alpha = 0.3
    
    def __init__(self):
        self.list = []

    def add(self, state):
        self.list.append(state)
    
    def update(self, terminating_state):
        print(self.list)
        self.list.append(terminating_state)
        for i in range(len(self.list) - 1):
            #assigining the activation
            for j in range(i+1):
                if j == i:
                    self.list[j].activate = 1
                else: 
                    self.list[j].activate = self.gam * self.list[j].activate
            
            cur_state = self.list[i]
            next_state = self.list[i+1]
            
            delta_val = self.alpha*(next_state.reward + self.gam*next_state.value - cur_state.value)
            
            for state in self.list:
                if isinstance(state, State):
                    state.value += delta_val*state.activate
                    state.value = int(state.value)
        

class RlBot(Bot):
    actions = ["F", "C", "x2", "x3", "A"]
    def __init__(self, name, state_list):
        self.name = name
        self.TD = TD()
        self.previous_action = None
        self.previous_state = None
        self.total_bet = 0
        self.state_list = state_list
        
    def bet(self, current_bet):
        
        if self.stack == 0:
            return [self.aggerate_bet, 0]
        
        #for pre-flop defaults to normal case
        if self.game.table == []:
            return super().bet(current_bet)
        
        #calulating the current winning% and then finding the assoicated state
        winning_percentage = int(self.winning_calc())
        new_state = self.state_list[winning_percentage]
        
        #if there was a self.previous state updating where we ended up
        if self.previous_state:
            self.previous_state.update_func(self.previous_action, new_state)
        
        #adding the current state to current path in TD, and updating previous state
        self.TD.add(new_state)
        self.previous_state = new_state
        
        #picking a random action and adding it as the previous action
        rand_action = random.choice(self.actions)
        self.previous_action = rand_action
        
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
    
    def winning_calc(self):
        sim = monte_carlo(self.cards, [], self.ACCURACY)
        winning_percentage = sim[0]
        split_percentage = sim[2]
        winning_percentage += split_percentage * self.SPLIT_MULTPLIER
        return winning_percentage * 100
    
    def reset(self):
        self.total_bet += self.aggerate_bet
        self.aggerate_bet = 0
    
    def endgame(self, win):
        net_change = 0
        if win:
            net_change = self.game.pot - self.total_bet 
        else:
            net_change = - self.total_bet
        net_change = int(net_change) 
        self.total_bet = 0
        
        terminating_state = self.state_list[101 if win else 102]
        terminating_state.reward = net_change * 8
        if self.previous_state:
            self.previous_state.update_terminate(self.previous_action, terminating_state)
        
        #updates values for all the states
        self.TD.update(terminating_state)
        
        #getting ready for next run
        self.TD.list = []
        self.previous_state = None
        self.previous_action = None
        
