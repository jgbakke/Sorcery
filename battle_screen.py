from typing import Dict, List

from game_agent import GameAgent
import pygame_gui
import pygame
from spell_words import SpellWords

BUTTON_WIDTH = 95
SPACING_BETWEEN_BUTTONS = 20
EMPTY_SPELL_STRING = '<b>Say a spell by selecting the word buttons</b>'


class BattleScreen:
    def __init__(self, player: GameAgent, enemy: GameAgent, gui_manager: pygame_gui.UIManager):
        self._player: GameAgent = player
        self._enemy: GameAgent = enemy
        self._gui_manager: gui_manager = gui_manager
        self._human_image = pygame.image.load(player.image_path).convert_alpha()
        self._enemy_image = pygame.image.load(enemy.image_path).convert_alpha()

        self.human_icon = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((20, 380), (200, 200)),
                                                      image_surface=self._human_image,
                                                      manager=gui_manager)

        self.enemy_icon = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((580, 380), (200, 200)),
                                                      image_surface=self._enemy_image,
                                                      manager=gui_manager)

        self.player_health_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((20, 350), (200, 20)),
                                                                 gui_manager,
                                                                 percent_method=player.health_percent)

        self.enemy_health_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((580, 350), (200, 20)),
                                                                gui_manager,
                                                                percent_method=enemy.health_percent)

        self.spell_buttons: Dict[pygame_gui.elements.UIButton, SpellWords] = self.create_spell_word_buttons()
        self.pending_spell_words: List[SpellWords] = list()
        self.pending_spell_words_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((40, 150), (700, 40)),
            html_text=EMPTY_SPELL_STRING,
            manager=self._gui_manager)

    def on_button_press(self, ui_element):
        pressed_word: SpellWords = self.spell_buttons.get(ui_element)
        if pressed_word:
            self.pending_spell_words.append(pressed_word)
            label_text = " ".join([str(word) for word in self.pending_spell_words])
            self.pending_spell_words_label.set_text(f"<b><i>{label_text}</i></b>")
            print(label_text)



    def create_spell_word_buttons(self) -> Dict[pygame_gui.elements.UIButton, SpellWords]:
        buttons = dict()
        button_size = (BUTTON_WIDTH, 50)

        for (button, word) in enumerate(SpellWords):
            button_position = (SPACING_BETWEEN_BUTTONS + button * BUTTON_WIDTH, 75)
            buttons[pygame_gui.elements.UIButton(relative_rect=pygame.Rect(button_position, button_size),
                                                 text=str(word),
                                                 manager=self._gui_manager)] = word
        return buttons

    def draw(self):
        pass
