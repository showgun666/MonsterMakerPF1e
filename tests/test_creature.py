#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for Creature class"

import unittest
from src.creature import Creature
from src.equipment import Equipment
from src.constants import STR
from src.attack import Attack

class TestCreature(unittest.TestCase):
    "Tests for creating a creature"
    def setUp(self):
        """ Create object for all tests """
        self.creature = Creature("Dragon", "5")
        self.eq = Equipment()

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

    def test_add_weapon(self):
        """Can add find correctly to creature"""
        self.creature.add_attack(
            self.eq.find_weapon("Longsword"),
            0,
            STR,
            STR,
            [],
            "Medium"
            )
        self.creature.add_attack(
            self.eq.find_weapon("Sword, short"),
            0,
            STR,
            STR,
            [],
            "Medium"
            )
        self.creature.add_attack(
            self.eq.find_weapon("Claw"),
            0,
            STR,
            STR,
            [],
            "Medium"
            )
        for attack in self.creature.attacks:
            self.assertIsInstance(attack, Attack)

        self.assertEqual(self.creature.attacks[0].name, "Longsword")
        self.assertEqual(self.creature.attacks[1].name, "Sword, short")
        self.assertEqual(self.creature.attacks[2].name, "Claw")

    def test_attack_damage(self):
        """
        accurately retrieves damage value for attack
        """
        self.creature.add_attack(
            self.eq.find_weapon("Longsword"),
            0,
            STR,
            STR,
            [],
            "Medium"
            )
        self.assertEqual(self.creature.attacks[0].calculate_weapon_damage(self.creature.ability_scores), 4)
        self.creature.ability_scores.set_ability_score(STR, 16)
        self.assertEqual(self.creature.attacks[0].calculate_weapon_damage(self.creature.ability_scores), 7)

    def test_get_damage(self):
        """accurately gets damage value"""
        self.creature.add_attack(
            self.eq.find_weapon("Longsword"),
            0,
            STR,
            STR,
            [],
            "Medium"
            )
        self.assertEqual(self.creature.damage, 4)

    def test_get_attack_bonus_average(self):
        """
        gets correct average attack bonus for all attacks
        """
        attacks = [
            self.eq.find_weapon("Claw"),
            self.eq.find_weapon("Claw"),
            self.eq.find_weapon("Claw"),
            self.eq.find_weapon("Claw"),
            self.eq.find_weapon("Bite"),
            self.eq.find_weapon("Wing"),
            self.eq.find_weapon("Wing"),
            self.eq.find_weapon("Tail Slap"),
            ]
        self.creature.ability_scores.set_ability_score(STR, 19)
        for attack in attacks:
            self.creature.add_attack(attack, self.creature.hit_dice.get_bab(), STR, STR, [], "Medium")

        self.assertEqual(self.creature.get_attack_bonus_average(), 8.125)

    def test_iterative_attacks(self):
        """
        iterative attacks iterate correctly.
        """
        creature_2 = Creature("Humanoid", "20")
        creature_3 = Creature("Humanoid", "10", "Large")
        creature_2.add_attack(self.eq.find_weapon("Greatsword"), creature_2.hit_dice.get_bab(), STR, STR, [], creature_2.size)
        creature_2.add_attack(self.eq.find_weapon("Longsword"), creature_3.hit_dice.get_bab(), STR, STR, [], creature_3.size)
        for attack in creature_3.attacks:
            print("\n\n\n")
            print(attack)
        self.assertEqual(creature_2.get_attack_bonus_average(), 17.5)
        self.assertEqual(creature_3.get_attack_bonus_average(), 12.5)