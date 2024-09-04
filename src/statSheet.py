#!/usr/bin/env python3
"""
Class for generating stat sheet.
"""
import helpers as help
SKILL_LIST = "src/tables/skillSummary.txt"

class StatBlock:
    "stat block class"
    def __init__(self) -> None:
        # Introduction Stats
        self.name = "creatureName"
        self.short_description = "short description of creature"
        self.cr = 1
        self.xp = 400           # BASED OFF cr
        self.race = "none"
        self.classes = []
        self.alignment = "N"
        self.size = "Medium"
        self.type = "humanoid"
        self.subtypes = ""
        self.initiative = 0     # CALCULATED
        self.senses = []
        self.auras = []

        # Defense
        self.ac = 10            # CALCULATED
        self.hp = 10            # CALCULATED
        self.fortitude = 0      # CALCULATED
        self.reflex = 0         # CALCULATED
        self.will = 0           # CALCULATED
        self.defensive_abilities = []
        self.dr = ""
        self.immunities = []
        self.resistances = []
        self.spell_resistance = ""
        self.weaknessess = ""

        # Offense
        self.speed = 30
        self.attacks_melee = []
        self.attacks_ranged = []
        self.space = 5
        self.reach = 5
        self.special_attacks = []
        self.spell_like_abilities = []
        self.spells_known_prepared = []

        # Tactics
        self.tactics = "" # Before Combat, During Combat, Morale

        # Statistics
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10

        self.bab = 0
        self.cmb = 0
        self.cmd = 10

        self.feats = []

        self.skills = help.generate_list_of_dictionaries(SKILL_LIST)

        self.languages = []

        self.special_qualities = []

        # Special Abilities
        self.special_abilities = []

        # Ecology
        self.environment = ""
        self.organization = ""
        self.treasure = ""
        self.ecological_information = ""
        self.miscellaneous = ""

        self.stat_block_string = ""

    def generate_stat_block_d20pfsrd(self):
        "generates a statblock as per d20pfsrd standard"
        stat_block_string = ""
        stat_block_string += self.name + "\n\n\n\n"
        stat_block_string += self.short_description + "\n\n"
        stat_block_string += self.name + str(self.cr) + "\n\n"
        stat_block_string += "xp " + str(self.xp) + "\n"
        stat_block_string += self.alignment + " " + self.size + " " + self.type

        if self.subtypes:
            stat_block_string += " ("
            for subtype in self.subtypes:
                stat_block_string += subtype
                stat_block_string += ", "
            stat_block_string.rstrip(2)
            stat_block_string += ")"

        stat_block_string += "Init +" + self.initiative + "; "
        stat_block_string += "Senses "
        for sense in self.senses:
            stat_block_string += sense
            stat_block_string += ", "
            stat_block_string.rstrip(2)
            stat_block_string += "; "
            stat_block_string += "Perception +" self.initiative

        return stat_block_string
