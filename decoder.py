import spell_words
from spell_words import SpellWords
from typing import List, Callable
from spell_types import no_spell
from elements import Element
from turn_context import TurnContext

MAX_SPELL_WORDS = 9


def decode(words: List, turn_context: TurnContext) -> str:
    additional_empty_words_needed = MAX_SPELL_WORDS - len(words)
    words.extend([SpellWords.UH for _ in range(additional_empty_words_needed)])
    words = words[:MAX_SPELL_WORDS]

    spell = get_spell_type(words)
    element_type = get_element_type(words[3])
    spell_arguments = words[4:8]
    target = turn_context.current_player if (words[-1].value & 1) else turn_context.non_current_player

    results = {}
    description = spell(element_type, spell_arguments, target, turn_context)
    if not spell.__name__ == "no_spell":
        spells = '-'.join([w.__str__() for w in words[:8]])
        results = {spells: [spell.__name__, "Player" if target.name == "Player" else "Enemy", description]}    
    return description, results

def get_spell_type(words: List[SpellWords]) -> Callable:
    words_tuple = tuple(words[:3])
    if words_tuple not in spell_words.SpellTranslations:
        return no_spell

    return spell_words.SpellTranslations[words_tuple]


def get_element_type(word: SpellWords) -> Element:
    return spell_words.ElementTranslations.get(word, Element.NONE)