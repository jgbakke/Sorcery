from typing import Callable


class GameAgent:
    def __init__(self, health: int, turn_decision_strategy: Callable, name: str):
        self._health: int = health
        self._turn_decision_strategy: Callable = turn_decision_strategy
        self.name: str = name
        self._poison_immunity: bool = False

    def take_turn(self, turn_context):
        self._turn_decision_strategy(turn_context)

    def is_alive(self):
        return self._health > 0

    def heal(self, health):
        self._health += health

    def damage(self, health):
        self._health -= health

    def set_poison_immunity(self, value):
        self._poison_immunity = value

    @property
    def poison_immunity(self):
        return self._poison_immunity

    @property
    def health(self):
        return self._health
