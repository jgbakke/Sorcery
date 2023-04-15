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

    def is_opposite(self, other) -> bool:
        elements: frozenset[Element] = frozenset([self, other])
        return elements in OPPOSITE_ELEMENTS


OPPOSITE_ELEMENTS: frozenset[frozenset[Element]] = frozenset([
    frozenset([Element.WATER, Element.LIGHTNING]),
    frozenset([Element.WATER, Element.FIRE]),
    frozenset([Element.EARTH, Element.FIRE]),
    frozenset([Element.AIR, Element.POISON])
])

@dataclass
class ElementalAttackData:
    base_damage: int
    description: str
    additional_effect: Callable[[], str] = lambda: None

