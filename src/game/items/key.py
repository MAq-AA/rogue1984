from dataclasses import dataclass

from api import Tile
from game.items.item import Item

key_colors = {
    "red": Tile.ITEM_KEY_RED,
    "green": Tile.ITEM_KEY_GREEN,
    "blue": Tile.ITEM_KEY_BLUE,
}


@dataclass
class Key(Item):
    color: str = "red"
    tile: Tile = Tile.ITEM_KEY_RED
    name: str = "red key"

    @classmethod
    def get(cls, color: str):
        tile = key_colors[color]
        name = f"{color} key"
        return cls(color=color, tile=tile, name=name)
