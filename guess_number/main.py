# Beginner projects 2 and 3, Guess number.
import random

def guess(x):
    """Create a random number to guess."""
    random_number = random.randint(1, x)

    # guess = 0  # guess = 0 to make sure guess != random_number.
    guess = ""  # declare guess without a value.

    while guess != random_number:
        guess = input(f"\nGuess a number between 1 and {x}: ")
        guess = int(guess)
        # print(guess)

        if guess < random_number:
            print(f"{guess} is too low, try again.")
        elif guess > random_number:
            print(f"{guess} is too high, try again.")

    # Print doesn't have to be in the loop.
    print(f"You guessed right, {random_number} is the right number!")

# guess(10)  # Uncomment to guess the random number again.


def computer_guess(x):
    """Have the computer guess the secret number."""
    low = 1
    high = x
    feedback = ''
    while feedback != 'c':  # 'c' for correct
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low  # Could also be high, low == high

        feedback = input(f"Is {guess} too high (H), too low (L), or correct (C)??").lower()
        if feedback == 'h':
            high = guess - 1
        elif feedback == 'l':
            low = guess + 1

    print(f"\nThe computer guessed your secret number, it's {guess}!") 

computer_guess(10000)
