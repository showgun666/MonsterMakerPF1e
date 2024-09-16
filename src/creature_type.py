#!/usr/bin/env python3
"""
Class for handling creature types in creature class.
Creature type includes character class levels.
Handles things tied to creature type.
"""
import src.helpers as helper_module
from src.constants import CREATURE_STATISTICS_BY_TYPE, CREATURE_HIT_DICE
from src.constants import GOOD, BAD, WILL, FORT, REF, SKILL_LIST

class CreatureType:
    "Class for handling creature types"
    def __init__(self, given_creature_type="Humanoid"):
        self.creature_type_statistics = self.creature_type_dictionary(given_creature_type)
        self.creature_type_statistics["Hit Die"] = int(self.creature_type_statistics["Hit Die"])
        bab = float(self.creature_type_statistics["Base Attack Bonus (BAB)"])
        self.creature_type_statistics["Base Attack Bonus (BAB)"] = bab
        sr = int(self.creature_type_statistics["Skill Ranks"])
        self.creature_type_statistics["Skill Ranks"] = sr

        self.saving_throw_progression = [None, None, None]
        self.set_save_progression(self.creature_type_statistics["Good Saving Throws"])
        self.saving_throw_progression = self.get_save_progressions()

    def creature_type_dictionary(self, creature_type):
        "get the dictionary for a specific creature type"
        creature_by_type = helper_module.generate_list_of_dictionaries(CREATURE_STATISTICS_BY_TYPE)
        return next((ct for ct in creature_by_type if ct["Type"] == creature_type), None)


    def hd_size(self):
        "returns hd size for current creature type as integer."
        return int(self.creature_type_statistics["Hit Die"])


    def bab_progression(self):
        "returns BAB progression rate for current creature type as a float"
        return float(self.creature_type_statistics["Base Attack Bonus (BAB)"])


    def set_class_skills(self):
        "returns class skills according to type as list"
        class_skill_list = []
        if self.creature_type_statistics["Class Skills"] != "None":
            class_skill_list = self.creature_type_statistics["Class Skills"].split(", ")

        for index, _ in enumerate(class_skill_list):
            if class_skill_list[index] == "Knowledge (all)":
                for entry in helper_module.generate_list_of_dictionaries(SKILL_LIST):
                    if "Knowledge" in entry["Skill"]:
                        class_skill_list.append(entry["Skill"])
                class_skill_list.pop(index)
                break
        return class_skill_list

    def skill_ranks_per_hd(self):
        "returns integer how many skill ranks type gain per hd"
        return self.creature_type_statistics["Skill Ranks"]


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


    def hit_dice_by_cr(self, cr):
        "returns how many hit dice are expected for a given CR of type"
        cr_statistics = helper_module.generate_list_of_dictionaries(CREATURE_HIT_DICE)
        for i, _ in enumerate(cr_statistics):
            if cr_statistics[i]["Creature Type"] == str(self):
                hit_dice_amount = cr_statistics[i][str(cr)]
        return int(hit_dice_amount)


    def __str__(self):
        "magic method, string returns type"
        return self.creature_type_statistics["Type"]
