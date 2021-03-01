# Beginner projects 2 Guess number.
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

guess(10)
 