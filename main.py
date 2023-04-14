import pygame
import pygame_gui
from battle_screen import BattleScreen
from game_agent import GameAgent
pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#148c1a'))

manager = pygame_gui.UIManager((800, 600), theme_path="theme.json")

human: GameAgent = GameAgent(10, lambda: None, "Player", {}, set(), "art/player.png")
enemy: GameAgent = GameAgent(10, lambda: None, "Enemy", {}, set(), "art/lion_warrior.png")
battle_screen: BattleScreen = BattleScreen(human, enemy, manager)

clock = pygame.time.Clock()
is_running = True

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                           text='Play',
                                           manager=manager)

quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 375), (100, 50)),
                                           text='Quit',
                                           manager=manager)


def on_button_press(pressedButton):
    if pressedButton == play_button:
        print('The game has not been made yet. You cannot play :(')
    if pressedButton == quit_button:
        exit(0)


while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            on_button_press(event.ui_element)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    battle_screen.draw()

    pygame.display.update()
