import pygame
import pygame_gui
from battle_screen import BattleScreen
from game_agent import GameAgent, EvadeStat
import game_manager
from elements import Element

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#148c1a'))

manager = pygame_gui.UIManager((800, 600), theme_path="theme.json")

clock = pygame.time.Clock()
is_running = True

human_player = GameAgent(10, game_manager.take_player_turn, "Player", {}, {Element.NONE}, "art/player.png")

ai_player = GameAgent(20,
                      game_manager.take_ai_turn,
                      "Monster",
                      {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3},
                      {Element.EARTH},
                      "art/lion_warrior.png")

gm: game_manager.GameManager = game_manager.GameManager(
    human_player,
    ai_player
)

battle_screen: BattleScreen = BattleScreen(human_player, ai_player, manager)


def on_button_press(pressedButton):
    pass


def do_turn():
    gm.next_turn()
    if human_player.health <= 0 or ai_player.health <= 0:
        print("Somebody did the win")
        exit(0)


take_turn_event = 25
# pygame.time.set_timer(take_turn_event, 1000)

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            battle_screen.on_button_press(event.ui_element)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    battle_screen.draw()

    pygame.display.update()
