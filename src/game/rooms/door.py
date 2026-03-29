from dataclasses import dataclass

from api import Tile
from game.base import GameObject

door_colors = {
    "red": Tile.DOOR_RED,
    "green": Tile.DOOR_GREEN,
    "blue": Tile.DOOR_BLUE,
}


@dataclass
class Door(GameObject):
    color: str = "red"
    tile: Tile = Tile.DOOR_RED

    @classmethod
    def get(cls, color: str):
        tile = door_colors[color]
        return cls(color=color, tile=tile)
