from enum import Enum
from typing import Dict, Tuple, Callable
from spell_types import *


class SpellWords(Enum):
    UH = 0
    HUP = 1
    RUH = 2
    WAH = 3
    GUH = 4
    FUS = 5
    RO = 6
    DAH = 7


SpellTranslations: Dict[Tuple[SpellWords, SpellWords, SpellWords], Callable] = {
    (SpellWords.FUS, SpellWords.RO, SpellWords.DAH): elemental_attack,
    (SpellWords.HUP, SpellWords.RO, SpellWords.WAH): healing
}

# TODO: Finish all these
ElementTranslations: Dict[SpellWords, Element] = {
    SpellWords.GUH: Element.POISON,
    SpellWords.FUS: Element.FIRE
}