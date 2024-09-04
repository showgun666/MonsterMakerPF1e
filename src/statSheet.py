#!/usr/bin/env python3
"""
Class for generating stat sheet.
"""
import src.helpers as help
SKILL_LIST = "src/tables/skillSummary.txt"

class StatBlock:
    "stat block class"
    def __init__(self):
        # Introduction Stats
        self.name = "creatureName"
        self.short_description = "short description of creature"
        self.cr = "1"
        self.xp = "400"           # BASED OFF cr
        self.race = "none"
        self.classes = []         # Contains information for stats to be used later
        self.alignment = "N"
        self.size = "Medium"
        self.type = "humanoid"
        self.subtypes = ""
        self.initiative = "0"     # CALCULATED
        self.senses = []
        self.auras = []

        # Defense
        self.ac = "10"            # CALCULATED
        self.ac_touch = "10"      # CALCULATED
        self.ac_flat_footed = "10"# CALCULATED
        self.ac_modifiers = "(armor size etc)"
        self.hp = "10"            # CALCULATED
        self.hd = "1"
        self.hd_size = "8"
        self.fortitude = "0"      # CALCULATED
        self.reflex = "0"         # CALCULATED
        self.will = "0"           # CALCULATED
        self.good_saves = []      # WILL BE USED FROM CLASS INSTEAD
        self.bad_saves = []
        self.defensive_abilities = []
        self.dr = "5/Bludgeoning"
        self.immunities = ["Cold", "Sonic"]
        self.resistances = ["Acid 10","Electricity 5"]
        self.spell_resistance = "18"
        self.weaknesses = "Fire"

        # Offense
        self.speed = ["30ft."]
        self.attacks_melee = []
        self.attacks_ranged = []
        self.space = "5"
        self.reach = "5"
        self.special_attacks = []
        self.spell_like_abilities = []
        self.spells_known_prepared = []

        # Tactics
        self.tactics = ""         # Before Combat, During Combat, Morale

        # Statistics
        self.strength = "10"
        self.dexterity = "10"
        self.constitution = "10"
        self.intelligence = "10"
        self.wisdom = "10"
        self.charisma = "10"

        self.bab = "0"
        self.cmb = "0"
        self.cmd = "10"

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

    def generate_stat_block_string_d20pfsrd(self):
        "generates a statblock as per d20pfsrd standard"

        stat_block_string = ""
        stat_block_string += self.name + "\n"
        stat_block_string += self.short_description + "\n\n"
        stat_block_string += self.name + "CR " + str(self.cr) + "\n\n"
        stat_block_string += "xp " + str(self.xp) + "\n"
        stat_block_string += self.alignment + " " + self.size + " " + self.type

        if self.subtypes:
            stat_block_string += " ("
            stat_block_string += help.comma_separated_string_from_list(self.subtypes)
            stat_block_string += ")"
        stat_block_string += "\n"
        stat_block_string += "Init +" + self.initiative + "; "
        stat_block_string += "Senses "
        if self.senses:
            stat_block_string += help.comma_separated_string_from_list(self.senses)
            stat_block_string += "; "
        stat_block_string += "Perception +" + self.initiative
        
        if self.auras:
            stat_block_string += help.comma_separated_string_from_list(self.auras)
        stat_block_string += "\n"

        stat_block_string += "\nDEFENSE\n\n"
        stat_block_string += "AC " + self.ac + ", "
        stat_block_string += "touch " + self.ac_touch + ", "
        stat_block_string += "flat-footed " + self.ac_flat_footed + "\n"

        stat_block_string += "hp " + self.hp + " "
        stat_block_string += self.hd + "d" + self.hd_size + "+" + "\n"# NEED TO ADD HP MODIFIER HERE. CON OR CHA OR WHATEVER IT IS FOR THE CREATURE
        stat_block_string += "Fort +" + self.fortitude + ", Ref +" + self.reflex + ", Will +" + self.will +"\n"

        defenses = []
        if self.dr:
            defenses.append("DR +" + self.dr)
        if self.immunities:
            defenses.append("Immune " + help.comma_separated_string_from_list(self.immunities))
        if self.resistances:
            defenses.append("Resistance " + help.comma_separated_string_from_list(self.resistances))
        if self.spell_resistance:
            defenses.append("SR " + self.spell_resistance)
        defense_string = ""
        for defense in defenses:
            defense_string += defense + "; "
        stat_block_string += defense_string.rstrip("; ")
        
        stat_block_string += "\n"

        if self.weaknesses:
            stat_block_string += "Weaknesses vulnerability to "
            stat_block_string += help.comma_separated_string_from_list(self.weaknesses)
            stat_block_string += "\n"

        stat_block_string += "\nOFFENSE\n\n"

        stat_block_string += "Speed "
        stat_block_string += help.comma_separated_string_from_list(self.speed)
        stat_block_string += "\n"


        stat_block_string += ""
        stat_block_string += ""
        stat_block_string += ""
        stat_block_string += ""
        return stat_block_string
