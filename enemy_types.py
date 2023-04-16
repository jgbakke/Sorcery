from dataclasses import dataclass
from typing import List, Dict, Set
from elements import Element
from game_agent import EvadeStat

@dataclass(frozen=True)
class EnemyAttack:
    name: str
    description: str
    hp: int # hp variable contains HP affected by attack, whether it be +HP healed or -HP inflicted
    target_self: bool = False # boolean value for whether target is self. True == self targeted attack. False == targeted at player
    persistent: bool = False # if attack is persistent

@dataclass(frozen=True)
class Enemy:
    name: str
    description: str
    attacks: List[EnemyAttack]
    elemental: Element
    filepath: str
    hp: int
    stats: Dict[EvadeStat, int]

#TODO: Add list of filepaths for each enemy, randomly choose one to use. Bosses will only have one element but common enemies may have variation.

RAT_KING = Enemy("Rat King", 
                 "Ruling over the sewer domain, the Rat King combines his wits and stature to become a powerful adversary.",
                 [EnemyAttack("King Bite", "The King bites hard.", 20), EnemyAttack("King Heal", "The King heals lots.", 20, target_self=True), EnemyAttack("King Tail Whip", "The King whips tail hard.", 12), EnemyAttack("King Poison Fart", "The King farts hard.", 5, persistent=True)],
                 Element.POISON,
                 "art/ratking_nostaff.png",
                 100,
                 {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

RAT_LESSER = Enemy("Rat Soldier",
                   "Acting under the stead of the Rat King, the Rat Solider fights for his homeland with ferocity.",
                   [EnemyAttack("Rat Bite", "The rat dude bites pretty hard", 10), EnemyAttack("Rat Tail Whip", "The rat whps its tail aroud, smacking you across the face.", 6), EnemyAttack("Rat Fart", "The rat farts... the stink stays with you.", 3, persistent=True)],
                   Element.POISON,
                    "",
                    100,
                    {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

DRAGON_COMMON = Enemy("Common Dragon",
                      "A normal dragon, might branch this out into different types.",
                      [EnemyAttack("Fire Breath", "The dragon breathes fire, as you would expect.", 14), EnemyAttack("Dragon Stomp", "The dragon stomps its claws into the ground in rage.", 8), EnemyAttack("Dragon Tail Whip", "The dragon whips its tail around to damage those attacking from behind.", 10)],
                      Element.FIRE,
                      "",
                      100,
                      {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

LION_WARRIOR = Enemy("Lion Warrior", 
                 "The Lion Warrior is a fierce opponent, with deadly claws and teeth.",
                 [EnemyAttack("Lion Bite", "The Lion bites hard.", 20), EnemyAttack("Lion Scratch", "The lion slashes his claws into your flesh.", 5)],
                 Element.EARTH,
                 "art/lion_warrior.png",
                 20,
                 {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

MAGE_LIGHTNING = Enemy("Lightning Mage",
               "A mage recenty graduated from the School of Spells and Magic, the Mage uses the most academically viable spells and magic in combat.",
               [EnemyAttack("Elemental Bolt", f"Fires a {Element.LIGHTNING} bolt at the player.", 10), EnemyAttack("Mage Heal", "Heals Mage", 10, target_self=True), EnemyAttack("Elemental Ball", f"Fires a {Element.LIGHTNING} ball at the player.", 15)],
               Element.ANY,
                "",
                100,
                {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

CAVE_OCTOPUS = Enemy("Cave Octopus",
                     "The cave octopus evolved for millenia in the darkness, nobody knows what tricks it has up its sleeves.",
                     [EnemyAttack("Choke Slam", "The cave octopus wraps its tentacles around your neck and slams you forcefully into the ground.", 15), EnemyAttack("Slap", "The octopus slaps you with every tentacle.", 8)],
                     Element.EARTH,
                     "",
                     100,
                     {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

CAVE_SCREECHER = Enemy("Cave Screecher",
                     "The cave screecher lives its whole life without sight, using noise as its only mechanism for attack.",
                     [EnemyAttack("Choke Slam", "The cave octopus wraps its tentacles around your neck and slams you forcefully into the ground.", 15)],
                     Element.EARTH,
                     "",
                     100,
                     {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

MUSHROOM_MAN = Enemy("Mushroom Man", 
                     "The Mushroom Man descripton (cant think of one rn)",
                     [],
                     Element.EARTH,
                     "",
                     100,
                     {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})

FINAL_BOSS = Enemy("FINAL BOSS",
                   "FINAL BOSS DESCRIPTION",
                   [],
                   Element.ALL,
                   "",
                   1000,
                   {EvadeStat.DEXTERITY: 4, EvadeStat.WILL: 3})



