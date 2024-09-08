#!/usr/bin/env python3
"""
Class for hit dice for HitDice class
"""

class HitDie:
    "class for handling hit die related things for creature class"
    def __init__(self, creature_type):
        self._type_statistics = creature_type
        self._type = str(creature_type)
        self._hit_die = creature_type.hd_size()
        self._bab = creature_type.bab_progression()
        self._save_progression = creature_type.get_save_progression()
        self._skill_ranks = creature_type.skill_ranks_per_hd()
        self._class_skills = creature_type.class_skills()

    def set_type(self, new_creature_type):
        "sets type and changes all other attributes based off of new type"
        self._type_statistics = new_creature_type
        self.set_hit_die()
        self.set_bab()
        self.set_save_progression()
        self.set_skill_ranks()
        self.set_class_skills()
        self._type = self._type_statistics["Type"]
    def get_type(self):
        "get type"
        return self._type

    def set_hit_die(self):
        "sets hit die size"
        self._hit_die = self._type_statistics["Hit Die"]
    def get_hit_die(self):
        "get hit die size"
        return self._hit_die

    def set_bab(self):
        "sets BAB"
        self._bab = self._type_statistics["Base Attack Bonus (BAB)"]
    def get_bab(self):
        "get BAB"
        return self._bab

    def set_save_progression(self):
        "sets save progressions"
        self._save_progression = self._type_statistics.get_save_progressions()
    def get_save_progression(self):
        "get save progressions"
        return self._save_progression

    def set_skill_ranks(self):
        "sets Skill Ranks per HD"
        self._skill_ranks = self._type_statistics["Skill Ranks"]
    def get_skill_ranks(self):
        "get Skill Ranks per HD"
        return self._skill_ranks

    def set_class_skills(self):
        "sets class skills for creature type"
        self._class_skills = self._type_statistics["Class Skills"]
    def get_class_skills(self):
        "get class skills for creature type"
        return self._class_skills
