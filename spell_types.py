from random import uniform
from typing import List, Optional
from elements import Element, ElementalAttackData
from turn_context import TurnContext, PersistentEffect, TurnCallbackTime, apply_poison
from game_agent import GameAgent, EvadeStat
from dataclasses import dataclass


@dataclass
class AttackResult:
    damage: int
    hit: bool
    attack_description: str


def get_target_description(caster: GameAgent, target: GameAgent):
    if caster is target:
        return "yourself"

    return target.name


def get_evade_flavor_text(target: GameAgent, evade_stat: EvadeStat) -> str:
    if evade_stat == EvadeStat.DEXTERITY:
        return f'The {target.name} quickly dodges the attack.'
    if evade_stat == EvadeStat.WILL:
        return f'You focus hard on the spell, but you cannot make it effect the {target.name}.'
    if evade_stat == EvadeStat.ARMOR:
        return f'The attack fails to penetrate the {target.name}\'s armor.'


def attack(damage: int, element: Element, target: GameAgent, evade_stat: EvadeStat) -> AttackResult:
    if target.evade(evade_stat, damage):
        return AttackResult(0, False, get_evade_flavor_text(target, evade_stat))

    damage = target.reduce_damage(damage, evade_stat)
    target.damage(damage)
    return AttackResult(damage, True, f'The attack hits {target.name} for {damage} damage')


def critical_hit(base_damage: int) -> int:
    return round(uniform(1.8, 2.2) * base_damage)

def heal(health_recovered, element, recover_from_poison, turns_of_poison_immunity, target: GameAgent,
         turn_context: TurnContext):
    # TODO: Recover from poison
    # TODO: Use element
    if turns_of_poison_immunity > 0:
        target.set_poison_immunity(True)

        turn_context.register_callback(PersistentEffect(turn_context.current_player, turns_of_poison_immunity,
                                                        "Poison immunity",
                                                        TurnCallbackTime.START,
                                                        lambda: None,
                                                        lambda: None,
                                                        lambda: target.set_poison_immunity(False)))

    target.heal(health_recovered)


# Spells start here
def no_spell(element: Element, arguments: List, target: GameAgent, turn_context: TurnContext):
    return "You wait a moment but nothing happens."


def elemental_attack(element: Element, arguments: List, target: GameAgent, turn_context: TurnContext):
    additional_damage = arguments[0].value + arguments[1].value + arguments[2].value

    def elemental_attack_type() -> Optional[ElementalAttackData]:
        if element == Element.WATER:
            return ElementalAttackData(1, "large splash of water")
        if element == Element.FIRE:
            return ElementalAttackData(5, "fireball")
        if element == Element.EARTH:
            return ElementalAttackData(4, "rock the size of your head")
        if element == Element.AIR:
            return ElementalAttackData(1, "mighty gust of wind")
        if element == Element.LIGHTNING:
            return ElementalAttackData(4, "ball of electricity")
        if element == Element.POISON:
            poison_effect = apply_poison(turn_context.current_player, target, additional_damage, 1 + arguments[3].value)
            return ElementalAttackData(1, "cloud of poison",
                                       lambda: (turn_context.register_callback(
                                           poison_effect)) if poison_effect is not None else None)

        return None

    attack_data: ElementalAttackData = elemental_attack_type()
    if attack_data is None:
        return f'You feel strange energy within you, but after waiting a moment nothing happens.'

    total_damage = attack_data.base_damage
    if element != element.POISON:
        total_damage += additional_damage

    if target.is_opposite_element(element):
        total_damage = critical_hit(total_damage)

    attack_result: AttackResult = attack(total_damage, element, target, EvadeStat.DEXTERITY)
    if attack_result.hit:
        attack_data.additional_effect()

    return f'You create a {attack_data.description} and cast it toward ' \
           f'{get_target_description(turn_context.current_player, target)}. {attack_result.attack_description}'


def healing(element: Element, arguments: List, target: GameAgent, turn_context: TurnContext):
    healing_amount = arguments[0].value

    if target.is_opposite_element(element):
        attack_result: AttackResult = attack(healing_amount, element, target, EvadeStat.WILL)
        if attack_result.hit:
            return f'{target.name} writhes in pain. {target.name} loses {healing_amount} HP.'
        else:
            return f'You feel yourself casting energy at the {target.name}. {attack_result.attack_description}'

    # TODO: Wire in recover from poison
    poison_immunity_turns = arguments[2].value
    heal(healing_amount, element, arguments[1].value & 4, poison_immunity_turns, target, turn_context)

    poison_immunity_string = "" if poison_immunity_turns == 0 else f' {target.name} gains poison immunity for {poison_immunity_turns} turns'

    return f'{target.name}\'s wounds begin to heal. {target.name} gains {healing_amount} HP.{poison_immunity_string}'
