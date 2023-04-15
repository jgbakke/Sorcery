from typing import Callable
from enemy_types import Enemy, EnemyAttack

class GameAgent:
    def __init__(self, health: int, turn_decision_strategy: Callable, name: str, enemy: Enemy = None):
        self._health: int = health
        self._turn_decision_strategy: Callable = turn_decision_strategy
        self.name: str = name
        self._poison_immunity: bool = False
        self.enemy : Enemy = enemy

    def take_turn(self, turn_context):
        if self.enemy != None:
            self._turn_decision_strategy(self.enemy, turn_context)
        else:
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
