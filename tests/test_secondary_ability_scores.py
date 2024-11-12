#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for skills class"

import unittest
from src.secondary_attributes import SecondaryAttributes
from src.ability_scores import AbilityScores
from src.hit_dice import HitDice
from src.constants import CON

class TestSecondaryAttributesScores(unittest.TestCase):
    """
    class for testing the skills class, submodule for unittests.
    derives from unittest.TestCase
    """
    def setUp(self):
        """ Create object for all tests """
        self.abscrs = AbilityScores()
        hd = HitDice()
        hd.add_hit_die("Humanoid", 5)
        size = 1
        self.sas = SecondaryAttributes(self.abscrs, size, hd)

    def tearDown(self):
        """ Remove dependencies after test """
        self.sas = None
        self.abscrs = None

    def test_calculate_dc(self):
        """Test if we can set DCs"""
        self.abscrs.set_ability_score(1, 16)
        dc = self.sas.calculate_difficulty_class(1, 5, -1)
        # Armor Class Dex 16, 0 armorbonus, -1 penalty
        self.assertEqual(dc, 17)
        self.abscrs.set_ability_score(1, 15)
        dc = self.sas.calculate_difficulty_class(1, 5, -1)
        self.assertEqual(dc, 10+2+5-1)
        self.abscrs.set_ability_score(1, 5)
        dc = self.sas.calculate_difficulty_class(1, 5, -1)
        self.assertEqual(dc, 10-3+5-1)
        self.abscrs.set_ability_score(5, 12)
        dc = self.sas.calculate_difficulty_class(5, 3, -3)
        self.assertEqual(dc, 10+1+3-3)

    def test_get_hp(self):
        """Can get accurate hp value"""
        hp = self.sas.get_hit_points(2, 0, 0, 3)
        self.assertEqual(5, len(self.sas.hit_dice))
        self.assertEqual(hp[1], 3)

        self.abscrs.set_ability_score(2, 16)
        hp = self.sas.get_hit_points(2, 0, 0, 3)
        self.assertEqual(hp[0], int((4.5*5) //1) + 5*3 + 3)
        self.assertEqual(hp[1], 5*3 + 3)

        self.abscrs.set_ability_score(2, 6)
        hp = self.sas.get_hit_points(2, 0, 0)
        self.assertEqual(hp[0], int((4.5*5) //1) + 5*-2)
        self.assertEqual(hp[1], 5*-2)

        hp = self.sas.get_hit_points(2, 5, -5)
        self.assertEqual(hp[0], int((4.5*5)//1) + 5*-2 +5 -5)
        self.assertEqual(hp[1], 5*-2 +5 -5)

        self.abscrs.set_ability_score(CON, 18)
        hp = self.sas.get_hit_points(CON)
        self.assertEqual(hp[0], int((4.5*5)//1) + 5*4)
        self.assertEqual(hp[1], 5*4)
