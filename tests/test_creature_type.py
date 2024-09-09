#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for CreatureType class"

import unittest
from src.creature_type import CreatureType

class TestSkills(unittest.TestCase):
    """class for testing CreatureType, submodule for unittests. derives from unittest.TestCase"""
    def setUp(self):
        """ Create object for all tests """
        self.creature_type = CreatureType()

    def tearDown(self):
        """ Remove dependencies after test """
        self.creature_type = None

    def test_init(self):
        """init properly executes"""
        self.assertEqual(self.creature_type.creature_type_statistics["Type"], "Humanoid")
        self.assertEqual(self.creature_type.creature_type_statistics["Hit Die"], 8)
        self.assertNotEqual(self.creature_type.creature_type_statistics["Hit Die"], "8")
        self.assertEqual(self.creature_type.creature_type_statistics["Base Attack Bonus (BAB)"], 0.75)
        self.assertNotEqual(self.creature_type.creature_type_statistics["Base Attack Bonus (BAB)"], "0.75")
        self.assertEqual(self.creature_type.creature_type_statistics["Good Saving Throws"], "1")
        self.assertEqual(self.creature_type.saving_throw_progression, [False, False, False])

    def test_hd_size(self):
        """can get hd size of type"""
        self.assertEqual(self.creature_type.hd_size(), 8)
        self.assertNotEqual(self.creature_type.hd_size(), "8")

    def test_bab_progression(self):
        """can get bab progression of type"""
        self.assertEqual(self.creature_type.bab_progression(), 0.75)
        self.assertNotEqual(self.creature_type.bab_progression(), "0.75")

    def test_class_skills(self):
        """can get class skills"""
        self.assertIsInstance(self.creature_type.set_class_skills(), list)
        self.assertIn("Climb", self.creature_type.set_class_skills())
        self.assertNotIn("Acrobatics", self.creature_type.set_class_skills())

    def test_skill_ranks(self):
        """Can get skill ranks per hd for type"""
        self.assertEqual(self.creature_type.skill_ranks_per_hd(), 2)
        self.assertNotEqual(self.creature_type.skill_ranks_per_hd(), "2")

    def test_get_save_progressions(self):
        """can get save progressions"""
        self.assertEqual(self.creature_type.get_save_progressions(), [False, False, False])

    def test_hd_by_cr(self):
        """hit_dice_by_cr works properly"""
        self.assertEqual(self.creature_type.hit_dice_by_cr(1), 2)
        self.assertEqual(self.creature_type.hit_dice_by_cr(2), 3)
        self.assertEqual(self.creature_type.hit_dice_by_cr(5), 7)
