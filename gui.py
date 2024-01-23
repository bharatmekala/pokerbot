import PySimpleGUI as sg
from game import *
from bot import *
from time import sleep

class PokerWindow:
    def __init__(self):
        font1= ("Helvetica", 30)
        self.layout = [
            [sg.Text("Poker Game", font=("Helvetica", 50), justification="center", size=(20, 1))],
            [sg.Text("Your Hand: ", font = font1), sg.Text(size=(20, 1), key="-HAND-", font=font1)],
            [sg.Text("Board:  ", font = font1), sg.Text(size=(20, 1), key="-BOARD-", font = font1), ],
            [sg.Text("Pot: ", font = font1), sg.Text(size=(20, 1), key="-POT-", font = font1)],
            [sg.Text("Your Stack: ", font = font1), sg.Text(size=(20, 1), key="-STACK-", font = font1)],
            [sg.Text("Amount to Call: ", font = font1), sg.Text(size=(20, 1), key="-TO_CALL-", font = font1)],
            [sg.Text("Bot Move: ", font = font1), sg.Text(size=(20, 1), key="-OPP_MOVE-", font = font1)],
            [sg.Button("Fold", font = font1), sg.Button("Call", font = font1)],
            [sg.Slider((0, 200), orientation="h", size=(15, 20), key="-RAISE_SLIDER-",font = font1, visible=False),
             sg.Button("Confirm Raise", key="-RAISE_BUTTON-",font = font1, visible=False)],
            [sg.ProgressBar(100, orientation="h", size=(20, 20), key="-PROGRESS-", bar_color=("green", "white"))]
        ]

        self.window = sg.Window("Poker Game", self.layout, finalize=True)

    def update_elements(self, hand, board, pot, stack, to_call, slider_bounds, opp_move):
        self.window["-HAND-"].update(hand)
        self.window["-BOARD-"].update(board)
        self.window["-POT-"].update(pot)
        self.window["-STACK-"].update(stack)
        self.window["-TO_CALL-"].update(to_call)
        self.window["-OPP_MOVE-"].update(opp_move)
        self.window["-RAISE_SLIDER-"].update(range=slider_bounds)

    def show_raise_controls(self, show=True):
        self.window["-RAISE_SLIDER-"].update(visible=show)
        self.window["-RAISE_BUTTON-"].update(visible=show)

    def read_event(self):
        event, values = self.window.read()
        return event, values

    def close(self):
        self.window.close()
        
    def run_progress(self, seconds):
        progress_bar = self.window["-PROGRESS-"]
        progress_bar.update(0)  # Reset progress bar

        for i in range(seconds * 10):  # Assuming 0.1 seconds per step
            sleep(0.1)
            progress_bar.update_bar(i + 1)

        progress_bar.update(100)  # Set progress bar to 100% when finished
        

class GUIplayer(Player):
    
    def __init__(self, name):
        super().__init__(name)
        self.gui = PokerWindow()
        self.past_pot = 3
        self.past_move = 0
    
    def pre_flop(self, current_bet):
        
        "Updates GUI elements"
       
        opp_move = self.get_opp_move()
        self.gui.update_elements(f"{self.cards}", f"{self.game.table}", f"{self.game.pot}", f"{self.stack}", min(current_bet - self.aggerate_bet, self.stack), (0, 0), opp_move)
        self.gui.show_raise_controls(False)

        move = self.get_move()
        self.gui.run_progress(5)
        print(move)
        
        if move == -1:
            # Player chose to fold
            return move
        elif move == 0:
            move = min(current_bet - self.aggerate_bet, self.stack)
        
        self.past_pot = self.game.pot + move
        self.past_move = move
        self.stack -= move
        return move
    
    def bet(self, current_bet):
        opp_move = self.get_opp_move()
        self.gui.update_elements(f"{self.cards}", f"{self.game.table}", f"{self.game.pot}", f"{self.stack}", min(current_bet - self.aggerate_bet, self.stack), (min(2*current_bet - self.aggerate_bet, self.stack), self.stack), opp_move)
        self.gui.show_raise_controls(True)
        
        move = self.get_move()
        self.gui.run_progress(5)
        print(move)

        if move == -1:
            return [self.aggerate_bet, move]
        elif move == 0:
            move = min(current_bet - self.aggerate_bet, self.stack)

        
        self.past_pot = self.game.pot + move
        self.past_move = move
        self.stack -= move
        self.aggerate_bet += move

        return [self.aggerate_bet, move]
    
    def get_move(self):
        while True:
            event, values = self.gui.read_event()
            if event == sg.WINDOW_CLOSED:
                print("Window closed")
                return -1
            elif event == "Fold":
                return -1
            elif event == "Call":
                return 0
            elif event == "-RAISE_BUTTON-":
                raise_amount = int(values["-RAISE_SLIDER-"])
                return raise_amount
    
    def get_opp_move(self):
        opp_move = self.game.pot - self.past_pot
        if self.aggerate_bet == 0:
            self.past_move = 0
        if opp_move == self.past_move:
            return f"Called - {opp_move}"
        elif self.game.pot > self.past_pot:
            return f"Raised - {opp_move}"
        return "N/A" 
