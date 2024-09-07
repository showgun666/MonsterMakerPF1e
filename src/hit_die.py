#!/usr/bin/env python3
"""
Class for hit dice for HitDice class
"""

class HitDie:
    "class for handling hit die related things for creature class"

    def __init__(self, die_type="Humanoid", saves=False, size=8, bab=0.75, skill_ranks=2):
        self.type = die_type
        self.die_size = size
        self.bab = bab
        self.skill_ranks = skill_ranks
        if saves:
            self.saves = saves
        else:
            self.saves = [True, False, False]
