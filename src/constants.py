"Module with constant variables"

# TABLE FILE PATHS
SKILL_LIST = "src/tables/skillSummary.txt"
CREATURE_HIT_DICE = "src/tables/creatureHitDice.txt"
CREATURE_STATISTICS_BY_TYPE = "src/tables/creatureStatisticsByType.txt"
MONSTER_STATISTICS_BY_CR = "src/tables/monsterStatisticsByCR.txt"
CREATURE_SIZES = "src/tables/creatureSizes.txt"
EXPERIENCE_POINT_AWARDS = "src/tables/experiencePointAwards.txt"
NATURAL_ATTACKS = "src/naturalAttacks.txt"

# INDEX VALUES OF ATTRIBUTE SCORES
STR = 0
DEX = 1
CON = 2
INT = 3
WIS = 4
CHA = 5

# INDEX VALUES OF SAVING THROWS
FORT = 0
REF = 1
WILL = 2

# SAVE PROGRESSION BOOLEANS
GOOD = True
BAD = False

# DAMAGE DICE PROGRESSION LIST, 2 STEPS PER SIZE INCREASE
DAMAGE_DICE_PROGRESSION = [
    "1", "1d2", "1d3", "1d4", "1d6", "1d8",
    "1d10", "2d6", "2d8", "3d6", "3d8", "4d6",
    "4d8", "6d6", "6d8", "8d6", "8d8", "12d6",
    "12d8", "16d6", "16d8", "24d6", "24d8",
    "36d6", "36d8"
    ]
