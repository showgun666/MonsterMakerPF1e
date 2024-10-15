from dataclasses import dataclass
from typing import Optional, Callable
@dataclass
class SpecialAbility:
    """
    Special Ability class stores special abilities
    """
    name: str
    description: str
    effect: Optional[Callable] = None

    def apply(self, **kwargs):
        "Apply effect(s) to effect"
        if self.effect:
            return self.effect(**kwargs)
        return None
