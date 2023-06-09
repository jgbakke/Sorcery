from typing import Callable, Optional
from game_agent import GameAgent
from enum import Enum


class TurnContext:
    def __init__(self, turn: int, game_manager, current_player: GameAgent, non_current_player: GameAgent, battle_gui):
        self.turn = turn
        self._game_manager = game_manager
        self.current_player: GameAgent = current_player
        self.non_current_player: GameAgent = non_current_player
        self._battle_gui = battle_gui

    def register_callback(self, callback):
        self._game_manager.register_callback(callback)

    def write_to_gui(self, message):
        self._battle_gui.write_message(message)


class TurnCallbackTime(Enum):
    START = 1,
    END = 2


class PersistentEffect:
    def __init__(self, caster: GameAgent, turns: int, tooltip: str, effect_time: TurnCallbackTime,
                 initial_effect: Callable, per_turn_effect: Callable, end_effect: Callable):
        self.caster = caster
        self.turns = turns
        self.tooltip = tooltip
        self.effect_time = effect_time
        self.initial_effect = initial_effect
        self.per_turn_effect = per_turn_effect
        self.end_effect = end_effect


def apply_poison(caster: GameAgent, target: GameAgent, turns: int, damage_per_turn: int) -> Optional[PersistentEffect]:
    if target.poison_immunity:
        return None

    return PersistentEffect(caster, turns,
                            f'{target.name} is afflicted with poison and will suffer {damage_per_turn} damage per turn',
                            TurnCallbackTime.END,
                            lambda: None,
                            lambda: target.damage(damage_per_turn),
                            lambda: None)
