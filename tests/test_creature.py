#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for Creature class"

import unittest
from src.creature import Creature

class TestCreature(unittest.TestCase):
    "Tests for creating a creature"
    def setUp(self):
        """ Create object for all tests """
        self.creature = Creature("Dragon", "5")

    def tearDown(self):
        """ Remove dependencies after test """
        self.creature = None

    def test_can_create_creature(self):
        """Can create creature"""
        creature = Creature("Aberration", 5)
        self.assertEqual(creature.get_cr(), 5)

    def test_can_write_stat_block(self):
        """Can get a stat block"""
        self.creature.get_d20pfsrd_stat_block()

    def test_can_get_xp_value_by_cr(self):
        """Gets correct xp value by cr"""
        self.assertEqual("1600", self.creature.get_xp_reward_by_cr(self.creature.get_cr()))
        self.creature2 = Creature("Aberration", 3)
        self.assertEqual("800", self.creature2.get_xp_reward_by_cr(self.creature2.get_cr()))
        self.creature3 = Creature("Aberration", 4)
        self.assertEqual("1200", self.creature3.get_xp_reward_by_cr(self.creature3.get_cr()))
