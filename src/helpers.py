"module for helper functions"
import csv
import re
from src.constants import CREATURE_SIZES, DAMAGE_DICE_PROGRESSION, SIZES_LIST
from src.exceptions import SearchMiss

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

def closest_integer(low_int, high_int, given_int):
    """
    Finds the closest integer
    returns closest integer to given_int
    if equally far, gives low(because always round down)
    """
    diff1 = abs(low_int - given_int)
    diff2 = abs(high_int - given_int)
    if diff1 > diff2:
        return high_int
    else:
        return low_int

def average_dice(dice_str):
    """
    Gives average result rounded down of dice string
    """
    # In case of number
    if re.match(r'^[+-]?\d+$', dice_str):
        return int(dice_str)

    matched_dice_rolls = re.match(r'([+-]?\d*)d(\d+)', dice_str)

    if matched_dice_rolls:
        num_dice = int(matched_dice_rolls.group(1))
        dice_size = int(matched_dice_rolls.group(2))

        return int(num_dice/abs(num_dice)) * int((abs(num_dice) * ((1 + dice_size) / 2)) // 1)

    raise ValueError(f'Unknown dice expression: {dice_str}')

def get_average_dice(expression):
    """
    recursively finds average result of die string
    """
    expression = expression.strip()

    terms = re.findall(r'[+-]?\d*d\d+|[+-]?\d+', expression)

    total = sum(average_dice(term) for term in terms)

    return total

def damage_dice_by_size_conversion(dice, original_size, new_size):
    """
    dice is string such as 1d6
    size is the size category such as small
    """
    if new_size == original_size:
        return dice

    original_size_index = 0
    i = 0
    # Only goes up to colossal. Can't handle larger differences. Fine is also smallest
    for size in SIZES_LIST:
        if size == original_size:
            original_size_index = i
        i += 1
    size_difference = get_size_difference(original_size, new_size)

    # IF dice are in progression chart we can move according to chart
    i = None
    if dice in DAMAGE_DICE_PROGRESSION:
        damage_dice = change_damage_dice_size(dice, original_size_index, size_difference)
    # ELSE we convert dice to something that can move along progression chart
    elif parse_dice(dice)[1] == 10:
        if size_difference > 0:
            damage_dice = f'{parse_dice(dice)[0]*2}d8'
        else:
            damage_dice = f'{parse_dice(dice)[0]}d8'
    else:
        damage_dice = change_damage_dice_size(get_adjusted_damage_dice(dice), original_size_index, size_difference)
    return damage_dice

def get_size_difference(original_size, new_size):
    """
    returns size difference as an integer.
    """
    original_size_index = 0
    new_size_index = 0
    i = 0
    # Get indexes of original size and new size
    # Only goes up to colossal. Can't handle larger differences.
    for size in SIZES_LIST:
        if size == original_size:
            original_size_index = i
        if size == new_size:
            new_size_index = i
        i += 1
    # DIFFERENCE of current and target size in chart.
    # Negative number means go backwards
    # Positive number means go forwards
    return new_size_index - original_size_index

def get_adjusted_damage_dice(dice):
    """
    returns adjusted damage dice
    If the damage is a number of d6,
    find the next lowest number of d6 on the chart and use that number of d8 
    (for example, 10d6 would instead be treated as 8d8).

    If the damage is a number of d8,
    find the next highest number of d8 on the chart and use that number of d6
    (for example, 5d8 would instead be treated as 6d6).
    """
    die_values = parse_dice(dice)
    i = 1
    if die_values[1] == 8:
        while i < 36:
            if f'{die_values[0] + i}d6' in DAMAGE_DICE_PROGRESSION:
                damage_dice = f'{die_values[0] + i}d6'
                break
            i += 1
    elif die_values[1] == 6:
        while i > 0:
            if f'{die_values[0] - i}d8' in DAMAGE_DICE_PROGRESSION:
                damage_dice = f'{die_values[0] - i}d8'
                break
            i += 1
    elif die_values[1] == 4 and die_values[0]%2 == 0:
        damage_dice = f'{int(die_values[0]/2)}d8'
    elif die_values[1] == 4 and die_values[0]%3 == 0:
        damage_dice = f'{int(die_values[0]/3*2)}d6'
    elif die_values[1] == 12:
        damage_dice = f'{int(die_values[0])*2}d6'
    else:
        raise ValueError(f'{dice} not an accounted damage dice expression.')
    return damage_dice

def change_damage_dice_size(dice, size_index, size_difference):
    """
    gets new damage value based on damage dice progression chart
    """
    if size_difference == 0:
        return dice
    i = DAMAGE_DICE_PROGRESSION.index(dice)
    # IF size difference is positive and original size is medium or larger
    if size_difference > 0 and size_index >= 4:
        if dice not in DAMAGE_DICE_PROGRESSION[:5]:
            damage_dice = DAMAGE_DICE_PROGRESSION[i+2]
        else:
            damage_dice = DAMAGE_DICE_PROGRESSION[i+1]
    # IF size difference is negative and original size is medium or larger
    elif size_difference < 0 and size_index >=4:
        if dice not in DAMAGE_DICE_PROGRESSION[:6]:
            damage_dice = DAMAGE_DICE_PROGRESSION[i-2]
        else:
            damage_dice = DAMAGE_DICE_PROGRESSION[i-1]
    # IF size difference is positive and original size is small or smaller
    elif size_difference > 0 and size_index <= 3:
        damage_dice = DAMAGE_DICE_PROGRESSION[i+1]
    # IF Size difference is negative and original size is small or smaller
    elif size_difference < 0 and size_index <= 3:
        damage_dice = DAMAGE_DICE_PROGRESSION[i-1]

    if size_difference > 0:
        newdiff = size_difference -1
        size_index += 1
    else:
        newdiff = size_difference +1
        size_index -= 1

    return change_damage_dice_size(damage_dice, size_index, newdiff)

def find_size(size):
    "returns dictionary of size"
    sizes = generate_list_of_dictionaries(CREATURE_SIZES)
    for category in sizes:
        if size in next(iter(category)):
            return category
    raise SearchMiss(f'Could not find size category {size}.')

def parse_dice(dice):
    """
    parses dice and returns (dice_number, die_size)
    """
    dice_number, die_size = dice.split("d")
    return (int(dice_number), int(die_size))
