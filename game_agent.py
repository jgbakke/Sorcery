from enum import Enum
from typing import Callable, Dict
from random import randint


class EvadeStat(Enum):
    NONE = 0,
    DEXTERITY = 1,
    ARMOR = 2,
    WILL = 3


class GameAgent:
    def __init__(self, health: int, turn_decision_strategy: Callable, name: str, stats: Dict[EvadeStat, int]):
        self._health: int = health
        self._turn_decision_strategy: Callable = turn_decision_strategy
        self.name: str = name
        self._poison_immunity: bool = False
        self._stats = stats

    def take_turn(self, turn_context):
        self._turn_decision_strategy(turn_context)

    def is_alive(self):
        return self._health > 0

    def heal(self, health):
        self._health += health

    def damage(self, health):
        self._health -= health

    def reduce_damage(self, damage: int, evade_stat: EvadeStat) -> int:
        if evade_stat == EvadeStat.ARMOR:
            return damage - self._get_evade_stat(evade_stat)

        return damage

    def set_poison_immunity(self, value):
        self._poison_immunity = value

    def evade(self, evade_stat: EvadeStat, attack_strength: int) -> bool:
        evade_stat_score: int = self._get_evade_stat(evade_stat)

        if evade_stat == EvadeStat.NONE:
            return True
        if (evade_stat == EvadeStat.DEXTERITY) or (evade_stat == EvadeStat.WILL):
            return randint(1, 10) <= evade_stat_score
        if evade_stat == EvadeStat.ARMOR:
            return attack_strength < evade_stat_score

    def _get_evade_stat(self, evade_stat: EvadeStat):
        return self._stats.get(evade_stat, 0)

    @property
    def poison_immunity(self):
        return self._poison_immunity

    @property
    def health(self):
        return self._health
