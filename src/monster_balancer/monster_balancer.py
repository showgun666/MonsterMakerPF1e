"""
This module is going to be handling intuitive balancing of monster statistics.

The idea behind the whole module:

For each CR a creature is expected to have roughly a certain value of HP, AC, Damage, Attack, Saves and DCs.
Lower values for lower CR and higher values for higher CR.

For a creature that has all the average values for a CR 10 monster, the monster should logically be CR 10.
If then the creature's HP value is adjusted to be just a little lower, it is still technically a CR 10.
Though a CR 10 with a lower than average Defensive score as well as a lower than average HP score.
If the creature's AC value is then increased a little bit to compensate, the theory is that it will again have an average Defensive score, even though the HP score is lower than average and the AC score is higher than average.
So if a creature with all statistics being those of a CR 10 creature except for the HP which is that of a CR 9 and the AC which is that of a CR 11 is still a CR 10 creature.
"""
from src.constants import MONSTER_STATISTICS_BY_CR
from src.helpers import generate_list_of_dictionaries

MONSTER_STATISTICS = generate_list_of_dictionaries(MONSTER_STATISTICS_BY_CR)

def get_statistic_column(statistic):
    """
    returns a list that only values of requested statistic.
    index 0 is CR 1/2 and following indexes are equal to the CR they represent.
    """
    statistic_column = []
    for row in MONSTER_STATISTICS:
        statistic_column.append(int(row[statistic]))
    return statistic_column

