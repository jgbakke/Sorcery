from game_agent import GameAgent
import pygame_gui
import pygame


class BattleScreen:
    def __init__(self, player: GameAgent, enemy: GameAgent, gui_manager: pygame_gui.UIManager):
        self._player: GameAgent = player
        self._enemy: GameAgent = enemy
        self._gui_manager: gui_manager
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

    def draw(self):
        pass
