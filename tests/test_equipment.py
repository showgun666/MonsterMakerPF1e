#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for Creature class"

import unittest
from src.equipment import Equipment
from src.exceptions import SearchMiss

class TestCreature(unittest.TestCase):
    "Tests for creating a creature"
    def setUp(self):
        """ Create object for all tests """
        self.equipment = Equipment()

    def tearDown(self):
        """ Remove dependencies after test """
        self.equipment = None

    def test_find_weapon(self):
        """Can add find correctly to creature"""
        eq = Equipment()
        # Martial weapons
        longsword = eq.find_weapon("Longsword")
        kukri = eq.find_weapon("Kukri")
        greatsword = eq.find_weapon("Greatsword")
        shortbow = eq.find_weapon("Shortbow")
        claw = eq.find_weapon("Claw")

        self.assertEqual(longsword["Cost"], "15")
        self.assertEqual(longsword["Weight"], "4")
        self.assertEqual(greatsword["Dmg (M)"], "2d6")
        self.assertEqual(kukri["Type"], "S")
        self.assertEqual(shortbow["Dmg (S)"], "1d4")
        self.assertEqual(claw["Attack Type"], "Primary")

        weapons = []
        for weapon_category in eq.weapons_list:
            for weapon in weapon_category:
                weapons.append(weapon[next(iter(weapon))]) # Add all weapon names

        for weapon in weapons:
            # Iterate through all weapon names
            # see that it can find the weapon and that it is indeed that weapon
            self.assertEqual(weapon, next(iter(eq.find_weapon(weapon).values())))

    def test_searching_for_nonexistent_weapon_raises_searchmiss(self):
        """
        raises searchmiss exception if trying to find nonexistant weapon.
        """
        eq = Equipment()

        with self.assertRaises(SearchMiss):
            eq.find_weapon("Master Sword")
