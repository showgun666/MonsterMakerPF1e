#!/usr/bin/env python3
"""
Class for hit dice and related progression for creature class
"""
import src.hit_die as hd

class HitDice:
    "class for handling hit die related things for creature class"
    def __init__(self):
        self._hit_dice = []

    def add_hit_die(self, creature_type, amount=1):
        "Add a hit die to hit dice."
        while amount > 0:
            self._hit_dice.append(hd.HitDie(creature_type))
            amount -= 1
    def remove_hit_die(self, index):
        "Remove a hit die from hit dice"
        self._hit_dice.pop(index)

    def saves_from_hit_dice(self):
        "Returns saving throw bonus for saves"
        saves_bonuses = [0, 0, 0]
        creature_type_progressions = {}

        for hit_die in self.get_hit_dice():
            creature_type = hit_die.get_type()
            if creature_type not in creature_type_progressions:
                creature_type_progressions[creature_type] = [0, hit_die.get_save_progression()]
            creature_type_progressions[creature_type][0] += 1

        def calculate_save_bonus(dice, progression):
            "Helper function to calculate save bonus based on progression"
            return (dice // 2) + 2 if progression else dice // 3

        for dice, progressions in creature_type_progressions.values():
            for i in range(3):
                saves_bonuses[i] += calculate_save_bonus(dice, progressions[i])

        return saves_bonuses

    def get_bab(self):
        """ Returns BAB from hit dice. """
        type_bab = {}
        for hit_die in self.get_hit_dice():
            type_bab[hit_die.get_type()] = 0
        for hit_die in self.get_hit_dice():
            type_bab[hit_die.get_type()] += hit_die.get_bab()
        bab = 0
        for dice_type in type_bab.values():
            bab += int(dice_type // 1)
        return bab

    def get_hit_dice(self):
        """Get a list of all hit dice"""
        return self._hit_dice

    def __len__(self):
        """Returns how many dice in object as int"""
        return len(self.get_hit_dice())
### NEED TO BUILD METHODS THAT CAN BE TESTED EASIER:::::
### ALSO NEED TO START COMMENTING CODE::::
