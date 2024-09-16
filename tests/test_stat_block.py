#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for StatBlock class"

import unittest
from src.creature import Creature

class TestStatBlock(unittest.TestCase):
    "Class for testing StatBlock"

    def test_generate_stat_block(self):
        "test that the class can generate a stat block" ### FAKE TEST ###
        creature = Creature("Aberration", "5")
        creature.ability_scores.set_ability_score(0, 15)
        creature.ability_scores.set_ability_score(1, 15)
        creature.ability_scores.set_ability_score(2, 15)
        creature.ability_scores.set_ability_score(3, 15)
        creature.ability_scores.set_ability_score(4, 15)
        creature.ability_scores.set_ability_score(5, 15)

        with open("test_stat_block.txt", "w", encoding="UTF-8") as f:
            f.write(creature.get_d20pfsrd_stat_block())
