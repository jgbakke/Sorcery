from typing import List, Callable, Union
from turn_context import TurnContext, TurnCallbackTime, PersistentEffect, apply_poison
from decoder import decode
from spell_words import SpellWords
from enemy_types import *
from random import sample
from game_agent import GameAgent, EvadeStat
from elements import Element


class GameManager:
    def __init__(self, human_player: GameAgent, ai_player: GameAgent):
        self._human_player = human_player
        self._ai_player = ai_player
        self._turn_callbacks: List[PersistentEffect] = list()
        self.turn = 0

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
        current_player.take_turn(TurnContext(self.turn, self, current_player, non_current_player))
        self.execute_callbacks(current_player, TurnCallbackTime.END)

        return self.check_winner()

    def check_winner(self) -> Union[GameAgent, None]:
        if not self._human_player.is_alive():
            print("AI wins!")
            return self._ai_player

        if not self._ai_player.is_alive():
            print("Human wins")
            return self._human_player

    def start_battle(self):
        print("Using the GUI now. Will be removing this func")


def ai_attack(turn_context: TurnContext, damage: int, element: Element):
    damage_to_player = turn_context.non_current_player.reduce_damage(damage, EvadeStat.NONE, element)
    turn_context.non_current_player.damage(damage_to_player)
    print("Player takes", damage_to_player, "damage")


def take_ai_turn(turn_context: TurnContext):
    attacks: List[Callable] = [
        lambda: ai_attack(turn_context, 1, Element.EARTH),
        lambda: turn_context.non_current_player.damage(7),
        lambda: turn_context.current_player.heal(3),
        lambda: turn_context.register_callback(
            apply_poison(turn_context.current_player, turn_context.non_current_player, 5, 2))
    ]

    attacks[0]()

def take_enemy_turn(enemy, turn_context: TurnContext):
    if enemy == None:
        return
    attack = sample(enemy.attacks, k=1)[0]
    print(attack.name, attack.description)
    if attack.target_self:
        turn_context.current_player.heal(attack.hp)
    else:
        turn_context.non_current_player.damage(attack.hp)


    
def example_enemy_turn():
    game_manager: GameManager = GameManager(GameAgent(100, take_player_turn, "Player"),
                                            GameAgent(200,
                                                    take_enemy_turn,
                                                    RAT_KING.name,
                                                    enemy=RAT_KING)
                                            )
    game_manager.start_battle()
