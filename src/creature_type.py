#!/usr/bin/env python3
"""
Class for handling creature types in creature class.
Creature type includes character class levels.
Handles things tied to creature type and hd progression. HD PROGRESSION MIGHT NEED TO BE BROKEN OUT INTO A DIFFERENT CLASS !!!!
"""
import src.helpers as helper_module
from src.constants import * # Continuously check that this * import is not loading unneccessary stuff.

class CreatureType:
    "Class for handling creature types"
    def __init__(self, given_creature_type="Humanoid"):
        self.creature_type = self.change_type(given_creature_type)

    def change_type(self, creature_type):
        "select type of stat block"
        self.creature_type_statistics = self.get_creature_type_dictionary(creature_type)

        self.type = self.creature_type_statistics["Type"]
        self.hit_die_size = self.creature_type_statistics["Hit Die"]
        self.bab_progression = self.creature_type_statistics["Base Attack Bonus (BAB)"]
        self.set_save_progression(self.creature_type_statistics["Good Saving Throws"])
        self.skill_ranks_per_hd = self.creature_type_statistics["Skill Ranks"]
        self.set_class_skills(self.get_class_skills_by_type())

    def set_default_hit_dice_by_cr(self):
        "set default hit dice based off CR and type"
        hit_dice_data_list = helper_module.generate_list_of_dictionaries(CREATURE_HIT_DICE)
        for creature_type_dictionary in hit_dice_data_list:
            if creature_type_dictionary["Creature Type"] == self.type:
                self.set_hd(creature_type_dictionary[self.get_cr()])
    def set_hd(self, given_hd):
        "set creature hd"
        self._hd = given_hd
        self.update_statistics_by_hit_dice()

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

    def get_creature_type_dictionary(self, creature_type):
        "get the dictionary for a specific creature type"
        creature_by_type = helper_module.generate_list_of_dictionaries(CREATURE_STATISTICS_BY_TYPE)
        for creature_type_dictionary in creature_by_type:
            if creature_type_dictionary["Type"] == creature_type:
                return creature_type_dictionary


    def set_save_progression(self, good_saves_list):
        "sets save progression for good and bad saves. Will, Fort, Ref"
        good_saves = good_saves_list.split(", ")
        if "Ref" in good_saves:
            self.reflex_progression = "Good Save"
        else:
            self.reflex_progression = "Bad Save"

        if "Fort" in good_saves:
            self.fortitude_progression = "Good Save"
        else:
            self.fortitude_progression = "Bad Save"

        if "Will" in good_saves:
            self.will_progression = "Good Save"
        else:
            self.will_progression = "Bad Save"

    def set_default_hit_dice_by_cr(self):
        "set default hit dice based off CR and type"
        hit_dice_data_list = helper_module.generate_list_of_dictionaries(CREATURE_HIT_DICE)
        for creature_type_dictionary in hit_dice_data_list:
            if creature_type_dictionary["Creature Type"] == self.type:
                self.set_hd(creature_type_dictionary[self.get_cr()])

    def set_hd(self, given_hd):
        "set creature hd"
        self._hd = given_hd
        self.update_statistics_by_hit_dice()
    def get_hd(self):
        "get creature hd"
        return self._hd

    def set_save_progression(self, good_saves_list):
        "sets save progression for good and bad saves. Will, Fort, Ref"
        good_saves = good_saves_list.split(", ")
        if "Ref" in good_saves:
            self.reflex_progression = "Good Save"
        else:
            self.reflex_progression = "Bad Save"

        if "Fort" in good_saves:
            self.fortitude_progression = "Good Save"
        else:
            self.fortitude_progression = "Bad Save"

        if "Will" in good_saves:
            self.will_progression = "Good Save"
        else:
            self.will_progression = "Bad Save"
