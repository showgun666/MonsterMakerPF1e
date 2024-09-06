#!/usr/bin/env python3
"""
Class for attributes
"""
from src.constants import STR, DEX, CON, INT, WIS, CHA
class Attributes:
    "Class for handling attributes in creature class"
    def __init__(self, attributes=[10, 10, 10, 10, 10, 10] ):
        self._attributes = [
            attributes[STR],
            attributes[DEX],
            attributes[CON],
            attributes[INT],
            attributes[WIS],
            attributes[CHA]
        ]
    
    def set_attribute(self, attribute):
        "set one of the attributes score"
        if attribute == STR:
            self.set_strength(attribute)
        elif attribute == DEX:
            self.set_dexterity(attribute)
        elif attribute == CON:
            self.set_constitution(attribute)
        elif attribute == INT:
            self.set_intelligence(attribute)
        elif attribute == WIS:
            self.set_wisdom(attribute)
        elif attribute == CHA:
            self.set_charisma(attribute)

    def get_attribute_scores(self):
        "get attribute scores as a list"
        return self._attributes

    ### NEED UPDATE METHODS FOR ALL THINGS RELATED TO DIFFERENT ATTRIBUTES ###
    def set_strength(self, score):
        "set strength attribute"
        self._attributes[STR] = score
    def get_strength(self):
        "get strength attribute"
        return self._attributes[STR]

    def set_dexterity(self, score):
        "set dexterity attribute"
        self._attributes[DEX] = score
    def get_dexterity(self):
        "set dexterity attribute"
        return self._attributes[DEX]

    def set_constitution(self, score):
        "set constitution attribute"
        self._attributes[CON] = score
    def get_constitution(self):
        "get constitution attribute"
        return self._attributes[CON]

    def set_intelligence(self, score):
        "set intelligence attribute"
        self._attributes[INT] = score
    def get_intelligence(self):
        "get intelligence attribute"
        return self._attributes[INT]

    def set_wisdom(self, score):
        "set wisdom attribute"
        self._attributes[WIS] = score
    def get_wisdom(self):
        "get wisdom attribute"
        return self._attributes[WIS]

    def set_charisma(self, score):
        "set charisma attribute"
        self._attributes[CHA] = score
    def get_charisma(self):
        "get charisma attribute"
        return self._attributes[CHA]
