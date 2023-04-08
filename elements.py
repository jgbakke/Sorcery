from enum import Enum
from typing import Callable

from dataclasses import dataclass

class Element(Enum):
    def __str__(self):
        return self.name.lower()

    WATER = 1,
    FIRE = 2,
    EARTH = 3,
    AIR = 4,
    LIGHTNING = 5,
    POISON = 6,
    NONE = 7

@dataclass
class ElementalAttackData:
    base_damage: int
    description: str
    additional_effect: Callable[[], str] = lambda: None

