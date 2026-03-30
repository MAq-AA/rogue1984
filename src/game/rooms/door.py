from dataclasses import dataclass

from api import Tile
from enum import Enum
from game.base import GameObject


class DoorColor(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


door_tiles = {
    DoorColor.RED: Tile.DOOR_RED,
    DoorColor.GREEN: Tile.DOOR_GREEN,
    DoorColor.BLUE: Tile.DOOR_BLUE,
}


@dataclass
class Door(GameObject):
    color: DoorColor = DoorColor.RED
    tile: Tile = Tile.DOOR_RED

    @classmethod
    def get(cls, color: DoorColor):
        tile = door_tiles[color]
        return cls(color=color, tile=tile)
