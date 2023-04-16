from typing import Dict, List, Callable

from pygame_gui.core.interfaces import IUIElementInterface

from game_agent import GameAgent
import pygame_gui
import pygame
from notebook import Notebook
from spell_words import SpellWords

BUTTON_WIDTH = 95
SPACING_BETWEEN_BUTTONS = 20
EMPTY_SPELL_STRING = '<b>Say a spell by selecting the word buttons</b>'


class BattleScreen:
    def __init__(self, player: GameAgent,
                 enemy: GameAgent,
                 gui_manager: pygame_gui.UIManager,
                 player_turn_callback: Callable[[List[SpellWords]], None]):
        self._player: GameAgent = player
        self._enemy: GameAgent = enemy
        self._gui_manager: gui_manager = gui_manager
        self._ui_elements: List[IUIElementInterface] = list()
        self._human_image = pygame.image.load(player.image_path).convert_alpha()
        self._enemy_image = pygame.image.load(enemy.image_path).convert_alpha()

        self.human_icon = self.add_element(pygame_gui.elements.UIImage(relative_rect=pygame.Rect((20, 520), (200, 200)),
                                                                       image_surface=self._human_image,
                                                                       manager=gui_manager))

        self.enemy_icon = self.add_element(
            pygame_gui.elements.UIImage(relative_rect=pygame.Rect((780, 520), (200, 200)),
                                        image_surface=self._enemy_image,
                                        manager=gui_manager))

        self.player_health_bar = self.add_element(pygame_gui.elements.UIStatusBar(pygame.Rect((20, 490), (200, 20)),
                                                                                  gui_manager,
                                                                                  percent_method=player.health_percent))

        self.enemy_health_bar = self.add_element(pygame_gui.elements.UIStatusBar(pygame.Rect((780, 490), (200, 20)),
                                                                                 gui_manager,
                                                                                 percent_method=enemy.health_percent))

        self.spell_buttons: Dict[pygame_gui.elements.UIButton, SpellWords] = self.create_spell_word_buttons()
        self.pending_spell_words: List[SpellWords] = list()
        self.pending_spell_words_label = self.add_element(pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((100, 80), (800, 40)),
            html_text=EMPTY_SPELL_STRING,
            manager=self._gui_manager))

        self._message_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((20, 230), (960, 100)),
            html_text="",
            manager=self._gui_manager)

        self._persistent_effects_box = self.add_element(pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((300, 510), (400, 180)),
            html_text="",
            manager=self._gui_manager))

        self.cast_spell = self.add_element(
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect((425, 140), (150, 60)),
                                         text="Cast Spell",
                                         manager=self._gui_manager))

        self.player_turn_callback: Callable[[List[SpellWords]], None] = player_turn_callback

        self._player_turn_buttons = [i for i in self.spell_buttons.keys()] + [self.cast_spell]
        self.notebook = Notebook

    def clear_ui(self):
        for element in self._ui_elements:
            element.kill()

    def add_element(self, button: IUIElementInterface) -> IUIElementInterface:
        self._ui_elements.append(button)
        return button

    def write_message(self, message):
        self._message_box.set_text(str(message))

    def read_notebook(self):
        self.notebook.read_results()

    def write_to_notebook(self, data):
        self.notebook.write_results(data)

    def write_persistent_effects(self, message: List[str]):
        self._persistent_effects_box.set_text("<br>".join(message))

    def on_button_press(self, ui_element):
        if ui_element == self.cast_spell:
            self.player_turn_callback(self.pending_spell_words)

        pressed_word: SpellWords = self.spell_buttons.get(ui_element)
        if pressed_word:
            self.pending_spell_words.append(pressed_word)
            label_text = " ".join([str(word) for word in self.pending_spell_words])
            self.pending_spell_words_label.set_text(f"<b><i>{label_text}</i></b>")
            print(label_text)

    def enable_player_turn_buttons(self, enabled: bool):
        for button in self._player_turn_buttons:
            if enabled:
                button.enable()
            else:
                button.disable()

    def create_spell_word_buttons(self) -> Dict[pygame_gui.elements.UIButton, SpellWords]:
        buttons = dict()
        button_size = (BUTTON_WIDTH, 50)

        for (button, word) in enumerate(SpellWords):
            button_position = (100 + SPACING_BETWEEN_BUTTONS + button * BUTTON_WIDTH, 15)
            added_button: pygame_gui.elements.UIButton = self.add_element(
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(button_position, button_size),
                                             text=str(word),
                                             manager=self._gui_manager))

            buttons[added_button] = word

        return buttons

    def clear_pending_spell(self):
        self.pending_spell_words.clear()
        self.pending_spell_words_label.set_text(EMPTY_SPELL_STRING)
