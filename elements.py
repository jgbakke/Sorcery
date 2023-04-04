from enum import Enum


class Element(Enum):
    def __str__(self):
        return self.name.lower()

    WATER = 1,
    FIRE = 2,
    EARTH = 3,
    AIR = 4,
    LIGHTNING = 5,
    POISON = 6
