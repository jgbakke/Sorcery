from enum import Enum
from typing import Callable, Dict, Set, Tuple
from random import randint
from elements import Element
from enemy_types import Enemy, EnemyAttack


class EvadeStat(Enum):
    NONE = 0,
    DEXTERITY = 1,
    ARMOR = 2,
    WILL = 3


class GameAgent:
    def __init__(self, health: int, turn_decision_strategy: Callable, name: str, stats: Dict[EvadeStat, int], element: Set[Element], image_path: str, enemy: Enemy = None):
        self.name: str = name
        self.image_path: str = image_path
        self._health: int = health
        self._starting_health = self._health
        self._turn_decision_strategy: Callable = turn_decision_strategy
        self._poison_immunity: bool = False
        self._stats = stats
        self._elements = element
        self._shield: Tuple[Element, int] = (Element.NONE, 0)
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
        self._health -= max(0, health)

    def reduce_damage(self, damage: int, evade_stat: EvadeStat, attack_element: Element) -> int:
        if evade_stat == EvadeStat.ARMOR:
            return damage - self._get_evade_stat(evade_stat)

        shield_strength: int = self._shield[1]
        if shield_strength > 0:
            if self._shield[0].is_opposite(attack_element):
                shield_strength *= 2
            print("Shield blocks", shield_strength)
            self.clear_shield()
            return damage - shield_strength

        return damage

    def set_poison_immunity(self, value):
        self._poison_immunity = value

    def apply_shield(self, element: Element, shield_strength: int):
        self._shield = (element, shield_strength)

    def clear_shield(self):
        self._shield = (Element.NONE, 0)

    def is_element_type(self, element: Element) -> bool:
        return element in self._elements

    def is_opposite_element(self, other_element: Element) -> bool:
        return any([element.is_opposite(other_element) for element in self._elements])

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

    def health_percent(self) -> float:
        return self._health / self._starting_health
