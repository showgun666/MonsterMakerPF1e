#!/usr/bin/env python3
"""
Class for creature
"""
import src.helpers as helper
SKILL_LIST = "src/tables/skillSummary.txt"
CREATURE_HIT_DICE = "src/tables/creatureHitDice.txt"
CREATURE_STATISTICS_BY_TYPE = "src/tables/creatureStatisticsByType.txt"
MONSTER_STATISTICS_BY_CR = "src/tables/monsterStatisticsByCR.txt"

class Creature:
    "Class for creatures"
    def __init__(self, creature_type="Humanoid", cr="1", ):
        self.skills = helper.generate_list_of_dictionaries(SKILL_LIST)

        self.change_type(creature_type)
        self.set_class_skills_by_type()
        self.set_cr(cr)
        self.set_default_hit_dice_by_cr()
        self.update_statistics_by_hit_dice()

        self._attributes = {
            "Str": "10",
            "Dex": "10",
            "Con": "10",
            "Int": "10",
            "Wis": "10",
            "Cha": "10"
            }


    def change_type(self, creature_type):
        "select type of stat block"
        self.creature_type_statistics = self.get_creature_type_dictionary(creature_type)

        self.type = self.creature_type_statistics["Type"]
        self.hit_die_size = self.creature_type_statistics["Hit Die"]
        self.bab_progression = self.creature_type_statistics["Base Attack Bonus (BAB)"]
        self.set_save_progression(self.creature_type_statistics["Good Saving Throws"])
        self.skill_ranks_per_hd = self.creature_type_statistics["Skill Ranks"]
        self.set_class_skills_by_type()


    def set_default_hit_dice_by_cr(self):
        "set default hit dice based off CR and type"
        hit_dice_data_list = helper.generate_list_of_dictionaries(CREATURE_HIT_DICE)
        for creature_type_dictionary in hit_dice_data_list:
            if creature_type_dictionary["Creature Type"] == self.type:
                self.set_hd(creature_type_dictionary[self.get_cr])
    def set_hd(self, given_hd):
        "set creature hd"
        self._hd = given_hd
        self.update_statistics_by_hit_dice()
    def get_hd(self):
        "get creature hd"
        return self._hd

    def set_cr(self, given_cr):
        "sets cr value"
        self._cr = given_cr
    def get_cr(self):
        "get cr value"
        return self._cr

    def set_attribute(self, attribute):
        "set one of the attributes" # NEED UPDATE METHODS FOR ALL THINGS RELATED TO DIFFERENT ATTRIBUTES
    def set_strength(self, score):
        "set strength attribute"
    def set_dexterity(self, score):
        "set dexterity attribute"
    def set_constitution(self, score):
        "set constitution attribute"
    def set_intelligence(self, score):
        "set intelligence attribute"
    def set_wisdom(self, score):
        "set wisdom attribute"
    def set_charisma(self, score):
        "set charisma attribute"

    def update_statistics_by_hit_dice(self):
        "updates statistics based off of hd"
        # Feats by hd
        self._feats_from_hd = str((int(self.get_hd) // 2) + 1)
        # Skill ranks
        self._skill_ranks_from_hd = int(self.creature_type_statistics["Skill Ranks"]) * int(self.get_hd)
        # saves
        # hp
        # bab
        self._bab = str(int(bool(self.creature_type_statistics["Base Attack Bonus (BAB)"]) * int(self.get_hd) // 1))
        # bab updates cmb and cmd
        # DCs
        # Ability Scores for creatures with class levels


    def update_cmb_and_cmd(self):
        "updates values of cmb and cmd"


    def set_class_skills_by_type(self):
        "sets class skills according to type"
        self.class_skills_list = []
        if self.creature_type_statistics["Class Skills"] != "None":
            type_class_skills = self.creature_type_statistics["Class Skills"].split(", ")
        for i, entry in enumerate(type_class_skills):
            if "Knowledge (pick one)" == entry:
                # PICK A KNOWLEDGE THAT IS NOT A CLASS SKILL
                # FOR NOW WE JUST POP IT. IT IS BROKEN
                # FIX THIS LATER
                type_class_skills.pop(i)
            if "plus" in entry:
                # FIX THIS ANOTHER TIME
                # ONE CASE IS FOR CLASS SKILLS COMBINED WITH CREATURE TYPE
                # ONE CASE IS FOR OUTSIDERS THAT HAVE +4
                type_class_skills.pop(i)
            if "Knowledge (all)" in entry:
                type_class_skills.pop(i)
                for skill in self.skills:
                    if "Knowledge" in skill["Skill"]:
                        type_class_skills.append(skill["Skill"])


    def get_creature_type_dictionary(self, creature_type):
        "get the dictionary for a specific creature type"
        creature_by_type = helper.generate_list_of_dictionaries(CREATURE_STATISTICS_BY_TYPE)
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
