from dataclasses import dataclass

from api import Tile
from game.entities.entity import Entity
from game.items import fist
from game.items.item import Item
from game.items.treasure import Treasure


class Backpack:
    def __init__(self):
        self.items: list[Item] = []

    def remove(self, item):
        self.items.remove(item)

    def put(self, item) -> bool:
        self.items.append(item)
        return True


@dataclass
class Character(Entity):
    tile: Tile = Tile.CHARACTER
    max_hp: int = 20
    hp: int = max_hp
    str = 5
    dex = 5
    weapon = fist
    backpack: Backpack = Backpack()
    name = "player"

    @property
    def treasure(self):
        return sum(
            item.value for item in self.backpack.items if isinstance(item, Treasure)
        )
