import random
from dataclasses import dataclass
from typing import ClassVar

from api import Tile
from game.items.item import Item


@dataclass
class Weapon(Item):
    tile: Tile = Tile.ITEM_WEAPON
    names: ClassVar[list[str]] = [
        "mace",
        "sword",
        "dagger",
        "flail",
        "spear",
        "halberd",
    ]

    @classmethod
    def get_random(cls, level):
        value = random.randint(1, level)
        name = random.choice(Weapon.names)
        return cls(str_=value, name=name)
