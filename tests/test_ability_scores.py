#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for ability scores class"

import unittest
from src.ability_scores import AbilityScores
from src.constants import STR, DEX, CON, INT, WIS, CHA

class TestAbilityScores(unittest.TestCase):
    """ Testing AbilityScores class """
    def setUp(self):
        """ Create object for all tests """
        self.ability_scores = AbilityScores()

    def tearDown(self):
        """ Remove dependencies after test """
        self.ability_scores = None

    def test_get_ability_score(self):
        """Can get ability scores"""
        self.assertEqual(self.ability_scores.get_ability_score(STR), 10)
        self.assertEqual(self.ability_scores.get_ability_score(DEX), 10)
        self.assertEqual(self.ability_scores.get_ability_score(CON), 10)
        self.assertEqual(self.ability_scores.get_ability_score(INT), 10)
        self.assertEqual(self.ability_scores.get_ability_score(WIS), 10)
        self.assertEqual(self.ability_scores.get_ability_score(CHA), 10)
        self.assertNotEqual(self.ability_scores.get_ability_score(CHA), 11)

    def test_set_ability_score(self):
        """can set ability scores"""
        self.ability_scores.set_ability_score(STR, 17)
        self.ability_scores.set_ability_score(DEX, 71)
        self.ability_scores.set_ability_score(CON, 10)
        self.ability_scores.set_ability_score(INT, 15)
        self.ability_scores.set_ability_score(WIS, 12)
        self.ability_scores.set_ability_score(CHA, 9)
        self.ability_scores.set_ability_score(CHA, 7)
        self.assertNotEqual(self.ability_scores.get_ability_score(STR), 10)
        self.assertEqual(self.ability_scores.get_ability_score(STR), 17)
        self.assertNotEqual(self.ability_scores.get_ability_score(DEX), 1)
        self.assertEqual(self.ability_scores.get_ability_score(DEX), 71)
        self.assertNotEqual(self.ability_scores.get_ability_score(CON), 7)
        self.assertEqual(self.ability_scores.get_ability_score(CON), 10)
        self.assertNotEqual(self.ability_scores.get_ability_score(INT), 10)
        self.assertEqual(self.ability_scores.get_ability_score(INT), 15)
        self.assertNotEqual(self.ability_scores.get_ability_score(WIS), "10")
        self.assertNotEqual(self.ability_scores.get_ability_score(WIS), "12")
        self.assertEqual(self.ability_scores.get_ability_score(WIS), 12)
        self.assertNotEqual(self.ability_scores.get_ability_score(CHA), 10)
        self.assertEqual(self.ability_scores.get_ability_score(CHA), 7)

    def test_get_ability_modifier(self):
        """can get correct ability modifier for ability score"""
        self.ability_scores.set_ability_score(STR, 14)
        self.ability_scores.set_ability_score(DEX, 4)
        self.ability_scores.set_ability_score(CON, 15)
        self.ability_scores.set_ability_score(INT, 5)
        self.ability_scores.set_ability_score(WIS, 40)
        self.ability_scores.set_ability_score(CHA, 210)
        self.assertEqual(self.ability_scores.get_ability_modifier(STR), 2)
        self.assertEqual(self.ability_scores.get_ability_modifier(DEX), -3)
        self.assertEqual(self.ability_scores.get_ability_modifier(CON), 2)
        self.assertEqual(self.ability_scores.get_ability_modifier(INT), -3)
        self.assertEqual(self.ability_scores.get_ability_modifier(WIS), 15)
        self.assertEqual(self.ability_scores.get_ability_modifier(CHA), 100)
        self.assertNotEqual(self.ability_scores.get_ability_modifier(CHA), "100")
