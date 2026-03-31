import random

from api import Tile
from game.base import GameObject
from game.items import fist


class Entity(GameObject):
    tile: Tile
    max_hp: int
    max_hp_mod = 0
    hp: int
    str: int
    str_mod = 0
    dex: int
    dex_mod = 0
    weapon = fist
    name: "str" = "unknown"
    MIN_PART_OF_THE_STAT: float = 0.5

    def get_damage(self, amount):
        self.hp -= amount

    def attack(self, other: "Entity"):
        is_got_hit = self.roll_dexterity() > other.roll_dexterity()

        if is_got_hit:
            other.get_damage(self.roll_strength())

    def roll_strength(self):
        min_str = int((self.str + self.str_mod) * self.MIN_PART_OF_THE_STAT)
        return random.randint(min_str, self.str)

    def roll_dexterity(self):
        min_dex = int((self.dex + self.dex_mod) * self.MIN_PART_OF_THE_STAT)
        return random.randint(min_dex, self.dex)
