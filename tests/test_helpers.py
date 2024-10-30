#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for Helpers Module"

import unittest
import src.helpers as helpers
from src.constants import DAMAGE_DICE_PROGRESSION, CREATURE_SIZES

TEXT_FILE = "src/tables/skillSummary.txt"

class TestHelpers(unittest.TestCase):
    "Class for testing helpers"

    def test_generate_skills_generates_correctly(self):
        "test that the function can generate skill list"

        skills = helpers.generate_list_of_dictionaries(TEXT_FILE)

    def test_generate_dictionary_list_from_nonexistent_file_raises_error(self):
        "generating list of dictionaries from nonexistent file raises error"
        with self.assertRaises(FileNotFoundError):
            helpers.generate_list_of_dictionaries("nonexistent.txt")

    def test_closest_integer(self):
        """closest integer finds correct integer"""

        self.assertEqual(helpers.closest_integer(1, 5, 2), 1)
        self.assertEqual(helpers.closest_integer(1, 1, 2), 1)
        self.assertEqual(helpers.closest_integer(5, 5, 2), 5)
        self.assertEqual(helpers.closest_integer(-1, 5, 2), -1)
        self.assertEqual(helpers.closest_integer(-1, -5, 2), -1)
        self.assertEqual(helpers.closest_integer(19, -5, 2), -5)
        self.assertEqual(helpers.closest_integer(2, 4, 3), 2)
        self.assertEqual(helpers.closest_integer(2, 4444, 3), 2)
        self.assertEqual(helpers.closest_integer(12, 20, 3), 12)
        self.assertEqual(helpers.closest_integer(2, 18, 13), 18)
        self.assertEqual(helpers.closest_integer(2, 18, 13.5), 18)
        self.assertEqual(helpers.closest_integer(2, 4, 3.5), 4)

    def test_recursive_average(self):
        """
        correctly gives expected result
        """
        self.assertEqual(helpers.get_average_dice("1d6+1"), 4)
        self.assertEqual(helpers.get_average_dice("1d6 -2"), 1)
        self.assertEqual(helpers.get_average_dice("2d4+1"), 6)
        self.assertEqual(helpers.get_average_dice("3d6+10"), 20)
        self.assertEqual(helpers.get_average_dice("1d8-1"), 3)
        self.assertEqual(helpers.get_average_dice("1d3+1d6"), 5)
        self.assertEqual(helpers.get_average_dice("-1d6"), -3)
        self.assertEqual(helpers.get_average_dice("1d8"), 4)
        self.assertEqual(helpers.get_average_dice("1d8-1d6"), 1)
        self.assertEqual(helpers.get_average_dice("1d8"), 4)
        self.assertEqual(helpers.get_average_dice("1d8+1d8+1+11+2d4-2d4-11-1-1d8-1d8"), 0)

    def test_get_adjusted_damage_dice(self):
        """
        can adjust damage dice to dice on progression chart.
        """
        dice = ["2d12", "10d6", "5d8", "2d4", "3d4"]

        self.assertEqual(helpers.get_adjusted_damage_dice(dice[0]), "4d6")
        self.assertEqual(helpers.get_adjusted_damage_dice(dice[3]), "1d8")
        self.assertEqual(helpers.get_adjusted_damage_dice(dice[4]), "2d6")
        self.assertEqual(helpers.get_adjusted_damage_dice(dice[2]), "6d6")
        self.assertEqual(helpers.get_adjusted_damage_dice(dice[1]), "8d8")

    def test_change_damage_dice_size(self):
        """
        correctly changes damage dice size
        """
        dice = ["1d4", "1d6", "1d8", "2d6", "1d10", ]

        self.assertEqual(helpers.change_damage_dice_size(dice[1], 4, 1), "1d8")
        self.assertEqual(helpers.change_damage_dice_size(dice[2], 4, 1), "2d6")
        self.assertEqual(helpers.change_damage_dice_size(dice[3], 4, 1), "3d6")
        self.assertEqual(helpers.change_damage_dice_size(dice[0], 4, 1), "1d6")

        self.assertEqual(helpers.change_damage_dice_size(dice[1], 4, -1), "1d4")
        self.assertEqual(helpers.change_damage_dice_size(dice[2], 4, -1), "1d6")
        self.assertEqual(helpers.change_damage_dice_size(dice[3], 4, -1), "1d8")
        self.assertEqual(helpers.change_damage_dice_size(dice[0], 4, -1), "1d3")

        self.assertEqual(helpers.change_damage_dice_size(dice[1], 4, 3), "3d6")
        self.assertEqual(helpers.change_damage_dice_size(dice[3], 4, -3), "1d4")



    def test_damage_dice_conversion(self):
        """
        Correctly converts dice according to rules.
        """
        sizes = helpers.generate_list_of_dictionaries(CREATURE_SIZES)
        dmg1 = helpers.damage_dice_by_size_conversion(DAMAGE_DICE_PROGRESSION[4], sizes[4]["Creature Size"].split()[0], sizes[4]["Creature Size"].split()[0])
        dmg2 = helpers.damage_dice_by_size_conversion(DAMAGE_DICE_PROGRESSION[5], sizes[4]["Creature Size"].split()[0], sizes[5]["Creature Size"].split()[0])
        dmg3 = helpers.damage_dice_by_size_conversion(DAMAGE_DICE_PROGRESSION[7], sizes[5]["Creature Size"].split()[0], sizes[4]["Creature Size"].split()[0])
        dmg4 = helpers.damage_dice_by_size_conversion("3d6", "Large", "Small")
        dmg5 = helpers.damage_dice_by_size_conversion("3d6", "Large", "Tiny")

        self.assertEqual(dmg1, DAMAGE_DICE_PROGRESSION[4])
        self.assertEqual(dmg3, DAMAGE_DICE_PROGRESSION[5])
        self.assertEqual(dmg2, DAMAGE_DICE_PROGRESSION[7])
        self.assertEqual(dmg4, "1d8")
        self.assertEqual(dmg5, "1d6")
