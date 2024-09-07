#!/usr/bin/env python3
"""
Class for handling creature types in creature class.
Creature type includes character class levels.
Handles things tied to creature type.
"""
import src.helpers as helper_module
from src.constants import CREATURE_STATISTICS_BY_TYPE, GOOD, BAD, WILL, FORT, REF

class CreatureType:
    "Class for handling creature types"
    def __init__(self, given_creature_type="Humanoid"):
        self.creature_type_statistics = self.creature_type_dictionary(given_creature_type)
        self.set_save_progression(self.creature_type_statistics["Good Saving Throws"])
        self.saving_throw_progression = self.get_save_progressions()

    def creature_type_dictionary(self, creature_type):
        "get the dictionary for a specific creature type"
        creature_by_type = helper_module.generate_list_of_dictionaries(CREATURE_STATISTICS_BY_TYPE)
        for creature_type_dictionary in creature_by_type:
            if creature_type_dictionary["Type"] == creature_type:
                return creature_type_dictionary


    def hd_size(self):
        "returns hd size for current creature type as integer."
        return int(self.creature_type_statistics["Hit Die"])


    def bab_progression(self):
        "returns BAB progression rate for current creature type as a float"
        return float(self.creature_type_statistics["Base Attack Bonus (BAB)"])


    def class_skills(self):
        "returns class skills according to type as list"
        class_skill_list = []
        if self.creature_type_statistics["Class Skills"] != "None":
            class_skill_list = self.creature_type_statistics["Class Skills"].split(", ")
        return class_skill_list

    def skill_ranks_per_hd(self):
        "returns integer how many skill ranks type gain per hd"
        return int(self.creature_type_statistics["Skill Ranks"])


    def set_save_progression(self, good_saves_list):
        "sets save progression for good and bad saves. Will, Fort, Ref"
        good_saves = good_saves_list.split(", ")
        if "Ref" in good_saves:
            self.saving_throw_progression[REF] = GOOD
        else:
            self.saving_throw_progression[REF] = BAD

        if "Fort" in good_saves:
            self.saving_throw_progression[FORT] = GOOD
        else:
            self.saving_throw_progression[FORT] = BAD

        if "Will" in good_saves:
            self.saving_throw_progression[WILL] = GOOD
        else:
            self.saving_throw_progression[WILL] = BAD

    def get_save_progressions(self):
        "returns save progressions as a list"
        return self.saving_throw_progression


    def __str__(self):
        "magic method, string returns type"
        return self.creature_type_statistics["Type"]
