import random  # Randomly choose a word.
from words import words  # List of words.
import string  # Create alphabet.


# Make sure the chosen word doesn't contain dashes or spaces.
def get_valid_word(words):
    """ """
    word = random.choice(words)  # Randomly choose item from the list.
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


def hangman():
    word = get_valid_word(words)
    word_letters = set(word)  # letters in the word.
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # Userguessed letters.

    lives = 6

    # Get user input.
    while len(word_letters) > 0 and lives > 0:
        # Display letters used.
        print(f"\nJe hebt nog {lives} levens.")
        print("Deze letters zijn gekozen:", " ".join(used_letters))

        # Display current word.
        word_list = [
            letter if letter in used_letters
            else '-' for letter in word
            ]
        print("Huidig woord: ", " ".join(word_list))

        # Get user input
        user_letter = input("\nRaad een letter: ").upper()
 
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1  # Takes away a life.
                print(f"'{user_letter.upper()}' is niet goed.")
            
        elif user_letter in used_letters:
            print(f"Je hebt de letter {user_letter} al geraden. Probeer een andere letter.")

        else:
            print(f"De letter {user_letter} zit niet in het woord. Probeer het nog eens.")

    # When len(word_letters) == 0 OR when lives == O
    if lives == 0:
        print(f"\nHelaas, je hebt verloren. Het woord was {word}\n")
    else:
        print(f"\n\tGoedzo! Je hebt het woord {word} geraden!\n")

hangman()
