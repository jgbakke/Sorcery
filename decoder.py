import spell_words
from spell_words import SpellWords
from typing import List, Callable
from spell_types import no_spell
from elements import Element

MAX_SPELL_WORDS = 9


class Decoder:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def decode(self, words: List):
        additional_empty_words_needed = MAX_SPELL_WORDS - len(words)
        words.extend([SpellWords.EMPTY for _ in range(additional_empty_words_needed)])
        words = words[:MAX_SPELL_WORDS]

        spell = get_spell_type(words)
        element_type = get_element_type(words[3])
        spell_arguments = words[4:8]
        target = self.player if (words[-1].value & 1) else self.enemy

        return spell(element_type, spell_arguments, target)


def get_spell_type(words: List[SpellWords]) -> Callable:
    words_tuple = tuple(words[:3])
    if words_tuple not in spell_words.SpellTranslations:
        return no_spell

    return spell_words.SpellTranslations[words_tuple]


def get_element_type(word: SpellWords) -> Element:
    if word not in spell_words.ElementTranslations:
        return Element.NONE

    return spell_words.ElementTranslations[word]

# decoder = Decoder("player", "AI")
# casted_spell = decoder.decode([SpellWords.FUS, SpellWords.RO, SpellWords.DAH, SpellWords.GUH, SpellWords.FUS, SpellWords.RO, SpellWords.DAH])
# print()
# casted_spell = decoder.decode([SpellWords.HUP, SpellWords.RO, SpellWords.WAH, SpellWords.GUH, SpellWords.GUH, SpellWords.HUP, SpellWords.WAH])
# print()
# casted_spell = decoder.decode([SpellWords.FUS, SpellWords.RO, SpellWords.DAH, SpellWords.GUH, SpellWords.RO, SpellWords.RO, SpellWords.DAH])
