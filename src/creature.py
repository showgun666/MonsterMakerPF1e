#!/usr/bin/env python3
"""
Class for creature
"""
import ability_scores as ability_scores_class
import src.creature_type as creature_type_class
import src.skills as skills_class
from src.constants import * # Continuously check that this * import is not loading unneccessary stuff.

class Creature:
    "Class for creatures"
    def __init__(self, creature_type="Humanoid", cr="1", ):
        ### MIGHT NEED TO PUT IN A LIST OR SOMETHING OF TYPES ETC
        # FOR MULTICLASSING OR HAVING MULTIPLE PROGRESSIONS WITH DIFFERENT TYPES
        self.set_cr(cr)
        self.attability_scores = ability_scores_class.AbilityScores()
        self.creature_type = creature_type_class.CreatureType(creature_type)
        self.skills = skills_class.Skills(self.creature_type.class_skills())

        self.set_default_hit_dice_by_cr()
        self.update_statistics_by_hit_dice()
        self.change_type(creature_type)

    def set_cr(self, given_cr):
        "sets cr value"
        self._cr = given_cr
    def get_cr(self):
        "get cr value"
        return self._cr


    def update_cmb_and_cmd(self):
        "updates values of cmb and cmd"

    def set_hd(self, given_hd):
        "set creature hd"
        self._hd = given_hd
        self.update_statistics_by_hit_dice()

    def get_hd(self):
        "get creature hd"
        return self._hd

    def set_default_hit_dice_by_cr(self):
        "set default hit dice based off CR and type"
        hit_dice_data_list = helper_module.generate_list_of_dictionaries(CREATURE_HIT_DICE)
        for creature_type_dictionary in hit_dice_data_list:
            if creature_type_dictionary["Creature Type"] == self.type:
                self.set_hd(creature_type_dictionary[self.get_cr()])

    def change_type(self, creature_type):
        "select type of stat block"
        self.creature_type_statistics = self.creature_type_dictionary(creature_type)

        self.type = self.creature_type_statistics["Type"]
        self.hit_die_size = self.creature_type_statistics["Hit Die"]
        # self.bab_progression = self.creature_type_statistics["Base Attack Bonus (BAB)"]
        self.set_save_progression(self.creature_type_statistics["Good Saving Throws"])
        self.skill_ranks_per_hd = self.creature_type_statistics["Skill Ranks"]
        self.set_class_skills(self.get_class_skills_by_type())

    def update_statistics_by_hit_dice(self):
        "updates statistics based off of hd"
        # Feats by hd
        self._feats_from_hd = str((int(self.get_hd()) // 2) + 1)
        # Skill ranks
        self._skill_ranks_from_hd = int(self.creature_type_statistics["Skill Ranks"]) * int(self.get_hd())
        # saves
        # hp
        # bab
        self._bab = str(int(bool(self.creature_type_statistics["Base Attack Bonus (BAB)"]) * int(self.get_hd()) // 1))
        # bab updates cmb and cmd
        # DCs
        # Ability Scores for creatures with class levels
