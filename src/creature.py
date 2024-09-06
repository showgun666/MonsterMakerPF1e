#!/usr/bin/env python3
"""
Class for creature
"""
import src.helpers as helper_module
import src.attributes as attribute_class
import src.creature_type as creature_type_class
import src.skills as skills_class
from src.constants import * # Continuously check that this * import is not loading unneccessary stuff.

class Creature:
    "Class for creatures"
    def __init__(self, creature_type="Humanoid", cr="1", ):
        self.skills = skills_class.Skills(creature_type)
        ### MIGHT NEED TO PUT IN A LIST OR SOMETHING OF TYPES ETC FOR MULTICLASSING OR HAVING MULTIPLE PROGRESSIONS WITH DIFFERENT TYPES
        self.set_cr(cr)
        self.attributes = attribute_class.Attributes()
        self.creature_type = creature_type_class.CreatureType(creature_type)

        self.set_default_hit_dice_by_cr()
        self.update_statistics_by_hit_dice()
        self.change_type(creature_type)

    def set_cr(self, given_cr):
        "sets cr value"
        self._cr = given_cr
    def get_cr(self):
        "get cr value"
        return self._cr


    def update_cmb_and_cmd(self):
        "updates values of cmb and cmd"
