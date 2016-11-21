from copy import deepcopy
import os
import data_manager
import random


# This function gets the input from the user. It checks if the guess is
# a correct guess.
def player_guess(word_to_display):
    while True:
        try:
            input_guess = input("Please enter a letter a-z: ")
            if input_guess.isdigit() or len(input_guess) != 1:
                raise ValueError
            for word in word_to_display:
                if input_guess in word:
                    raise ValueError
            break
        except ValueError:
            print("Please try again!")
            continue
        except (KeyboardInterrupt, EOFError):
            os.system('clear')
            print("\nbye")
            quit()
    return input_guess.lower()


# This changes the original sentence / word to a list of lists of "_"-s.
def print_word(to_guess):
    words = to_guess.split()
    word_to_display = []
    for word in words:
        word_to_display.append(["_ "] * len(word))
    return word_to_display


# This function takes the input guess function and gets the input. Then
# copies the word to display and checks whether the input is in the original
# sentence / word. If so, it changes the index of the word to be displayed
# to the guessed letter. If the copied version (which didn't change) is the same
# as the version which has to be modified, that means the guess was incorrect,
# and the player loses one life.
def change_word_to_display(guess, word_to_display, to_guess, lives):
    words = to_guess.split()
    copy_word_to_display = deepcopy(word_to_display)
    for i in range(len(words)):
        for j in range(len(words[i])):
            if guess == words[i][j].lower():
                word_to_display[i][j] = words[i][j]
    if copy_word_to_display == word_to_display:
        lives -= 1
        return word_to_display, lives
    return word_to_display, lives


# print the table: clear the terminal, print the name of the game and quit option,
# print the lives left. Then the word which has to be guessed.
def print_table(word_to_display, lives):
    os.system('clear')
    print("Hangman by Oli. Press ctrl + d to quit")
    print("\n")
    print("Total guesses left: {}".format(lives))
    print()
    for word in word_to_display:
        print("".join(word), end=" ")
    print("\n")


# Check if the player wants to play again
def wanna_play_again():
    play_again = None
    while not (play_again == "y" or play_again == "n"):
        try:
            play_again = input("Do you want to play again? (y/n): ")
            if play_again.isdigit():
                raise ValueError
        except ValueError:
            print("y or n please!")
            continue
    if play_again == "y":
        return True
    else:
        print("See ya!")
        return False


# player chooses a mode (easy, medium or hard)
def mode():
    current_mode = None
    while not (current_mode == "e" or current_mode == "m" or current_mode == "h"):
        try:
            current_mode = input("Choose a mode: easy ('e'), medium ('m') or hard ('h'): ")
            if current_mode.isdigit():
                raise ValueError
        except ValueError:
            print("'e' or 'm' or 'h' please!")
            continue
    return current_mode


# Initializing the game: setting the word to be guessed,
# change it to empty characters, and setting lives.
def init_game():
    while True:
        try:
            filename = input("please enter a filename: ")
            sentences = data_manager.get_sentence_from_file(filename)
            break
        except (TypeError, FileNotFoundError):
            print("Oops, no such file. Please try again!")
            continue
    to_guess = random.choice(sentences)
    word_to_display = print_word(to_guess)
    current_mode = mode()
    if current_mode == "h":
        total_lives = 5
    elif current_mode == "m":
        total_lives = 8
    elif current_mode == "e":
        total_lives = 10
    return to_guess, word_to_display, total_lives


# Check if the game has come to an end:
def check_if_won(word_to_display, total_lives):
    # First, we check if the player lost (has no lives left)
    if total_lives == 0:
        print("Too bad, GAME OVER!")
        return True
    # Check if we have any empty letters to guess:
    for word in word_to_display:
        if "_ " in word:
            return False
    # If not, then player won
    print_table(word_to_display, total_lives)
    print("Congrats pal, you won!")
    return True


# We initialize the game, then in the main loop:
# - print the table (word to be guessed and lives)
# - get the input from the user and modify our board
# - check if the player won / lose
# - if so, check if he wants to play again
def main():
    to_guess, word_to_display, total_lives = init_game()
    while True:
        print_table(word_to_display, total_lives)
        word_to_display, total_lives = change_word_to_display(
            player_guess(word_to_display), word_to_display, to_guess, total_lives)
        if check_if_won(word_to_display, total_lives):
            if wanna_play_again():
                to_guess, word_to_display, total_lives = init_game()
            else:
                break


if __name__ == '__main__':
    main()
