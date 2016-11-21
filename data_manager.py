import os


# @file_name: string
def get_sentence_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "") for element in lines]
    return table


# get inputs and examine if OK:
def get_input(input_message):
    while True:
        try:
            user_input = input(input_message)
            if user_input.isdigit():
                raise ValueError
            break
        except ValueError:
            print("Please choose from the available options!")
            continue
        except (KeyboardInterrupt, EOFError):
            os.system('clear')
            print("bye")
            quit()
    return user_input
