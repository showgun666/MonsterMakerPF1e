#!/usr/bin/env python3
"""
Class for hit dice and related progression for creature class
"""
import src.hit_die as hd

class HitDice:
    "class for handling hit die related things for creature class"
    def __init__(self):
        self.hit_dice = []

    def add_hit_die(self, creature_type):
        "Add a hit die to hit dice."
        self.hit_dice.append(hd.HitDie(creature_type))

    def remove_hit_die(self, index):
        "Remove a hit die from hit dice"
        self.hit_dice.pop(index)

    def saves_from_hit_dice(self):
        "Returns saving throw bonus for saves"
        saves_bonuses = [0, 0, 0]
        unique_types = {}
        for hit_die in self.hit_dice:
            if hit_die.get_type() not in unique_types:
                unique_types[hit_die.get_type()] = [1]
            else:
                unique_types[hit_die.get_type()][0] += 1
            unique_types[hit_die.get_type()].append(hit_die.get_save_progression)

        for _, value in unique_types.items():
            dice = value[0]
            if value[1][0]:
                saves_bonuses[0] += (dice // 2) + 2
            else:
                saves_bonuses[0] += dice // 3
            if value[1][1]:
                saves_bonuses[1] += (dice // 2) + 2
            else:
                saves_bonuses[1] += dice // 3
            if value[1][2]:
                saves_bonuses[2] += (dice // 2) + 2
            else:
                saves_bonuses[2] += dice // 3

        return saves_bonuses
