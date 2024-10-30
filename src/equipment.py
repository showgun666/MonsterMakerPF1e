"""Class for handling equipment for creature class"""
from src.helpers import generate_list_of_dictionaries
from src.exceptions import SearchMiss
from src.constants import NATURAL_ATTACKS, SIMPLE_UNARMED
from src.constants import MARTIAL_LIGHT, MARTIAL_ONE, MARTIAL_RANGED, MARTIAL_TWO
from src.constants import SIMPLE_LIGHT, SIMPLE_ONE, SIMPLE_RANGED, SIMPLE_TWO
from src.constants import EXOTIC_LIGHT, EXOTIC_ONE, EXOTIC_RANGED, EXOTIC_TWO

class Equipment:
    """
    Equipment class
    Handles Combat Equipment
    Handles Treasure
    """
    def __init__(self):
        self.light_armors = {}
        self.medium_armors = {}
        self.weapons_list = [
            generate_list_of_dictionaries(SIMPLE_UNARMED),
            generate_list_of_dictionaries(SIMPLE_LIGHT),
            generate_list_of_dictionaries(SIMPLE_ONE),
            generate_list_of_dictionaries(SIMPLE_TWO),
            generate_list_of_dictionaries(SIMPLE_RANGED),
            generate_list_of_dictionaries(MARTIAL_LIGHT),
            generate_list_of_dictionaries(MARTIAL_ONE),
            generate_list_of_dictionaries(MARTIAL_TWO),
            generate_list_of_dictionaries(MARTIAL_RANGED),
            generate_list_of_dictionaries(EXOTIC_LIGHT),
            generate_list_of_dictionaries(EXOTIC_ONE),
            generate_list_of_dictionaries(EXOTIC_TWO),
            generate_list_of_dictionaries(EXOTIC_RANGED),
            generate_list_of_dictionaries(NATURAL_ATTACKS),
        ]
        self.treasure = {}

    def get_armors(self):
        """
        Returns list of all armor names.
        """

    def get_ranged_weapons(self):
        """
        Returns list of all ranged weapons names.
        """

    def get_melee_weapons(self):
        """
        Returns list of all melee weapons names.

        """
        return generate_list_of_dictionaries(NATURAL_ATTACKS)

    def get_natural_weapons(self):
        """
        returns list of all natural weapons
        """
        return generate_list_of_dictionaries(NATURAL_ATTACKS)

    def find_weapon(self, weapon_name):
        """
        weapon_name:str
        Returns dictionary for requested weapon.
        """
        # Linear and bad search. Should probably figure out a better data structure.
        for category in self.weapons_list:
            for weapon in category:
                if weapon[next(iter(weapon))] == weapon_name:
                    return weapon
        raise SearchMiss(f'Could not find weapon {weapon_name} in equipment list.')

    def find_armor(self, armor_name):
        """
        armor_name:str
        Returns dictionary for requested armor.
        """
