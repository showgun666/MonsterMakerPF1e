#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for Creature class"

import unittest
from src.creature import Creature
from src.creature_maker import CreatureMaker
from src.equipment import Equipment
from src.constants import STR, CON, DEX

class TestCreature(unittest.TestCase):
    "Tests for creating a creature"
    def setUp(self):
        """ Create object for all tests """
        self.creature = Creature("Dragon", "5")
        self.equipment = Equipment()
        self.maker = CreatureMaker()
        csize = self.creature.size

        self.creature.add_attack(self.equipment.find_weapon("Bite"), 0, STR, STR, [], csize)
        self.creature.add_attack(self.equipment.find_weapon("Claw"), 0, STR, STR, [], csize)
        self.creature.add_attack(self.equipment.find_weapon("Claw"), 0, STR, STR, [], csize)

    def tearDown(self):
        """ Remove dependencies after test """
        self.creature = None
        self.maker = None

    def test_get_average_integer_from_dictionary(self):
        """ can get correct value """
        test_dict1 = {
            "1":2,
            "2":2,
            "3":2,
            "4":2,
            "5":2,
        }
        test_dict2 = {
            "1":2,
            "2":2,
            "3":2,
            "4":2,
            "5":3,
        }
        test_dict3 = {
            "1":1,
            "2":2,
            "3":3,
            "4":4,
            "5":5,
        }
        self.assertEqual(self.maker.get_average_integer_from_dictionary(test_dict1), 2)
        self.assertEqual(self.maker.get_average_integer_from_dictionary(test_dict2), 2)
        self.assertEqual(self.maker.get_average_integer_from_dictionary(test_dict3), 3)

    def test_retrieve_stats(self):
        """
        correctly retrieves values from creature
        """
        damage = self.maker.retrieve_stat_from_creature("damage", self.creature)
        self.assertEqual(3, self.creature.attacks[0].calculate_weapon_damage(self.creature.ability_scores))
        self.assertEqual(2, self.creature.attacks[1].calculate_weapon_damage(self.creature.ability_scores))
        self.assertEqual(2, self.creature.attacks[2].calculate_weapon_damage(self.creature.ability_scores))
        self.assertEqual(damage, 7)
        self.creature.ability_scores.set_ability_score(STR, 12)
        self.assertEqual(4, self.creature.attacks[0].calculate_weapon_damage(self.creature.ability_scores))
        self.assertEqual(3, self.creature.attacks[1].calculate_weapon_damage(self.creature.ability_scores))
        self.assertEqual(3, self.creature.attacks[2].calculate_weapon_damage(self.creature.ability_scores))
        damage = self.maker.retrieve_stat_from_creature("damage", self.creature)
        self.assertEqual(damage, 10)

    def test_calculate_expected_cr(self):
        """ Can calculate expected CR correctly. """
        expected_cr = self.maker.calculate_expected_cr(self.creature)
        with open ('output1.txt', 'w') as file:
            file.write(self.creature.get_d20pfsrd_stat_block())
        self.creature.ability_scores.set_ability_score(STR, 22)
        self.creature.ability_scores.set_ability_score(CON, 18)
        self.creature.ability_scores.set_ability_score(DEX, 30)
        with open ('output2.txt', 'w') as file:
            file.write(self.creature.get_d20pfsrd_stat_block())

        with open ('output3.txt', 'w') as file:
            file.write(self.creature.get_d20pfsrd_stat_block())
        self.assertEqual(expected_cr, 5)
