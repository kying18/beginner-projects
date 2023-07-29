"""
Implementation of rock, paper, scissors by Kylie Ying

YouTube Kylie Ying: https://www.youtube.com/ycubed 
Twitch KylieYing: https://www.twitch.tv/kylieying 
Twitter @kylieyying: https://twitter.com/kylieyying 
Instagram @kylieyying: https://www.instagram.com/kylieyying/ 
Website: https://www.kylieying.com
Github: https://www.github.com/kying18 
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ 
"""

import random

def play():
    choices = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
    user = input("What's your choice? 'r' for rock, 'p' for paper, 's' for scissors\n").lower()
    computer = random.choice(['r', 'p', 's'])

    if user == computer:
        return "It's a tie!"  # If user choice matches computer choice, it's a tie

    if (user == 'r' and computer == 's') or (user == 's' and computer == 'p') or (user == 'p' and computer == 'r'):
        return f'You won! The computer chose {choices[computer]}.'  # Check if the user wins based on choices

    return f'You lost! The computer chose {choices[computer]}.'  # If the user didn't win, it's a loss

print(play())
