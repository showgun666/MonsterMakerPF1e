"Module with constant variables"

# TABLE FILE PATHS
SKILL_LIST = "src/tables/skillSummary.txt"
CREATURE_HIT_DICE = "src/tables/creatureHitDice.txt"
CREATURE_STATISTICS_BY_TYPE = "src/tables/creatureStatisticsByType.txt"
MONSTER_STATISTICS_BY_CR = "src/tables/monsterStatisticsByCR.txt"
CREATURE_SIZES = "src/tables/creatureSizes.txt"
EXPERIENCE_POINT_AWARDS = "src/tables/experiencePointAwards.txt"
NATURAL_ATTACKS = "src/tables/equipment/naturalAttacks.txt"
SIMPLE_ONE = "src/tables/equipment/simpleOne-HandedMeleeWeapons.txt"
SIMPLE_UNARMED = "src/tables/equipment/simpleUnarmedAttacks.txt"
SIMPLE_LIGHT = "src/tables/equipment/simpleLightMeleeWeapons.txt"
SIMPLE_TWO = "src/tables/equipment/simpleTwo-HandedMeleeWeapons.txt"
SIMPLE_RANGED = "src/tables/equipment/simpleRangedWeapons.txt"
MARTIAL_ONE = "src/tables/equipment/martialOne-HandedMeleeWeapons.txt"
MARTIAL_LIGHT = "src/tables/equipment/martialLightMeleeWeapons.txt"
MARTIAL_TWO = "src/tables/equipment/martialTwo-HandedMeleeWeapons.txt"
MARTIAL_RANGED = "src/tables/equipment/martialRangedWeapons.txt"
EXOTIC_ONE = "src/tables/equipment/exoticOne-HandedMeleeWeapons.txt"
EXOTIC_LIGHT = "src/tables/equipment/exoticLightMeleeWeapons.txt"
EXOTIC_TWO = "src/tables/equipment/exoticTwo-HandedMeleeWeapons.txt"
EXOTIC_RANGED = "src/tables/equipment/exoticRangedWeapons.txt"

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
SIZES_LIST = [
    "Fine",
    "Diminutive",
    "Tiny",
    "Small",
    "Medium",
    "Large",
    "Huge",
    "Gargantuan",
    "Colossal",
    ]
"""
If the size increases by one step, look up the original damage on the chart and increase the damage by two steps.
If the initial size is Small or lower (or is treated as Small or lower) or the initial damage is 1d6 or less, instead increase the damage by one step.

If the size decreases by one step, look up the original damage on the chart and decrease the damage by two steps.
If the initial size is Medium or lower (or is treated as Medium or lower) or the initial damage is 1d8 or less, instead decrease the damage by one step.

If the exact number of original dice is not found on this chart, apply the following before adjusting the damage dice.
If the damage is a number of d6, find the next lowest number of d6 on the chart and use that number of d8 as the original damage value (for example, 10d6 would instead be treated as 8d8).
If the damage is a number of d8, find the next highest number of d8 on the chart and use that number of d6 as the original damage value (for example, 5d8 would instead be treated as 6d6).
Once you have the new damage value, adjust by the number of steps noted above.

If the die type is not referenced on this chart, apply the following rules before adjusting the damage dice.
2d4 counts as 1d8 on the chart, 3d4 counts as 2d6 on the chart, and so on for higher numbers of d4. 1d12 counts as 2d6 on the chart, and so on for higher numbers of d12.

Finally, 2d10 increases to 4d8 and decreases to 2d8, regardless of the initial size, and so on for higher numbers of d10.
"""
