import random
from dataclasses import dataclass
from typing import ClassVar

from api import Tile
from game.items.item import Item


@dataclass
class Food(Item):
    names: ClassVar[list[str]] = ["Apple", "Milk", "Bread", "Cheese", "Meat", "Potato"]
    tile: Tile = Tile.ITEM_FOOD

    @classmethod
    def get_random(cls, level):
        value = random.randint(1, level)
        name = random.choice(cls.names)
        return cls(name=name, hp=value)
