#!/usr/bin/env python3
"""
Class for ability scores and all things closely related.
"""

from src.constants import STR, DEX, CON, INT, WIS, CHA
class AbilityScores:
    "Class for handling ability_scores in creature class"
    def __init__(self, ability_scores_string="10 10 10 10 10 10"):
        ability_scores = ability_scores_string.split(" ")
        self._ability_scores = [
            ability_scores[STR],
            ability_scores[DEX],
            ability_scores[CON],
            ability_scores[INT],
            ability_scores[WIS],
            ability_scores[CHA]
        ]

    def set_ability_score(self, ability_score):
        "set one of the ability_scores value"
        if ability_score == STR:
            self.set_strength_score(ability_score)
        elif ability_score == DEX:
            self.set_dexterity_score(ability_score)
        elif ability_score == CON:
            self.set_constitution_score(ability_score)
        elif ability_score == INT:
            self.set_intelligence_score(ability_score)
        elif ability_score == WIS:
            self.set_wisdom_score(ability_score)
        elif ability_score == CHA:
            self.set_charisma_score(ability_score)

    def get_ability_score(self, ability_score):
        "get one of the ability scores's value"
        requested_ability_score = None
        if ability_score == STR:
            requested_ability_score = self.get_strength_score()
        elif ability_score == DEX:
            requested_ability_score = self.get_dexterity_score()
        elif ability_score == CON:
            requested_ability_score = self.get_constitution_score()
        elif ability_score == INT:
            requested_ability_score = self.get_intelligence_score()
        elif ability_score == WIS:
            requested_ability_score = self.get_wisdom_score()
        elif ability_score == CHA:
            requested_ability_score = self.get_charisma_score()
        return requested_ability_score

    def get_ability_modifier(self, ability_score):
        "get one of the ability scores modifier"
        return self.calculate_ability_modifier(self.get_ability_score(ability_score))

    def get_ability_scores(self):
        "get ability scores as a list"
        return self._ability_scores

    def set_strength_score(self, score):
        "set strength ability score"
        self._ability_scores[STR] = score
    def get_strength_score(self):
        "get strength ability score"
        return self._ability_scores[STR]

    def set_dexterity_score(self, score):
        "set dexterity ability score"
        self._ability_scores[DEX] = score
    def get_dexterity_score(self):
        "set dexterity ability score"
        return self._ability_scores[DEX]

    def set_constitution_score(self, score):
        "set constitution ability score"
        self._ability_scores[CON] = score
    def get_constitution_score(self):
        "get constitution ability score"
        return self._ability_scores[CON]

    def set_intelligence_score(self, score):
        "set intelligence ability score"
        self._ability_scores[INT] = score
    def get_intelligence_score(self):
        "get intelligence ability score"
        return self._ability_scores[INT]

    def set_wisdom_score(self, score):
        "set wisdom ability score"
        self._ability_scores[WIS] = score
    def get_wisdom_score(self):
        "get wisdom ability score"
        return self._ability_scores[WIS]

    def set_charisma_score(self, score):
        "set charisma ability score"
        self._ability_scores[CHA] = score
    def get_charisma_score(self):
        "get charisma ability score"
        return self._ability_scores[CHA]

    def calculate_ability_modifier(self, ability_score):
        "returns ability score modifier of given ability score"
        return (ability_score - 10) // 2
