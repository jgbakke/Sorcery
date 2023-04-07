from typing import List
import elements


def attack(damage, element, target, evade_stat):
    # TODO: This will be moved to the combat api
    # TODO: EvadeStat will not be a string, maybe an Enum for combat api to look up in the Enemy class?
    #  Or maybe EvadeStat will just be passed in as a number target.getDexterity()
    print(target, " was attacked by elemental", element, "attack and received", damage, "damage")


def heal(health_recovered, element, recover_from_poison, turns_of_poison_immunity, target):
    # TODO: Another thing that belongs in the combat api
    print("Recovered", health_recovered, "HP")


# Spells start here
def no_spell(element: elements.Element, arguments: List, target):
    print("You wait a moment but nothing happens.")


def elemental_attack(element: elements.Element, arguments: List, target):
    base_damage = 3
    # TODO: To avoud needing to always do .value or a count_bits() function, create util methods in decoder.py
    additional_damage = arguments[0].value + arguments[1].value + arguments[2].value
    total_damage = base_damage + additional_damage

    attack(total_damage, element, target, "dexterity")
    print("You cast", element, "attack")


def healing(element: elements.Element, arguments: List, target):
    heal(arguments[0].value, element, arguments[1].value & 4, arguments[2].value, target)
    print("You cast", element, "Heal. Gain immunity from poision for", arguments[2].value, "turns")