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

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                           text='Play',
                                           manager=manager)

quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 375), (100, 50)),
                                           text='Quit',
                                           manager=manager)

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
    if pressedButton == play_button:
        print('The game has not been made yet. You cannot play :(')
    if pressedButton == quit_button:
        exit(0)


def do_turn():
    gm.next_turn()
    if human_player.health <= 0 or ai_player.health <= 0:
        print("Somebody did the win")
        exit(0)


take_turn_event = pygame.USEREVENT+1
pygame.time.set_timer(take_turn_event, 1000)

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # TODO: Why is the user timer triggering this one?
        # if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #     on_button_press(event.ui_element)

        if event.type == take_turn_event:
            do_turn()

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    battle_screen.draw()

    pygame.display.update()
