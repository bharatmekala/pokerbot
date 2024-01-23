from game import *
from bot import *
from gui import *
from policy import *
from RLbot import *

state_list = [State(int(800 * pow((x/100)-0.5,3)), False, x).load_state("save_state/" + str(x)) for x in range(100 + 1)]
state_list += [State_terminate(True), State_terminate(False)]


player1 = Player("Sharan")
player2 = Bot("Bot1")


while player1.stack > 0 and player2.stack > 0:
    game = Game(player1, player2)
    players = game.start()
    print(game.sb.name, game.sb.cards, game.sb.stack)
    print(game.bb.name, game.bb.cards, game.bb.stack)
    print(game.table, game.pot)
    player1 = players[0]
    player2 = players[1]

print("the winner is ", max(players, key=lambda x: x.stack).name, "!")
