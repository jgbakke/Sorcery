from random import sample
from typing import Union

from battle_screen import BattleScreen
from enemy_types import *
from game_agent import GameAgent
from turn_context import TurnContext, TurnCallbackTime, PersistentEffect


class GameManager:
    def __init__(self, human_player: GameAgent, ai_player: GameAgent):
        self._human_player = human_player
        self._ai_player = ai_player
        self._turn_callbacks: List[PersistentEffect] = list()
        self.turn = 0
        self._battle_gui = None

    def init_gui(self, battle_gui: BattleScreen):
        self._battle_gui = battle_gui

    def register_callback(self, callback):
        self._turn_callbacks.append(callback)

    def execute_callbacks(self, current_player: GameAgent, callback_type: TurnCallbackTime):
        expired_callbacks: List[PersistentEffect] = list()

        for callback in self._turn_callbacks:
            if callback.caster is current_player and callback.effect_time == callback_type:
                callback.per_turn_effect()
                callback.turns -= 1
                if callback.turns <= 0:
                    callback.end_effect()
                    expired_callbacks.append(callback)

        for expired in expired_callbacks:
            self._turn_callbacks.remove(expired)

    def get_persistent_effects_messages(self) -> List[str]:
        messages: List[str] = list()
        for callback in self._turn_callbacks:
            messages.append(f'{callback.tooltip} for {callback.turns} more turns')

        return messages

    def take_human_turn(self) -> Union[GameAgent, None]:
        return self._take_turn(self._human_player, self._ai_player)

    def take_ai_turn(self) -> Union[GameAgent, None]:
        return self._take_turn(self._ai_player, self._human_player)

    def _take_turn(self, current_player: GameAgent, non_current_player: GameAgent):
        self.execute_callbacks(current_player, TurnCallbackTime.START)
        current_player.take_turn(TurnContext(self.turn, self, current_player, non_current_player, self._battle_gui))
        self.execute_callbacks(current_player, TurnCallbackTime.END)

        return self.check_winner()

    def check_winner(self) -> Union[GameAgent, None]:
        if not self._human_player.is_alive():
            print("AI wins!")
            return self._ai_player

        if not self._ai_player.is_alive():
            print("Human wins")
            return self._human_player


def take_enemy_turn(turn_context: TurnContext):
    attacks = turn_context.current_player.attacks
    attack = sample(attacks, k=1)[0]
    gui_output = f'{turn_context.current_player.name} uses {attack.name}. {attack.description}'
    attack_strength = attack.hp # TODO: A little randomization here? +/- 10% maybe?

    if attack.target_self:
        turn_context.current_player.heal(attack_strength)
        gui_output += f' {turn_context.current_player.name} heals {attack_strength}.'
    else:
        turn_context.non_current_player.damage(attack_strength)
        gui_output += f' {turn_context.non_current_player.name} takes {attack_strength} damage.'

    turn_context.write_to_gui(gui_output)


def EnemyFactory(enemy: Enemy) -> GameAgent:
    name = enemy.name
    desc = enemy.description
    attacks = enemy.attacks
    elemental = {enemy.elemental}
    filepath = enemy.filepath
    hp = enemy.hp
    stats = enemy.stats
    return GameAgent(hp,
                     take_enemy_turn,
                     name,
                     stats,
                     elemental,
                     filepath,
                     attacks=attacks)
