#!/usr/bin/env python3
"""
Module for secondary attributes
carrying capacity, initiative, hp, ac

"""
from src.constants import DEX, CON

class SecondaryAttributes:
    """Class for handling secondary attributes of the Creature class"""
    def __init__(self, attributes, size, hit_dice):
        self.attributes = attributes
        self.hit_dice = hit_dice
        self._size = size
        self._carrying_capacity = {"light":0, "medium":0, "heavy":0} # This needs to be set by a method but not a rush
        self._initiative = self.get_bonus(self.attributes.get_ability_modifier(DEX))
        self._hp = self.get_hit_points(CON)
        self.speed = {
            "Burrow":None,
            "Climb":None,
            "Fly":None,
            "Land":30,
            "Swim":None,
        }
        self.fly_maneuverability = {
            "Clumsy":-8,
            "Poor":-4,
            "Average":0,
            "Good":+4,
            "Perfect":+8,
        }

    def set_carrying_capacity(self, size, strength_score=10, modifier_to_strength=0, multiplier=1):
        """set carrying capacity"""
        ...
    def get_carrying_capacity(self):
        """get carrying capacity"""
        ...

    def calculate_difficulty_class(self, ability_mod, bonuses=0, penalties=0, hd=0):
        """set armor class or dice check"""
        return int(10 + hd // 2 + self.attributes.get_ability_modifier(ability_mod) + bonuses + penalties)


# NEEED TO MAKE SURE THAT IT CAN EITHER HANDLE NONE AS ARGUMENT FOR GETTING HIT POINTS OR SOMETHING ELSE
# THINK CONSTRUCTS
# A GOOD THING WOULD BE TO MAKE AN ACTUAL GETTER THAT AUTOMATICALLY CHECKS IF UNDEAD OR CONSTRUCT
    def get_hit_points(self, ability_score, bonuses=0, penalties=0, static_bonus=0):
        """set hit points"""
        hp = 0.0
        hp_bonus = static_bonus
        for die in self.hit_dice.get_hit_dice():
            hp += (die.get_hit_die() + 1) / 2
            hp_bonus += self.attributes.get_ability_modifier(ability_score) + bonuses + penalties
        hp += hp_bonus
        return int(hp), hp_bonus

    def get_bonus(self, ability_mod=0, bonus=0, penalty=0, multiplier=1):
        """set bonus such as initiative, damage, etc"""
        return int(((ability_mod + bonus - penalty) * multiplier) // 1)
