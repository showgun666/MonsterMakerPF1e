#!/usr/bin/env python3
"""
Class for hit dice and related progression for creature class
"""
import src.hit_die as hd

class HitDice:
    "class for handling hit die related things for creature class"
    def __init__(self):
        self.hit_dice = []

    def add_hit_die(self):
        "Add a hit die to hit dice"
        self.hit_dice.append(hd.HitDie())

    def remove_hit_die(self, index):
        "Remove a hit die from hit dice"
        self.hit_dice.pop(index)
