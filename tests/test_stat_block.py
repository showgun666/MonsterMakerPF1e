#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for StatBlock class"

import unittest
from src.statSheet import StatBlock

class TestStatBlock(unittest.TestCase):
    "Class for testing StatBlock"

    def test_generate_stat_block(self):
        "test that the class can generate a stat block" ### FAKE TEST ###
        statblock = StatBlock()
        print(statblock.generate_stat_block_string_d20pfsrd())
        with open("test_stat_block.txt", "w") as f:
            f.write(statblock.generate_stat_block_string_d20pfsrd())
