"""Class for handling equipment for creature class"""
from src.helpers import generate_list_of_dictionaries
from constants import NATURAL_ATTACKS

class Equipment:
    """
    Equipment class
    Handles Combat Equipment
    Handles Treasure
    """
    def __init__(self):
        self.armors = {}
        self.ranged_weapons = {}
        self.melee_weapons = {}
        self.natural_weapons = {}
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
        weapons = self.get_natural_weapons()
        for weapon in weapons:
            if weapon["Natural Attacks"] == weapon_name:
                return weapon

    def find_armor(self, armor_name):
        """
        armor_name:str
        Returns dictionary for requested armor.
        """

    def add_armor(self, armor):
        """
        statistics:dict
        Add an armor to armors
        """

    def add_weapon(self, weapon, weapon_type):
        """
        statistics:dict
        Add a weapon to weapons
        """
        if weapon_type == "Natural Attack":
            self.natural_weapons[weapon["Natural Attacks"]] = weapon


    def remove_armor(self, armor_name):
        """
        remove armor
        """

    def remove_weapon(self, weapon_name):
        """
        remove weapon
        """
