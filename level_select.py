from dataclasses import dataclass
from typing import List, Dict

import pygame
import pygame_gui

from enemy_types import Enemy
import enemy_types
import spell_words


@dataclass(frozen=True)
class Level:
    enemy: Enemy
    level_description: str
    level_start_message: str
    spell_hint_reward: str


class LevelSelect:
    def __init__(self, levels: List[Level], gui_manager):
        self._text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((250, 20), (500, 180)),
                                                       html_text='You wish to become the greatest sorcerer in all the '
                                                                 'land. To do so, you must strengthen your power by '
                                                                 'increasing your knowledge of '
                                                                 'the ancient language of sorcery. There are many '
                                                                 'places you can explore to learn secrets that will '
                                                                 'help you piece together your understanding of the '
                                                                 'language. It is up to you to decide where to go.',
                                                       manager=gui_manager)

        self._level_select_buttons: Dict[pygame_gui.elements.UIButton, Level] = dict()

        for index, level in enumerate(levels):
            self._level_select_buttons[pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((100, 220 + 50 * index), (800, 40)),
                text=level.level_description,
                manager=gui_manager)] = level

    def on_button_press(self, ui_element) -> Level:
        return self._level_select_buttons.get(ui_element)

    def clear_ui(self):
        self._text_box.kill()
        for button in self._level_select_buttons:
            button.kill()


LEVELS = [
    Level(enemy_types.RAT_KING,
          "Explore the ancient caves underneath the castle.",
          "While exploring the old dark caves, The Rat King ambushes you!",
          "You get a reward"),
    Level(enemy_types.LION_WARRIOR,
          "Defend the castle from the attacking Lion Warriors",
          "The champion of the Lion Army approaches you, ready to fight to the death.",
          "You get a reward"),
    Level(enemy_types.MAGE_LIGHTNING,
          "Steal the ancient scrolls from the Lightning Mage\'s secret study room",
          "The Lightning Mage catches you stealing from his study room. Prepare to fight!",
          f'The scroll says that using {spell_words.SpellWords.FUS} as the fourth word of a spell will make it a '
          f'Lightning spell.')
]
