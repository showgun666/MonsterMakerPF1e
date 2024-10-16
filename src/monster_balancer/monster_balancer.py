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

def determine_cr_float(statistic, given_value):
    """
    statistic is the statistic that we are looking at, e.g. Hit Points or Armor Class
    given_value is the value that we have for that statistic and want to compare to.

    This function will return the determined CR value depending on given_value 
    """

    statistic_column = get_statistic_column(statistic)
    # Iterate through and find the right row in column.
    index = 0
    for value in statistic_column:
        # If value is exactly same as an average value entry in the table, then simply return that CR value.
        # 0 means CR1/2
        if given_value == value:
            return_value = statistic_column.index(value)
            break
        # If given value is lower than the lowest value in table
        # we have to raise an error now.
        elif given_value < statistic_column[0]:
            raise ValueError(f'Given value {given_value} is lower than the lowest entry {statistic_column[0]} in table for {statistic}')
        elif given_value > statistic_column[-1]:
            raise ValueError(f'Given value {given_value} is higher than the highest entry {statistic_column[0]} in table for {statistic}')
        # If it is not exactly the same as an average value entry in the table, then we do some math.
        elif value > given_value:
            low_value = statistic_column[index - 1]
            high_value = statistic_column[index]
            whole = high_value - low_value
            difference = given_value - low_value
            return_value = index - 1 + difference / whole
            break
        index += 1
    ### ERROR HANDLING HERE?
    return round(return_value, 2)
