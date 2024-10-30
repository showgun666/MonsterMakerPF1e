#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for attack class"

import unittest
from src.equipment import Equipment
from src.creature import Creature
from src.attack import Attack
from src.constants import STR

class TestAttack(unittest.TestCase):
    """ Testing AbilityScores class """
    def setUp(self):
        """ Create object for all tests """
        self.creature = Creature()
        self.eq = Equipment()

    def tearDown(self):
        """ Remove dependencies after test """
        self.creature = None
        self.eq = None
'''
    def test_attack_damage_changes_by_size(self):
        """
        changing size of attack correctly changes damage value.
        """

        longsword_dict = self.eq.find_weapon("Longsword")

        self.creature.add_attack(longsword_dict, 0, STR, STR, [], self.creature.size)
        damage = self.creature.attacks[0].calculate_weapon_damage(self.creature.ability_scores)
        self.assertEqual(self.creature.attacks[0].damage_dice, "1d8")
        self.assertEqual(damage, 4)

        self.creature.attacks[0].weapon_size = "Large"
        print("\n\n\n\n\n\n\n\n\n\n" + self.creature.attacks[0].weapon_size + "\n\n\n\n\n\n\n\n\n\n")
        self.assertEqual(self.creature.attacks[0].damage_dice, "2d6")
        damage = self.creature.attacks[0].calculate_weapon_damage(self.creature.ability_scores)
        self.assertEqual(damage, 7)
'''