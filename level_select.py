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
    Level(enemy_types.RAT_SOLDIER,
          "Explore the sewers going into the caves.",
          "While trudging through the rancid sewers, you come across a Rat Soldier!",
          "You get a reward"),
    Level(enemy_types.MUSHROOM_MAN,
          "Enter the opening to the ancient caves under the castle",
          "While entering the ancient caves through a dank passage, you are attacked by a slimy humanoid figure that detached itself from a wall of untouched fungus.",
          "You get a reward"),
    Level(enemy_types.SHRIEKER,
          "Explore the ancient caves underneath the castle",
          "While exploring the ancient caves, you are surpirsed by a deafening shriek, and see a seemingly blind creature slowly creep into your line of sight.",
          "You get a reward"),
    Level(enemy_types.RAT_KING,
          "Enter the ominous throne room at the depths of the caves.",
          "While approaching the door to the throne room, The Rat King flings it open, taken aback by your presence, and prepares for battle!",
          "You get a reward"),
    Level(enemy_types.CAVE_OCTOPUS,
          "Exit the ancient caves underneath the castle.",
          "While leaving the ancient caves through a newly opened passage, you are attacked by a large mass with various tentacles and one single eye.",
          "You get a reward"),
    Level(enemy_types.LION_WARRIOR,
          "Defend the castle from the attacking Lion Warriors.",
          "The champion of the Lion Army approaches you, ready to fight to the death.",
          "You get a reward"),
    Level(enemy_types.DRAGON_COMMON,
          "Defend the castle from the roaming Dragon.",
          "A dragon swoops down from below the clouds, ready to wreak havoc.",
          "You get a reward"),
    Level(enemy_types.MAGE_LIGHTNING,
          "Steal the ancient scrolls from the Lightning Mage\'s secret study room",
          "The Lightning Mage catches you stealing from his study room. Prepare to fight!",
          f'The scroll says that using {spell_words.SpellWords.FUS} as the fourth word of a spell will make it a '
          f'Lightning spell.')
]
