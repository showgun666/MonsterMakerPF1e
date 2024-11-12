#!/usr/bin/env python3
"""
Class for hit dice for HitDice class
"""
from src.creature_type import CreatureType

class HitDie:
    "class for handling hit die related things for creature class"
    def __init__(self, creature_type):
        self._creature_type = CreatureType(creature_type)
        self._hit_die = self.get_creature_type().hd_size()
        self._bab = self.get_creature_type().bab_progression()
        self._save_progression = self.get_creature_type().get_save_progressions()
        self._skill_ranks = self.get_creature_type().skill_ranks_per_hd()
        self._class_skills = self.get_creature_type().set_class_skills()

    def set_type(self, new_creature_type):
        "sets type and changes all other attributes based off of new type"
        self._creature_type = CreatureType(new_creature_type)
        self.set_hit_die()
        self.set_bab()
        self.set_save_progression()
        self.set_skill_ranks()
        self.set_class_skills()
    def get_type(self):
        "get type as string"
        return str(self._creature_type)

    def get_creature_type(self):
        "Get creature object for die"
        return self._creature_type

    def set_hit_die(self):
        "sets hit die size"
        self._hit_die = self._creature_type.hd_size()
    def get_hit_die(self):
        "get hit die size"
        return self._hit_die

    def set_bab(self):
        "sets BAB"
        self._bab = self._creature_type.bab_progression()
    def get_bab(self):
        "get BAB"
        return self._bab

    def set_save_progression(self):
        "sets save progressions"
        self._save_progression = self._creature_type.get_save_progressions()
    def get_save_progression(self):
        "get save progressions"
        return self._save_progression

    def set_skill_ranks(self):
        "sets Skill Ranks per HD"
        self._skill_ranks = self._creature_type.skill_ranks_per_hd()
    def get_skill_ranks(self):
        "get Skill Ranks per HD"
        return self._skill_ranks

    def set_class_skills(self):
        "sets class skills for creature type"
        self._class_skills = self._creature_type.set_class_skills()
    def add_class_skill(self, skill):
        "add class skill for hd"
        self._class_skills.append(skill)
    def remove_class_skill(self, skill):
        "Removes class skill from class skills"
        for i, value in enumerate(self.get_class_skills()):
            if value == skill:
                removed_skill = self._class_skills.pop(i)
                return removed_skill
    def get_class_skills(self):
        "get class skills for creature type"
        return self._class_skills
