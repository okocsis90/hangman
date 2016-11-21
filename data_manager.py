# @file_name: string
def get_sentence_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "") for element in lines]
    return table
