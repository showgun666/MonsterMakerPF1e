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

