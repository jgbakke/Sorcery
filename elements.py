from enum import Enum
from typing import Callable
from random import randint

from dataclasses import dataclass

class Element(Enum):
    def __str__(self):
        return self.name.lower()
    ANY = randint(1, 6),
    WATER = 1,
    FIRE = 2,
    EARTH = 3,
    AIR = 4,
    LIGHTNING = 5,
    POISON = 6,
    NONE = 7
    ALL = 8

@dataclass
class ElementalAttackData:
    base_damage: int
    description: str
    additional_effect: Callable[[], str] = lambda: None

