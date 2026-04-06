import builtins
from dataclasses import dataclass
from typing import TypeVar

from api import Tile
from game.entities.entity import Entity
from game.items import fist
from game.items.item import Item
from game.items.key import Key
from game.items.treasure import Treasure
from game.items.weapon import Weapon
from game.rooms.door import Door
from stat_tracker import stat_tracker

T = TypeVar("T")


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

    def find_all(self, item_type: type[T]) -> list[T]:
        return [x for x in self.items if isinstance(x, item_type)]


@dataclass
class Character(Entity):
    MIN_PART_OF_THE_STAT: float = 0.5
    tile: Tile = Tile.CHARACTER
    max_hp: int = 20
    hp: int = max_hp
    str: int = 5
    dex: int = 5
    backpack: Backpack = Backpack()
    name: builtins.str = "player"
    is_stunned: bool = False

    @property
    def treasure(self):
        return sum(item.value for item in self.backpack.find_all(Treasure))

    def equip(self, item_id: int):
        if item_id:
            item = self.backpack.find(item_id)
            if isinstance(item, Weapon):
                self.weapon = item
            self.backpack.remove(item)
        elif item_id == 0:
            if self.weapon != fist and self.backpack.put(self.weapon):
                self.weapon = fist

    def use_food(self, item_id: int):
        item = self.backpack.find(item_id)
        self.hp = min(self.hp + item.hp, self.max_hp + self.max_hp_mod)
        self.backpack.remove(item)
        stat_tracker.food += 1

    def use_elixir(self, item_id: int):
        item = self.backpack.find(item_id)
        self.max_hp_mod += item.max_hp
        self.hp += item.max_hp
        self.str_mod += item.str_
        self.dex_mod += item.dex
        self.backpack.remove(item)
        stat_tracker.elixirs += 1

    def use_scroll(self, item_id: int):
        item = self.backpack.find(item_id)
        self.max_hp += item.max_hp
        self.hp += item.max_hp
        self.str += item.str_
        self.dex += item.dex
        self.backpack.remove(item)
        stat_tracker.scrolls += 1

    def open_door(self, door: Door):
        keys = self.backpack.find_all(Key)
        if any(x.color == door.color for x in keys):
            door.open()

    def remove_bonuses(self):
        self.hp = max(1, self.hp - self.max_hp_mod)
        self.max_hp_mod = 0
        self.str_mod = 0
        self.dex_mod = 0

    def remove_keys(self):
        keys = self.backpack.find_all(Key)
        for k in keys:
            self.backpack.remove(k)

    def move(self, x: int = 0, y: int = 0):
        super().move(x, y)
        stat_tracker.tiles += abs(x) + abs(y)

    def get_damage(self, amount):
        super().get_damage(amount)
        stat_tracker.hits += 1

    def attack(self, other: Entity):
        super().attack(other)
        stat_tracker.attacks += 1
