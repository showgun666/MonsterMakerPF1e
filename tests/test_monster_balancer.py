#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for monster balancer module"

import unittest
from src.monster_balancer.monster_balancer import determine_cr_float
from src.monster_balancer.monster_balancer import armor_class_deviated
from src.monster_balancer.monster_balancer import calculate_average_defensive_cr
from src.monster_balancer.monster_balancer import calculate_average_offensive_cr
from src.monster_balancer.monster_balancer import calculate_average_cr

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
            determine_cr_float("Hit Points", 10, 3), # 0.0
            determine_cr_float("Hit Points", 33, 4), # 3.3
            determine_cr_float("Hit Points", 370, 18), # 20
            determine_cr_float("Primary Ability DC", 27, 17), # 20
            determine_cr_float("Armor Class", 22, 10), # 8.5
            determine_cr_float("Hit Points", 29, 4), # 2.9
        ]
        self.assertEqual(values[5], 2.9)
        self.assertEqual(values[4], 8.5)
        self.assertEqual(values[1], 3.3)
        self.assertEqual(values[2], 20)
        self.assertEqual(values[3], 20)
        self.assertEqual(values[0], 0)

    def test_determine_cr_float_low_value_raises_value_error(self):
        """
        giving a lower number than available on table raises a value error.
        """
        with self.assertRaises(ValueError):
            determine_cr_float("Hit Points", -10)
            determine_cr_float("Hit Points", 8)
            determine_cr_float("Hit Points", 0)
            determine_cr_float("Primary Ability DC", 36)

    def test_armor_class_deviation(self):
        """
        correctly determines if ac value deviates too much.
        """
        high_low1 = armor_class_deviated(22, 3)
        high_low2 = armor_class_deviated(12, 3)
        high_low3 = armor_class_deviated(11, 7)
        high_low4 = armor_class_deviated(18, 3)
        high_low5 = armor_class_deviated(47, 30)

        # Too high
        self.assertEqual(high_low1, 1)

        # Low but OK
        self.assertEqual(high_low2, 0)

        # Too low
        self.assertEqual(high_low3, -1)

        # High but ok
        self.assertEqual(high_low4, 0)

        # Max value OK
        self.assertEqual(high_low5, 0)
    def test_calculate_average_offensive_cr_none_and_zeros(self):
        """
        Test calculate_average_offensive_cr with None for attack and zeros for damage and DC
        """
        cr_value_for_attack = None
        cr_value_for_damage = 0
        cr_value_for_dc = 0
        primarily_attacker = True
        ability_reliant = True

        result = calculate_average_offensive_cr(cr_value_for_attack, cr_value_for_damage, cr_value_for_dc, primarily_attacker, ability_reliant)

        self.assertEqual(result, 0.0)
    def test_calculate_average_defensive_cr(self):
        """correctly calculates average defensive cr"""
        cr_values = [1, 3, 5, 7, 9, 11, 0]
        average_cr_all_zero = calculate_average_defensive_cr(cr_values[6], cr_values[6], cr_values[6], cr_values[6], cr_values[6])
        self.assertEqual(average_cr_all_zero, 0.0)
        average_cr_saves_zero = calculate_average_defensive_cr(cr_values[2], cr_values[3], cr_values[6], cr_values[6], cr_values[6])
        self.assertEqual(average_cr_saves_zero, 4.0)
        average_cr_all_same = calculate_average_defensive_cr(cr_values[1],cr_values[1],cr_values[1],cr_values[1],cr_values[1])
        self.assertEqual(average_cr_all_same, 3.0)
        average_cr_some_different = calculate_average_defensive_cr(cr_values[0], cr_values[1], cr_values[2], cr_values[3], cr_values[3])
        self.assertEqual(average_cr_some_different, 3.444)
    def test_calculate_average_offensive_cr_only_damage(self):
        """
        Test calculate_average_offensive_cr with only damage included
        """
        cr_value_for_attack = 5.0
        cr_value_for_damage = 7.0
        cr_value_for_dc = 6.0
        primarily_attacker = False
        ability_reliant = False

        result = calculate_average_offensive_cr(cr_value_for_attack, cr_value_for_damage, cr_value_for_dc, primarily_attacker, ability_reliant)

        self.assertEqual(result, 7.0)
    def test_calculate_average_offensive_cr_primarily_attacker_and_ability_reliant(self):
        """
        Test calculate_average_offensive_cr with primarily_attacker and ability_reliant set to True
        """
        cr_value_for_attack = 5.0
        cr_value_for_damage = 7.0
        cr_value_for_dc = 6.0
        primarily_attacker = True
        ability_reliant = True

        result = calculate_average_offensive_cr(cr_value_for_attack, cr_value_for_damage, cr_value_for_dc, primarily_attacker, ability_reliant)

        expected_average = (5.0 + 7.0 + 6.0) / 3
        self.assertAlmostEqual(result, round(expected_average, 3))
    def test_calculate_average_offensive_cr_only_dc(self):
        """
        Test calculate_average_offensive_cr with only DC included
        """
        cr_value_for_attack = 5.0
        cr_value_for_damage = 7.0
        cr_value_for_dc = 6.0
        primarily_attacker = False
        ability_reliant = True

        result = calculate_average_offensive_cr(cr_value_for_attack, cr_value_for_damage, cr_value_for_dc, primarily_attacker, ability_reliant)

        self.assertEqual(result, 6.5)
    def test_calculate_average_offensive_cr_primarily_attacker_only(self):
        """
        Test calculate_average_offensive_cr with primarily_attacker set to True and ability_reliant set to False
        """
        cr_value_for_attack = 5.0
        cr_value_for_damage = 7.0
        cr_value_for_dc = 6.0
        primarily_attacker = True
        ability_reliant = False

        result = calculate_average_offensive_cr(cr_value_for_attack, cr_value_for_damage, cr_value_for_dc, primarily_attacker, ability_reliant)

        self.assertEqual(result, 6.0)

    def test_calculate_average_cr_just_outside_rounding_threshold(self):
        """
        Test calculate_average_cr with values just outside the rounding threshold
        """
        average_defensive_cr = 6.68
        average_offensive_cr = 6.68

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        self.assertEqual(result, 7)

    def test_calculate_average_cr_within_rounding_threshold(self):
        """
        Test calculate_average_cr with values just within rounding threshold
        """
        average_defensive_cr = 4.32
        average_offensive_cr = 4.68

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        self.assertEqual(result, 4)

    def test_calculate_average_cr_extreme_difference(self):
        """
        Test calculate_average_cr with extreme difference between defensive and offensive CR
        """
        average_defensive_cr = 20
        average_offensive_cr = 1

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        # Expected result is 11 (rounded up from 10.5 due to high defense)
        self.assertEqual(result, 10)

    def test_calculate_average_cr_zero_values(self):
        """
        Test calculate_average_cr with zero values for both defensive and offensive CR
        """
        average_defensive_cr = 0
        average_offensive_cr = 0

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        self.assertEqual(result, 0)

    def test_calculate_average_cr_exact_midpoint(self):
        """
        Test calculate_average_cr with average_defensive_cr and average_offensive_cr both at 10.5
        """
        average_defensive_cr = 10.5
        average_offensive_cr = 10.5

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        self.assertEqual(result, 10)

    def test_calculate_average_cr_high_offense_rounding_down(self):
        """
        Test calculate_average_cr with high offense and low defense to verify rounding down
        """
        average_defensive_cr = 2.3
        average_offensive_cr = 2.7

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        self.assertEqual(result, 2)

    def test_calculate_average_cr_high_defense_rounding_up(self):
        """
        Test calculate_average_cr with high defense CR and slightly lower offense CR
        """
        average_defensive_cr = 7.8
        average_offensive_cr = 8.1

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        self.assertEqual(result, 8)

    def test_calculate_average_cr_rounding_behavior(self):
        """
        Test calculate_average_cr with average_defensive_cr = 3.6 and average_offensive_cr = 4.2
        to check rounding behavior
        """
        average_defensive_cr = 3.6
        average_offensive_cr = 4.2

        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)

        # The average CR would be (3.6 + 4.2) / 2 = 3.9
        # it should round up to 4
        self.assertEqual(result, 4)

    def test_calculate_average_cr_equal_values(self):
        """
        Test calculate_average_cr with equal defensive and offensive CR values
        """
        average_defensive_cr = 5
        average_offensive_cr = 5
        result = calculate_average_cr(average_defensive_cr, average_offensive_cr)
        self.assertEqual(result, 5)
