"""
Attack class module for handling attacks
An attack is made from a weapon attack
it takes variables from creature
"""
from dataclasses import dataclass, field
from typing import List
from src.helpers import get_average_dice, damage_dice_by_size_conversion

@dataclass
class Attack:
    """
    class for handling attack logic
    """
    name: str
    attack_bonuses: dict
    attack_ability_score: int # Ability score
    damage_dice: str  # e.g., "1d6", "2d4"
    damage_ability_score: int  # e.g., 0 for str, 1 for dex etc, see constants
    critical_range: List[int]  # e.g., [19, 20]
    critical_multiplier: int  # e.g., 2 for x2
    damage_types: List[str]  # e.g., ["bludgeoning", "slashing", "piercing", "B", "S", "P"]
    special_abilities: List[str] = field(default_factory=list)  # Descriptions or identifiers
    tags: List[str] = field(default_factory=list)  # Tags for feats or other interactions
    _weapon_size: str = "Medium"

    if _weapon_size != "Medium":
        damage_dice = damage_dice_by_size_conversion(damage_dice, "Medium", _weapon_size)

    def calculate_weapon_damage(self, ability_scores) -> int:
        """Calculate damage based on damage dice and ability modifier."""
        total_damage = get_average_dice(self.damage_dice) + ability_scores.get_ability_modifier(self.damage_ability_score)
        return total_damage

    def calculate_attack_bonus(self, creature) -> int:
        """calculate the attack bonus"""
        # attack_mod = creature.ability_scores.get_ability_modifier(self.attack_ability_score)
        return sum(self.attack_bonuses.values())

    @property
    def weapon_size(self):
        """
        Getter for weapon size
        """
        return self._weapon_size

    @weapon_size.setter
    def weapon_size(self, value="Medium"):
        """
        Setter for weapon size
        """
        self.damage_dice = damage_dice_by_size_conversion(self.damage_dice, self._weapon_size, value)
        self._weapon_size = value
