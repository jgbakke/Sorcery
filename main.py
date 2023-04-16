from typing import Union

import pygame
import pygame_gui

import game_manager
from battle_screen import BattleScreen
from decoder import decode
from game_agent import GameAgent
from level_select import LevelSelect, Level, LEVELS
from spell_words import SpellWords
from turn_context import TurnContext

TIME_BETWEEN_TURNS = 5000
from enemy_types import *

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1000, 750))

background = pygame.Surface((1000, 750))
background.fill(pygame.Color('#148c1a'))

manager = pygame_gui.UIManager((1000, 750), theme_path="theme.json")

clock = pygame.time.Clock()
is_running = True
player_words = []


def decode_player_spell(turn_context: TurnContext):
    spell_effect_description, results = decode(player_words, turn_context)
    battle_screen.write_message(spell_effect_description)
    if results:
        battle_screen.write_to_notebook(results)
        battle_screen.read_notebook()


human_player = GameAgent(100, decode_player_spell, "Player", {}, {Element.NONE}, "art/player.png")
ai_player: GameAgent
gm: game_manager.GameManager

player_turn: bool = True
in_battle: bool = False
player_took_turn_at: int = 0
battle_screen: BattleScreen = None
level_select: LevelSelect = LevelSelect(LEVELS, manager)


def take_player_turn(words: List[SpellWords]):
    global player_turn, player_words, player_took_turn_at
    if player_turn:
        player_turn = False
        battle_screen.enable_player_turn_buttons(False)
        player_words = words

        if not check_end_battle(gm.take_human_turn()):
            battle_screen.clear_pending_spell()
            battle_screen.write_persistent_effects(gm.get_persistent_effects_messages())
            player_took_turn_at = pygame.time.get_ticks()


def start_battle(enemy: Enemy, message: str):
    global battle_screen, gm, in_battle, ai_player
    level_select.clear_ui()
    ai_player = game_manager.EnemyFactory(enemy)
    gm = game_manager.GameManager(human_player, ai_player)
    battle_screen = BattleScreen(human_player, ai_player, manager, take_player_turn)
    gm.init_gui(battle_screen)
    battle_screen.write_message(message)
    in_battle = True


def check_end_battle(winning_agent: Union[GameAgent, None]) -> bool:
    global battle_screen, in_battle
    if winning_agent is None:
        return False

    if winning_agent is human_player:
        # TODO: Get a tip and add it to the notebook, then reset and pick new battle
        battle_screen.write_message(
            f'You defeated the {ai_player.name}! {level.spell_hint_reward} Reload the game to choose another enemy to '
            f'fight. Your Notebook has been auto-saved.')
    elif winning_agent is ai_player:
        battle_screen.write_message(f'You died! Reload the game to try again.')

    in_battle = False
    return True


while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if in_battle:
                battle_screen.on_button_press(event.ui_element)
            else:
                level: Level = level_select.on_button_press(event.ui_element)
                if level is not None:
                    start_battle(level.enemy, level.level_start_message)

        manager.process_events(event)

    manager.update(time_delta)

    if in_battle and not player_turn and pygame.time.get_ticks() - player_took_turn_at > TIME_BETWEEN_TURNS:
        player_turn = True
        if not check_end_battle(gm.take_ai_turn()):
            battle_screen.write_persistent_effects(gm.get_persistent_effects_messages())
            battle_screen.enable_player_turn_buttons(True)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
