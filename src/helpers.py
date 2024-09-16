"module for helper functions"
import csv

def generate_list_of_dictionaries(text_file):
    "Generates a list of dictionaries from given csv table"
    with open(text_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        return [row for row in reader]

def comma_separated_string_from_list(given_list):
    "Generates a comma separated string"
    comma_separated_string = ""
    if len(given_list) > 1:
        for i in given_list:
            comma_separated_string += i + ", "
    else:
        comma_separated_string += given_list[0]

    return comma_separated_string.rstrip(", ")
