from dataclasses import dataclass

from api import Tile
from game.items.item import Item
from game.rooms.door import DoorColor

key_tiles = {
    DoorColor.RED: Tile.ITEM_KEY_RED,
    DoorColor.GREEN: Tile.ITEM_KEY_GREEN,
    DoorColor.BLUE: Tile.ITEM_KEY_BLUE,
}


@dataclass
class Key(Item):
    color: DoorColor = DoorColor.RED
    tile: Tile = Tile.ITEM_KEY_RED
    name: str = "red key"

    @classmethod
    def get(cls, color: DoorColor):
        tile = key_tiles[color]
        name = f"{color.value} key"
        return cls(color=color, tile=tile, name=name)
