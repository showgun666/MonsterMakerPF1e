#!/usr/bin/env python3
"""
Class for generating stat sheet.
"""
import src.helpers as helper
SKILL_LIST = "src/tables/skillSummary.txt"
CREATURE_HIT_DICE = "src/tables/creatureHitDice.txt"
CREATURE_STATISTICS_BY_TYPE = "src/tables/creatureStatisticsByType.txt"
MONSTER_STATISTICS_BY_CR = "src/tables/monsterStatisticsByCR.txt"

class StatBlock:
    "stat block class"
    def __init__(self, creature):
        # Introduction Stats
        self.name = "creatureName"
        self.short_description = "short description of creature"
        self.cr = creature.get_cr()
        self.xp = creature.get_xp_reward_by_cr(self.cr)           # BASED OFF cr
        self.race = "none"
        self.classes = []         # Contains information for stats to be used later
        self.alignment = "N"
        self.size = creature.size["Creature Size"]
        self.type = "NotSet"
        self.subtypes = ""
        self.initiative = creature.secondary_attributes.get_bonus(1)     # CALCULATED
        self.senses = []
        self.auras = []

        # Defense
        self.ac = creature.secondary_attributes.calculate_difficulty_class(1)            # CALCULATED
        self.ac_touch = creature.secondary_attributes.calculate_difficulty_class(1)      # CALCULATED
        self.ac_flat_footed = creature.secondary_attributes.calculate_difficulty_class(1)# CALCULATED
        self.ac_modifiers = "(armor size etc)"
        self.hp, self.bonus_hp = creature.secondary_attributes.get_hit_points(2)            # CALCULATED
        self.hd = str(len(creature.hit_dice.get_hit_dice()))
        self.hd_size = "8" #NEED TO BE ABLE TO GENERATE THE HP STRING BASED ON HIT DICE
        saves = creature.find_saves()
        self.fortitude = saves[0]
        self.reflex = saves[1]
        self.will = saves[2]
        self.good_saves = []      # WILL BE USED FROM CLASS INSTEAD
        self.bad_saves = []
        self.defensive_abilities = []
        self.dr = "5/Bludgeoning"
        self.immunities = ["Cold", "Sonic"]
        self.resistances = ["Acid 10","Electricity 5"]
        self.spell_resistance = "18"
        self.weaknesses = ["Fire"]

        # Offense
        self.speed = []
        for key, value in creature.secondary_attributes.speed.items():
            if value:
                self.speed.append(key + " " + str(value) + " ft.")
        self.attacks_melee = ['bite +25 (2d8+15)', '2 claws +25 (2d6+10)', '2 wings +23 (1d8+5)', 'tail slap +23 (2d6+15)'] # GENERATED WITH METHOD
        self.attacks_ranged = ['bow +25 (2d8+15)']
        self.space = "15 ft."
        self.reach = "5 ft. (10 ft. with bite)"
        self.special_attacks = ['breath weapon (50-ft. cone, DC 24, 12d10 fire)', 'crush (Small Creatures, DC 24, 2d8+15)']
        self.spell_like_abilities = []
        self.caster_level = "17th" # 1st / 3rd / 4th need to fix
        self.concentration = "+20" # Standard to have + or - here.
        self.spells_known_prepared = []

        # Tactics
        self.tactics = ""         # Before Combat, During Combat, Morale

        # Statistics
        self.attributes = {
            "str":creature.ability_scores.get_ability_score(0),
            "dex":creature.ability_scores.get_ability_score(1),
            "con":creature.ability_scores.get_ability_score(2),
            "int":creature.ability_scores.get_ability_score(3),
            "wis":creature.ability_scores.get_ability_score(4),
            "cha":creature.ability_scores.get_ability_score(5),
            }

        self.bab = "+17"
        self.cmb = "+29"
        self.cmd = "39 (43 vs. trip)"

        self.feats = ['Cleave', 'Greater Vital Strike',
                      'Improved Initiative', 'Improved Iron Will',
                      'Improved Vital Strike', 'Iron Will',
                      'Multiattack', 'Power Attack', 'Vital Strike']

        self.skills = creature.skills

        self.languages = ['Common', 'Draconic', 'Dwarven', 'Orc']

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
            stat_block_string += helper.comma_separated_string_from_list(self.subtypes)
            stat_block_string += ")"
        stat_block_string += "\n"
        stat_block_string += "Init +" + str(self.initiative) + "; "
        stat_block_string += "Senses "
        if self.senses:
            stat_block_string += helper.comma_separated_string_from_list(self.senses)
            stat_block_string += "; "
        stat_block_string += "Perception +" + str(self.skills.find_skill("Perception")["Modifier"])

        if self.auras:
            stat_block_string += helper.comma_separated_string_from_list(self.auras)
        stat_block_string += "\n"

        stat_block_string += "\nDEFENSE\n\n"
        stat_block_string += "AC " + str(self.ac) + ", "
        stat_block_string += "touch " + str(self.ac_touch) + ", "
        stat_block_string += "flat-footed " + str(self.ac_flat_footed) + "\n"

        stat_block_string += "hp " + str(self.hp) + " ("
        stat_block_string += str(self.hd) + "d" + str(self.hd_size) + "+" + str(self.bonus_hp) + ")\n"# NEED TO ADD HP MODIFIER HERE. CON OR CHA OR WHATEVER IT IS FOR THE CREATURE
        stat_block_string += "Fort +" + str(self.fortitude) + ", Ref +" + str(self.reflex) + ", Will +" + str(self.will) +"\n"

        defenses = []
        if self.dr:
            defenses.append("DR +" + self.dr)
        if self.immunities:
            defenses.append("Immune " + helper.comma_separated_string_from_list(self.immunities))
        if self.resistances:
            defenses.append("Resistance " + helper.comma_separated_string_from_list(self.resistances))
        if self.spell_resistance:
            defenses.append("SR " + self.spell_resistance)
        defense_string = ""
        for defense in defenses:
            defense_string += defense + "; "
        stat_block_string += defense_string.rstrip("; ")
        
        stat_block_string += "\n"

        if self.weaknesses:
            stat_block_string += "Weaknesses vulnerability to "
            stat_block_string += helper.comma_separated_string_from_list(self.weaknesses)
            stat_block_string += "\n"

        stat_block_string += "\nOFFENSE\n\n"

        stat_block_string += "Speed "
        stat_block_string += helper.comma_separated_string_from_list(self.speed)
        stat_block_string += "\n"

        if self.attacks_melee:
            melee_string = "Melee "
            for melee_attack in self.attacks_melee:
                melee_string += melee_attack + ", "
            stat_block_string += melee_string.rstrip(", ") + "\n"
        if self.attacks_ranged:
            ranged_string = "Ranged "
            for ranged_attack in self.attacks_ranged:
                ranged_string += ranged_attack + ", "
            stat_block_string += ranged_string.rstrip(", ") + "\n"

        stat_block_string += "Space " + self.space + "; "
        stat_block_string += "Reach " + self.reach
        stat_block_string += "\n"

        if self.special_attacks:
            special_attack_string = "Special Attacks "
            for special_attack in self.special_attacks:
                special_attack_string += special_attack + ", "
            stat_block_string += special_attack_string.rstrip(", ") + "\n"

        if self.spell_like_abilities:
            spell_like_abilities_string = "Spell-like Abilities "
            spell_like_abilities_string += "(" + self.caster_level + ", " + self.concentration + ")\n"
            ### WE ADD MAGIC AND SPELLS LATER. NOT IMPORTANT FOR ALL CREATURES WITHOUT THEM SO NOT PART OF CORE CORE CORE

        stat_block_string += "\nSTATISTICS\n\n"
        attributes_string = ""
        for attribute, score in self.attributes.items():
            attributes_string += attribute + " " + str(score) + ", "
        stat_block_string += attributes_string.rstrip(", ") + "\n"

        stat_block_string += "BAB " + self.bab + "; CMB " + self.cmb + "; CMD " + self.cmd + "\n"

        if self.feats:
            feats_string = "Feats "
            for feat in self.feats:
                feats_string += feat + ", "
            stat_block_string += feats_string.rstrip(", ") + "\n"

        ### NEED TO MAKE SOMETHING MORE SOPHISTICATED FOR SKILL BONUSES LATER ###
        trained_skills_list = []
        for i in self.skills._skills:
            if int(i["Skill Ranks"]) > 0:
                trained_skills_list.append(i["Skill"] + " +" + i["Skill Ranks"])
        if trained_skills_list:
            trained_skills_string = "Skills "
            for i in trained_skills_list:
                trained_skills_string += i + ", "
            stat_block_string += trained_skills_string.rstrip(", ") + "\n"


        if self.languages:
            languages_string = "Languages "
            for language in self.languages:
                languages_string += language + ", "
            stat_block_string += languages_string.rstrip(", ") + "\n"


        if self.special_abilities:
            stat_block_string += "\nSPECIAL ABILITIES\n\n"
            special_abilities_string = ""
            for special_ability in self.special_abilities:
                special_abilities_string += special_ability + ", "
            stat_block_string += special_abilities_string.rstrip(", ") + "\n"

        ### NEED TO ADD ECOLOGY STUFF AS WELL

        stat_block_string += ""
        stat_block_string += ""
        stat_block_string += ""
        stat_block_string += ""
        return stat_block_string
