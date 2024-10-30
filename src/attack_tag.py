"Attack tag module"
from enum import Enum

class AttackTag(Enum):
    """
    class for handling tags
    """
    BONUS_ATTACK = "bonus_attack"
    REACH = "reach"
    FINESSE = "finesse"
    TWO_HANDED = "two_handed"
    MELEE = "melee"
    UNARMED = "unarmed"
    CROSSBOW = "crossbow"
    BOW = "bow"
    SIMPLE = "simple"
    MARTIAL = "martial"
    EXOTIC = "exotic"
    NATURAL = "natural"
    PRIMARY = "primary_attack"
    SECONDARY = "secondary_attack"
    MANUFACTURED = "manufactured"
