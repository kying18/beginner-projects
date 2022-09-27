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
    user = is_user()

    computer = random.choice(['r', 'p', 's'])

    print('Computer output is '+computer) #give output for computer

    if user == computer:
        return 'tie'

    if is_win(user, computer):
        return 'You win'
    
    return 'You Lose !'
    
def is_user():
    user = input("'r' for rock, 'p' for paper, 's' for scissors ")
    if user != 'r' and user != 'p' and user != 's':
        print('You input wrong key to play!!')
        is_user()
    return user

   
def is_win(player, opponent):
    if(player == 'r' and opponent == 's') or (player == 's' and opponent == 'p') \
        or (player == 'p' and opponent == 'r'):
        return True

print(play())
#play again option
while True:
    play1 = input('Still wanna play ? (y/n) ')
    if play1 == 'Y' or play1 == 'y':
        print(play())
    elif play1 == 'N' or play1 == 'n':
        quit()
