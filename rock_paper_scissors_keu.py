# ffc Beginner projects 4, Rock paper scissors.

import random

# Rules of the game
# r > s, s > p, p > r

def play():
    """Play rock-paper-scissors against the computer."""
    print(f"\nLet's play Rock paper scissors!")
    user = input(f"'R' for rock, 'P' for paper, 'S' for scissors:  ").lower()
    computer = random.choice(['r', 'p', 's'])

    if user == computer:
        return "It's a tie"

    if is_win(user, computer):
        return("You won!")
    else:
        return("You lost!")

def is_win(player, opponent):
    """Determine the winner if it's not a tie."""
    # Return True if player wins.
    if (player == 'r' and opponent == 's') \
        or (player == 's' and opponent == 'p') \
            or (player == 'p' and opponent == 'r'):
        return True

# Display the returned result.
print(play())
