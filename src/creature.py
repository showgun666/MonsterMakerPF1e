#!/usr/bin/env python3
"""
Class for creature
"""
import src.ability_scores as ability_scores_class
import src.creature_type as creature_type_class
import src.skills as skills_class
import src.hit_dice as hit_dice_class

class Creature:
    "Class for creatures"
    def __init__(self, creature_type="Humanoid", cr="1", ):
        initial_creature_type = creature_type_class.CreatureType(creature_type)

        self.set_cr(cr)
        self._hit_dice = hit_dice_class.HitDice()
        self.ability_scores = ability_scores_class.AbilityScores()
        self.skills = skills_class.Skills(creature_type)
        i = int(initial_creature_type.hit_dice_by_cr(self.get_cr()))
        while i > 0:
            self._hit_dice.add_hit_die(creature_type)
            i -= 1

        # self.update_statistics_by_hit_dice()

    def set_cr(self, given_cr):
        "sets cr value"
        self._cr = given_cr
    def get_cr(self):
        "get cr value"
        return self._cr


    def update_cmb_and_cmd(self):
        "updates values of cmb and cmd"

"""    def update_statistics_by_hit_dice(self):
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
"""