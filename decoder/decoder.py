import spell_words
from spell_words import SpellWords
from typing import List
import elements

MAX_SPELL_WORDS = 9


class Decoder:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def decode(self, words: List):
        additional_empty_words_needed = MAX_SPELL_WORDS - len(words)
        words.extend([SpellWords.EMPTY for i in range(additional_empty_words_needed)])
        words = words[:MAX_SPELL_WORDS]

        spell = spell_words.SpellTranslations[tuple(words[:3])]
        element_type = spell_words.ElementTranslations[words[3]]
        spell_arguments = words[4:8]
        target = self.player if (words[-1].value & 1) else self.enemy

        return spell(element_type, spell_arguments, target)


decoder = Decoder("player", "AI")
casted_spell = decoder.decode([SpellWords.FUS, SpellWords.RO, SpellWords.DAH, SpellWords.GUH, SpellWords.FUS, SpellWords.RO, SpellWords.DAH])
print()
casted_spell = decoder.decode([SpellWords.HUP, SpellWords.RO, SpellWords.WAH, SpellWords.GUH, SpellWords.GUH, SpellWords.HUP, SpellWords.WAH])
print()
casted_spell = decoder.decode([SpellWords.FUS, SpellWords.RO, SpellWords.DAH, SpellWords.GUH, SpellWords.RO, SpellWords.RO, SpellWords.DAH])
