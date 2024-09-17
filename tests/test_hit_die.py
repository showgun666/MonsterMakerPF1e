#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for skills class"

import unittest
from src.hit_die import HitDie

class TestHitDie(unittest.TestCase):
    """
    class for testing the HitDie class, submodule for unittests.
    Derives from unittest.TestCase
    """
    def setUp(self):
        """ Create object for all tests """
        creature_type = "Humanoid"
        self.hd = HitDie(creature_type)

    def tearDown(self):
        """ Remove dependencies after test """
        self.hd = None

    def test_get_hd(self):
        """get_hd returns correct value"""
        self.assertEqual(self.hd.get_hit_die(), 8)
        self.assertNotEqual(self.hd.get_hit_die(), "8")
        self.assertNotEqual(self.hd.get_hit_die(), 6)

    def test_get_bab(self):
        """get_bab returns correct value"""
        self.assertEqual(self.hd.get_bab(), 0.75)
        self.assertNotEqual(self.hd.get_bab(), "0.75")

    def test_get_save_progression(self):
        """get_save_progression returns correct value"""
        self.assertEqual(self.hd.get_save_progression(), [False, False, False])

    def test_get_skill_ranks(self):
        """get_skill_ranks returns correct value"""
        self.assertEqual(self.hd.get_skill_ranks(), 2)

    def test_get_class_skills(self):
        """get_class_skills returns correct values"""
        self.assertEqual(self.hd.get_class_skills()[0], "Climb")
        self.assertEqual(self.hd.get_class_skills()[1], "Craft")
        self.assertEqual(self.hd.get_class_skills()[2], "Handle Animal")
        self.assertEqual(self.hd.get_class_skills()[3], "Heal")

    def test_add_class_skill(self):
        """set_class_skills correctly sets class skills"""
        self.assertNotIn("Acrobatics", self.hd.get_class_skills())
        self.hd.add_class_skill("Acrobatics")
        self.assertIn("Acrobatics", self.hd.get_class_skills())

    def test_remove_class_skill(self):
        """set_class_skills correctly sets class skills"""
        self.assertIn("Climb", self.hd.get_class_skills())
        self.hd.remove_class_skill("Climb")
        self.assertNotIn("Climb", self.hd.get_class_skills())
        self.assertIn("Heal", self.hd.get_class_skills())

    def test_set_type(self):
        """Can set hd to new type"""
        self.hd.set_type("Dragon")

        self.assertNotEqual(self.hd.get_type(), "Humanoid")
        self.assertEqual(self.hd.get_type(), "Dragon")
        self.assertNotEqual(self.hd.get_hit_die(), 8)
        self.assertEqual(self.hd.get_hit_die(), 12)
        self.assertNotEqual(self.hd.get_bab(), 0.75)
        self.assertEqual(self.hd.get_bab(), 1)
        self.assertNotEqual(self.hd.get_save_progression(), [False, False, False])
        self.assertEqual(self.hd.get_save_progression(), [True, True, True])
        self.assertEqual(self.hd.get_skill_ranks(), 6)
        self.assertNotIn("Handle Animal", self.hd.get_class_skills())
        self.assertIn("Intimidate", self.hd.get_class_skills())
        self.assertIn("Knowledge (arcana)", self.hd.get_class_skills())
        self.assertNotIn("Knowledge (all)", self.hd.get_class_skills())
