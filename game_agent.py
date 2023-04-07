from typing import Callable


class GameAgent:
    def __init__(self, health, turn_decision_strategy):
        self._health: int = health
        self._turn_decision_strategy: Callable = turn_decision_strategy

    def take_turn(self, turn_context):
        self._turn_decision_strategy(turn_context)

    def is_alive(self):
        return self._health > 0
