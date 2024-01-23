from game import Game
from tqdm import tqdm
from bot import Bot
from RLbot import RlBot, State, State_terminate
from extra import print_colored_number
from policy import policy


#creating state classes for winning% (1-100) and adding win/lose
#.load_state("save_state/" + str(x))
state_list = [State(int(800 * pow((x/100)-0.5,3)), False, x).load_state("save_state/" + str(x)) for x in range(100 + 1)]
state_list += [State_terminate(True), State_terminate(False)]

for state in state_list:
            if isinstance(state, State):
                print(state.winning, end="")
                print_colored_number(state.reward)
player1 = Bot("Bot1")
botWin = 0
player2 = RlBot("RLBot", state_list)
RLbOTWIN = 0

RLWin = 0
for _ in tqdm(range(1000)):
    while player1.stack > 0 and player2.stack > 0:
        game = Game(player1, player2)
        players = game.start()
        player1 = players[0]
        player2 = players[1]
    # if max(players, key=lambda x: x.stack).name == "Bot1":
    #     botWin += 1
    # else: 
    #     RLbOTWIN += 1
    # #print("RlBot win total: ", RLbOTWIN)
    # #print("Bot win total: ", botWin)
    for state in state_list:
        print_colored_number(state.value)
    
    for state in state_list:
        if isinstance(state, State):
            state.save_state("save_state/" + str(state.winning))
    player1 = Bot("Bot1")
    player2 = RlBot("RLBot", state_list)

print("the winner is ", max(players, key=lambda x: x.stack).name, "!")

print(policy(state_list).values())
