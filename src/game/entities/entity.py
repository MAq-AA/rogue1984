import builtins
import random
from dataclasses import dataclass, field

from api import Tile
from game.base import GameObject
from game.items import Weapon, fist


@dataclass
class Entity(GameObject):
    max_hp: int = 0
    max_hp_mod: int = 0
    hp: int = 0
    str: int = 0
    str_mod: int = 0
    dex: int = 0
    dex_mod: int = 0
    name: builtins.str = "unknown"
    weapon: Weapon = field(default_factory=lambda: fist)
    MIN_PART_OF_THE_STAT: float = 0.5

    def get_damage(self, amount):
        self.hp -= amount

    def attack(self, other: "Entity"):
        is_got_hit = self.roll_dexterity() > other.roll_dexterity()

        if is_got_hit:
            other.get_damage(self.roll_strength())

    def roll_strength(self):
        min_str = int((self.str + self.str_mod) * self.MIN_PART_OF_THE_STAT)
        return random.randint(min_str, max(min_str, self.str))

    def roll_dexterity(self):
        min_dex = int((self.dex + self.dex_mod) * self.MIN_PART_OF_THE_STAT)
        return random.randint(min_dex, max(min_dex, self.dex))
