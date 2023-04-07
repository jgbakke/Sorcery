
class TurnContext:
    def __init__(self, turn: int, game_manager, current_player, non_current_player):
        self.turn = turn
        self._game_manager = game_manager
        self.current_player = current_player
        self.non_current_player = non_current_player

    def register_callback(self, callback):
        self._game_manager.register_callback(callback)
