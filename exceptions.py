#user input functions

def preflop_cannotraise(bet_to_call, stack):
    while True:
        print("-1 to fold, ", min(bet_to_call, stack), " to call: ")
    
        try:
            move = int(input())
    
            if move > stack:
                print("Invalid Input: You cannot bet more then your stack")
            elif move >bet_to_call:
                print("Invalid Input: You cannot re-raise big blind pre-flop")
            elif move < bet_to_call and move != stack and move != -1:
                print("Invalid Input: You must bet", min(bet_to_call, stack))
            else:
                break
    
        except ValueError:
            print("Invalid Input: input must be an integer")
    
    return move
    
def postflop_check(current_bet, stack):
    while True:
        print("0 to check or raise")
    
        try:
            move = int(input())
    
            if move > stack:
                print("Invalid Input: You cannot bet more then your stack")
            elif move < current_bet:
                print("Invalid Input: You must bet", current_bet)
            else:
                break
    
        except ValueError:
            print("Invalid Input: input must be an integer")
    
    return move

def postflop_bet(current_bet, stack, aggerate):
    while True:
        print("-1 to fold, ", min(current_bet - aggerate, stack), " to call, or raise:")
    
        try:
            move = int(input())
        
            if move > stack:
                print("Invalid Input: You cannot bet more then your stack")
            elif current_bet - aggerate < move < 2 * current_bet - aggerate and move != stack:
                print("Invalid Input: Minium raise is", min(stack, 2 * current_bet - aggerate))
            elif move < current_bet - aggerate and move != -1 and  move != stack:
                print("Invalid Input: You must bet atleast", min(current_bet - aggerate, stack))
            else:
                break
        except ValueError:
            print("Invalid Input: input must be an integer")
    
    return move
