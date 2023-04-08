from typing import Callable

from game_agent import GameAgent
from enum import Enum


class TurnContext:
    def __init__(self, turn: int, game_manager, current_player: GameAgent, non_current_player: GameAgent):
        self.turn = turn
        self._game_manager = game_manager
        self.current_player: GameAgent = current_player
        self.non_current_player: GameAgent = non_current_player

    def register_callback(self, callback):
        self._game_manager.register_callback(callback)


class TurnCallbackTime(Enum):
    START = 1,
    END = 2


class PersistentEffect:
    def __init__(self, caster: GameAgent, turns: int, tooltip: str, effect_time: TurnCallbackTime,
                 initial_effect: Callable, per_turn_effect: Callable, end_effect: Callable):
        self.effect_time = effect_time
        self.end_effect = end_effect
        self.per_turn_effect = per_turn_effect
        self.initial_effect = initial_effect
        self.tooltip = tooltip
        self.turns = turns
        self.caster = caster
