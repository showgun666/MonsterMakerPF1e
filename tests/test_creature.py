#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for Creature class"

import unittest
from src.creature import Creature

class TestCreature(unittest.TestCase):
    "Tests for creating a creature"

    def test_can_create_creature(self):
        creature = Creature()
        ### REALLY NEED TO FLESH THIS OUT
