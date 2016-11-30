from copy import deepcopy
import os
import data_manager
import random
import time


# This function gets the input from the user. It checks if the guess is
# a correct guess.
def player_guess(word_to_display):
    while True:
        try:
            input_guess = data_manager.get_input("Please enter a letter a-z: ")
            if len(input_guess) != 1:
                raise ValueError
            for word in word_to_display:
                if input_guess in word:
                    raise ValueError
            break
        except ValueError:
            print("Please try again!")
            continue
    return input_guess.lower()


# This changes the original sentence / word to a list of lists of "_"-s.
def print_word(to_guess):
    words = to_guess.split()
    word_to_display = []
    for word in words:
        if word == "!" or word == "?" or word == ",":
            word_to_display.append(word)
        else:
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
def print_table(word_to_display, lives, type_to_guess, name, score):
    os.system('clear')
    print("Hangman by Oli. Press ctrl + d to quit")
    print("User: %s\nScore: %s" % (name, score))
    print("\n")
    print(type_to_guess + ":" + "\n")
    print("Total guesses left: {}".format(lives))
    print()
    for word in word_to_display:
        print("".join(word), end=" ")
    print("\n")


# Check if the player wants to play again
def wanna_play_again():
    while True:
        play_again = data_manager.get_input("Do you want to play again? (y/n): ")
        if play_again == "y" or play_again == "n":
            break
        print("'y' or 'n' please!")
    if play_again == "y":
        return True
    else:
        os.system('clear')
        print("See ya!")
        return False


# player chooses a mode (easy, medium or hard)
def mode():
    while True:
        current_mode = data_manager.get_input("Choose a mode: easy ('e'), medium ('m') or hard ('h'): ")
        if current_mode == "e" or current_mode == "m" or current_mode == "h":
            break
        print("'e', 'm' or 'h' please!")
    return current_mode


# Initializing the game: setting the word to be guessed,
# change it to empty characters.
def init_game():
    while True:
        try:
            filename = data_manager.get_input("please enter a filename: ")
            sentences = data_manager.get_sentence_from_file(filename)
            break
        except (TypeError, FileNotFoundError):
            print("Oops, no such file. Please try again!")
            continue
    whole_sentence = random.choice(sentences)
    type_to_guess = whole_sentence.split(";")[0]
    to_guess = whole_sentence.split(";")[1]
    word_to_display = print_word(to_guess)
    return type_to_guess, to_guess, word_to_display


# initializing total lives
def init_lives():
    current_mode = mode()
    if current_mode == "h":
        total_lives = 5
    elif current_mode == "m":
        total_lives = 8
    elif current_mode == "e":
        total_lives = 10
    return total_lives, current_mode


# Check if the game has come to an end:
def check_if_won(word_to_display, total_lives, type_to_guess, to_guess, name, score, current_mode, dict_all_names):
    # First, we check if the player lost (has no lives left)
    if total_lives == 0:
        os.system('clear')
        print("Too bad, GAME OVER! The solution was: %s" % to_guess)
        return score, dict_all_names, True
    # Check if we have any empty letters to guess:
    for word in word_to_display:
        if "_ " in word:
            return score, dict_all_names, False
    # If not, then player won
    score, dict_all_names = score_gets_higher(name, score, current_mode, dict_all_names)
    print_table(word_to_display, total_lives, type_to_guess, name, score)
    print("Congrats pal, you won!")
    return score, dict_all_names, True


# asks player to enter a name or choose an existing one from the file
def make_dict_from_all_names():
    all_names = data_manager.get_sentence_from_file("export.csv")
    dict_all_names = {}
    for i in all_names:
        dict_all_names.update({i.split(";")[0]: i.split(";")[1]})
    return dict_all_names


# choose from an existing name
def choose_existing_name(dict_all_names):
    os.system("clear")
    names = []
    for i in dict_all_names.keys():
        names.append(i)
    print()
    for i, name in enumerate(names, 1):
        print(i, ": ", name, "; score: ", dict_all_names[name])
    while True:
        option = data_manager.get_input("choose from the existing names: (or type 'back' to Main Menu): ")
        if option.lower() == "back":
            return dict_all_names, names[0], dict_all_names[names[0]], False
        if option not in names:
            print("Oops, no such name. Please try again!")
            continue
        for n in names:
            if n == option:
                score = dict_all_names[n]
                return dict_all_names, n, score, True
            else:
                continue


# set a new player
def set_new_name(dict_all_names):
    os.system("clear")
    new_name = data_manager.get_input("Please enter a new name: (or type 'back' to Main Menu): ")
    score = None
    if new_name.lower() == "back":
        return dict_all_names, new_name, score, False
    dict_all_names.update({"new_name": "0"})
    score = 0
    return dict_all_names, new_name, score, True


# saves score of the player to our csv file.
def score_gets_higher(name, score, current_mode, dict_all_names):
    if current_mode == "e":
        dict_all_names[name] = int(score) + 1
    elif current_mode == "m":
        dict_all_names[name] = int(score) + 2
    elif current_mode == "h":
        dict_all_names[name] = int(score) + 3
    score = str(dict_all_names[name])
    list_of_names = []
    for k, v in dict_all_names.items():
        list_of_names.append([k, str(v)])
    data_manager.save_data_to_file("export.csv", list_of_names)
    return score, dict_all_names


def game_engine(dict_names, name, score, total_lives, current_mode):
    type_to_guess, to_guess, word_to_display = init_game()
    while True:
        print_table(word_to_display, total_lives, type_to_guess, name, score)
        word_to_display, total_lives = change_word_to_display(
            player_guess(word_to_display), word_to_display, to_guess, total_lives)
        score, dict_names, is_it_true = check_if_won(word_to_display, total_lives, type_to_guess,
                                                     to_guess, name, score, current_mode, dict_names)
        if is_it_true:
            if wanna_play_again():
                type_to_guess, to_guess, word_to_display = init_game()
            else:
                break
    return False


def handle_main_menu():
    os.system("clear")
    print("Main Menu \nPlease choose an option: ")
    print()
    list_to_print = ["New game", "Choose existing player", "Exit"]
    for i, op in enumerate(list_to_print, 1):
        print(i, ": %s" % op)


def choose():
    option = input("Please enter a number: ")
    if option == "1":
        dict_names, name, score, is_it_true = set_new_name(make_dict_from_all_names())
        total_lives = None
        current_mode = None
        if is_it_true is False:
            return dict_names, name, score, total_lives, current_mode, False
        total_lives, current_mode = init_lives()
    elif option == "2":
        dict_names, name, score, is_it_true = choose_existing_name(make_dict_from_all_names())
        total_lives = None
        current_mode = None
        if is_it_true is False:
            return dict_names, name, score, total_lives, current_mode, False
        total_lives, current_mode = init_lives()
    elif option == "3":
        os.system("clear")
        print("Bye!")
        quit()
    else:
        raise KeyError
    return dict_names, name, score, total_lives, current_mode, True


def main():
    while True:
        handle_main_menu()
        try:
            dict_names, name, score, total_lives, current_mode, is_it_true = choose()
            if is_it_true is False:
                continue
            os.system("clear")
            if game_engine(dict_names, name, score, total_lives, current_mode) is False:
                continue
        except KeyError:
            os.system("clear")
            print("There is no such option!")
            time.sleep(1)
            continue
        except (KeyboardInterrupt, EOFError):
            os.system('clear')
            print("bye")
            quit()


if __name__ == '__main__':
    main()
