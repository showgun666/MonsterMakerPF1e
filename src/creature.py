#!/usr/bin/env python3
"""
Class for creature
"""
import src.ability_scores as ability_scores_class
import src.creature_type as creature_type_class
import src.skills as skills_class
import src.hit_dice as hit_dice_class
import src.secondary_attributes as secondary_attributes_class
import src.statSheet as stat_sheet_class
import src.helpers as helper_module
from src.constants import CREATURE_SIZES, EXPERIENCE_POINT_AWARDS

class Creature:
    "Class for creatures"
    def __init__(self, creature_type="Humanoid", cr="1", size="Medium"):
        creature_type = creature_type_class.CreatureType(creature_type)

        self.set_cr(cr)
        self.hit_dice = hit_dice_class.HitDice()
        self.ability_scores = ability_scores_class.AbilityScores()
        self.skills = skills_class.Skills(creature_type)
        self.set_size(size)
        #### CONSIDER CACHING SKILL MODIFIERS AND SKILLS EVERY TIME THEY CHANGE
        #### IF THIS DATA WILL BE CHANGED OFTEN
        i = int(creature_type.hit_dice_by_cr(self.get_cr()))
        while i > 0:
            self.hit_dice.add_hit_die(str(creature_type))

            i -= 1
        self.secondary_attributes = secondary_attributes_class.SecondaryAttributes(
            self.ability_scores, self.get_size()["Creature Size"], self.hit_dice)
        #self._size = self.get_size_data()
        # Sizes fine, diminutive, tiny, small, medium, large, huge, gargantuan, colossal

        # self.update_statistics_by_hit_dice()

    def set_cr(self, given_cr):
        "sets cr value"
        ### UPDATE HD?
        ### SET HD AGAIN?
        self._cr = given_cr
    def get_cr(self):
        "get cr value"
        return self._cr

    def set_size(self, given_size):
        """Set size of self"""
        sizes = helper_module.generate_list_of_dictionaries(CREATURE_SIZES)
        for size in sizes:
            if size["Creature Size"] == given_size:
                self.size = size
    def get_size(self):
        """Get size of self"""
        return self.size

    def get_skill_modifier(self, skill):
        """get modifier to d20 roll for select skill"""
        # ENCUMBERMENT?
        skillmod = 0
        skill = self.skills.find_skill(skill)

        skillmod += skill["Skill Ranks"]
        skillmod += self.ability_scores.get_ability_modifier(skill["Key Ability"])
        if skill in self.skills.class_skills_list:
            skillmod += 3
        if skill == "Stealth":
            skillmod += self.size["Size Modifier to Stealth"]
        #### FLY SKILL MANEUVERABILITY + SIZE

        return skillmod

    def get_d20pfsrd_stat_block(self):
        """create d20pfsrd format stat block as .txt file"""
        return stat_sheet_class.StatBlock(self).generate_stat_block_string_d20pfsrd()

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


    def get_xp_reward_by_cr(self, given_cr):
        """
        return:str  XP value for given_cr
        """
        xp_dictionary = helper_module.generate_list_of_dictionaries(EXPERIENCE_POINT_AWARDS)

        for index in xp_dictionary:
            if index["CR"] == str(given_cr):
                return index["Total XP"]

    def find_saves(self):
        """
        Retrieve saves
        """
        return self.hit_dice.saves_from_hit_dice()
