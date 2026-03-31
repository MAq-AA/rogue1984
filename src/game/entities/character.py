from __future__ import annotations
import random
from dataclasses import dataclass
from typing import TYPE_CHECKING


from api import Tile
from game.entities.entity import Entity
from game.items import fist
from game.items.item import Item
from game.items.treasure import Treasure

if TYPE_CHECKING:
    from game.entities.monster import Monster


class Backpack:
    def __init__(self):
        self.items: list[Item] = []

    def remove(self, item):
        self.items.remove(item)

    def put(self, item) -> bool:
        self.items.append(item)
        return True

    def find(self, item_id: int) -> Item:
        return next(x for x in self.items if id(x) == item_id)


@dataclass
class Character(Entity):
    MIN_PART_OF_THE_STAT = 0.5
    tile: Tile = Tile.CHARACTER
    max_hp: int = 20
    hp: int = max_hp
    str = 5
    dex = 5
    weapon = fist
    backpack: Backpack = Backpack()
    name = "player"
    is_stunned = False

    @property
    def treasure(self):
        return sum(
            item.value for item in self.backpack.items if isinstance(item, Treasure)
        )

    def equip(self, item_id: int):
        if item_id:
            item = self.backpack.find(item_id)
            self.weapon = item
            self.backpack.remove(item)
        elif item_id == 0:
            if self.weapon != fist and self.backpack.put(self.weapon):
                self.weapon = fist

    def use_food(self, item_id: int):
        item = self.backpack.find(item_id)
        self.hp = min(self.hp + item.hp, self.max_hp + self.max_hp_mod)
        self.backpack.remove(item)

    def use_elixir(self, item_id: int):
        item = self.backpack.find(item_id)
        self.max_hp_mod += item.max_hp
        self.hp += item.max_hp
        self.str_mod += item.str_
        self.dex_mod += item.dex
        self.backpack.remove(item)

    def use_scroll(self, item_id: int):
        item = self.backpack.find(item_id)
        self.max_hp += item.max_hp
        self.hp += item.max_hp
        self.str += item.str_
        self.dex += item.dex
        self.backpack.remove(item)

    def attack(self, monster: Monster):
        is_got_hit = self.roll_dexterity() > monster.roll_dexterity()

        if is_got_hit:
            monster.get_damage(self.roll_strength())

    def roll_strength(self):
        min_str = int((self.str + self.str_mod)*self.MIN_PART_OF_THE_STAT)
        return random.randint(min_str, self.str)

    def roll_dexterity(self):
        min_dex = int((self.dex + self.dex_mod)*self.MIN_PART_OF_THE_STAT)
        return random.randint(min_dex, self.dex)

    def get_damage(self, amount):
        self.hp -= amount
