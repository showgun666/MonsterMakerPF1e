"module for helper functions"

def generate_list_of_dictionaries(text_file):
    "Generates a list of dictionaries from given csv table"
    with open(text_file, 'r', encoding='utf-8') as file:
        row = 0
        columns = []
        data = []

        for line in file:
            if row == 0:
                columns = line.split(";")
                row +=1
                continue
            dictionary = {}
            row_values = line.split(";")
            for i, _ in enumerate(columns):
                dictionary[columns[i].replace("\n", "")] = row_values[i].replace("\n", "")
            data.append(dictionary)
            row += 1

    return data

def comma_separated_string_from_list(given_list):
    "Generates a comma separated string"
    comma_separated_string = ""
    if len(given_list) > 1:
        for i in given_list:
            comma_separated_string += i + ", "
    else:
        comma_separated_string += given_list[0]

    return comma_separated_string.rstrip(", ")
