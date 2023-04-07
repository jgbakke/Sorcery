from typing import Callable, List
from turn_context import TurnContext
from decoder import decode
from spell_words import SpellWords
from game_agent import GameAgent


class GameManager:
    def __init__(self, human_player: GameAgent, ai_player: GameAgent):
        self._human_player = human_player
        self._ai_player = ai_player
        self._turn_callbacks: List[Callable] = list()

    def register_callback(self, callback):
        self._turn_callbacks.append(callback)

    def start_battle(self):
        for i in range(20):  # TODO: Go until somebody is dead
            print("Starting round", i)
            self._human_player.take_turn(TurnContext(i, self, self._human_player, self._ai_player))
            self._ai_player.take_turn(TurnContext(i, self, self._ai_player, self._human_player))
            # TODO: Check healths
            print()
            print()


def take_player_turn(turn_context: TurnContext):
    # TODO: Real impl for getting input
    if turn_context.turn == 2:
        decode(
            [SpellWords.HUP, SpellWords.RO, SpellWords.WAH, SpellWords.FUS, SpellWords.RO, SpellWords.DAH,
             SpellWords.DAH], turn_context)
    else:
        decode([SpellWords.WAH, SpellWords.WAH, SpellWords.GUH], turn_context)


game_manager: GameManager = GameManager(GameAgent(10, take_player_turn),
                                        GameAgent(20, lambda _: print("AI says \"I am not yet a sentient AI :(\"")))
game_manager.start_battle()