def get_average_damage_column():
    """
    returns a list that contains the average damage values per CR.
    index 0 is the lowest CR available.
    """
    low_damage_column = get_statistic_column("Average Damage Low")
    high_damage_column = get_statistic_column("Average Damage High")
    average_damage_column = []
    imax = len(low_damage_column)
    i = 0
    while i < imax:
        average_damage_column.append(int(((low_damage_column[i] + high_damage_column[i]) / 2) // 1))
        i += 1
    return average_damage_column

def determine_cr_float(statistic, given_value, target_cr=10):
    """
    statistic is the statistic that we are looking at, e.g. Hit Points or Armor Class
    given_value is the value that we have for that statistic and want to compare to.

    This function will return the determined CR value depending on given_value 
    """
    if statistic != "Damage":
        statistic_column = get_statistic_column(statistic)
    else:
        statistic_column = get_average_damage_column()

    if target_cr:
        target_cr = int(target_cr)
        index = target_cr
    else:
        index = len(statistic_column) // 2

    # Iterate through and find the right row in column.
    print("\n\n\n\n")
    print(statistic_column)
    print(f'given value: {given_value}')
    given_value = float(given_value)
    up = False
    down = False
    while index >= 0 and index < len(statistic_column):
        # If value is exactly same as an average value entry in the table, then simply return that CR value.
        # 0 means CR1/2
        value = statistic_column[index]

        print(f'index: {index}\nvalue: {value}\ngiven value: {given_value}')
        # If given value is lower than the lowest value in table
        # we have to raise an error now.
        if given_value < statistic_column[0]:
            raise ValueError(f'Given value {given_value} is lower than the lowest entry {statistic_column[0]} in table for {statistic}')
        elif given_value > statistic_column[-1]:
            raise ValueError(f'Given value {given_value} is higher than the highest entry {statistic_column[0]} in table for {statistic}')
        elif given_value == value:
            return_value = statistic_column.index(value)
            break
        # If it is not exactly the same as an average value entry in the table, then we do some math.
        elif given_value > value:
            print(f'\ngiven value {given_value} is higher than {value}')
            index += 1
            up = True
        else:
            print(f'\ngiven value {given_value} is lower than {value}')
            index -= 1
            down = True
        if up and down:
            low_value = statistic_column[index - 1]
            high_value = statistic_column[index]
            whole = high_value - low_value
            difference = given_value - low_value
            return_value = index - 1 + difference / whole
            break


    print(f"\nSuccessful!\n Returning {round(return_value, 2)}")
    ### ERROR HANDLING HERE?
    return round(return_value, 2)

def calculate_average_defensive_cr(cr_value_for_ac, cr_value_for_hp, cr_value_for_fort, cr_value_for_reflex, cr_value_for_will):
    """ Calculate average CR for defensive stats"""
    # Ensure that all values are floats and default to 0 if not provided
    cr_value_for_ac = float(cr_value_for_ac) if cr_value_for_ac is not None else 0.0
    cr_value_for_hp = float(cr_value_for_hp) if cr_value_for_hp is not None else 0.0
    cr_value_for_fort = float(cr_value_for_fort) if cr_value_for_fort is not None else 0.0
    cr_value_for_reflex = float(cr_value_for_reflex) if cr_value_for_reflex is not None else 0.0
    cr_value_for_will = float(cr_value_for_will) if cr_value_for_will is not None else 0.0


    # Calculate the average of saves
    saves = [cr_value_for_fort, cr_value_for_reflex, cr_value_for_will]
    cr_value_for_saves = sum(saves) / 3 if sum(saves) != 0 else 0.0

    total_defensive = cr_value_for_ac + cr_value_for_hp + cr_value_for_saves
    count = 0

    if cr_value_for_ac > 0:
        count += 1
    if cr_value_for_hp > 0:
        count += 1
    if cr_value_for_saves > 0:
        count += 1

    if count > 0:
        average_defensive_cr = total_defensive / 3
    else:
        average_defensive_cr = 0.0

    return round(average_defensive_cr, 3)

def calculate_average_offensive_cr(cr_value_for_attack, cr_value_for_damage, cr_value_for_dc, primarily_attacker, ability_reliant):
    """ Calculate average CR for offensive stats"""
    # Ensure that all values are floats and default to 0 if not provided
    cr_value_for_attack = float(cr_value_for_attack) if cr_value_for_attack is not None else 0.0
    cr_value_for_damage = float(cr_value_for_damage) if cr_value_for_damage is not None else 0.0
    cr_value_for_dc = float(cr_value_for_dc) if cr_value_for_dc is not None else 0.0

    values = [cr_value_for_damage]
    if primarily_attacker:
        values.append(cr_value_for_attack)
    if ability_reliant:
        values.append(cr_value_for_dc)
    count = len(values)
    total_offensive = sum(values) / count if sum(values) != 0 else 0.0

    return round(total_offensive, 3)

def armor_class_deviated(armor_class, target_cr):
    """
    Checks if armor class is deviating by 6 or more from target cr AC.
    Returns True if armor class deviates too much.
    Returns HIGH and LOW respectively as a string to determine in what direction the AC is differing.
    Returns MID if the AC is within the confines of what is deemed reasonable by the system.
    """
    ac_column = get_statistic_column("Armor Class")
    origin_ac = ac_column[int(target_cr)]

    if origin_ac > int(armor_class) + 5:
        return -1
    elif origin_ac < int(armor_class) - 5:
        return 1
    else:
        return 0

def get_damage_range_average_column():
    """
    returns a new damage column that contains average values.
    float values.
    """
    average_damage_column = []
    for row in MONSTER_STATISTICS:
        average_damage_column.append((row["Average Damage High"] + row["Average Damage Low"]) / 2)

    return average_damage_column

def get_attack_column(primary_weapon_user):
    """
    retrieves the attack column for high attack if true and low attack if false
    """
    if primary_weapon_user:
        return get_statistic_column("High Attack")
    return get_statistic_column("Low Attack")

def get_dc_column(primary_ability_user):
    """
    retrieves the DC column for primary ability DC if true and secondary DC if false
    """
    if primary_ability_user:
        return get_statistic_column("Primary Ability DC")
    return get_statistic_column("Secondary Ability DC")

def calculate_average_cr(average_defensive_cr, average_offensive_cr):
    """
    Calculates the average CR for the given defensive and offensive averages.
    Determines the suggested CR based on both the defensive and offensive CR values.
    
    If the result is close to an integer, it rounds in that direction:
    - If average CR is within 0.33 to 0.66, it rounds down for high offense / low defense
      and rounds up for high defense / low offense to suggest the nearest whole CR.
    """
    total_cr_values = average_defensive_cr + average_offensive_cr
    average_cr = total_cr_values / 2

    # Define the cutoff ranges for special rounding
    rounded_cr = round(average_cr)
    if abs(average_cr - rounded_cr) >= 0.33 and abs(average_cr - rounded_cr) <= 0.66:
        # High offense, low defense: round down if closer to lower bound
        if average_offensive_cr >= average_defensive_cr:
            average_cr = rounded_cr - 0.5 if average_cr < rounded_cr else rounded_cr
        # High defense, low offense: round up if closer to upper bound
        else:
            average_cr = rounded_cr + 0.5 if average_cr > rounded_cr else rounded_cr
    else:
        # Standard rounding outside of the cutoff range
        average_cr = round(average_cr)

    return int(average_cr // 1)

def get_min_max_value(statistic_column, target_cr_index, deviation=3):
    """
    Gets the minimum and maximum CR values that fall within the deviation range of the target CR.
    """
    deviation = int(deviation)
    target_cr = int(target_cr_index)
    length_of_column = len(statistic_column)
    # Handling out of range for minimum and maximum so we don't accidentally try to access indexes outside of range.
    if target_cr - deviation < 0:
        minimum = statistic_column[0]
    else:
        minimum = statistic_column[int(target_cr) - deviation]
    if target_cr + deviation > length_of_column:
        maximum = statistic_column[length_of_column - 1]
    else:
        maximum = statistic_column[int(target_cr) + deviation]
    return minimum, maximum
