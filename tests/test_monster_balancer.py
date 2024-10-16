#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for monster balancer module"

import unittest
from src.monster_balancer.monster_balancer import determine_cr_float

class TestMonsterBalancer(unittest.TestCase):
    "Tests for monster balancer module"
    def setUp(self):
        """ setUp for all tests """

    def tearDown(self):
        """ Remove dependencies after test """

    def test_determine_cr_float(self):
        """
        correctly determines value
        """
        values = [
            determine_cr_float("Hit Points", 10), # 0.0
            determine_cr_float("Hit Points", 33), # 3.3
            determine_cr_float("Hit Points", 370), # 20
            determine_cr_float("Primary Ability DC", 27), # 20
        ]
        self.assertEqual(values[0], 0)
        self.assertEqual(values[1], 3.3)
        self.assertEqual(values[2], 20)
        self.assertEqual(values[3], 20)

    def test_determine_cr_float_low_value_raises_value_error(self):
        """
        giving a lower number than available on table raises a value error.
        """
        with self.assertRaises(ValueError):
            determine_cr_float("Hit Points", -10)
            determine_cr_float("Hit Points", 8)
            determine_cr_float("Hit Points", 0)
            determine_cr_float("Primary Ability DC", 36)
