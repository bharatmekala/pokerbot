from colorama import Style

card_print = {}
Suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
Suits_1 = ['c', 'h', 'd', 's']
Ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
Ranks_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

for i in range(4):
    card_print[Suits_1[i]] = Suits[i]

for i in range(13):
    card_print[Ranks_1[i]] = Ranks[i]


def print_colored_number(number):
    color = determine_color(number)
    colored_number = f"{color}{number}{Style.RESET_ALL}"
    print(colored_number, end='\t')

def determine_color(number):
    normalized_value = (number + 1500) / 3000  # Normalize the value between 0 and 1
    # Interpolate the color based on the normalized value
    r = int(255 * (1 - normalized_value))
    g = int(255 * normalized_value)
    b = 0
    return f"\033[38;2;{r};{g};{b}m"
