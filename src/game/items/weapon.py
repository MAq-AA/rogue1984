import random
from dataclasses import dataclass
from typing import ClassVar

from api import DisplayItem, Tile
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

    def display_item(self):
        stat = max(self.hp, self.max_hp, self.dex, self.str_)
        return DisplayItem(
            name=f"{self.name} ({stat})",
            stat=stat,
            id=id(self),
        )
