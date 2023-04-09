from typing import List, Callable
from turn_context import TurnContext, TurnCallbackTime, PersistentEffect, apply_poison
from decoder import decode
from spell_words import SpellWords
from game_agent import GameAgent, EvadeStat
from elements import Element


class GameManager:
    def __init__(self, human_player: GameAgent, ai_player: GameAgent):
        self._human_player = human_player
        self._ai_player = ai_player
        self._turn_callbacks: List[PersistentEffect] = list()

    def register_callback(self, callback):
        self._turn_callbacks.append(callback)

    def execute_callbacks(self, current_player: GameAgent, callback_type: TurnCallbackTime):
        expired_callbacks: List[PersistentEffect] = list()

        for callback in self._turn_callbacks:
            if callback.caster is current_player and callback.effect_time == callback_type:
                callback.per_turn_effect()
                callback.turns -= 1
                if callback.turns == 0:
                    print(callback.tooltip, "wears off")  # TODO: Name instead of tooltip?
                    callback.end_effect()
                    expired_callbacks.append(callback)

        for expired in expired_callbacks:
            self._turn_callbacks.remove(expired)

        self.check_alive()

    def take_turn(self, current_player: GameAgent, non_current_player: GameAgent, turn_num):
        self.execute_callbacks(current_player, TurnCallbackTime.START)
        current_player.take_turn(TurnContext(turn_num, self, current_player, non_current_player))
        self.check_alive()
        self.execute_callbacks(current_player, TurnCallbackTime.END)

    def check_alive(self):
        if not self._human_player.is_alive():
            print("AI wins!")
            exit(0)

        if not self._ai_player.is_alive():
            print("Human wins")
            exit(0)

    def start_battle(self):
        for i in range(20):  # TODO: Go until somebody is dead
            print("Starting round", i)
            print("Player health:", self._human_player.health, "| Poison Immunity:",
                  self._human_player._poison_immunity)
            self.take_turn(self._human_player, self._ai_player, i)
            print("AI health:", self._ai_player._health, "| Poison Immunity:", self._ai_player._poison_immunity)
            self.take_turn(self._ai_player, self._human_player, i)
            print()
            print()


def take_player_turn(turn_context: TurnContext):
    # TODO: Real impl for getting input
    spell_effect_description: str
    if turn_context.turn == 2:
        spell_effect_description = decode(
            [SpellWords.HUP, SpellWords.RO, SpellWords.WAH,
             SpellWords.RUH,
             SpellWords.WAH, SpellWords.HUP, SpellWords.RUH, SpellWords.GUH,
             SpellWords.RO], turn_context)
    else:
        spell_effect_description = decode([SpellWords.FUS, SpellWords.RO, SpellWords.DAH,
                                           SpellWords.RUH], turn_context)

    print(spell_effect_description)  # TODO: Into UI instead


def take_ai_turn(turn_context: TurnContext):
    attacks: List[Callable] = [
        lambda: turn_context.non_current_player.damage(1),
        lambda: turn_context.non_current_player.damage(7),
        lambda: turn_context.current_player.heal(3),
        lambda: turn_context.register_callback(
            apply_poison(turn_context.current_player, turn_context.non_current_player, 5, 2))
    ]

    attacks[0]()


game_manager: GameManager = GameManager(GameAgent(10, take_player_turn, "Player", {}, {Element.NONE}),
                                        GameAgent(20,
                                                  take_ai_turn,
                                                  "Monster",
                                                  {
                                                      EvadeStat.DEXTERITY: 4,
                                                      EvadeStat.WILL: 2
                                                  },
                                                  {Element.EARTH})
                                        )
game_manager.start_battle()
